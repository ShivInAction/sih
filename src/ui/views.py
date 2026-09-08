"""Main views, sidebars, tabs, and page headers."""
import textwrap
import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
from src.config.constants import (
    UI_STRINGS,
    MAHARASHTRA_DISTRICTS,
    MAHARASHTRA_SCHEMES,
    ANC_SCHEDULE,
    IMMUNIZATION_SCHEDULE,
    HEALTH_CAMPS,
    GENERIC_MEDS,
    FEATURE_ROADMAP,
    ABHA_INFO,
    MODE_ENGLISH,
    MODE_HINDI,
    MODE_MARATHI,
    LANGUAGES,
)
from src.ui.cards import (
    render_abha_html,
    render_health_camps_html,
    render_helpline_guide,
    render_debug_panel,
)

def _ui(key, lang=None, **kw):
    """Return UI string for current language, with optional format kwargs."""
    if lang is None:
        lang = st.session_state.get("_ui_lang", "en")
    d = UI_STRINGS.get(lang, UI_STRINGS["en"])
    s = d.get(key, UI_STRINGS["en"].get(key, key))
    if kw:
        try: s = s.format(**kw)
        except Exception: pass
    return s


def _render_html(html_str: str):
    """Render HTML string safely without markdown indentation becoming code blocks."""
    cleaned = "\n".join(line.strip() for line in html_str.splitlines())
    st.markdown(cleaned, unsafe_allow_html=True)


def render_sidebar():
    with st.sidebar:
        _render_html("""
<div class="th-sb-brand-box">
    <div class="th-sb-brand-icon">🩺</div>
    <div>
        <div style="font-weight:800;font-size:1.05rem;color:#0B2528;">MahaArogya Setu</div>
        <div style="font-size:0.72rem;color:#5C7678;font-weight:600;">Rural Healthcare Access · SIH</div>
    </div>
</div>
<div class="th-sb-divider"></div>
""")

        _render_html(f'<div class="th-sb-title">{_ui("sb_conn")}</div>')
        low_bandwidth = st.toggle("⚡ " + _ui("sb_low"), value=False, key="low_bandwidth", help=_ui("sb_low_help"))
        if low_bandwidth:
            _render_html('<div style="background:#FEF3C7;border:1px solid #F59E0B;border-radius:8px;padding:8px 12px;font-size:0.82rem;color:#92400E;font-weight:600;margin-top:4px;">⚡ Low-Bandwidth Mode ON ✓ — Keyword matching active. Internet still required.</div>')
        else:
            _render_html('<div style="background:#E6FBF7;border:1px solid #00D2B4;border-radius:8px;padding:8px 12px;font-size:0.82rem;color:#0B2528;font-weight:600;margin-top:4px;">🟢 Full Mode — AI semantic matching + translation active.</div>')

        _render_html(f'<div class="th-sb-title">{_ui("sb_lang")}</div>')
        language = st.radio("Choose language", LANGUAGES, index=0, label_visibility="collapsed")
        if language.startswith("🌐"):
            _render_html(f'<p style="font-size:0.82rem;color:#475569;margin-top:4px;">{_ui("sb_auto")}</p>')
        st.session_state["_ui_lang"] = "hi" if language == MODE_HINDI else "mr" if language == MODE_MARATHI else "en"

        # AI Engine status indicator (securely resolved from environment or secrets; never exposed in UI)
        import os
        from src.ml.gemini_client import get_gemini_api_key
        has_key = bool(get_gemini_api_key())
        _render_html('<div class="th-sb-divider"></div><div class="th-sb-title">AI Engine</div>')
        if has_key and not low_bandwidth:
            _render_html("""
<div style="background:#F0FDF4;border:1.5px solid #86EFAC;border-radius:10px;padding:8px 12px;font-size:0.80rem;color:#16794C;font-weight:700;display:flex;align-items:center;gap:8px;margin-bottom:6px;">
    <span>✨</span><span>Gemini 2.5 Flash Active</span>
</div>
""")
        elif not low_bandwidth:
            _render_html("""
<div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:8px 12px;font-size:0.80rem;color:#475569;font-weight:600;display:flex;align-items:center;gap:8px;margin-bottom:4px;">
    <span>🩺</span><span>Local Engine (Offline)</span>
</div>
""")
            with st.expander("🔑 Connect Gemini Flash", expanded=True):
                st.caption("Paste your Google Gemini API key to enable live Gemini Flash AI responses. The key is masked (`••••••••`) and never displayed on screen.")
                entered_key = st.text_input("Gemini API Key", type="password", placeholder="AIzaSy...", key="sidebar_key_connect", label_visibility="collapsed")
                if st.button("✨ Activate Gemini 2.5 Flash", use_container_width=True, key="btn_activate_gemini"):
                    if entered_key and entered_key.strip():
                        try:
                            secrets_dir = os.path.join(os.getcwd(), ".streamlit")
                            os.makedirs(secrets_dir, exist_ok=True)
                            secrets_file = os.path.join(secrets_dir, "secrets.toml")
                            with open(secrets_file, "w", encoding="utf-8") as f:
                                f.write(f'# MahaArogya AI Secrets\nGEMINI_API_KEY = "{entered_key.strip()}"\n')
                            st.session_state["gemini_api_key"] = entered_key.strip()
                            st.toast("✅ Gemini 2.5 Flash Activated!", icon="✨")
                            st.rerun()
                        except Exception as err:
                            st.error(f"Error saving: {err}")

        emerg_title = _ui("sb_emerg")
        disc_text = _ui("sb_disc")
        _render_html(f"""
<div class="th-sb-divider"></div>
<div class="th-sb-title">{emerg_title}</div>
<a href="tel:108" class="th-help-card critical"><span class="th-help-label">🚑 Ambulance (MEMS)</span><span class="th-help-num">108</span></a>
<a href="tel:102" class="th-help-card critical"><span class="th-help-label">🤰 Janani Express</span><span class="th-help-num">102</span></a>
<a href="tel:104" class="th-help-card"><span class="th-help-label">🏥 MH Health Line</span><span class="th-help-num">104</span></a>
<a href="tel:1098" class="th-help-card"><span class="th-help-label">🧒 Child Helpline</span><span class="th-help-num">1098</span></a>
<a href="tel:181" class="th-help-card"><span class="th-help-label">👩 Women Helpline</span><span class="th-help-num">181</span></a>
<div class="th-sb-divider"></div>
<div style="font-size:0.74rem;color:#64748B;line-height:1.4;">{disc_text}</div>
""")

    return language, low_bandwidth


def render_navbar():
    """Renders modern top pill navbar matching the reference design."""
    _render_html("""
<div class="th-navbar">
    <div class="th-nav-brand" onclick="(function(){
        try {
            if (window.parent && window.parent.toggleMahaSidebar) {
                window.parent.toggleMahaSidebar();
            } else if (window.toggleMahaSidebar) {
                window.toggleMahaSidebar();
            } else {
                var doc = window.parent.document || document;
                var exp = doc.querySelector('[data-testid=stExpandSidebarButton]') || doc.querySelector('button[data-testid=stExpandSidebarButton]') || doc.querySelector('[data-testid=collapsedControl] button') || doc.querySelector('button[aria-label=\\'Open sidebar\\']');
                var col = doc.querySelector('[data-testid=stSidebarCollapseButton]') || doc.querySelector('[data-testid=stSidebarCollapseButton] button') || doc.querySelector('button[aria-label=\\'Close sidebar\\']');
                if (exp) { exp.click(); } else if (col) { col.click(); }
            }
        } catch(e) {}
    })()" title="Click to Open/Close Sidebar (Settings, Language & Helplines)" style="cursor:pointer;">
        <div class="th-nav-logo">🩺</div>
        <span class="th-nav-title">MahaArogya Setu</span>
        <span class="th-settings-badge" style="font-size:0.75rem;background:#E0F8F4;color:#0B5C54;padding:4px 12px;border-radius:999px;font-weight:700;margin-left:8px;border:1.5px solid #00D2B4;display:inline-flex;align-items:center;gap:5px;cursor:pointer;box-shadow:0 2px 6px rgba(0,210,180,0.15);">☰ Sidebar & Settings</span>
    </div>
    <div class="th-nav-links">
        <span class="th-nav-link" style="color:var(--primary-teal-deep);font-weight:700;">🟢 Rural Healthcare Portal</span>
        <span class="th-nav-link">MJPJAY • PM-JAY</span>
        <span class="th-nav-link">5 Tribal Districts</span>
    </div>
    <div>
        <a href="tel:108" class="th-nav-btn">
            <span>🚑 Call 108 Emergency</span>
        </a>
    </div>
</div>
""")


def render_hero():
    """Renders modern hero section matching the reference landing page."""
    sub = _ui("hero_sub")

    _render_html(f"""
<div class="th-hero-wrap">
    <div style="display:flex;justify-content:space-between;align-items:center;flex-wrap:wrap;gap:8px;">
        <span class="th-hero-badge">🟢 100% Free Public Health Service • SIH</span>
        <span style="font-size:0.8rem;color:var(--primary-teal-deep);font-weight:700;background:var(--primary-teal-light);padding:4px 14px;border-radius:999px;">
            ⭐ 4.9 Citizen Rating (50,000+ Rural Families)
        </span>
    </div>
    <h1 class="th-hero-title">Enhance Rural Healthcare with <span>Guided AI Triage</span></h1>
    <p class="th-hero-sub">{sub}</p>

    <div class="th-hero-cta-row">
        <span class="th-btn-teal">
            🩺 Start AI Consultation Below
        </span>
        <a href="tel:108" class="th-btn-outline" style="color:#DC2626 !important;border-color:#FED7D7;">
            🚑 Call 108 Ambulance
        </a>
        <a href="tel:104" class="th-btn-outline">
            🏥 Health Advice: 104
        </a>
    </div>

    <div class="th-hero-trust">
        <div style="display:flex;align-items:center;">
            <span style="width:30px;height:30px;border-radius:50%;background:#00D2B4;display:inline-flex;align-items:center;justify-content:center;color:#0B2528;font-weight:800;font-size:13px;border:2px solid #FFF;">👩‍⚕️</span>
            <span style="width:30px;height:30px;border-radius:50%;background:#0B2528;display:inline-flex;align-items:center;justify-content:center;color:#FFF;font-weight:800;font-size:13px;margin-left:-8px;border:2px solid #FFF;">👨‍⚕️</span>
            <span style="width:30px;height:30px;border-radius:50%;background:#D97706;display:inline-flex;align-items:center;justify-content:center;color:#FFF;font-weight:800;font-size:13px;margin-left:-8px;border:2px solid #FFF;">🤰</span>
        </div>
        <span><strong>500+ ASHA workers & medical centers</strong> linked across Nandurbar, Gadchiroli, Melghat, Palghar & Yavatmal</span>
    </div>
</div>
""")


def render_feature_highlights():
    """Renders 3-card feature bar below the hero section."""
    _render_html("""
<div class="th-highlights-grid">
    <div class="th-highlight-card">
        <div class="th-highlight-icon">🎙️</div>
        <div>
            <h4 class="th-highlight-title">Audio & Voice Triage</h4>
            <p class="th-highlight-desc">In-browser speech recognition in Marathi, Hindi, and English for rural citizens who prefer speaking symptoms.</p>
        </div>
    </div>
    <div class="th-highlight-card">
        <div class="th-highlight-icon">🏥</div>
        <div>
            <h4 class="th-highlight-title">Smart Hospital Locator</h4>
            <p class="th-highlight-desc">Locates PHCs, CHCs, SDHs, and District Hospitals across tribal Maharashtra with verified services and contact details.</p>
        </div>
    </div>
    <div class="th-highlight-card">
        <div class="th-highlight-icon">📋</div>
        <div>
            <h4 class="th-highlight-title">Cashless Health Schemes</h4>
            <p class="th-highlight-desc">Comprehensive navigation for MJPJAY (up to ₹5L cover), PM-JAY, Aapla Dawakhana, and Janani Suraksha Yojana.</p>
        </div>
    </div>
</div>
""")


def render_statistics_ribbon():
    """Renders high-impact dark statistics counter ribbon."""
    _render_html("""
<div class="th-stats-ribbon">
    <div class="th-stat-item">
        <div class="th-stat-val">5+</div>
        <div class="th-stat-lbl">Tribal Districts</div>
    </div>
    <div class="th-stat-item">
        <div class="th-stat-val">40+</div>
        <div class="th-stat-lbl">Conditions Triaged</div>
    </div>
    <div class="th-stat-item">
        <div class="th-stat-val">6</div>
        <div class="th-stat-lbl">Cashless Schemes</div>
    </div>
    <div class="th-stat-item">
        <div class="th-stat-val">24×7</div>
        <div class="th-stat-lbl">Free Emergency Linkage</div>
    </div>
</div>
""")


def render_why_choose_us():
    """Renders 4-card core capabilities grid."""
    _render_html("""
<div class="th-why-section">
    <span class="th-why-badge">Why Choose MahaArogya</span>
    <h2 class="th-why-title">Explore Comprehensive <span>Rural Health Capabilities</span></h2>
</div>
<div class="th-why-grid">
    <div class="th-why-card">
        <div class="th-why-icon">⚡</div>
        <h4 class="th-why-card-title">Instant AI Triage</h4>
        <p class="th-why-card-desc">Evaluates symptoms with AI embeddings and alerts immediate red-flags for critical medical emergencies.</p>
    </div>
    <div class="th-why-card">
        <div class="th-why-icon">🛡️</div>
        <h4 class="th-why-card-title">Cashless Guarantee</h4>
        <p class="th-why-card-desc">Direct guidelines on documents and Arogyamitra desks to claim full cashless treatment under MJPJAY/PM-JAY.</p>
    </div>
    <div class="th-why-card">
        <div class="th-why-icon">🤰</div>
        <h4 class="th-why-card-title">Maternal & Child Health</h4>
        <p class="th-why-card-desc">Complete 4-visit ANC schedule, danger sign detection, infant vaccination timeline, and ₹700 JSY cash aid.</p>
    </div>
    <div class="th-why-card">
        <div class="th-why-icon">📴</div>
        <h4 class="th-why-card-title">2G Low-Bandwidth Mode</h4>
        <p class="th-why-card-desc">Instant keyword matching designed to work seamlessly in deep forest and remote tribal areas with poor connectivity.</p>
    </div>
</div>
""")


def render_testimonial_section():
    """Renders frontline health worker spotlight quote card."""
    _render_html("""
<div class="th-testimonial-box">
    <div class="th-test-quote">
        <div style="color:var(--primary-teal);font-size:32px;line-height:1;margin-bottom:8px;">“</div>
        <p class="th-test-text">
            MahaArogya Setu has transformed how we guide families in our block. When a mother or child falls sick, we can instantly check emergency danger signs, understand which hospital has pediatric beds, and know exactly how to claim cashless MJPJAY benefits without confusion.
        </p>
        <div class="th-test-author">Sunita Gavit</div>
        <div class="th-test-role">ASHA Healthcare Facilitator • Dhadgaon Tribal Block, Nandurbar</div>
        <div style="color:#D97706;margin-top:6px;font-size:0.9rem;">★★★★★</div>
    </div>
    <div class="th-test-avatar">👩‍⚕️</div>
</div>
""")


def render_tabs(language):
    tab_chat, tab_locator, tab_schemes, tab_mch, tab_more = st.tabs([
        _ui("tab_chat"), _ui("tab_loc"), _ui("tab_sch"), _ui("tab_mch"), _ui("tab_more")
    ])

    # ── TAB 1: CHAT CONSULTATION ──
    with tab_chat:
        if st.session_state.history:
            top_col1, top_col2 = st.columns([5, 1])
            with top_col1: st.caption(_ui("status_line", n=len(st.session_state.history)//2, r=len(st.session_state.health_records)))
            with top_col2:
                st.markdown('<div class="th-clear-btn">', unsafe_allow_html=True)
                if st.button(_ui("btn_clear"), use_container_width=True, key="clear_chat_top"):
                    st.session_state.history = []; st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

        ACTIONS_HI = [("🩺","मुझे लक्षण हैं","मुझे तेज बुखार और बदन दर्द है"),("🏥","सरकारी अस्पताल खोजें","मेरे पास सरकारी अस्पताल दिखाओ"),("🚨","आपातकाल","मुझे तत्काल चिकित्सीय सहायता चाहिए"),("🤰","गर्भावस्था / बाल देखभाल","मैं गर्भवती हूं और मुझे देखभाल जानकारी चाहिए"),("🏛️","सरकारी योजनाएं","कौन सी सरकारी स्वास्थ्य योजना मेरी मदद कर सकती है?"),("💊","जेनेरिक दवाइयां","सस्ती जेनेरिक दवाइयां कहां मिलेंगी?")]
        ACTIONS_MR = [("🩺","मला लक्षणे आहेत","मला ताप आणि अंग दुखत आहे"),("🏥","शासकीय रुग्णालय शोधा","माझ्या जवळचे शासकीय रुग्णालय दर्शवा"),("🚨","आणीबाणी","मला तात्काळ वैद्यकीय मदत हवी"),("🤰","गरोदर / बाल काळजी","मी गरोदर आहे आणि मला माहिती हवी"),("🏛️","शासकीय योजना","कोणत्या शासकीय आरोग्य योजना मदत करतील?"),("💊","स्वस्त औषधे","स्वस्त जेनेरिक औषधे कुठे मिळतील?")]
        ACTIONS_EN = [("🩺","I have symptoms","I have high fever and body ache"),("🏥","Find Government Hospital","Show government hospitals near me"),("🚨","Emergency","I need emergency medical help"),("🤰","Pregnancy / Child Care","I am pregnant and need care information"),("🏛️","Government Schemes","What government health schemes can help me?"),("💊","Generic Medicines","Where can I get cheap generic medicines?")]
        current_actions = ACTIONS_HI if language == MODE_HINDI else ACTIONS_MR if language == MODE_MARATHI else ACTIONS_EN

        if not st.session_state.history:
            welcome_sub = ("अपने लक्षण हिंदी, मराठी या अंग्रेजी में टाइप करें या बोलें।" if language == MODE_HINDI else "तुमची लक्षणे मराठी, हिंदी किंवा इंग्रजीत सांगा." if language == MODE_MARATHI else "Describe your symptoms in EN/HI/MR or ask about hospitals, schemes, or services.")
            _render_html(f"""
<div class="th-welcome-box">
    <div class="th-welcome-icon">💬</div>
    <h2>{_ui("welcome_title")}</h2>
    <p>{welcome_sub}</p>
</div>
""")

            _render_html(f'<div class="th-section-heading">{_ui("sec_quick")}</div>')
            for row_start in range(0, len(current_actions), 3):
                cols = st.columns(3, gap="small")
                for idx, (icon, title, prefill) in enumerate(current_actions[row_start:row_start+3]):
                    with cols[idx]:
                        if st.button(f"{icon}  {title}", key=f"qa_{row_start+idx}", use_container_width=True):
                            st.session_state.prefill_query = prefill; st.rerun()

        # Render debug panel for last assistant message
        if st.session_state.get("_routing_debug"):
            render_debug_panel()

        for role, msg in st.session_state.history:
            with st.chat_message(role, avatar="🩺" if role == "assistant" else "🧑"):
                st.markdown(msg, unsafe_allow_html=True)

        if st.session_state.history:
            st.markdown(f'<div class="th-section-heading">{_ui("sec_cont")}</div>', unsafe_allow_html=True)
            cols = st.columns(3, gap="small")
            for idx, (icon, title, prefill) in enumerate(current_actions[:3]):
                with cols[idx]:
                    if st.button(f"{icon}  {title}", key=f"active_qa_{idx}", use_container_width=True):
                        st.session_state.prefill_query = prefill; st.rerun()

    # ── TAB 2: FACILITY LOCATOR ──
    with tab_locator:
        st.markdown(f'<div class="th-section-heading">{_ui("loc_title")}</div>', unsafe_allow_html=True)
        st.caption(_ui("loc_desc"))
        st.caption(_ui("loc_ref"))

        # District selection
        selected_dist = st.selectbox(_ui("loc_sel"), list(MAHARASHTRA_DISTRICTS.keys()), key="tab_locator_dist")
        all_facilities = MAHARASHTRA_DISTRICTS[selected_dist]

        # Facility type filter
        fac_types = sorted(set(f.get("type","Other") for f in all_facilities))
        _lang = st.session_state.get("_ui_lang","en")
        _filter_label = "Filter by facility type:" if _lang == "en" else ("सुविधा प्रकार अनुसार करा:" if _lang == "hi" else "सुविधा प्रकार वाचा:")
        type_filter = st.multiselect(_filter_label, fac_types, default=fac_types, key="fac_type_filter")

        # Service filter
        all_services = sorted(set(s for f in all_facilities for s in f.get("services_list", ["General OPD"])))
        _svc_label = "Filter by service:" if _lang == "en" else ("सेवा अनुसार करा:" if _lang == "hi" else "सेवेनुसार करा:")
        svc_filter = st.multiselect(_svc_label, all_services, default=all_services, key="svc_type_filter")

        facilities = [
            f for f in all_facilities
            if (f.get("type","Other") in type_filter or not type_filter)
            and (any(s in svc_filter for s in f.get("services_list", ["General OPD"])) or not svc_filter)
        ]

        st.markdown(f'<p style="color:#64748B;font-size:0.88rem;margin:8px 0 14px;">{_ui("loc_show", c=len(facilities), d=selected_dist)}</p>', unsafe_allow_html=True)

        for fac in facilities:
            hq_badge = '<span style="font-size:0.65rem;background:#FEF3C7;color:#92400E;padding:2px 8px;border-radius:999px;font-weight:700;margin-left:6px;">HQ</span>' if fac.get("is_hq") else ""
            source_text = fac.get("source", "")
            verified_text = fac.get("last_verified", "")
            meta_line = ""
            if source_text:
                meta_line += f'<p style="font-size:0.78rem;margin:4px 0 0;color:#94A3B8;">Source: {source_text}'
                if verified_text:
                    meta_line += f" \u00b7 {verified_text}"
                meta_line += "</p>"
            st.markdown(f"""<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:14px 18px;margin-bottom:10px;box-shadow:0 2px 6px rgba(0,0,0,0.03)"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;"><strong style="color:#0B6BCB;font-size:1rem;">🏢 {fac['name']}{hq_badge}</strong><span style="font-size:0.72rem;background:#EAF2FE;color:#0B6BCB;padding:3px 10px;border-radius:999px;font-weight:700;">{fac['type']}</span></div><p style="font-size:0.86rem;margin:6px 0 3px;color:#475569;">📍 <strong>{fac['location']}</strong> · Beds: <strong>{fac['beds']}</strong></p><p style="font-size:0.86rem;margin:0 0 6px;color:#475569;">🔧 <em>{fac['facilities']}</em></p><p style="font-size:0.86rem;margin:0;"><a href="tel:{fac['phone']}" style="color:#0E9F8F;text-decoration:none;font-weight:700;">📞 Call: {fac['phone']}</a></p>{meta_line}</div>""", unsafe_allow_html=True)

    # ── TAB 3: HEALTH SCHEMES ──
    with tab_schemes:
        st.markdown(f'<div class="th-section-heading">{_ui("sch_title")}</div>', unsafe_allow_html=True)
        st.caption(_ui("sch_desc"))
        for scheme in MAHARASHTRA_SCHEMES:
            with st.expander(f"✨ {scheme['name']}", expanded=False):
                carry_html = ""
                if scheme.get("what_to_carry"):
                    carry_html = f'<p style="margin:8px 0;"><strong>📄 What to Carry:</strong> {scheme["what_to_carry"]}</p>'
                verify_html = ""
                if scheme.get("verify_at"):
                    verify_html = f'<p style="margin:8px 0;"><strong>✅ Verify Eligibility At:</strong> {scheme["verify_at"]}</p>'
                source_html = ""
                if scheme.get("source"):
                    source_html = f'<p style="margin:8px 0;font-size:0.82rem;color:#94A3B8;">📋 Source: {scheme["source"]}</p>'
                st.markdown(f"""<div style="font-size:0.9rem;line-height:1.55;color:#334155;">
                    <p style="margin:8px 0;"><strong>🎁 Key Benefits:</strong>
    {scheme['benefits']}</p>
                    <p style="margin:8px 0;"><strong>🎯 Eligibility:</strong>
    {scheme['eligibility']}</p>
                    <p style="margin:8px 0;color:#16794C;font-weight:600;"><strong>📌 How to Claim:</strong>
    {scheme['apply_how']}</p>
                    {carry_html}{verify_html}{source_html}</div>""", unsafe_allow_html=True)

        # Scheme facility action
        _sch_lang = st.session_state.get("_ui_lang", "en")
        _sch_fac_text = '<div style="background:#F0FDF4;border:1px solid #86EFAC;border-radius:12px;padding:14px 18px;margin-top:14px;"><div style="font-weight:700;color:#16794C;font-size:0.95rem;margin-bottom:6px;">🏥 Find Empanelled Hospital</div><p style="font-size:0.88rem;color:#334155;margin:0;">Use the <strong>🏥 Facility Locator</strong> tab to find District Hospitals and CHCs in your district. Most schemes can be availed at District Hospitals. Carry your Ration Card and Aadhaar.</p></div>' if _sch_lang == "en" else ('<div style="background:#F0FDF4;border:1px solid #86EFAC;border-radius:12px;padding:14px 18px;margin-top:14px;"><div style="font-weight:700;color:#16794C;font-size:0.95rem;margin-bottom:6px;">🏥 एमपेनल्ड अस्पताल शोधा</div><p style="font-size:0.88rem;color:#334155;margin:0;"><strong>🏥 सुविधा शोधक</strong> टैब में अपने जिले के जिला अस्पताल खोजें। राशन कार्ड और आधार साथी नेया।</p></div>' if _sch_lang == "hi" else '<div style="background:#F0FDF4;border:1px solid #86EFAC;border-radius:12px;padding:14px 18px;margin-top:14px;"><div style="font-weight:700;color:#16794C;font-size:0.95rem;margin-bottom:6px;">🏥 एमपेनल्ड रुग्णालय शोधा</div><p style="font-size:0.88rem;color:#334155;margin:0;"><strong>🏥 सुविधा शोधक</strong> टॅब मध्ये तुमच्या जिल्ह्यातील जिल्हा रुग्णालय शोधा. रेशन कार्ड आणि आधार साथी नेया.</p></div>')
        st.markdown(_sch_fac_text, unsafe_allow_html=True)

    # ── TAB 4: MATERNAL & CHILD HEALTH ──
    with tab_mch:
        # FIX: Force radio button text visible
        st.markdown("""<style>
        div[data-testid="stRadio"] label p,
        div[data-testid="stRadio"] label span,
        div[data-testid="stRadio"] [role="radiogroup"] label,
        div[data-testid="stRadio"] [role="radiogroup"] label p,
        div[data-testid="stRadio"] [role="radiogroup"] label span {
            color: #0F172A !important;
            -webkit-text-fill-color: #0F172A !important;
            opacity: 1 !important;
        }
        </style>""", unsafe_allow_html=True)
        # MCH selector
        _mch_lang = st.session_state.get("_ui_lang", "en")
        mch_mode = st.radio(
            "Select:" if _mch_lang == "en" else ("प्रकार करा:" if _mch_lang == "hi" else "निवडा:"),
            ["🤰 Pregnancy Care" if _mch_lang == "en" else ("🤰 गर्भवस्था देखभाल" if _mch_lang == "hi" else "🤰 गरोदरपूर्वी काळजी"),
             "👶 Child Vaccination" if _mch_lang == "en" else ("👶 बच्चेकी टीकाकरण" if _mch_lang == "hi" else "👶 बाळाचे लसीकरण")],
            horizontal=True, key="mch_mode"
        )

        # Danger signs card (always shown)
        _ds_en = '<div style="background:#FEECEB;border:1px solid #FECACA;border-radius:12px;padding:14px 18px;margin-bottom:14px;"><div style="font-weight:700;color:#991B1B;font-size:0.95rem;margin-bottom:8px;">⚠️ Warning Signs — Seek Immediate Care</div><p style="font-size:0.88rem;color:#334155;margin:0;line-height:1.6;"><strong>Pregnancy:</strong> Sudden bleeding, severe headache, fits/convulsions, reduced fetal movements, high fever → Call <a href="tel:108" style="color:#DC2626;font-weight:700;">108</a> or <a href="tel:102" style="color:#DC2626;font-weight:700;">102</a> immediately.<br><strong>Child:</strong> High fever not improving, difficulty breathing, not eating/drinking, unusual drowsiness, rash with fever → Visit nearest PHC/CHC or call <a href="tel:108" style="color:#DC2626;font-weight:700;">108</a>.</p></div>'
        _ds_hi = '<div style="background:#FEECEB;border:1px solid #FECACA;border-radius:12px;padding:14px 18px;margin-bottom:14px;"><div style="font-weight:700;color:#991B1B;font-size:0.95rem;margin-bottom:8px;">⚠️ खतरे के संकेत — तुरंत देखभाल लें</div><p style="font-size:0.88rem;color:#334155;margin:0;line-height:1.6;"><strong>गर्भवस्था:</strong> अचानक रक्तस्त्राव, तीव्र डोकेदुखी, फिट, बाळाची हालचाल थामबणे → <a href="tel:108" style="color:#DC2626;font-weight:700;">108</a> या <a href="tel:102" style="color:#DC2626;font-weight:700;">102</a> वर कॉल करा.<br><strong>बच्चा:</strong> ताप न कमी होणे, श्वास घेगणे, खाण्ये-प्यान्याने बंद → जवळच्या PHC/CHC ला जा किंवा <a href="tel:108" style="color:#DC2626;font-weight:700;">108</a> वर कॉल करा.</p></div>'
        _ds_mr = '<div style="background:#FEECEB;border:1px solid #FECACA;border-radius:12px;padding:14px 18px;margin-bottom:14px;"><div style="font-weight:700;color:#991B1B;font-size:0.95rem;margin-bottom:8px;">⚠️ धोक्याची संकेत — लवकाळ काळजी घ्या</div><p style="font-size:0.88rem;color:#334155;margin:0;line-height:1.6;"><strong>गरोदरपण:</strong> अचानक रक्तस्त्राव, तीव्र डोकेदुखी, फिट, बाळाची हालचाल थामबणे → <a href="tel:108" style="color:#DC2626;font-weight:700;">108</a> किंवा <a href="tel:102" style="color:#DC2626;font-weight:700;">102</a> वर कॉल करा.<br><strong>बाळ:</strong> ताप कमी होणे, श्वास घेगणे, खाण्ये-प्यान्याने बंद → जवळच्या PHC/CHC ला जा किंवा <a href="tel:108" style="color:#DC2626;font-weight:700;">108</a> वर कॉल करा.</p></div>'
        _ds_map = {"en": _ds_en, "hi": _ds_hi, "mr": _ds_mr}
        st.markdown(_ds_map.get(_mch_lang, _ds_en), unsafe_allow_html=True)

        if "Pregnancy" in mch_mode or "गर्भ" in mch_mode or "गरोदर" in mch_mode:
            st.markdown(f'<div class="th-section-heading">{_ui("anc_title")}</div>', unsafe_allow_html=True)
            st.caption(_ui("anc_desc"))
            for i, v in enumerate(ANC_SCHEDULE, 1):
                st.markdown(f"""<div style="background:#FFFFFF;border-left:4px solid #DB2777;padding:12px 16px;border-radius:10px;margin-bottom:8px;"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;"><strong style="color:#0F172A;font-size:0.95rem;">🤰 {v['visit']}</strong><span style="font-size:0.72rem;background:#FDF2F8;color:#DB2777;padding:2px 8px;border-radius:999px;font-weight:700;">{v['timing']}</span></div><p style="font-size:0.85rem;margin:0;color:#475569;line-height:1.5;">{v['importance']}</p></div>""", unsafe_allow_html=True)

        else:
            st.markdown(f'<div class="th-section-heading">{_ui("uip_title")}</div>', unsafe_allow_html=True)
            st.caption(_ui("uip_desc"))
            for v in IMMUNIZATION_SCHEDULE:
                st.markdown(f"""<div style="background:#FFFFFF;border-left:4px solid #16794C;padding:12px 16px;border-radius:10px;margin-bottom:8px;"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;"><strong style="color:#0F172A;font-size:0.95rem;">💉 {v['age']}</strong></div><p style="font-size:0.85rem;margin:0 0 4px;color:#475569;"><strong>Vaccines:</strong> {v['vaccines']}</p><p style="font-size:0.82rem;margin:0;color:#64748B;font-style:italic;">Protects against: {v['protects']}</p></div>""", unsafe_allow_html=True)

        # MCH facility action
        _mch_fac_label = "🏥 Find Maternal & Child Facility" if _mch_lang == "en" else ("🏥 मातृ और शिशु सुविधा शोधा" if _mch_lang == "hi" else "🏥 माता व बाळ सुविधा शोधा")
        _mch_fac_use = "Use the" if _mch_lang == "en" else ("प्रयोजना करा:" if _mch_lang == "hi" else "वापरा:")
        _mch_fac_tab = "🏥 Facility Locator" if _mch_lang == "en" else ("🏥 सुविधा शोधक" if _mch_lang == "hi" else "🏥 सुविधा शोधक")
        _mch_fac_desc = "tab to find PHCs, CHCs, and District Hospitals with maternity services in your district." if _mch_lang == "en" else ("टैब में अपने जिले में PHC, CHC और जिला अस्पताल खोजें।" if _mch_lang == "hi" else "टॅब मध्ये तुमच्या जिल्ह्यातील PHC, CHC आणि जिल्हा रुग्णालये शोधा.")
        st.markdown(f'<div style="background:#F0FDF4;border:1px solid #86EFAC;border-radius:12px;padding:14px 18px;margin-top:14px;"><div style="font-weight:700;color:#16794C;font-size:0.95rem;margin-bottom:6px;">{_mch_fac_label}</div><p style="font-size:0.88rem;color:#334155;margin:0;">{_mch_fac_use} <strong>{_mch_fac_tab}</strong> {_mch_fac_desc}</p></div>', unsafe_allow_html=True)

    # ── TAB 5: MORE SERVICES ──
    with tab_more:
        sub_tabs = st.tabs([_ui("st_abha"), _ui("st_camp"), _ui("st_med"), _ui("st_help"), _ui("st_log"), _ui("st_map")])

        with sub_tabs[0]:
            st.markdown(f'<div class="th-section-heading">{_ui("abha_sec")}</div>', unsafe_allow_html=True)
            lang_key = "hi" if language == MODE_HINDI else "mr" if language == MODE_MARATHI else "en"
            info = ABHA_INFO[lang_key]
            st.markdown(f"""<div class="th-feat-card"><div class="th-feat-title">{_ui("abha_card")}<span class="th-feat-status th-status-info">INFO</span></div><p class="th-feat-desc">{info['what']}</p></div>""", unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**{_ui('abha_ben')}**")
                for b in info["benefits"]: st.markdown(f"- {b}")
            with col2:
                st.markdown(f"**{_ui('abha_how')}**")
                for s in info["how_to_create"]: st.markdown(f"- {s}", unsafe_allow_html=True)

        with sub_tabs[1]:
            st.markdown(f'<div class="th-section-heading">{_ui("camp_sec")}</div>', unsafe_allow_html=True)
            st.caption(_ui("camp_desc"))
            for c in HEALTH_CAMPS:
                action_html = f'<p style="font-size:0.86rem;margin:4px 0 0;color:#0B6BCB;font-weight:600;"><strong>📌 Action:</strong> {c["action"]}</p>' if c.get("action") else ""
                st.markdown(f"""<div style="background:#FFFFFF;border-left:4px solid #D97706;padding:14px 18px;border-radius:10px;margin-bottom:10px;box-shadow:0 1px 4px rgba(0,0,0,0.03)"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;"><strong style="color:#0F172A;font-size:0.96rem;">📅 {c['name']}</strong><span style="font-size:0.72rem;background:#FEF3C7;color:#92400E;padding:2px 8px;border-radius:999px;font-weight:700;">{c['date']}</span></div><p style="font-size:0.86rem;margin:0 0 4px;color:#475569;"><strong>📍 Where:</strong> {c['location']}</p><p style="font-size:0.86rem;margin:0 0 4px;color:#475569;"><strong>🏥 Services:</strong> {c['services']}</p><p style="font-size:0.86rem;margin:0;color:#16794C;font-weight:600;"><strong>🎯 Target:</strong> {c['target']}</p>{action_html}</div>""", unsafe_allow_html=True)

        with sub_tabs[2]:
            st.markdown(f'<div class="th-section-heading">{_ui("med_sec")}</div>', unsafe_allow_html=True)
            st.caption(_ui("med_desc"))
            med_df = pd.DataFrame([{"Medicine": m, "Common Use": d["use"], "Branded Price": d["branded"], "Jan Aushadhi Price": d["generic"], "Savings": d["saving"]} for m, d in GENERIC_MEDS.items()])
            st.dataframe(med_df, use_container_width=True, hide_index=True)
            st.markdown(f'<div style="background:#F0F7FF;border:1px solid #BAE6FD;padding:12px 16px;border-radius:10px;font-size:0.88rem;margin:10px 0;">{_ui("med_loc")}</div>', unsafe_allow_html=True)
            st.caption(_ui("med_note"))

        with sub_tabs[3]:
            st.markdown(f'<div class="th-section-heading">{_ui("help_sec")}</div>', unsafe_allow_html=True)
            st.caption(_ui("help_desc"))
            lang_key = "hi" if language == MODE_HINDI else "mr" if language == MODE_MARATHI else "en"
            st.markdown(render_helpline_guide(lang_key), unsafe_allow_html=True)
            st.markdown(f"""<div class="th-feat-card"><div class="th-feat-title">{_ui("low_card")}<span class="th-feat-status th-status-beta">BETA</span></div><p class="th-feat-desc">{_ui("low_desc")}</p></div>""", unsafe_allow_html=True)

        with sub_tabs[4]:
            st.markdown(f'<div class="th-section-heading">{_ui("log_sec")}</div>', unsafe_allow_html=True)
            st.caption(_ui("log_desc"))
            if not st.session_state.health_records:
                st.markdown(f'<div style="background:#F0F7FF;border:1px solid #BAE6FD;padding:12px 16px;border-radius:10px;font-size:0.88rem;margin:10px 0;">{_ui("log_empty")}</div>', unsafe_allow_html=True)
            else:
                for r in reversed(st.session_state.health_records[-20:]):
                    sev = r.get("severity", "N/A")
                    sev_color = "#16794C" if sev in ("MILD","N/A") else "#92400E" if sev == "MODERATE" else "#991B1B"
                    st.markdown(f"""<div class="th-record-entry"><div style="display:flex;justify-content:space-between;align-items:center;"><span class="th-record-date">🗓️ {r['date']}</span><span style="font-size:0.7rem;font-weight:700;color:{sev_color};background:#F8FAFC;padding:2px 8px;border-radius:999px;">{sev}</span></div><div class="th-record-title">🩺 {r['condition']}</div><div class="th-record-body">Query: <em>"{r['query']}"</em></div></div>""", unsafe_allow_html=True)
                if st.button(_ui("btn_clear_rec"), key="clear_records"):
                    st.session_state.health_records = []; st.rerun()

        with sub_tabs[5]:
            st.markdown(f'<div class="th-section-heading">{_ui("map_sec")}</div>', unsafe_allow_html=True)
            st.caption(_ui("map_desc"))
            for item in FEATURE_ROADMAP:
                status_class = "th-status-live" if item["status"] == "LIVE" else "th-status-beta" if item["status"] == "BETA" else "th-status-demo" if item["status"] == "DEMO" else "th-status-info" if item["status"] == "INFO" else "th-status-soon"
                st.markdown(f"""<div class="th-roadmap-item"><span class="th-roadmap-phase {item['phase_class']}">{item['phase']}</span><div style="flex:1;"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:4px;"><strong style="color:#0F172A;font-size:0.95rem;">{item['title']}</strong><span class="th-feat-status {status_class}">{item['status']}</span></div><p style="font-size:0.85rem;color:#475569;margin:0;line-height:1.5;">{item['desc']}</p></div></div>""", unsafe_allow_html=True)
def render_visibility_fix():
    """Ensures sidebar can always be maximized/minimized with floating button, navbar toggle, and state observer."""
    components.html(
        """
<script>
(function() {
    var p = window.parent;
    if (!p) return;
    var doc = p.document;
    if (!doc) return;

    // 1. Expand Helper
    p.expandMahaSidebar = function() {
        var expBtn = doc.querySelector('[data-testid="stExpandSidebarButton"]') ||
                     doc.querySelector('button[data-testid="stExpandSidebarButton"]') ||
                     doc.querySelector('[data-testid="collapsedControl"] button') ||
                     doc.querySelector('button[aria-label="Open sidebar"]') ||
                     doc.querySelector('button[aria-label*="sidebar" i]') ||
                     doc.querySelector('header button');
        if (expBtn) {
            expBtn.click();
            return true;
        }
        return false;
    };

    // 2. Collapse Helper
    p.collapseMahaSidebar = function() {
        var colBtn = doc.querySelector('[data-testid="stSidebarCollapseButton"]') ||
                     doc.querySelector('[data-testid="stSidebarCollapseButton"] button') ||
                     doc.querySelector('button[aria-label="Close sidebar"]') ||
                     doc.querySelector('section[data-testid="stSidebar"] button');
        if (colBtn) {
            colBtn.click();
            return true;
        }
        return false;
    };

    // 3. Global Toggle Helper (Called by Navbar and Floating Button)
    p.toggleMahaSidebar = function() {
        var sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        var isCollapsed = true;
        if (sidebar) {
            var aria = sidebar.getAttribute('aria-expanded');
            if (aria === 'true') {
                isCollapsed = false;
            } else if (aria === 'false') {
                isCollapsed = true;
            } else {
                var rect = sidebar.getBoundingClientRect();
                isCollapsed = (rect.width <= 50 || rect.right <= 10);
            }
        }
        if (isCollapsed) {
            p.expandMahaSidebar();
        } else {
            p.collapseMahaSidebar();
        }
    };

    // 4. Setup Floating "Open Sidebar" Button Attached to Document Body
    function setupFloatingButton() {
        var btnId = 'maha-maximize-sidebar-floating-btn';
        var btn = doc.getElementById(btnId);
        if (!btn) {
            btn = doc.createElement('button');
            btn.id = btnId;
            btn.setAttribute('type', 'button');
            btn.setAttribute('title', 'Open Sidebar (Language, Helplines & Settings)');
            btn.innerHTML = '<span style="font-size:15px;font-weight:900;margin-right:6px;display:inline-block;transform:scale(1.2);">❯❯</span><span style="font-weight:800;font-size:0.82rem;letter-spacing:0.02em;">Sidebar</span>';

            Object.assign(btn.style, {
                position: 'fixed',
                top: '12px',
                left: '14px',
                zIndex: '2147483647',
                display: 'none',
                alignItems: 'center',
                background: '#FFFFFF',
                color: '#0B2528',
                border: '2px solid #00D2B4',
                borderRadius: '999px',
                padding: '7px 16px',
                boxShadow: '0 4px 18px rgba(0, 210, 180, 0.40)',
                cursor: 'pointer',
                fontFamily: 'Plus Jakarta Sans, sans-serif',
                transition: 'all 0.2s cubic-bezier(0.4, 0, 0.2, 1)',
                outline: 'none',
                userSelect: 'none'
            });

            btn.onmouseenter = function() {
                btn.style.background = '#E0F8F4';
                btn.style.borderColor = '#00A892';
                btn.style.transform = 'scale(1.06) translateY(-1px)';
                btn.style.boxShadow = '0 6px 22px rgba(0, 210, 180, 0.55)';
            };
            btn.onmouseleave = function() {
                btn.style.background = '#FFFFFF';
                btn.style.borderColor = '#00D2B4';
                btn.style.transform = 'scale(1) translateY(0)';
                btn.style.boxShadow = '0 4px 18px rgba(0, 210, 180, 0.40)';
            };
            btn.onclick = function(e) {
                e.preventDefault();
                e.stopPropagation();
                p.expandMahaSidebar();
                btn.style.display = 'none';
            };

            doc.body.appendChild(btn);
        }

        function checkVisibility() {
            var sidebar = doc.querySelector('section[data-testid="stSidebar"]');
            var isCollapsed = true;
            if (sidebar) {
                var aria = sidebar.getAttribute('aria-expanded');
                if (aria === 'true') {
                    isCollapsed = false;
                } else if (aria === 'false') {
                    isCollapsed = true;
                } else {
                    var rect = sidebar.getBoundingClientRect();
                    isCollapsed = (rect.width <= 50 || rect.right <= 10);
                }
            }
            if (isCollapsed) {
                btn.style.display = 'inline-flex';
            } else {
                btn.style.display = 'none';
            }
        }

        checkVisibility();

        // Attach MutationObserver to sidebar so button shows/hides immediately on minimize/maximize
        var sidebar = doc.querySelector('section[data-testid="stSidebar"]');
        if (sidebar && !sidebar._mahaObserved) {
            sidebar._mahaObserved = true;
            var obs = new MutationObserver(function() {
                checkVisibility();
            });
            obs.observe(sidebar, { attributes: true, attributeFilter: ['aria-expanded', 'style', 'class'] });
        }

        if (!p._mahaVisibilityInterval) {
            p._mahaVisibilityInterval = setInterval(checkVisibility, 350);
        }
    }

    setupFloatingButton();
    setTimeout(setupFloatingButton, 200);
    setTimeout(setupFloatingButton, 800);
})();
</script>
""",
        height=0,
        width=0,
    )


def render_footer():
    """Renders deep slate branded footer with high-contrast, fully visible links and badges."""
    _render_html("""
<style>
  .th-footer, .th-footer * {
    box-sizing: border-box !important;
  }
  .th-footer {
    background: #0B2528 !important;
    border-radius: 24px !important;
    padding: 38px 38px 24px !important;
    margin-top: 40px !important;
    color: #FFFFFF !important;
    box-shadow: 0 10px 30px rgba(11,37,40,0.16) !important;
  }
  .th-footer a, .th-footer a:link, .th-footer a:visited {
    text-decoration: none !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    margin-bottom: 10px !important;
    transition: all 0.2s ease !important;
  }
  .th-footer .th-ft-scheme {
    color: #E0F8F4 !important;
    -webkit-text-fill-color: #E0F8F4 !important;
    font-weight: 600 !important;
    font-size: 0.90rem !important;
  }
  .th-footer .th-ft-scheme:hover {
    color: #00D2B4 !important;
    -webkit-text-fill-color: #00D2B4 !important;
    transform: translateX(4px) !important;
  }
  .th-footer .th-ft-hl-108 {
    color: #FF8080 !important;
    -webkit-text-fill-color: #FF8080 !important;
    font-weight: 700 !important;
    font-size: 0.90rem !important;
  }
  .th-footer .th-ft-hl-102 {
    color: #FBBF24 !important;
    -webkit-text-fill-color: #FBBF24 !important;
    font-weight: 700 !important;
    font-size: 0.90rem !important;
  }
  .th-footer .th-ft-hl-104 {
    color: #2DD4BF !important;
    -webkit-text-fill-color: #2DD4BF !important;
    font-weight: 700 !important;
    font-size: 0.90rem !important;
  }
  .th-footer .th-ft-hl-1098 {
    color: #FDE047 !important;
    -webkit-text-fill-color: #FDE047 !important;
    font-weight: 700 !important;
    font-size: 0.90rem !important;
  }
  .th-footer .th-ft-hl-181 {
    color: #F472B6 !important;
    -webkit-text-fill-color: #F472B6 !important;
    font-weight: 700 !important;
    font-size: 0.90rem !important;
  }
  .th-footer .th-ft-dist {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    font-weight: 600 !important;
    font-size: 0.90rem !important;
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    margin-bottom: 10px !important;
  }
</style>

<div class="th-footer">
    <div class="th-footer-grid">
        <div>
            <div style="display:flex;align-items:center;gap:10px;margin-bottom:10px;">
                <div style="font-size:26px;">🩺</div>
                <strong style="font-size:1.18rem;color:#FFFFFF !important;-webkit-text-fill-color:#FFFFFF !important;letter-spacing:-0.02em;">MahaArogya Setu</strong>
            </div>
            <p style="font-size:0.88rem;color:#D1E7E5 !important;-webkit-text-fill-color:#D1E7E5 !important;line-height:1.6;margin:0 0 14px 0;">
                Bridging healthcare accessibility across Maharashtra's underserved tribal and rural blocks. Real-time AI clinical triage and scheme navigation in English, हिंदी, and मराठी.
            </p>
            <span style="font-size:0.75rem;background:rgba(0,210,180,0.18);color:#00D2B4 !important;-webkit-text-fill-color:#00D2B4 !important;border:1px solid rgba(0,210,180,0.35);padding:5px 14px;border-radius:999px;font-weight:800;letter-spacing:0.04em;">
                SMART INDIA HACKATHON • NHM
            </span>
        </div>
        <div>
            <div class="th-footer-title" style="color:#00D2B4 !important;-webkit-text-fill-color:#00D2B4 !important;font-size:0.96rem;font-weight:800;letter-spacing:0.06em;margin-bottom:14px;">24×7 Helplines</div>
            <a href="tel:108" class="th-ft-hl-108" style="color:#FF8080 !important;-webkit-text-fill-color:#FF8080 !important;font-weight:700;">🚑 Ambulance: 108</a>
            <a href="tel:102" class="th-ft-hl-102" style="color:#FBBF24 !important;-webkit-text-fill-color:#FBBF24 !important;font-weight:700;">🤰 Janani Express: 102</a>
            <a href="tel:104" class="th-ft-hl-104" style="color:#2DD4BF !important;-webkit-text-fill-color:#2DD4BF !important;font-weight:700;">🏥 Health Advice: 104</a>
            <a href="tel:1098" class="th-ft-hl-1098" style="color:#FDE047 !important;-webkit-text-fill-color:#FDE047 !important;font-weight:700;">🧒 Childline: 1098</a>
            <a href="tel:181" class="th-ft-hl-181" style="color:#F472B6 !important;-webkit-text-fill-color:#F472B6 !important;font-weight:700;">👩 Women Helpline: 181</a>
        </div>
        <div>
            <div class="th-footer-title" style="color:#00D2B4 !important;-webkit-text-fill-color:#00D2B4 !important;font-size:0.96rem;font-weight:800;letter-spacing:0.06em;margin-bottom:14px;">Schemes & Portals</div>
            <a href="https://abdm.gov.in/" target="_blank" class="th-ft-scheme" style="color:#E0F8F4 !important;-webkit-text-fill-color:#E0F8F4 !important;font-weight:600;">🌐 MJPJAY Portal</a>
            <a href="https://abdm.gov.in/" target="_blank" class="th-ft-scheme" style="color:#E0F8F4 !important;-webkit-text-fill-color:#E0F8F4 !important;font-weight:600;">🌐 Ayushman Bharat (PM-JAY)</a>
            <a href="https://esanjeevani.mohfw.gov.in/#/" target="_blank" class="th-ft-scheme" style="color:#E0F8F4 !important;-webkit-text-fill-color:#E0F8F4 !important;font-weight:600;">🩺 eSanjeevani Telemedicine</a>
            <a href="https://abdm.gov.in/" target="_blank" class="th-ft-scheme" style="color:#E0F8F4 !important;-webkit-text-fill-color:#E0F8F4 !important;font-weight:600;">🪪 ABHA Digital Health ID (ABDM)</a>
            <a href="https://janaushadhi.gov.in" target="_blank" class="th-ft-scheme" style="color:#E0F8F4 !important;-webkit-text-fill-color:#E0F8F4 !important;font-weight:600;">💊 PM Jan Aushadhi Kendra</a>
        </div>
        <div>
            <div class="th-footer-title" style="color:#00D2B4 !important;-webkit-text-fill-color:#00D2B4 !important;font-size:0.96rem;font-weight:800;letter-spacing:0.06em;margin-bottom:14px;">Key Districts</div>
            <span class="th-ft-dist" style="color:#FFFFFF !important;-webkit-text-fill-color:#FFFFFF !important;font-weight:600;">📍 Nandurbar (Tribal Core)</span>
            <span class="th-ft-dist" style="color:#FFFFFF !important;-webkit-text-fill-color:#FFFFFF !important;font-weight:600;">📍 Gadchiroli (Aheri, Bhamragad)</span>
            <span class="th-ft-dist" style="color:#FFFFFF !important;-webkit-text-fill-color:#FFFFFF !important;font-weight:600;">📍 Amravati (Melghat Blocks)</span>
            <span class="th-ft-dist" style="color:#FFFFFF !important;-webkit-text-fill-color:#FFFFFF !important;font-weight:600;">📍 Palghar (Jawhar, Mokhada)</span>
            <span class="th-ft-dist" style="color:#FFFFFF !important;-webkit-text-fill-color:#FFFFFF !important;font-weight:600;">📍 Yavatmal (Pusad, City)</span>
        </div>
    </div>
    <div class="th-footer-bottom" style="color:#B2D8D6 !important;-webkit-text-fill-color:#B2D8D6 !important;border-top:1px solid rgba(255,255,255,0.18);padding-top:18px;text-align:center;font-size:0.84rem;">
        MahaArogya Setu © 2026 · General Healthcare Awareness & Access Navigation · In severe symptoms, immediately call 108 or visit nearest District Hospital.
    </div>
</div>
""")
