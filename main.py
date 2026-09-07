"""
MahaArogya Setu — Rural Healthcare Access Platform
Smart India Hackathon (SIH) Entrypoint Application
"""
import html
import streamlit as st

# 1. Page Configuration & Theme
from src.config.theme import setup_page
setup_page()

# 2. Imports from modular architecture
from src.config.constants import (
    MODE_HINDI,
    MODE_MARATHI,
    MODE_ENGLISH,
)
from src.config.settings import MAX_QUERY_LENGTH, MAX_HISTORY_LENGTH
from src.data_access.loader import load_data
from src.ml.engine import (
    load_model,
    web_speech_lang,
)
from src.ui.audio import inject_mic_component
from src.ui.views import (
    _ui,
    render_sidebar,
    render_hero,
    render_tabs,
)
from src.ui.pipeline import generate_response

# 3. Load Dataset
df = load_data()

# 4. Session State Initialization
if "history" not in st.session_state:
    st.session_state.history = []
if "prefill_query" not in st.session_state:
    st.session_state.prefill_query = None
if "health_records" not in st.session_state:
    st.session_state.health_records = []
if "conversation_context" not in st.session_state:
    st.session_state.conversation_context = {}

# 5. Sidebar & Hero Header
language, low_bandwidth = render_sidebar()
render_hero()

# 6. Main Tabbed Interface
render_tabs(language)

# 7. Web Microphone Component
inject_mic_component(web_speech_lang(language))

# 8. ML Matcher Resource Cache
@st.cache_resource(show_spinner=False)
def _load_matcher_resources():
    """Cache-safe: loads model + embeddings without session_state dependency."""
    model = load_model()
    if not model:
        return None, None, None
    try:
        return (
            model,
            model.encode(df["symptoms"].tolist(), convert_to_tensor=True),
            model.encode(df["disease"].tolist(), convert_to_tensor=True),
        )
    except Exception:
        return None, None, None

def get_matcher():
    """Per-session wrapper: respects low_bandwidth toggle without polluting cache."""
    if st.session_state.get("low_bandwidth", False):
        return None, None, None
    return _load_matcher_resources()

# 9. Chat Input & Processing Pipeline
placeholder_text = (
    "अपने लक्षण या स्वास्थ्य प्रश्न बताएं..."
    if language == MODE_HINDI
    else "तुमची लक्षणे किंवा आरोग्य प्रश्न सांगा..."
    if language == MODE_MARATHI
    else "Type your symptoms or ask about hospitals, schemes, ABHA..."
)

st.markdown(
    f"""<div style="text-align:center;margin-bottom:4px;padding:6px 0;">
        <span style="font-size:0.78rem;color:#64748B;background:#F8FAFC;border:1px solid #E2E8F0;padding:4px 14px;border-radius:999px;">
            {_ui("voice_hint")}
        </span>
    </div>""",
    unsafe_allow_html=True,
)

query = st.chat_input(placeholder_text)
used_voice, final_query = False, query

if final_query is None and st.session_state.prefill_query:
    final_query, st.session_state.prefill_query = st.session_state.prefill_query, None

if final_query:
    # Input validation
    if len(final_query) > MAX_QUERY_LENGTH:
        final_query = final_query[:MAX_QUERY_LENGTH]
        st.toast(f"⚠️ Query truncated to {MAX_QUERY_LENGTH} characters.", icon="⚠️")

    user_display = f"🎙️ *{html.escape(final_query)}*" if used_voice else html.escape(final_query)
    st.session_state.history.append(("user", user_display))
    with st.chat_message("user", avatar="🧑"):
        st.markdown(user_display)

    with st.chat_message("assistant", avatar="🩺"):
        with st.spinner(_ui("analyzing")):
            model, symptom_embeddings, name_embeddings = get_matcher()
            try:
                response = generate_response(
                    final_query, language, df, symptom_embeddings, name_embeddings, model
                )
            except Exception as e:
                response = f'<div class="th-alert caution"><h4>{_ui("sys_err")}</h4></div>'

        st.session_state.history.append(("assistant", response))
        if len(st.session_state.history) > MAX_HISTORY_LENGTH:
            st.session_state.history = st.session_state.history[-MAX_HISTORY_LENGTH:]
        st.markdown(response, unsafe_allow_html=True)
