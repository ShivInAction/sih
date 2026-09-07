"""Machine learning models, speech recognition, and matching algorithms."""
import re
import streamlit as st
import pandas as pd
from src.config.constants import (
    MAHARASHTRA_DISTRICTS,
    DISTRICT_COORDS,
    MODE_HINDI,
    MODE_MARATHI,
    MODE_ENGLISH,
)
from src.data_access.geography import haversine_km, get_facility_coords
from src.ml.nlp_utils import (
    tokenize,
    keyword_bonus,
    _merge_compound_aches,
)

def match_and_rank_facilities(district, required_services=None, facility_type=None, urgency=None, requested_service=None, entities=None):
    """Weighted facility matching and ranking.
    Uses structured semantic query to produce context-aware rankings.
    Never invents facilities, phones, or services.

    Priority hierarchy:
      1. Emergency/critical-care requirement — highest safety priority
      2. Explicitly requested service — very high priority (+50 exact, +45 text, +40 synonym)
      3. Patient type / demographic context — meaningful boost (+25)
      4. Facility type relevance (+20)
      5. Proximity / "nearest" bonus (+30 nearest, +15 nearby)
      6. Government facility boost (+12 when requested)
      7. General OPD / generic healthcare — low fallback (+3)
      8. HQ / facility quality tie-breaker (+5)

    Returns: list of (fac_dict, list_of_reason_strings) tuples sorted by score desc.
    Each reason string is a human-readable tag like "✅ Immunization match".
    """
    facilities_in_district = []
    for dist_key, facs in MAHARASHTRA_DISTRICTS.items():
        pure_key = re.sub(r"[ऀ-ॿ() ]", "", dist_key).lower()
        if district and (district.lower() in pure_key or district.lower() in dist_key.lower()):
            facilities_in_district = facs
            break

    if not facilities_in_district:
        for facs in MAHARASHTRA_DISTRICTS.values():
            facilities_in_district.extend(facs)

    # Build a set of canonical requested services for matching
    _req_service_set = set()
    if requested_service:
        _req_service_set.add(requested_service.lower())
    if required_services:
        for rs in required_services:
            _req_service_set.add(rs.lower())

    scored = []
    for fac in facilities_in_district:
        score = 0
        reasons = []
        services = [s.lower() for s in fac.get("services_list", [])]
        services_text = " ".join(services) + " " + fac.get("facilities", "").lower()
        fac_type_lower = fac.get("type", "").lower()

        # === HIGHEST WEIGHT: Exact requested_service match (+50 exact, +45 text, +40 synonym) ===
        # This is the SINGLE MOST IMPORTANT signal — user's explicit request.
        if requested_service:
            req_lower = requested_service.lower()
            # Check services_list (exact canonical match in structured data)
            if req_lower in services:
                score += 50
                reasons.append(f"✅ {requested_service} service")
            # Check facilities text (broader text match)
            elif req_lower in services_text:
                score += 45
                reasons.append(f"✅ {requested_service} (facility description)")
            # Synonym matching for immunization/vaccination
            elif req_lower in ("immunization", "vaccination") and ("immunization" in services_text or "vaccination" in services_text or "cold chain" in services_text):
                score += 40
                reasons.append(f"✅ Immunization (via cold chain/vaccine)")
            # Synonym matching for maternity
            elif req_lower in ("maternity", "pregnancy", "delivery") and ("maternity" in services_text or "delivery" in services_text or "gynaecology" in services_text):
                score += 40
                reasons.append(f"✅ Maternity/Delivery")
            # Synonym matching for pediatric
            elif req_lower in ("pediatric", "child care") and ("pediatric" in services_text or "child" in services_text or "nicu" in services_text):
                score += 40
                reasons.append(f"✅ Pediatric")
            # Synonym matching for laboratory
            elif req_lower in ("laboratory", "lab") and ("laboratory" in services_text or "lab" in services_text or "diagnostic" in services_text):
                score += 40
                reasons.append(f"✅ Laboratory")
            # Synonym matching for telemedicine
            elif req_lower in ("telemedicine",) and ("telemedicine" in services_text or "esanjeevani" in services_text):
                score += 40
                reasons.append(f"✅ Telemedicine")

        # === Emergency capability (when urgency is EMERGENCY): dominant safety priority ===
        if urgency == "EMERGENCY":
            if "emergency" in services:
                score += 60  # Higher than any service match — safety first
                reasons.append("🚨 Emergency capable")
            if "hospital" in fac_type_lower or "district" in fac_type_lower or "medical college" in fac_type_lower:
                score += 25
                reasons.append("🏥 Hospital-level care")

        # === Patient-type suitability: meaningful boost (+25) ===
        # Only applied when patient type is in the required_services set
        if "pediatric" in _req_service_set or "child" in _req_service_set:
            if "pediatric" in services or "pediatric" in services_text:
                score += 25
                if "✅ Pediatric" not in reasons:
                    reasons.append("👶 Pediatric ward")
        if "maternity" in _req_service_set:
            if "maternity" in services or "maternity" in services_text:
                score += 25
                if "✅ Maternity/Delivery" not in reasons:
                    reasons.append("🤰 Maternity services")
        if "emergency" in _req_service_set:
            if "emergency" in services:
                score += 25
                if "🚨 Emergency capable" not in reasons:
                    reasons.append("🚨 Emergency services")

        # === Facility type matching: smaller boost (+20) ===
        if facility_type:
            ft_lower = facility_type.lower()
            if ft_lower in fac_type_lower:
                score += 20
                reasons.append(f"🏢 {fac.get('type', '')}")
            elif "hospital" in ft_lower and ("hospital" in fac_type_lower or "medical college" in fac_type_lower):
                score += 15
            elif "phc" in ft_lower and "primary" in fac_type_lower:
                score += 15
            elif "chc" in ft_lower and "community" in fac_type_lower:
                score += 15

        # === Supporting service relevance (from required_services, excluding already-counted) ===
        # Only boost if NOT already counted via requested_service match
        if required_services:
            for req_svc in required_services:
                req_lower = req_svc.lower()
                # Skip if this service was already the primary requested_service
                if requested_service and req_lower == requested_service.lower():
                    continue
                if req_lower in services:
                    score += 10
                    # Add reason only if not already tagged
                    _tag = f"✅ {req_svc}"
                    if _tag not in reasons:
                        reasons.append(_tag)
                elif req_lower in services_text:
                    score += 8

        # === Proximity / "nearest" boost ===
        # When user explicitly asks for "nearest", rank by approximate distance
        if entities and entities.get("proximity_request"):
            _fac_coords = get_facility_coords(fac)
            if _fac_coords:
                # Use district center as reference if no user location
                _district_center = DISTRICT_COORDS.get(district.title(), None) if district else None
                if _district_center:
                    _dist_km = haversine_km(_district_center[0], _district_center[1], _fac_coords[0], _fac_coords[1])
                    # HQ facility (assumed center of district) gets top boost
                    if fac.get("is_hq") and _dist_km < 5:
                        score += 30
                        reasons.append("📍 Nearest (HQ)")
                    elif _dist_km < 30:
                        score += 20
                        reasons.append("📍 Nearby")
                    else:
                        score += 5  # Far facilities get smaller boost
                        reasons.append("📍 Further away")

        # === Government facility boost ===
        # When user explicitly requests government facilities, boost gov type
        if entities and entities.get("wants_government"):
            _gov_types = ["district hospital", "sub-district hospital", "community health",
                          "primary health", "sdh", "chc", "phc", "district general",
                          "government", "govt", "civil hospital"]
            if any(gt in fac_type_lower for gt in _gov_types):
                score += 12
                reasons.append("🏛️ Government facility")

        # === General OPD: low fallback weight (+3) — never dominates specific services ===
        if "general opd" in services:
            score += 3
            # Only add reason if no specific service reasons exist
            if not any(r.startswith("✅") for r in reasons):
                reasons.append("📋 General OPD")

        # === HQ bonus: tie-breaker (+5) ===
        if fac.get("is_hq"):
            score += 5
            reasons.append("🏛️ District HQ")

        scored.append((score, fac, reasons))

    scored.sort(key=lambda x: (-x[0], -x[1].get("is_hq", False)))
    return [(fac, reasons) for _, fac, reasons in scored]



def offline_keyword_matcher(query_en, df):
    """Low-bandwidth mode uses the SAME routing contract as full mode.
    Returns the same structured intent/entity/urgency objects."""
    query_tokens = tokenize(query_en)
    if not query_tokens: return 0.0, 0, df.iloc[0]
    best_idx, best_score = 0, 0.0
    for i, row in df.iterrows():
        s_tokens = tokenize(row["symptoms"] + " " + row["disease"])
        intersection = query_tokens & s_tokens
        if not intersection: continue
        base = len(intersection) / len(query_tokens)
        score = min(base + keyword_bonus(query_en, row), 1.0)
        if score > best_score:
            best_score, best_idx = score, i
    return best_score, best_idx, df.iloc[best_idx]

def rank_diseases(query_en, df, symptom_embeddings, name_embeddings, model):
    if st.session_state.get("low_bandwidth", False) or model is None:
        best_score, best_idx, row = offline_keyword_matcher(query_en, df)
        ranked = [(best_score, best_idx, row)]
        for i, r in df.iterrows():
            if i != best_idx: ranked.append((0.1, i, r))
        return ranked
    from sentence_transformers import util
    query_embedding = model.encode(_merge_compound_aches(query_en), convert_to_tensor=True)
    symptom_scores = util.cos_sim(query_embedding, symptom_embeddings)[0]
    name_scores = util.cos_sim(query_embedding, name_embeddings)[0]
    ranked = []
    for i, row in df.iterrows():
        semantic = 0.8 * float(symptom_scores[i]) + 0.2 * float(name_scores[i])
        ranked.append((min(semantic + keyword_bonus(query_en, row), 1.0), i, row))
    ranked.sort(key=lambda x: x[0], reverse=True)
    return ranked



def load_whisper():
    try:
        from faster_whisper import WhisperModel
        return WhisperModel("small", device="cpu", compute_type="int8")
    except Exception: return None

def _audio_to_pcm(audio_bytes):
    import av, io
    audio_bytes = audio_bytes.getvalue() if hasattr(audio_bytes, "getvalue") else audio_bytes
    container = av.open(io.BytesIO(audio_bytes))
    resampler = av.AudioResampler(format="s16", layout="mono", rate=16000)
    pcm = b""
    for frame in container.decode(audio=0):
        for r in resampler.resample(frame): pcm += r.to_ndarray().tobytes()
    if not pcm: raise ValueError("no audio")
    return pcm, 16000, 2

def _transcribe_google(audio_bytes, google_lang):
    try:
        import speech_recognition as sr
        pcm, rate, width = _audio_to_pcm(audio_bytes)
        audio_data = sr.AudioData(pcm, rate, width)
        return (sr.Recognizer().recognize_google(audio_data, language=google_lang) if google_lang else sr.Recognizer().recognize_google(audio_data)).strip() or None
    except Exception: return None

def transcribe_audio(audio_bytes, lang):
    audio_bytes = audio_bytes.getvalue() if hasattr(audio_bytes, "getvalue") else audio_bytes
    if not audio_bytes: return None
    if lang == "mr": return _transcribe_google(audio_bytes, "mr-IN")
    whisper = load_whisper()
    if whisper:
        try:
            import tempfile, os
            with tempfile.NamedTemporaryFile(suffix=".webm", delete=False) as tmp:
                tmp.write(audio_bytes); path = tmp.name
            try:
                prompt = "मला ताप खोकला डोकेदुखी" if lang == "mr" else "मुझे बुखार खांसी" if lang == "hi" else None
                segments, _ = whisper.transcribe(path, language=lang, vad_filter=True, beam_size=5, initial_prompt=prompt)
                return " ".join(s.text for s in segments).strip() or None
            finally: os.unlink(path)
        except Exception: pass
    return _transcribe_google(audio_bytes, {"hi":"hi-IN","en":"en-IN"}.get(lang))

def asr_language_code(language): return "hi" if language == MODE_HINDI else "mr" if language == MODE_MARATHI else "en" if language == MODE_ENGLISH else None
def web_speech_lang(language): return "hi-IN" if language == MODE_HINDI else "mr-IN" if language == MODE_MARATHI else "en-IN"



@st.cache_resource(show_spinner=False)
def load_model():
    try:
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer("all-MiniLM-L6-v2")
    except Exception: return None
