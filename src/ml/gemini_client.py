"""Google Gemini Flash Client for Clinical AI Triage and Query Resolution."""
import os
import json
import logging
import html
import requests
import streamlit as st
from src.config.settings import (
    DEFAULT_GEMINI_MODEL,
    FALLBACK_GEMINI_MODEL,
    GEMINI_TIMEOUT_SECONDS,
)

logger = logging.getLogger(__name__)

def get_gemini_api_key() -> str:
    """Retrieve Gemini API key from environment, Streamlit secrets, or local configuration files.
    The API key is handled securely in the backend and is NEVER rendered or exposed in the UI.
    """
    # 1. Streamlit secrets
    try:
        if hasattr(st, "secrets"):
            if "GEMINI_API_KEY" in st.secrets and st.secrets["GEMINI_API_KEY"]:
                return str(st.secrets["GEMINI_API_KEY"]).strip()
            if "GOOGLE_API_KEY" in st.secrets and st.secrets["GOOGLE_API_KEY"]:
                return str(st.secrets["GOOGLE_API_KEY"]).strip()
    except Exception:
        pass

    # 2. Environment variables
    env_key = os.environ.get("GEMINI_API_KEY") or os.environ.get("GOOGLE_API_KEY")
    if env_key and env_key.strip():
        return env_key.strip()

    # 3. Direct inspection of .streamlit/secrets.toml
    try:
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        secrets_candidates = [
            os.path.join(project_root, ".streamlit", "secrets.toml"),
            os.path.join(os.getcwd(), ".streamlit", "secrets.toml"),
        ]
        for sec_path in secrets_candidates:
            if os.path.isfile(sec_path):
                with open(sec_path, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        if "=" in line:
                            k, v = line.split("=", 1)
                            k, v = k.strip(), v.strip().strip("'\"")
                            if k in ("GEMINI_API_KEY", "GOOGLE_API_KEY") and v:
                                return v
    except Exception:
        pass

    # 4. Direct inspection of .env
    try:
        project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        env_candidates = [
            os.path.join(project_root, ".env"),
            os.path.join(os.getcwd(), ".env"),
        ]
        for env_p in env_candidates:
            if os.path.isfile(env_p):
                with open(env_p, "r", encoding="utf-8") as f:
                    for line in f:
                        line = line.strip()
                        if not line or line.startswith("#"):
                            continue
                        if "=" in line:
                            k, v = line.split("=", 1)
                            k, v = k.strip(), v.strip().strip("'\"")
                            if k in ("GEMINI_API_KEY", "GOOGLE_API_KEY") and v:
                                return v
    except Exception:
        pass

    # 5. Streamlit Session State (Internal session storage if set programmatically)
    try:
        if "gemini_api_key" in st.session_state and st.session_state.gemini_api_key:
            return str(st.session_state.gemini_api_key).strip()
    except Exception:
        pass

    return ""


def is_gemini_available() -> bool:
    """Check if Gemini Flash is ready and allowed (disabled in low-bandwidth mode)."""
    try:
        if st.session_state.get("low_bandwidth", False):
            return False
    except Exception:
        pass
    return bool(get_gemini_api_key())


def _build_system_instruction(response_lang: str) -> str:
    """Construct a rigorous rural clinical triage system instruction."""
    lang_name = "मराठी (Marathi)" if response_lang == "mr" else ("हिंदी (Hindi)" if response_lang == "hi" else "English")
    return f"""You are 'MahaArogya AI Clinical Officer', an empathetic and expert medical triage assistant designed for rural and tribal Maharashtra, India (Smart India Hackathon).

Target Response Language: {lang_name}. You MUST generate your ENTIRE answer in {lang_name}.

Clinical Guidelines:
1. Immediate Triage Assessment: State whether symptoms appear MILD (self-care/PHC), MODERATE (CHC/SDH review within 24h), or CRITICAL/URGENT (seek immediate hospital care/Call 108).
2. Potential Causes: Explain 1-3 likely conditions in simple, non-alarmist layperson terms.
3. Red Flag Warning: Clearly highlight emergency danger signs (e.g. difficulty breathing, stiff neck, blood in cough/vomit, dehydration in infants, high fever >3 days).
4. Home Comfort & Safe Care: Recommend safe immediate supportive care (e.g. ORS hydration, tepid sponging for fever, rest, nutrition). NEVER prescribe schedule-H prescription antibiotics without a doctor's physical exam.
5. Public Healthcare Navigation: Guide the citizen to appropriate Maharashtra public facilities (Arogya Vardhini Kendra / PHC / CHC / District Hospital) and mention relevant schemes:
   - Mahatma Jyotirao Phule Jan Arogya Yojana (MJPJAY) for cashless hospitalization up to ₹5 Lakh.
   - Ayushman Bharat (PM-JAY).
   - Janani Suraksha Yojana (JSY) for ₹700 cash aid for rural institutional delivery.
6. Tone: Warm, respectful, clear, reassuring, and culturally accessible for rural families.
7. Always advise calling 108 for emergency MEMS ambulance or 104 for free state health advice.
"""


def query_gemini_flash(
    query: str,
    response_lang: str = "en",
    entities: dict = None,
    matched_disease_row: dict = None,
    matched_facilities: list = None,
) -> str:
    """Invoke Gemini Flash with patient context and groundings."""
    api_key = get_gemini_api_key()
    if not api_key:
        return ""

    entities = entities or {}
    age_str = f"{entities.get('age', '')} {entities.get('age_unit', '')}".strip()
    patient_group = entities.get("age_group", "adult")
    is_preg = entities.get("is_pregnant", False)
    district = entities.get("district", "")

    # Normalize matched_disease_row safely if it's a pandas Series or dict-like object
    disease_dict = None
    if matched_disease_row is not None:
        try:
            if hasattr(matched_disease_row, "to_dict"):
                disease_dict = matched_disease_row.to_dict()
            elif hasattr(matched_disease_row, "items"):
                disease_dict = dict(matched_disease_row)
            elif isinstance(matched_disease_row, dict):
                disease_dict = matched_disease_row
        except Exception as conv_err:
            logger.warning(f"Error converting matched_disease_row: {conv_err}")

    # Grounding context from local database
    grounding_info = []
    if district:
        grounding_info.append(f"Patient District: {district}, Maharashtra")
    if age_str:
        grounding_info.append(f"Patient Age: {age_str} ({patient_group})")
    if is_preg:
        grounding_info.append("Patient is Pregnant")

    if disease_dict:
        d_name = disease_dict.get("disease", "")
        d_sym = disease_dict.get("symptoms", "")
        d_prev = disease_dict.get("prevention", "")
        d_fac = disease_dict.get("recommended_facility", "PHC")
        grounding_info.append(
            f"Local Reference Clinical Database Match:\n- Suspected Condition: {d_name}\n- Common Symptoms: {d_sym}\n- Prevention/Care: {d_prev}\n- Recommended Facility Level: {d_fac}"
        )

    if matched_facilities:
        fac_names = [f.get("name", "") + f" ({f.get('type', '')} in {f.get('location', '')})" for f in matched_facilities[:3]]
        grounding_info.append(f"Nearby Verified Government Facilities in {district}:\n- " + "\n- ".join(fac_names))

    grounding_text = "\n".join(grounding_info)

    user_prompt = f"""Patient Query: "{query}"

Clinical Context & Local Grounding:
{grounding_text}

Provide an immediate, well-structured, compassionate triage response in {response_lang.upper()} following the required clinical guidelines."""

    system_instruction = _build_system_instruction(response_lang)

    candidate_models = [
        DEFAULT_GEMINI_MODEL,
        "gemini-3.5-flash",
        "gemini-3.6-flash",
        "gemini-3.7-flash",
        "gemini-flash-latest",
        FALLBACK_GEMINI_MODEL,
    ]
    seen = set()
    models_to_try = [m for m in candidate_models if m and not (m in seen or seen.add(m))]

    # 1. Try google.genai SDK
    try:
        from google import genai
        client = genai.Client(api_key=api_key)

        for model_name in models_to_try:
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=user_prompt,
                    config={
                        "system_instruction": system_instruction,
                        "temperature": 0.25,
                    },
                )
                if response and response.text:
                    return _format_ai_response_card(response.text, model_name, response_lang)
            except Exception as model_err:
                logger.warning(f"Failed SDK call with {model_name}: {model_err}")
                continue
    except ImportError:
        logger.info("google-genai not available, falling back to REST API.")
    except Exception as sdk_err:
        logger.warning(f"SDK call error: {sdk_err}, trying REST API.")

    # 2. Resilient REST API fallback
    try:
        return _query_gemini_rest(api_key, user_prompt, system_instruction, response_lang, models_to_try)
    except Exception as rest_err:
        logger.error(f"Gemini REST call failed: {rest_err}")
        return ""


def _query_gemini_rest(api_key: str, user_prompt: str, system_instruction: str, response_lang: str, models_to_try: list = None) -> str:
    """Direct HTTP fallback to Gemini REST endpoint."""
    headers = {"Content-Type": "application/json"}
    payload = {
        "contents": [{"parts": [{"text": user_prompt}]}],
        "systemInstruction": {"parts": [{"text": system_instruction}]},
        "generationConfig": {"temperature": 0.25},
    }

    if not models_to_try:
        models_to_try = [DEFAULT_GEMINI_MODEL, "gemini-3.5-flash", "gemini-3.6-flash"]

    for model_name in models_to_try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
        try:
            resp = requests.post(url, headers=headers, json=payload, timeout=GEMINI_TIMEOUT_SECONDS)
            if resp.status_code == 200:
                data = resp.json()
                candidates = data.get("candidates", [])
                if candidates:
                    parts = candidates[0].get("content", {}).get("parts", [])
                    if parts and "text" in parts[0]:
                        return _format_ai_response_card(parts[0]["text"], model_name, response_lang)
            else:
                logger.warning(f"REST attempt for {model_name} HTTP {resp.status_code}: {resp.text[:150]}")
        except Exception as e:
            logger.warning(f"REST attempt for {model_name} failed: {e}")
            continue

    return ""



def _format_ai_response_card(text: str, model_used: str, lang: str) -> str:
    """Format the raw Markdown from Gemini Flash into our clinical landing card design."""
    try:
        import markdown
        parsed_html = markdown.markdown(text, extensions=["extra", "nl2br"])
    except Exception:
        import re
        # Lightweight built-in markdown parser
        lines = []
        for l in text.splitlines():
            l = html.escape(l)
            l = re.sub(r"\*\*(.*?)\*\*", r"<strong>\1</strong>", l)
            l = re.sub(r"\*(.*?)\*", r"<em>\1</em>", l)
            if l.startswith("### "): lines.append(f"<h4 style='color:#0B2528;margin:10px 0 4px;'>{l[4:]}</h4>")
            elif l.startswith("## "): lines.append(f"<h3 style='color:#0B2528;margin:12px 0 6px;'>{l[3:]}</h3>")
            elif l.startswith("# "): lines.append(f"<h2 style='color:#0B2528;margin:14px 0 8px;'>{l[2:]}</h2>")
            elif l.startswith("- ") or l.startswith("* "): lines.append(f"<li>{l[2:]}</li>")
            else: lines.append(f"<p style='margin:4px 0;'>{l}</p>" if l.strip() else "<br/>")
        parsed_html = "\n".join(lines)

    badge_title = "✨ GEMINI FLASH CLINICAL AI TRIAGE"
    disclaimer = (
        "हे एआय आधारित प्राथमिक मार्गदर्शन आहे. गंभीर लक्षणांमध्ये त्वरित १०८ रुग्णवाहिका किंवा शासकीय जिल्हा रुग्णालयात संपर्क साधावा."
        if lang == "mr"
        else (
            "यह एआई आधारित प्राथमिक मार्गदर्शन है। गंभीर स्थिति में तुरंत 108 एम्बुलेंस या सरकारी जिला अस्पताल से संपर्क करें।"
            if lang == "hi"
            else "AI Clinical Guidance · In critical or worsening symptoms, immediately call 108 Ambulance or visit nearest District Hospital."
        )
    )

    card_html = f"""
<div class="th-dx-card" style="border: 2px solid #00D2B4; box-shadow: 0 8px 26px rgba(0, 210, 180, 0.12); margin-bottom: 16px;">
    <div class="th-dx-header" style="background: linear-gradient(135deg, #0B2528 0%, #00A892 100%);">
        <div style="display:flex;align-items:center;gap:10px;">
            <span style="font-size:24px;">🩺</span>
            <div>
                <strong style="font-size:1.02rem;color:#FFFFFF;display:block;">MahaArogya AI Clinical Consultant</strong>
                <span style="font-size:0.72rem;color:#E0F8F4;font-weight:700;letter-spacing:0.04em;">{badge_title}</span>
            </div>
        </div>
        <span style="font-size:0.72rem;background:rgba(255,255,255,0.2);color:#FFFFFF;padding:4px 10px;border-radius:999px;font-weight:700;">
            SIH Clinical Core
        </span>
    </div>
    <div class="th-dx-body" style="padding:22px 26px;color:#0B2528;font-size:0.94rem;line-height:1.65;">
        {parsed_html}
        <div style="margin-top:18px;padding:10px 14px;background:#F2FBF9;border-left:4px solid #00D2B4;border-radius:8px;font-size:0.80rem;color:#3D585B;">
            ⚠️ <strong>Disclaimer:</strong> {disclaimer}
        </div>
    </div>
</div>
"""
    return "\n".join(line.strip() for line in card_html.splitlines())
