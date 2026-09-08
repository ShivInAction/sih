"""Main views, sidebars, tabs, and page headers."""
import streamlit as st
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




def render_sidebar():
    with st.sidebar:
        st.markdown("""<div class="th-sb-brand-box"><div class="th-sb-brand-icon">🩺</div><div><div style="font-weight:800;font-size:1.05rem;color:#0F172A;">MahaArogya Setu</div><div style="font-size:0.72rem;color:#64748B;font-weight:600;">Rural Healthcare Access · SIH</div></div></div><div class="th-sb-divider"></div>""", unsafe_allow_html=True)

        st.markdown(f'<div class="th-sb-title">{_ui("sb_conn")}</div>', unsafe_allow_html=True)
        low_bandwidth = st.toggle("⚡ " + _ui("sb_low"), value=False, key="low_bandwidth", help=_ui("sb_low_help"))
        if low_bandwidth:
            st.markdown('<div style="background:#FEF3C7;border:1px solid #F59E0B;border-radius:8px;padding:8px 12px;font-size:0.82rem;color:#92400E;font-weight:600;margin-top:4px;">⚡ Low-Bandwidth Mode ON ✓ — Keyword matching active. Internet still required.</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div style="background:#F0FDF4;border:1px solid #86EFAC;border-radius:8px;padding:8px 12px;font-size:0.82rem;color:#16794C;font-weight:600;margin-top:4px;">🟢 Full Mode — AI semantic matching + translation active.</div>', unsafe_allow_html=True)

        st.markdown(f'<div class="th-sb-title">{_ui("sb_lang")}</div>', unsafe_allow_html=True)
        language = st.radio("Choose language", LANGUAGES, index=0, label_visibility="collapsed")
        if language.startswith("🌐"):
            st.markdown(f'<p style="font-size:0.82rem;color:#475569;margin-top:4px;">{_ui("sb_auto")}</p>', unsafe_allow_html=True)
            st.markdown("""<script>
            setTimeout(function(){
                var sb = document.querySelector('[data-testid="stSidebar"]');
                if(!sb) return;
                sb.querySelectorAll('p, span, small, label').forEach(function(el){
                    var cs = window.getComputedStyle(el);
                    if(cs.color === 'rgb(255, 255, 255)' || cs.color === 'rgba(0, 0, 0, 0)' || parseFloat(cs.opacity) < 0.5){
                        el.style.color = '#475569';
                        el.style.webkitTextFillColor = '#475569';
                        el.style.opacity = '1';
                    }
                });
            }, 500);
            </script>""", unsafe_allow_html=True)
        st.session_state["_ui_lang"] = "hi" if language == MODE_HINDI else "mr" if language == MODE_MARATHI else "en"

        st.markdown("""<div class="th-sb-divider"></div><div class="th-sb-title">""" + _ui("sb_emerg") + """</div>
            <a href="tel:108" class="th-help-card critical"><span class="th-help-label">🚑 Ambulance (MEMS)</span><span class="th-help-num">108</span></a>
            <a href="tel:102" class="th-help-card critical"><span class="th-help-label">🤰 Janani Express</span><span class="th-help-num">102</span></a>
            <a href="tel:104" class="th-help-card"><span class="th-help-label">🏥 MH Health Line</span><span class="th-help-num">104</span></a>
            <a href="tel:1098" class="th-help-card"><span class="th-help-label">🧒 Child Helpline</span><span class="th-help-num">1098</span></a>
            <a href="tel:181" class="th-help-card"><span class="th-help-label">👩 Women Helpline</span><span class="th-help-num">181</span></a>
            <div class="th-sb-divider"></div><div style="font-size:0.74rem;color:#64748B;">""" + _ui("sb_disc") + """</div>""", unsafe_allow_html=True)

    return language, low_bandwidth


def render_hero():
    st.markdown(f"""<div class="th-hero-container">
        <div class="th-hero-avatar-box">🩺<div class="th-online-dot"></div></div>
        <div style="flex:1;">
            <span class="th-hero-badge">{_ui("hero_badge")}</span>
            <h1 class="th-hero-title">{_ui("hero_title")}</h1>
            <p class="th-hero-sub">{_ui("hero_sub")}</p>
            <div>
                <span class="th-tag-pill th-tag-blue">{_ui("tag_facility")}</span>
                <span class="th-tag-pill th-tag-teal">{_ui("tag_schemes")}</span>
                <span class="th-tag-pill th-tag-purple">{_ui("tag_mch")}</span>
                <span class="th-tag-pill th-tag-green">{_ui("tag_tele")}</span>
                <span class="th-tag-pill th-tag-pink">{_ui("tag_med")}</span>
                <span class="th-tag-pill th-tag-amber">{_ui("tag_low")}</span>
            </div>
        </div>
    </div>""", unsafe_allow_html=True)


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
            st.markdown(f"""<div class="th-welcome-box"><div class="th-welcome-icon">💬</div><h2 style="font-size:1.4rem;font-weight:800;margin:0 0 8px 0;color:#0F172A;">{_ui("welcome_title")}</h2><p style="color:#64748B;font-size:0.95rem;margin:0 auto;max-width:680px;line-height:1.5;">{welcome_sub}</p></div>""", unsafe_allow_html=True)

            st.markdown(f'<div class="th-section-heading">{_ui("sec_quick")}</div>', unsafe_allow_html=True)
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
    """Injects JavaScript to force any low-contrast or hidden dynamic text in sidebar and radio buttons to remain visible."""
    import streamlit.components.v1 as components
    components.html("""<script>
    function fixVisibility() {
        var sb = parent.document.querySelector('[data-testid="stSidebar"]');
        if(sb) {
            sb.querySelectorAll('p, span, small, label, div').forEach(function(el){
                var cs = parent.window.getComputedStyle(el);
                if(cs.color === 'rgb(255, 255, 255)' || cs.color === 'rgba(0, 0, 0, 0)' || parseFloat(cs.opacity) < 0.3){
                    el.style.setProperty('color', '#475569', 'important');
                    el.style.setProperty('-webkit-text-fill-color', '#475569', 'important');
                    el.style.setProperty('opacity', '1', 'important');
                }
            });
        }
        parent.document.querySelectorAll('[data-testid="stRadio"] label p, [data-testid="stRadio"] label span').forEach(function(el){
            el.style.setProperty('color', '#0F172A', 'important');
            el.style.setProperty('-webkit-text-fill-color', '#0F172A', 'important');
            el.style.setProperty('opacity', '1', 'important');
        });
    }
    fixVisibility();
    var fixInterval = setInterval(fixVisibility, 300);
    setTimeout(function(){ clearInterval(fixInterval); }, 5000);
    try {
        var observer = new MutationObserver(function(){ setTimeout(fixVisibility, 100); });
        observer.observe(parent.document.body, { childList: true, subtree: true });
    } catch(e) {}
    </script>""", height=0)
