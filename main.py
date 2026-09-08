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
from src.ui.cards import render_medicine_showcase_grid, render_clinical_search_loader
from src.ui.views import (
    _ui,
    _render_html,
    render_navbar,
    render_sidebar,
    render_hero,
    render_feature_highlights,
    render_statistics_ribbon,
    render_why_choose_us,
    render_testimonial_section,
    render_tabs,
    render_visibility_fix,
    render_footer,
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

# 5. Sidebar & Top Navigation Bar
language, low_bandwidth = render_sidebar()
render_navbar()

# 6. Hero Header
render_hero()

# 7. Feature Highlights (3 Cards)
render_feature_highlights()

# 8. High-Impact Statistics Ribbon
render_statistics_ribbon()

# 9. ML Matcher Resource Cache
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

# 10. Web Microphone Component & Voice Guidance
inject_mic_component(web_speech_lang(language))
_render_html(
    f"""<div style="text-align:center;margin-bottom:8px;padding:4px 0;">
<span style="font-size:0.78rem;color:#64748B;background:#F8FAFC;border:1px solid #E2E8F0;padding:4px 14px;border-radius:999px;">
{_ui("voice_hint")}
</span>
</div>"""
)

# 11. Chat Input & Processing Pipeline (Executes before render_tabs so Tab 1 displays latest messages)
placeholder_text = (
    "अपने लक्षण या स्वास्थ्य प्रश्न बताएं..."
    if language == MODE_HINDI
    else "तुमची लक्षणे किंवा आरोग्य प्रश्न सांगा..."
    if language == MODE_MARATHI
    else "Type your symptoms or ask about hospitals, schemes, ABHA..."
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

    loader_placeholder = st.empty()
    loader_placeholder.markdown(render_clinical_search_loader(language), unsafe_allow_html=True)

    try:
        model, symptom_embeddings, name_embeddings = get_matcher()
        response = generate_response(
            final_query, language, df, symptom_embeddings, name_embeddings, model
        )
    except Exception as e:
        response = f'<div class="th-alert caution"><h4>{_ui("sys_err")}</h4></div>'
    finally:
        loader_placeholder.empty()

    st.session_state.history.append(("assistant", response))
    if len(st.session_state.history) > MAX_HISTORY_LENGTH:
        st.session_state.history = st.session_state.history[-MAX_HISTORY_LENGTH:]

# 12. Main Interactive Hub (Tabs) — Renders conversation history directly inside Tab 1
render_tabs(language)

# 13. "Proven Medical Relief" Generic Medicine Showcase Grid
_render_html(render_medicine_showcase_grid(st.session_state.get("_ui_lang", "en")))

# 14. "Why Choose Us" / Core Capabilities 4-Grid
render_why_choose_us()

# 15. Frontline Health Worker Spotlight
render_testimonial_section()

# 16. Modern Branded Footer
render_footer()

# 17. Global Visibility Enhancements
render_visibility_fix()
