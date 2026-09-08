"""Design system, CSS styling, and Streamlit page config."""
import streamlit as st

CUSTOM_CSS = """
<style>
  :root {
    color-scheme: light !important;
    --primary-blue: #0B6BCB;
    --primary-dark: #084F98;
    --primary-light: #EAF2FE;
    --accent-teal: #0E9F8F;
    --accent-green: #16794C;
    --accent-amber: #D97706;
    --accent-red: #DC2626;
    --accent-purple: #6941C6;
    --accent-pink: #DB2777;
    --bg-main: #F4F7FB;
    --card-bg: #FFFFFF;
    --text-main: #0F172A;
    --text-muted: #475569;
    --border-subtle: #E2E8F0;
  }
  .stApp, [data-testid="stAppViewContainer"], .main, .main .block-container {
    background-color: var(--bg-main) !important; color: var(--text-main) !important;
  }
  #MainMenu, footer, [data-testid="stDecoration"] { display: none !important; }
  .block-container { max-width: 1240px !important; padding-top: 0.8rem !important; padding-bottom: 6.8rem !important; }
  [data-testid="stStatusWidget"], .stStatusWidget { display: none !important; }
  
  /* Chat Input */
  [data-testid="stBottom"] {
    background: linear-gradient(180deg, rgba(244,247,251,0) 0%, rgba(244,247,251,0.96) 24%, #F4F7FB 100%) !important;
    backdrop-filter: blur(10px) !important; padding: 16px 0 12px !important; z-index: 100 !important;
  }
  div[data-testid="stChatInput"] > div, div[data-testid="stChatInput"] form {
    background-color: #FFFFFF !important; border: 1.5px solid #CBD5E1 !important;
    border-radius: 18px !important; box-shadow: 0 4px 18px rgba(15,23,42,0.06) !important;
  }
  div[data-testid="stChatInput"] > div:focus-within {
    border-color: #0B6BCB !important; box-shadow: 0 0 0 3.5px rgba(11,107,203,0.16) !important;
  }
  div[data-testid="stChatInput"] textarea {
    background-color: #FFFFFF !important; color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important; font-size: 0.98rem !important;
    font-weight: 500 !important; caret-color: #0B6BCB !important;
  }
  div[data-testid="stChatInput"] textarea::placeholder { color: #64748B !important; }
  div[data-testid="stChatInputSubmitButton"] {
    background-color: #0B6BCB !important; border-radius: 12px !important; margin: 4px !important;
  }
  div[data-testid="stChatInputSubmitButton"]:hover { background-color: #084F98 !important; }
  div[data-testid="stChatInputSubmitButton"] svg { fill: #FFFFFF !important; }

  /* Sidebar Controls */
  [data-testid="stHeader"] { background: transparent !important; z-index: 99 !important; }
  [data-testid="stSidebarCollapseButton"], [data-testid="stExpandSidebarButton"],
  [data-testid="collapsedControl"], [data-testid="stHeader"] button {
    display: flex !important; visibility: visible !important; opacity: 1 !important;
    background-color: #0F172A !important; color: #FFFFFF !important;
    border: 1px solid #334155 !important; border-radius: 10px !important;
  }
  [data-testid="stSidebarCollapseButton"] svg, [data-testid="stExpandSidebarButton"] svg,
  [data-testid="collapsedControl"] svg, [data-testid="stHeader"] button svg {
    fill: #FFFFFF !important; color: #FFFFFF !important;
  }
  [data-testid="stSidebarCollapseButton"]:hover, [data-testid="stExpandSidebarButton"]:hover,
  [data-testid="collapsedControl"]:hover, [data-testid="stHeader"] button:hover {
    background-color: #1E293B !important; border-color: #475569 !important;
  }

  /* Hero Header */
  .th-hero-container {
    background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
    border: 1.5px solid #E2E8F0; border-radius: 20px; padding: 22px 26px;
    margin-bottom: 16px; box-shadow: 0 4px 16px rgba(15,23,42,0.04);
    display: flex; align-items: center; gap: 22px; position: relative; overflow: hidden;
  }
  .th-hero-container::before {
    content: ""; position: absolute; top: 0; left: 0; width: 6px; height: 100%;
    background: linear-gradient(180deg, #0B6BCB 0%, #0E9F8F 50%, #6941C6 100%);
  }
  .th-hero-avatar-box {
    width: 68px; height: 68px; flex: 0 0 68px; border-radius: 18px;
    background: linear-gradient(135deg, #EAF2FE 0%, #F3EFFE 100%);
    display: flex; align-items: center; justify-content: center; font-size: 34px;
    border: 1.5px solid #D6E4F9; box-shadow: 0 4px 12px rgba(11,107,203,0.12); position: relative;
  }
  .th-online-dot {
    position: absolute; right: -3px; bottom: -3px; width: 14px; height: 14px;
    border-radius: 50%; background: #22C55E; border: 2.5px solid #FFFFFF;
  }
  .th-hero-badge {
    display: inline-flex; align-items: center; gap: 6px; font-size: 0.7rem;
    font-weight: 700; color: #0B6BCB; letter-spacing: 0.08em; text-transform: uppercase;
    background: #EAF2FE; border: 1px solid #D6E4F9; padding: 4px 11px;
    border-radius: 999px; margin-bottom: 6px;
  }
  .th-hero-title {
    font-size: 1.6rem !important; font-weight: 800 !important; margin: 0 0 4px 0 !important;
    color: #0F172A !important; letter-spacing: -0.02em; line-height: 1.25;
  }
  .th-hero-sub { color: #475569 !important; font-size: 0.94rem; margin: 0; line-height: 1.5; }
  .th-tag-pill {
    display: inline-flex; align-items: center; gap: 5px; font-size: 0.74rem;
    font-weight: 600; padding: 4px 11px; border-radius: 999px; margin-right: 6px; margin-top: 8px;
  }
  .th-tag-blue { background: #EAF2FE; color: #0B6BCB; border: 1px solid #D6E4F9; }
  .th-tag-teal { background: #E6F7F5; color: #0E9F8F; border: 1px solid #C8ECE7; }
  .th-tag-green { background: #EAF8EF; color: #16794C; border: 1px solid #C9EED7; }
  .th-tag-purple { background: #F3EFFE; color: #6941C6; border: 1px solid #E4DBFD; }
  .th-tag-pink { background: #FDF2F8; color: #DB2777; border: 1px solid #FBCFE8; }
  .th-tag-amber { background: #FEF3C7; color: #D97706; border: 1px solid #FDE68A; }

  /* Welcome & Sections */
  .th-welcome-box {
    background: linear-gradient(135deg, #FFFFFF 0%, #F8FAFC 100%);
    border: 1.5px solid #E2E8F0; border-radius: 18px; padding: 24px 20px;
    text-align: center; margin-bottom: 14px; box-shadow: 0 2px 10px rgba(15,23,42,0.03);
  }
  .th-welcome-icon {
    width: 52px; height: 52px; border-radius: 16px; background: #EAF2FE;
    border: 1px solid #D6E4F9; display: flex; align-items: center;
    justify-content: center; font-size: 26px; margin: 0 auto 10px;
  }
  .th-section-heading {
    font-size: 0.78rem; font-weight: 800; color: #64748B;
    letter-spacing: 0.08em; text-transform: uppercase; margin: 14px 2px 8px;
    display: flex; align-items: center; gap: 8px;
  }
  .th-section-heading::after {
    content: ""; flex: 1; height: 1px;
    background: linear-gradient(90deg, #E2E8F0 0%, transparent 100%);
  }

  /* Buttons */
  div[data-testid="stButton"] > button {
    background-color: #FFFFFF !important; color: #0F172A !important;
    border: 1.5px solid #E2E8F0 !important; border-radius: 14px !important;
    padding: 12px 16px !important; font-weight: 600 !important; font-size: 0.92rem !important;
    transition: all 0.2s ease !important; display: flex !important; align-items: center !important;
    justify-content: flex-start !important; text-align: left !important;
    width: 100% !important; min-height: 54px !important;
  }
  div[data-testid="stButton"] > button:hover {
    background-color: #F8FAFC !important; border-color: #0B6BCB !important;
    color: #0B6BCB !important; transform: translateY(-2px) !important;
    box-shadow: 0 6px 16px rgba(11,107,203,0.12) !important;
  }
  div[data-testid="stButton"] > button p { color: inherit !important; font-weight: 600 !important; }
  .th-clear-btn div[data-testid="stButton"] > button {
    min-height: 36px !important; padding: 6px 14px !important; border-radius: 10px !important;
    font-size: 0.84rem !important; background: #F8FAFC !important; color: #64748B !important;
    justify-content: center !important;
  }
  .th-clear-btn div[data-testid="stButton"] > button:hover {
    background: #FEECEB !important; border-color: #F8D5D1 !important; color: #B42318 !important;
  }

  /* Chat Bubbles */
  [data-testid="stChatMessage"] { background: transparent !important; padding: 5px 0 !important; border: none !important; }
  [data-testid="stChatMessage"] [data-testid="stChatMessageContent"] {
    background: #FFFFFF !important; border: 1.5px solid #E2E8F0 !important;
    border-radius: 16px !important; padding: 16px 20px !important;
    box-shadow: 0 2px 8px rgba(15,23,42,0.04) !important; color: #0F172A !important;
    max-width: 920px; line-height: 1.6 !important;
  }
  [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) { flex-direction: row-reverse !important; }
  [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stChatMessageContent"] {
    background: #EAF2FE !important; border-color: #D6E4F9 !important; border-radius: 16px 16px 4px 16px !important;
  }
  [data-testid="stChatMessageAvatar"] { background: #FFFFFF !important; border: 1.5px solid #E2E8F0 !important; border-radius: 12px !important; }

  /* Sidebar */
  [data-testid="stSidebar"] { background-color: #FFFFFF !important; border-right: 1px solid #E2E8F0 !important; }
  .th-sb-brand-box { display: flex; align-items: center; gap: 12px; padding: 4px 0; margin-bottom: 8px; }
  .th-sb-brand-icon {
    width: 42px; height: 42px; border-radius: 12px;
    background: linear-gradient(135deg, #EAF2FE 0%, #F3EFFE 100%);
    border: 1px solid #D6E4F9; display: flex; align-items: center;
    justify-content: center; font-size: 22px;
  }
  .th-sb-divider { height: 1px; background: #E2E8F0; margin: 14px 0; }
  .th-sb-title { font-size: 0.72rem; font-weight: 800; color: #64748B; letter-spacing: 0.08em; text-transform: uppercase; margin-bottom: 8px; }
  [data-testid="stSidebar"] [role="radiogroup"] > label {
    background: #FFFFFF !important; border: 1px solid #E2E8F0 !important;
    border-radius: 12px !important; padding: 10px 14px !important; margin-bottom: 6px !important;
  }
  [data-testid="stSidebar"] [role="radiogroup"] > label:hover { background: #F8FAFC !important; border-color: #0B6BCB !important; }
  [data-testid="stSidebar"] [role="radiogroup"] > label p { color: #0F172A !important; font-weight: 600 !important; font-size: 0.92rem !important; }
  [data-testid="stSidebar"] [role="radiogroup"] > label[data-checked="true"] { background: #EAF2FE !important; border-color: #0B6BCB !important; }

  .th-help-card {
    display: flex; align-items: center; justify-content: space-between;
    padding: 10px 14px; background: #FAFBFD; border: 1.5px solid #E2E8F0;
    border-radius: 12px; margin-bottom: 8px; text-decoration: none !important;
    transition: all 0.2s ease;
  }
  .th-help-card:hover { transform: translateX(3px); border-color: #0B6BCB; background: #FFFFFF; }
  .th-help-label { font-size: 0.86rem; font-weight: 600; color: #1E293B; }
  .th-help-num { font-size: 0.95rem; font-weight: 800; color: #0B6BCB; background: #EAF2FE; padding: 3px 9px; border-radius: 8px; border: 1px solid #D6E4F9; }
  .th-help-card.critical { background: #FEECEB; border-color: #F8D5D1; }
  .th-help-card.critical .th-help-num { color: #DC2626; background: #FDE8E7; border-color: #FCA5A5; }

  div[data-testid="stAudioInput"] { background-color: #FFFFFF !important; border: 1.5px dashed #CBD5E1 !important; border-radius: 14px !important; padding: 12px !important; }

  /* Disease Card */
  .th-dx-card {
    background: #FFFFFF; border: 1.5px solid #E2E8F0; border-radius: 18px;
    overflow: hidden; box-shadow: 0 4px 16px rgba(15,23,42,0.05); margin: 6px 0;
  }
  .th-dx-header {
    background: linear-gradient(135deg, #EAF2FE 0%, #F0F6FF 100%);
    padding: 16px 20px; border-bottom: 1.5px solid #D6E4F9;
    display: flex; align-items: center; justify-content: space-between; gap: 12px;
  }
  .th-dx-header-left { display: flex; align-items: center; gap: 12px; }
  .th-dx-header-icon {
    width: 42px; height: 42px; border-radius: 12px; background: #FFFFFF;
    border: 1px solid #D6E4F9; display: flex; align-items: center;
    justify-content: center; font-size: 22px;
  }
  .th-dx-title { margin: 0 !important; font-size: 1.2rem !important; font-weight: 800 !important; color: #0F172A !important; }
  .th-dx-badge {
    font-size: 0.72rem; font-weight: 700; color: #0B6BCB; background: #FFFFFF;
    border: 1px solid #D6E4F9; padding: 3px 10px; border-radius: 999px; text-transform: uppercase;
  }
  .th-dx-row { display: flex; gap: 14px; padding: 15px 20px; border-bottom: 1px solid #F1F5F9; align-items: flex-start; }
  .th-dx-icon-badge { width: 36px; height: 36px; flex: 0 0 36px; border-radius: 10px; display: flex; align-items: center; justify-content: center; font-size: 17px; }
  .th-dx-label { display: block; font-size: 0.76rem; text-transform: uppercase; letter-spacing: 0.05em; margin-bottom: 4px; font-weight: 800; }
  .th-dx-content { font-size: 0.95rem; color: #334155; line-height: 1.55; }
  .th-dx-alt-box { padding: 14px 20px; background: #FAFBFD; border-top: 1px solid #E2E8F0; font-size: 0.9rem; color: #334155; display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
  .th-dx-alt-pill { background: #FFFFFF; border: 1px solid #CBD5E1; padding: 3px 10px; border-radius: 999px; font-size: 0.82rem; font-weight: 600; color: #0B6BCB; }
  .th-dx-footer { padding: 12px 20px; background: #FAFBFD; border-top: 1px solid #F1F5F9; font-size: 0.8rem; color: #64748B; font-style: italic; }

  /* Metadata pills on disease cards */
  .th-meta-strip { display: flex; gap: 6px; flex-wrap: wrap; padding: 10px 20px; background: #F8FAFC; border-bottom: 1px solid #F1F5F9; }
  .th-meta-pill { font-size: 0.7rem; font-weight: 700; padding: 3px 9px; border-radius: 6px; letter-spacing: 0.02em; }
  .th-meta-severity-mild { background: #EAF8EF; color: #16794C; }
  .th-meta-severity-moderate { background: #FEF3C7; color: #92400E; }
  .th-meta-severity-severe { background: #FFEDD5; color: #9A3412; }
  .th-meta-severity-critical { background: #FEE2E2; color: #991B1B; }
  .th-meta-cat { background: #EAF2FE; color: #0B6BCB; }
  .th-meta-free { background: #EAF8EF; color: #16794C; }
  .th-meta-partial { background: #FEF3C7; color: #92400E; }
  .th-meta-facility { background: #F3EFFE; color: #6941C6; }

  /* Alerts */
  .th-alert { border-radius: 16px; padding: 18px 20px; border-left: 5px solid; display: flex; gap: 16px; margin-bottom: 14px; box-shadow: 0 4px 14px rgba(15,23,42,0.04); }
  .th-alert-icon { font-size: 26px; flex: 0 0 32px; padding-top: 2px; }
  .th-alert-body { flex: 1; }
  .th-alert h4 { margin: 0 0 6px 0 !important; font-weight: 800 !important; font-size: 1.08rem !important; }
  .th-alert.emerg { background: #FFF2F2; border-left-color: #DC2626; border: 1.5px solid #FECACA; border-left-width: 6px; }
  .th-alert.emerg h4, .th-alert.emerg p, .th-alert.emerg li { color: #991B1B !important; }
  .th-emerg-actions { display: flex; gap: 10px; margin-top: 12px; flex-wrap: wrap; }
  .th-emerg-btn { display: inline-flex; align-items: center; gap: 6px; background: #DC2626; color: #FFFFFF !important; font-weight: 700; font-size: 0.88rem; padding: 8px 16px; border-radius: 10px; text-decoration: none !important; }
  .th-emerg-btn-sub { display: inline-flex; align-items: center; gap: 6px; background: #FFFFFF; color: #991B1B !important; font-weight: 700; font-size: 0.88rem; padding: 8px 16px; border-radius: 10px; border: 1px solid #FECACA; text-decoration: none !important; }
  .th-alert.caution { background: #FFFBEB; border-left-color: #D97706; border: 1.5px solid #FDE68A; border-left-width: 6px; }
  .th-alert.caution h4 { color: #92400E !important; } .th-alert.caution p { color: #B45309 !important; }
  .th-alert.info { background: #F0F7FF; border-left-color: #0B6BCB; border: 1.5px solid #BAE6FD; border-left-width: 6px; }
  .th-alert.info h4 { color: #0369A1 !important; } .th-alert.info p { color: #0C4A6E !important; }
  .th-alert.success { background: #F0FDF4; border-left-color: #16794C; border: 1.5px solid #BBF7D0; border-left-width: 6px; }
  .th-alert.success h4 { color: #14532D !important; } .th-alert.success p { color: #166534 !important; }

  /* Tabs */
  .stTabs [data-baseweb="tab-list"] {
    gap: 6px; background: #FFFFFF; padding: 6px; border-radius: 14px;
    border: 1.5px solid #E2E8F0; margin-bottom: 14px;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent; border-radius: 10px; padding: 10px 16px;
    color: #475569; font-weight: 600; font-size: 0.88rem; border: none !important;
  }
  .stTabs [data-baseweb="tab"]:hover { background: #F8FAFC; color: #0B6BCB; }
  .stTabs [aria-selected="true"] {
    background: #EAF2FE !important; color: #0B6BCB !important;
    box-shadow: 0 2px 6px rgba(11,107,203,0.08);
  }

  /* Feature cards for new modules */
  .th-feat-card {
    background: #FFFFFF; border: 1.5px solid #E2E8F0; border-radius: 14px;
    padding: 16px; margin-bottom: 10px; transition: all 0.2s ease;
  }
  .th-feat-card:hover { border-color: #0B6BCB; box-shadow: 0 4px 14px rgba(11,107,203,0.08); }
  .th-feat-title { font-size: 1rem; font-weight: 800; color: #0F172A; margin: 0 0 4px 0; display: flex; align-items: center; gap: 8px; }
  .th-feat-desc { font-size: 0.86rem; color: #475569; margin: 0 0 8px 0; line-height: 1.5; }
  .th-feat-status {
    display: inline-flex; align-items: center; gap: 4px; font-size: 0.7rem;
    font-weight: 700; padding: 2px 8px; border-radius: 999px;
  }
  .th-status-live { background: #EAF8EF; color: #16794C; border: 1px solid #C9EED7; }
  .th-status-beta { background: #FEF3C7; color: #92400E; border: 1px solid #FDE68A; }
  .th-status-soon { background: #F3EFFE; color: #6941C6; border: 1px solid #E4DBFD; }
  .th-status-demo { background: #FFF8E6; color: #92400E; border: 1px solid #FDE68A; }
  .th-status-info { background: #F0F7FF; color: #0369A1; border: 1px solid #BAE6FD; }

  /* Roadmap timeline */
  .th-roadmap-item {
    display: flex; gap: 14px; padding: 14px 16px; background: #FFFFFF;
    border: 1.5px solid #E2E8F0; border-radius: 12px; margin-bottom: 8px;
  }
  .th-roadmap-phase {
    font-size: 0.7rem; font-weight: 800; color: #FFFFFF; background: #0B6BCB;
    padding: 4px 10px; border-radius: 6px; height: fit-content; letter-spacing: 0.05em;
  }
  .th-roadmap-p1 { background: #16794C; }
  .th-roadmap-p2 { background: #D97706; }
  .th-roadmap-p3 { background: #6941C6; }

  /* Health record card */
  .th-record-entry {
    background: #FFFFFF; border-left: 4px solid #0B6BCB; padding: 12px 16px;
    border-radius: 10px; margin-bottom: 8px; box-shadow: 0 1px 4px rgba(0,0,0,0.03);
  }
  .th-record-date { font-size: 0.75rem; color: #64748B; font-weight: 600; }
  .th-record-title { font-size: 0.95rem; font-weight: 700; color: #0F172A; margin: 4px 0; }
  .th-record-body { font-size: 0.86rem; color: #475569; line-height: 1.5; }

  /* GLOBAL FIX: Force all sidebar text visible */
  [data-testid="stSidebar"] p,
  [data-testid="stSidebar"] span,
  [data-testid="stSidebar"] small,
  [data-testid="stSidebar"] label,
  [data-testid="stSidebar"] div[data-testid="stCaptionContainer"],
  [data-testid="stSidebar"] .stCaption p {
    color: #475569 !important;
    -webkit-text-fill-color: #475569 !important;
  }

  /* GLOBAL FIX: Force all radio button text visible everywhere */
  div[data-testid="stRadio"] label p,
  div[data-testid="stRadio"] label span,
  div[data-testid="stRadio"] [role="radiogroup"] label p,
  div[data-testid="stRadio"] [role="radiogroup"] label span {
    color: #0F172A !important;
    -webkit-text-fill-color: #0F172A !important;
    opacity: 1 !important;
  }
</style>
"""

def setup_page():
    st.set_page_config(
        page_title="MahaArogya Setu — Rural Healthcare Access Platform | SIH",
        page_icon="🩺",
        layout="wide",
        initial_sidebar_state="expanded",
    )
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
