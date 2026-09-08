"""
MahaArogya Setu - FastAPI Backend API Layer
Exposes the existing src/ codebase via clean REST endpoints.

Run: venv/Scripts/uvicorn.exe api:app --port 8000 --reload
"""
import os
import sys
import logging
from contextlib import asynccontextmanager
from functools import lru_cache
from typing import Optional

import pandas as pd
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field

# ---------------------------------------------------------------------------
# Streamlit compatibility shim
# ---------------------------------------------------------------------------
# The existing src/ modules import `streamlit` and use `st.cache_data`,
# `st.cache_resource`, `st.session_state`, etc.  We provide a lightweight
# shim so those decorators become no-ops and session_state acts as a plain
# dict when running under FastAPI (i.e. without the Streamlit runtime).
# ---------------------------------------------------------------------------
import streamlit as st

# Ensure session_state exists as a plain dict (Streamlit runtime not active)
if not hasattr(st, "session_state") or st.session_state is None:
    st.session_state = {}

# Pre-populate keys that pipeline.py expects
for _key, _default in [
    ("history", []),
    ("conversation_context", {}),
    ("health_records", []),
    ("_routing_debug", {}),
    ("_ui_lang", "en"),
]:
    if _key not in st.session_state:
        st.session_state[_key] = _default

# ---------------------------------------------------------------------------
# Imports from existing src/ codebase (100% UNCHANGED)
# ---------------------------------------------------------------------------
from src.config.constants import (
    MAHARASHTRA_DISTRICTS,
    MAHARASHTRA_SCHEMES,
    GENERIC_MEDS,
    ANC_SCHEDULE,
    IMMUNIZATION_SCHEDULE,
    HEALTH_CAMPS,
    ABHA_INFO,
)
from src.config.settings import DATA_FILE
from src.ml.engine import match_and_rank_facilities, load_model
from src.ui.pipeline import generate_response

logger = logging.getLogger("api")

# ---------------------------------------------------------------------------
# Module-level singletons (replaces @st.cache_resource / @st.cache_data)
# ---------------------------------------------------------------------------
_df: Optional[pd.DataFrame] = None
_model = None
_symptom_embeddings = None
_name_embeddings = None


def _init_resources():
    """Load dataset and ML model once at startup."""
    global _df, _model, _symptom_embeddings, _name_embeddings

    # Load CSV dataset
    filepath = DATA_FILE
    if not os.path.exists(filepath):
        filepath = os.path.join(os.path.dirname(__file__), "disease_dataset.csv")
    _df = pd.read_csv(filepath)

    # Load sentence-transformer model and pre-compute embeddings
    _model = load_model()
    if _model is not None:
        try:
            _symptom_embeddings = _model.encode(
                _df["symptoms"].tolist(), convert_to_tensor=True
            )
            _name_embeddings = _model.encode(
                _df["disease"].tolist(), convert_to_tensor=True
            )
        except Exception as exc:
            logger.warning("Embedding computation failed: %s", exc)
            _symptom_embeddings = None
            _name_embeddings = None


# ---------------------------------------------------------------------------
# FastAPI Application
# ---------------------------------------------------------------------------
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Startup: pre-load dataset + ML model."""
    logger.info("🚀 Loading MahaArogya Setu resources...")
    _init_resources()
    logger.info("✅ Resources loaded — API ready")
    yield
    logger.info("🛑 Shutting down")


app = FastAPI(
    title="MahaArogya Setu API",
    description="Rural Healthcare Access Platform — FastAPI Backend",
    version="2.0.0",
    lifespan=lifespan,
)

# CORS — allow Next.js dev server on port 3000 (and any localhost origin)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000", "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ---------------------------------------------------------------------------
# Request / Response Models
# ---------------------------------------------------------------------------
class TriageRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500, description="User symptom or health query")
    language: str = Field("en", description="Response language: 'en', 'hi', or 'mr'")
    stream: bool = Field(False, description="Enable SSE token streaming (future)")
    low_bandwidth: bool = Field(False, description="Use fast keyword matching without heavy AI models")


class TriageResponse(BaseModel):
    html: str = Field(..., description="Rendered HTML triage response")
    routing_debug: dict = Field(default_factory=dict, description="Internal routing metadata")


class FacilityOut(BaseModel):
    name: str
    type: str
    location: str
    phone: str
    beds: str
    facilities: str
    services_list: list[str]


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.get("/", tags=["Health"])
async def health_check():
    """Server health check."""
    return {
        "status": "healthy",
        "app": "MahaArogya Setu API",
        "version": "2.0.0",
        "dataset_loaded": _df is not None,
        "model_loaded": _model is not None,
    }


@app.post("/api/triage", response_model=TriageResponse, tags=["Triage"])
async def triage(req: TriageRequest):
    """
    Core clinical triage endpoint.
    Evaluates emergency triggers, classifies intent, extracts entities,
    matches facilities, and returns a structured HTML clinical card.
    """
    # Map language code to the mode constants used by pipeline
    lang_map = {"en": "English", "hi": "हिंदी (Hindi)", "mr": "मराठी (Marathi)"}
    language = lang_map.get(req.language, "English")

    # Reset per-request session state
    st.session_state["conversation_context"] = st.session_state.get("conversation_context", {})
    st.session_state["_routing_debug"] = {}

    response_html = generate_response(
        query=req.query,
        language=language,
        df=_df,
        symptom_embeddings=None if req.low_bandwidth else _symptom_embeddings,
        name_embeddings=None if req.low_bandwidth else _name_embeddings,
        model=None if req.low_bandwidth else _model,
    )

    return TriageResponse(
        html=response_html,
        routing_debug=st.session_state.get("_routing_debug", {}),
    )


@app.get("/api/facilities", tags=["Facilities"])
async def list_facilities(
    district: Optional[str] = Query(None, description="District name (e.g. 'Nandurbar', 'Gadchiroli')"),
    service: Optional[str] = Query(None, description="Required service (e.g. 'Emergency', 'Maternity')"),
):
    """
    List and rank healthcare facilities.
    If district is provided, returns facilities in that district ranked by relevance.
    Otherwise returns all facilities across all districts.
    """
    if district:
        required_services = [service] if service else None
        ranked = match_and_rank_facilities(
            district,
            required_services=required_services,
            requested_service=service,
        )
        facilities = []
        for fac, reasons in ranked:
            facilities.append({
                **fac,
                "match_reasons": reasons,
            })
        return {"district": district, "count": len(facilities), "facilities": facilities}

    # No district specified — return all
    all_facilities = []
    for dist_name, facs in MAHARASHTRA_DISTRICTS.items():
        for fac in facs:
            all_facilities.append({**fac, "district": dist_name})
    return {"count": len(all_facilities), "facilities": all_facilities}


@app.get("/api/districts", tags=["Facilities"])
async def list_districts():
    """List all supported districts with facility counts."""
    districts = []
    for dist_name, facs in MAHARASHTRA_DISTRICTS.items():
        districts.append({
            "name": dist_name,
            "facility_count": len(facs),
            "facilities": [f["name"] for f in facs],
        })
    return {"count": len(districts), "districts": districts}


@app.get("/api/schemes", tags=["Government Schemes"])
async def list_schemes():
    """Return all Maharashtra government healthcare schemes."""
    return {"count": len(MAHARASHTRA_SCHEMES), "schemes": MAHARASHTRA_SCHEMES}


@app.get("/api/schedules", tags=["Schedules"])
async def get_schedules():
    """
    Return ANC (pregnancy) and UIP (immunization) schedules,
    plus upcoming health camp information.
    """
    return {
        "anc_schedule": ANC_SCHEDULE,
        "immunization_schedule": IMMUNIZATION_SCHEDULE,
        "health_camps": HEALTH_CAMPS,
    }


@app.get("/api/medicines", tags=["Medicines"])
async def list_medicines():
    """
    Return Jan Aushadhi generic medicines with branded vs. generic pricing
    and percentage savings.
    """
    medicines = []
    for name, info in GENERIC_MEDS.items():
        medicines.append({
            "name": name,
            "branded_price": info["branded"],
            "generic_price": info["generic"],
            "saving_percent": info["saving"],
            "use": info["use"],
        })
    return {"count": len(medicines), "medicines": medicines}


@app.get("/api/abha", tags=["ABHA"])
async def get_abha_info(lang: str = Query("en", description="Language: 'en', 'hi', or 'mr'")):
    """Return ABHA (Ayushman Bharat Health Account) creation guide."""
    info = ABHA_INFO.get(lang, ABHA_INFO.get("en", {}))
    return {"language": lang, "abha": info}
