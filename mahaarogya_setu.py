import re
import time
import html
from datetime import datetime, timedelta
import streamlit as st
import pandas as pd
from deep_translator import GoogleTranslator
from langdetect import detect, LangDetectException

# ============================================================================
# PAGE CONFIGURATION — REBRANDED FOR NEW PROBLEM STATEMENT
# ============================================================================
st.set_page_config(
    page_title="MahaArogya Setu — Rural Healthcare Access Platform | SIH",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================================
# DESIGN SYSTEM — PRODUCTION-GRADE CLINICAL HEALTHCARE THEME
# ============================================================================
st.markdown(
    """
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
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================================
# ENHANCED DATA LAYER — MAHARASHTRA FOCUSED WITH EXTENDED SCHEMA
# ============================================================================
REQUIRED_COLUMNS = ["disease", "symptoms", "prevention", "when_to_see_doctor", "home_care"]
ENHANCED_COLUMNS = ["severity", "age_group", "category", "rural_prevalence", "govt_free_treatment", "recommended_facility"]

STOPWORDS = {"a","an","the","and","or","in","of","with","for","to","my","me","i","i'm","im","have","has","had","is","are","was","were","am","it","this","that","some","someone","feeling","feel","got","get"}
GENERIC_SYMPTOMS = {"fever","pain","cough","fatigue","headache","weakness","rash","nausea","vomiting","cold","ache","tired","tiredness","sick"}
_STEM_EXCEPTIONS = {"aches":"ache","headaches":"headache","stomachaches":"stomachache"}
_COMPOUND_ACHE_WORDS = ("head","body","ear","stomach","tooth","back","neck","belly")

MAHARASHTRA_DISTRICTS = {
    "Nandurbar (नंदुरबार)": [
        {"name":"Civil Hospital Nandurbar","type":"District Hospital","location":"Nandurbar Town","phone":"02564-210111","beds":"200+","facilities":"ICU, Blood Bank, Pediatric Ward, MJPJAY Desk","services_list":["Emergency","Blood Bank","Pediatric","General OPD"],"is_hq":True,"source":"Reference dataset — verify before visiting","last_verified":"Reference data — verify before visiting","data_status":"reference"},
        {"name":"Sub-District Hospital Dhadgaon","type":"SDH / Tribal Core","location":"Dhadgaon Block","phone":"02564-262244","beds":"50","facilities":"Maternity Ward, Emergency Surgery, Telemedicine","services_list":["Maternity","Emergency","Telemedicine"],"source":"Reference dataset — verify before visiting","last_verified":"Reference data — verify before visiting","data_status":"reference"},
        {"name":"CHC Shahada","type":"Community Health Centre","location":"Shahada","phone":"02564-222055","beds":"30","facilities":"SOPD, Basic X-Ray, Laboratory, Delivery","services_list":["General OPD","X-Ray","Laboratory","Maternity"],"source":"Reference dataset — verify before visiting","last_verified":"Reference data — verify before visiting","data_status":"reference"},
        {"name":"PHC Molgi","type":"Primary Health Centre","location":"Akkalkuwa Tribal Block","phone":"02564-282133","beds":"6","facilities":"OPD, Immunization, Cold Chain, ASHA Center","services_list":["General OPD","Immunization"],"source":"Reference dataset — verify before visiting","last_verified":"Reference data — verify before visiting","data_status":"reference"}
    ],
    "Gadchiroli (गडचिरोली)": [
        {"name":"District General Hospital Gadchiroli","type":"District Hospital","location":"Gadchiroli HQ","phone":"07132-222152","beds":"250+","facilities":"Surgical ICU, Trauma Care, Sickle Cell Unit, MJPJAY","services_list":["Emergency","General OPD"],"is_hq":True,"source":"Reference dataset — verify before visiting","last_verified":"Reference data — verify before visiting","data_status":"reference"},
        {"name":"Sub-District Hospital Aheri","type":"SDH / Tribal","location":"Aheri Block","phone":"07132-237123","beds":"100","facilities":"Maternal Care (C-Section), Blood Storage, Emergency Ops","services_list":["Maternity","Blood Bank","Emergency"],"source":"Reference dataset — verify before visiting","last_verified":"Reference data — verify before visiting","data_status":"reference"},
        {"name":"CHC Bhamragad","type":"Community Health Centre","location":"Bhamragad Block","phone":"07132-284102","beds":"30","facilities":"Basic Care, Anti-Snake Venom, Malaria Unit","services_list":["General OPD","Emergency"],"source":"Reference dataset — verify before visiting","last_verified":"Reference data — verify before visiting","data_status":"reference"},
        {"name":"PHC Kasansur","type":"Primary Health Centre","location":"Etapalli Block","phone":"07132-286044","beds":"6","facilities":"Basic OPD, Maternal ANC Services","services_list":["General OPD","Maternity"],"source":"Reference dataset — verify before visiting","last_verified":"Reference data — verify before visiting","data_status":"reference"}
    ],
    "Amravati - Melghat (अमरावती - मेळघाट)": [
        {"name":"Sub-District Hospital Dharni","type":"SDH / Tribal","location":"Dharni (Melghat)","phone":"07226-222234","beds":"100","facilities":"Nutrition Rehab (NRC), Pediatric ICU, MJPJAY","services_list":["Pediatric","Emergency","General OPD"],"is_hq":True,"source":"Reference dataset — verify before visiting","last_verified":"Reference data — verify before visiting","data_status":"reference"},
        {"name":"Sub-District Hospital Chikhaldara","type":"SDH / Tribal","location":"Chikhaldara","phone":"07226-230240","beds":"50","facilities":"Maternal Delivery, Pediatric Isolation, Emergency OPD","services_list":["Maternity","Pediatric","Emergency"],"source":"Reference dataset — verify before visiting","last_verified":"Reference data — verify before visiting","data_status":"reference"},
        {"name":"PHC Harisal","type":"Digital PHC","location":"Harisal Block","phone":"07226-288101","beds":"6","facilities":"Telemedicine, Primary Diagnostics, Basic Lab","services_list":["Telemedicine","Laboratory","General OPD"],"source":"Reference dataset — verify before visiting","last_verified":"Reference data — verify before visiting","data_status":"reference"}
    ],
    "Palghar (पालघर)": [
        {"name":"District Hospital Palghar","type":"District Hospital","location":"Palghar HQ","phone":"02525-256108","beds":"200+","facilities":"NICU, General Surgery, MJPJAY Helpdesk","services_list":["Pediatric","Emergency","General OPD"],"is_hq":True,"source":"Reference dataset — verify before visiting","last_verified":"Reference data — verify before visiting","data_status":"reference"},
        {"name":"Sub-District Hospital Jawhar","type":"SDH / Tribal Core","location":"Jawhar Block","phone":"02525-224133","beds":"100","facilities":"Malnutrition Wing (NRC), Blood Storage, Gynaecology","services_list":["Pediatric","Blood Bank","Maternity"],"source":"Reference dataset — verify before visiting","last_verified":"Reference data — verify before visiting","data_status":"reference"},
        {"name":"CHC Mokhada","type":"Community Health Centre","location":"Mokhada Block","phone":"02525-252033","beds":"30","facilities":"SOPD, Basic Maternity, Pediatric Center","services_list":["General OPD","Maternity","Pediatric"],"source":"Reference dataset — verify before visiting","last_verified":"Reference data — verify before visiting","data_status":"reference"}
    ],
    "Yavatmal (यवतमाळ)": [
        {"name":"Shri Vasantrao Naik Govt Medical College","type":"Tertiary Medical College","location":"Yavatmal City","phone":"07232-242456","beds":"500+","facilities":"Super Specialty, Advanced Diagnostics, Trauma Center","services_list":["Emergency","Laboratory","General OPD"],"is_hq":True,"source":"Reference dataset — verify before visiting","last_verified":"Reference data — verify before visiting","data_status":"reference"},
        {"name":"Sub-District Hospital Pusad","type":"Sub-District Hospital","location":"Pusad Block","phone":"07232-222045","beds":"100","facilities":"Surgical Care, Maternity ICU, Diagnostic Lab","services_list":["Emergency","Maternity","Laboratory"],"source":"Reference dataset — verify before visiting","last_verified":"Reference data — verify before visiting","data_status":"reference"}
    ]
}



# --- FACILITY COORDINATES (approximate lat/lon for geographic ranking) ---
# Source: OpenStreetMap / public geographic data for Maharashtra administrative centers
# These are APPROXIMATE center-of-town/block coordinates, NOT exact facility GPS.
FACILITY_COORDS = {
    "Civil Hospital Nandurbar": (21.3700, 74.2400),
    "Sub-District Hospital Dhadgaon": (21.5200, 74.1200),
    "CHC Shahada": (21.5500, 74.4700),
    "PHC Molgi": (21.6100, 74.3200),
    "District General Hospital Gadchiroli": (20.1800, 80.0000),
    "Sub-District Hospital Aheri": (19.4200, 80.1500),
    "CHC Bhamragad": (19.3500, 80.6500),
    "PHC Kasansur": (19.5500, 80.3500),
    "Sub-District Hospital Dharni": (21.6700, 77.2500),
    "Sub-District Hospital Chikhaldara": (21.4200, 77.3300),
    "PHC Harisal": (21.5500, 77.1000),
    "District Hospital Palghar": (19.7000, 72.7700),
    "Sub-District Hospital Jawhar": (19.9200, 73.2300),
    "CHC Mokhada": (19.9800, 73.0200),
    "Shri Vasantrao Naik Govt Medical College": (20.3900, 78.1300),
    "Sub-District Hospital Pusad": (20.0800, 77.5800),
}

# Approximate district center coordinates for district-level proximity
DISTRICT_COORDS = {
    "Nandurbar": (21.3700, 74.2400),
    "Gadchiroli": (20.1800, 80.0000),
    "Amravati": (21.6700, 77.2500),
    "Palghar": (19.7000, 72.7700),
    "Yavatmal": (20.3900, 78.1300),
}

# Approximate block coordinates for locality-level proximity
BLOCK_COORDS = {
    "nandurbar town": (21.3700, 74.2400),
    "dhadgaon block": (21.5200, 74.1200),
    "shahada": (21.5500, 74.4700),
    "akkalkuwa tribal block": (21.6100, 74.3200),
    "gadchiroli hq": (20.1800, 80.0000),
    "aheri block": (19.4200, 80.1500),
    "bhamragad block": (19.3500, 80.6500),
    "etapalli block": (19.5500, 80.3500),
    "dharni (melghat)": (21.6700, 77.2500),
    "chikhaldara": (21.4200, 77.3300),
    "harisal block": (21.5500, 77.1000),
    "palghar hq": (19.7000, 72.7700),
    "jawhar block": (19.9200, 73.2300),
    "mokhada block": (19.9800, 73.0200),
    "yavatmal city": (20.3900, 78.1300),
    "pusad block": (20.0800, 77.5800),
}

import math

def haversine_km(lat1, lon1, lat2, lon2):
    """Calculate great-circle distance between two points on Earth (km)."""
    R = 6371.0  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def get_facility_coords(fac):
    """Get approximate coordinates for a facility from FACILITY_COORDS or location name."""
    name = fac.get("name", "")
    if name in FACILITY_COORDS:
        return FACILITY_COORDS[name]
    # Fall back to block-level coordinates from location field
    loc = fac.get("location", "").lower()
    if loc in BLOCK_COORDS:
        return BLOCK_COORDS[loc]
    return None

def facility_distance_km(fac, ref_lat, ref_lon):
    """Return approximate distance in km from reference point to facility, or None."""
    coords = get_facility_coords(fac)
    if not coords:
        return None
    return haversine_km(ref_lat, ref_lon, coords[0], coords[1])

MAHARASHTRA_SCHEMES = [
    {"name":"Mahatma Jyotirao Phule Jan Arogya Yojana (MJPJAY)","benefits":"Cashless treatment up to ₹5,00,000/family/year for 996 identified procedures.","eligibility":"Yellow, Orange, AAY, Annapurna Ration cards. Farmers in 14 distressed districts. Eligibility depends on scheme rules — verify through official channel.","apply_how":"Visit any empanelled hospital → 'Arogyamitra' desk with Ration Card + Aadhaar.","what_to_carry":"Yellow/Orange/AAY Ration Card, Aadhaar Card","verify_at":"Visit arogyamitra desk at empanelled hospital or call 1800-233-2085","source":"maha.gov.in","status":"LIVE"},
    {"name":"Ayushman Bharat - PMJAY (Integrated with MJPJAY)","benefits":"Cashless cover up to ₹5,00,000/family/year for secondary & tertiary care.","eligibility":"SECC 2011 identified poor & vulnerable families. Eligibility depends on scheme rules — verify through official channel.","apply_how":"Verify at pmjay.gov.in or contact Arogyamitra at any empanelled facility.","what_to_carry":"Aadhaar Card, Ration Card","verify_at":"pmjay.gov.in or call 14555","source":"pmjay.gov.in","status":"LIVE"},
    {"name":"Balasaheb Thackeray Aapla Dawakhana","benefits":"Free primary consults, essential medicines, 147 free diagnostic tests.","eligibility":"All Maharashtra citizens; focus on urban slums & rural pockets.","apply_how":"Walk-in directly to any Aapla Dawakhana clinic. No prior registration.","what_to_carry":"No documents required for basic consult","verify_at":"Contact nearest municipal health post","source":"MCGM / Maharashtra Health Dept","status":"LIVE"},
    {"name":"Navsanjivan Yojana (Tribal Focus)","benefits":"Specialized medical squads to tribal blocks, free maternal supplements, transport cash aid.","eligibility":"Tribal residents of 16 designated tribal districts of Maharashtra. Verify eligibility through block ICDS officer.","apply_how":"Coordinated through block ICDS officers, local ASHAs, or ANM workers.","what_to_carry":"Tribal certificate, Aadhaar Card","verify_at":"Block ICDS office or Tribal Development Dept","source":"Tribal Development Dept, Maharashtra","status":"LIVE"},
    {"name":"Janani Suraksha Yojana (JSY)","benefits":"₹700 cash + free institutional delivery for rural pregnant women.","eligibility":"All pregnant women in rural areas of Maharashtra (BPL preferred). Verify through ASHA or PHC.","apply_how":"Register at PHC/Sub-Centre through ASHA worker during first ANC visit.","what_to_carry":"Aadhaar Card, Bank Passbook, MCP Card","verify_at":"Nearest PHC/Sub-Centre or call ASHA worker","source":"National Health Mission","status":"LIVE"},
    {"name":"Rashtriya Bal Swasthya Karyakram (RBSK)","benefits":"Free health screening for children 0-18 yrs (4 D's: Defects, Diseases, Deficiencies, Development delays).","eligibility":"All children in Anganwadi, Government & Aided schools.","apply_how":"Mobile Health Teams visit schools/Anganwadis; free treatment referral to DEIC.","what_to_carry":"Child's Aadhaar (if available), School/Anganwadi ID","verify_at":"District RBSK office or nearest DEIC","source":"National Health Mission","status":"LIVE"}
]

GENERIC_MEDS = {
    "Paracetamol (500mg)": {"branded":"₹40 - ₹60","generic":"₹6 - ₹9","saving":"85%","use":"Fever, mild pain"},
    "Amoxicillin (500mg)": {"branded":"₹120 - ₹160","generic":"₹28 - ₹35","saving":"80%","use":"Bacterial infections"},
    "Metformin (500mg)": {"branded":"₹70 - ₹95","generic":"₹11 - ₹15","saving":"84%","use":"Type 2 Diabetes"},
    "Atorvastatin (10mg)": {"branded":"₹90 - ₹130","generic":"₹18 - ₹24","saving":"82%","use":"High cholesterol"},
    "ORS Sachet": {"branded":"₹22 - ₹28","generic":"₹5 - ₹7","saving":"78%","use":"Dehydration, diarrhea"},
    "Iron + Folic Acid": {"branded":"₹60 - ₹100","generic":"FREE at ASHA","saving":"100%","use":"Anemia, Pregnancy"},
    "Amlodipine (5mg)": {"branded":"₹80 - ₹110","generic":"₹12 - ₹18","saving":"83%","use":"High BP (Hypertension)"}
}

ANC_SCHEDULE = [
    {"visit":"1st ANC Visit","timing":"Within 12 weeks","importance":"Pregnancy confirmation, blood tests, MCP Card registration, free Folic Acid."},
    {"visit":"2nd ANC Visit","timing":"14-26 weeks","importance":"TT-1 injection, BP monitoring, fetal heartbeat, iron-folic acid tablets."},
    {"visit":"3rd ANC Visit","timing":"28-34 weeks","importance":"TT-2/Booster, fetal growth monitoring, anemia screening."},
    {"visit":"4th ANC Visit","timing":"36 weeks to delivery","importance":"Delivery planning, institutional delivery, 102 Janani Express linkage."}
]

IMMUNIZATION_SCHEDULE = [
    {"age":"At Birth","vaccines":"BCG, OPV-0, Hepatitis B","protects":"TB, Polio, Liver infection"},
    {"age":"6 Weeks","vaccines":"Pentavalent-1, OPV-1, RVV-1, fIPV-1","protects":"Diphtheria, Pertussis, Tetanus, HepB, HiB, Rotavirus, Polio"},
    {"age":"10 Weeks","vaccines":"Pentavalent-2, OPV-2, RVV-2","protects":"Continued protection"},
    {"age":"14 Weeks","vaccines":"Pentavalent-3, OPV-3, RVV-3, fIPV-2","protects":"Full early childhood protection"},
    {"age":"9 Months","vaccines":"MR-1 (Measles-Rubella), Vitamin A-1","protects":"Measles, Rubella, Vitamin A deficiency"},
    {"age":"16-24 Months","vaccines":"DPT Booster-1, OPV Booster, MR-2","protects":"Booster protection"}
]

HEALTH_CAMPS = [
    {"date":"Every 9th of Month","name":"Pradhan Mantri Surakshit Matritva Abhiyan (PMSMA)","location":"All PHCs & CHCs","services":"Free ANC checkup for pregnant women, USG, blood tests","target":"Pregnant women (2nd/3rd trimester)","action":"Contact your local PHC/CHC to confirm the schedule for this month."},
    {"date":"Every Wednesday","name":"Village Health, Nutrition & Sanitation Day (VHSND)","location":"Anganwadi Centers","services":"Immunization, growth monitoring, ANC, nutrition counseling","target":"Children under 5, Pregnant/Lactating women","action":"Visit your nearest Anganwadi center on Wednesday. Ask your ASHA worker for the schedule."},
    {"date":"Monthly (1st Saturday)","name":"Non-Communicable Disease (NCD) Screening Camp","location":"Sub-Centres & CHCs","services":"Free BP, Diabetes, Oral/Breast/Cervical cancer screening","target":"Adults 30+ years","action":"Visit your nearest Sub-Centre or CHC on the first Saturday. No registration needed."},
    {"date":"Quarterly","name":"Mission Indradhanush","location":"Village-level door-to-door","services":"Immunization of missed children (0-5 yrs) & pregnant women","target":"Unvaccinated / partially vaccinated","action":"ASHA/ANM workers will visit your village. Contact your ASHA worker or PHC for the next drive date."},
    {"date":"World TB Day (24 Mar)","name":"National TB Elimination Program Camp","location":"District Hospitals","services":"Free sputum test, X-Ray, DOTS enrollment","target":"Persistent cough >2 weeks","action":"Visit your nearest District Hospital. If you have persistent cough >2 weeks, visit any PHC for free sputum test anytime."}
]

ABHA_INFO = {
    "en": {
        "what": "ABHA (Ayushman Bharat Health Account) is a free 14-digit digital health identifier that can be used to link and access health records within the ABDM ecosystem, subject to applicable consent and participating healthcare providers. It is not mandatory.",
        "benefits": ["✅ Access linked health records through participating ABDM-enabled systems, with applicable consent","✅ Reduce paperwork at government facilities","✅ Can help reduce paperwork where supported by participating systems","✅ Digital prescriptions and lab reports in one place","✅ Portable health identifier accepted at participating ABDM facilities"],
        "how_to_create": ["1️⃣ Visit <a href='https://abha.abdm.gov.in' target='_blank' style='color:#0B6BCB;font-weight:700;'>abha.abdm.gov.in</a> or download 'ABHA' app","2️⃣ Choose 'Create ABHA Number using Aadhaar or Driving License'","3️⃣ Enter your Aadhaar → OTP verification","4️⃣ Set a username → ABHA ID generated instantly (FREE)","5️⃣ Download / screenshot your ABHA card"]
    },
    "hi": {
        "what": "ABHA (आयुष्मान भारत हेल्थ अकाउंट) एक मुफ्त 14-अंकीय डिजिटल हेल्थ पहचान संख्या है जो ABDM इकोसिस्टम में स्वास्थ्य रिकॉर्ड लिंक और एक्सेस करने के लिए उपयोग होती है। यह अनिवार्य नहीं है।",
        "benefits": ["✅ भारत के किसी भी अस्पताल से मेडिकल रिकॉर्ड एक्सेस करें","✅ सरकारी सुविधाओं में कागजी कार्रवाई कम","✅ सहभागी प्रणालींद्वारे कागजपत्रे कमी करण्यास मदत","✅ डिजिटल प्रिस्क्रिप्शन और लैब रिपोर्ट एक जगह","✅ ABDM सुविधाओं में स्वीकृत पोर्टेबल हेल्थ पहचान"],
        "how_to_create": ["1️⃣ <a href='https://abha.abdm.gov.in' target='_blank' style='color:#0B6BCB;font-weight:700;'>abha.abdm.gov.in</a> पर जाएं या 'ABHA' ऐप डाउनलोड करें","2️⃣ 'आधार से ABHA नंबर बनाएं' चुनें","3️⃣ आधार दर्ज करें → OTP सत्यापन","4️⃣ यूजरनेम सेट करें → ABHA ID तुरंत जनरेट (मुफ्त)","5️⃣ अपना ABHA कार्ड डाउनलोड करें"]
    },
    "mr": {
        "what": "ABHA (आयुष्मान भारत हेल्थ अकाउंट) हे एक विनामूल्य १४-अंकी डिजिटल आरोग्य ओळखपत्र आहे जे ABDM इकोसिस्टममध्ये आरोग्य रेकॉर्ड जोडण्यासाठी वापरले जाऊ शकते. हे अनिवार्य नाही.",
        "benefits": ["✅ सहभागी ABDM-सक्षम प्रणालींद्वारे आरोग्य रेकॉर्ड ऍक्सेस करा (संमती आवश्यक)","✅ सरकारी सुविधांमध्ये कागदपत्रे कमी","✅ सहभागी प्रणालींमध्ये कागदपत्रे कमी करण्यास मदत","✅ डिजिटल प्रिस्क्रिप्शन आणि लॅब अहवाल एका ठिकाणी","✅ ABDM सुविधांमध्ये स्वीकृत पोर्टेबल आरोग्य ओळख"],
        "how_to_create": ["1️⃣ <a href='https://abha.abdm.gov.in' target='_blank' style='color:#0B6BCB;font-weight:700;'>abha.abdm.gov.in</a> ला भेट द्या किंवा 'ABHA' अ‍ॅप डाउनलोड करा","2️⃣ 'आधार वापरून ABHA नंबर तयार करा' निवडा","3️⃣ आधार टाका → OTP पडताळणी","4️⃣ वापरकर्तानाव सेट करा → ABHA आयडी तात्काळ (विनामूल्य)","5️⃣ आपले ABHA कार्ड डाउनलोड करा"]
    }
}

FEATURE_ROADMAP = [
    {"phase":"PHASE 1","phase_class":"th-roadmap-p1","status":"DEMO","title":"🏥 Rural Facility Locator","desc":"District-wise directory of PHCs, CHCs, SDHs across 5 major tribal Maharashtra districts with call-to-action integration."},
    {"phase":"PHASE 1","phase_class":"th-roadmap-p1","status":"DEMO","title":"📋 Government Schemes Portal","desc":"6 major schemes: MJPJAY, PM-JAY, Aapla Dawakhana, Navsanjivan, JSY, RBSK with eligibility & application steps."},
    {"phase":"PHASE 1","phase_class":"th-roadmap-p1","status":"DEMO","title":"🤰 Maternal & Child Health Module","desc":"4-visit ANC schedule, complete UIP immunization timeline, danger sign detection, JSY linkage."},
    {"phase":"PHASE 2","phase_class":"th-roadmap-p2","status":"INFO","title":"📞 Telemedicine Guide (eSanjeevani)","desc":"Step-by-step instructions for eSanjeevani OPD + 104 Health Helpline. No API integration — informational only."},
    {"phase":"PHASE 2","phase_class":"th-roadmap-p2","status":"LIVE","title":"🚑 Emergency Helplines","desc":"Clickable tel: links for 108 MEMS, 102 Janani Express, 104 Health Line, 1098 Child, 181 Women helplines."},
    {"phase":"PHASE 2","phase_class":"th-roadmap-p2","status":"INFO","title":"👩‍⚕️ ASHA & ANM Worker Guide","desc":"Educational content about frontline health worker services, how to contact, medicines they can dispense free."},
    {"phase":"PHASE 3","phase_class":"th-roadmap-p3","status":"DEMO","title":"💊 Jan Aushadhi Generic Drug Guide","desc":"Cost comparison of 7 essential medicines. Prices are reference estimates — verify at your local store."},
    {"phase":"PHASE 3","phase_class":"th-roadmap-p3","status":"BETA","title":"📴 Low-Bandwidth Mode","desc":"Reduces processing by using keyword matching instead of AI models, and skipping translation APIs. Still requires a server connection — not offline."},
    {"phase":"PHASE 3","phase_class":"th-roadmap-p3","status":"INFO","title":"🆔 ABHA Digital Health ID","desc":"Complete guide to create Ayushman Bharat Health Account for portable digital records."},
    {"phase":"PHASE 3","phase_class":"th-roadmap-p3","status":"INFO","title":"📅 Health Program Calendar","desc":"Recurring government health programs: PMSMA, VHSND, NCD screening, Mission Indradhanush schedules."},
    {"phase":"PHASE 3","phase_class":"th-roadmap-p3","status":"LIVE","title":"📓 Session Symptom Log","desc":"Session-based symptom log records queries during consultation. Session-only: data held in browser memory, cleared on page refresh."},
    {"phase":"PHASE 3","phase_class":"th-roadmap-p3","status":"INFO","title":"📱 Emergency Contact Guide","desc":"Guidance for accessing emergency and public health helplines when internet access is limited."}
]

# ============================================================================
# NLP & TRANSLATION LAYER
# ============================================================================
def _merge_compound_aches(text):
    t = (text or "").lower()
    for w in _COMPOUND_ACHE_WORDS:
        t = re.sub(rf"\b{w}\s+aches?\b", w + "ache", t)
    return t

def _stem_word(w):
    w = (w or "").lower()
    if len(w) <= 3: return w
    if w in _STEM_EXCEPTIONS: return _STEM_EXCEPTIONS[w]
    if w.endswith("ies") and len(w) > 4: return w[:-3] + "y"
    if w.endswith("ing"): return w[:-3] if len(w[:-3]) >= 3 else w
    if w.endswith("ed"): return w[:-2] if len(w[:-2]) >= 3 else w
    if w.endswith("ly") and len(w) > 5: return w[:-2]
    if w.endswith("es") and len(w) > 4: return w[:-2]
    if w.endswith("s") and len(w) > 3 and not w.endswith("ss"): return w[:-1]
    return w

GENERIC_SYMPTOMS_STEMMED = set(GENERIC_SYMPTOMS) | {_stem_word(w) for w in GENERIC_SYMPTOMS}

RED_FLAG_PHRASES_EN = ["difficulty breathing","shortness of breath","can't breathe","cannot breathe","unable to breathe","hard to breathe","breathless","gasping","chest pain","pain in chest","tightness in chest","pressure in chest","unconscious","unconsciousness","fainted","fainting","passed out","collapsed","not waking","not responding","loss of consciousness","coughing blood","coughing up blood","vomiting blood","blood in vomit","blood in stool","bloody stool","black stool","severe bleeding","uncontrolled bleeding","seizure","seizures","convulsion","convulsions","stiff neck","neck stiffness","blue lips","bluish lips","blue face","severe abdominal pain","severe stomach pain","confusion","disoriented","very drowsy","difficulty swallowing","cannot swallow","no urine","not passing urine","sunken eyes","high fever not improving","fever not improving after 3 days","hot dry skin","not sweating"]
RED_FLAG_PHRASES_HI = ["सांस लेने में तकलीफ","सांस नहीं आ","सांस फूल","बेहोश","बेहोशी","सीने में दर्द","छाती में दर्द","खून की उल्टी","खून आ रहा","खून निकल","दौरा पड़","दौरे आ","गर्दन अकड़",
    "सांस लेने में दिक्कत",
    "सांस लेने में बहुत",
    "सांस में तकलीफ",
    "सांस में दिक्कत"]
RED_FLAG_PHRASES_MR = ["श्वास घेण्यास त्रास",
    "श्वास घेण्यास खूप",
    "श्वास लागला",
    "श्वास घेऊ शकत नाही","दम लागणे","छातीत दुखणे","बेहोश","शुद्ध हरपणे","रक्ताची उलटी","रक्तस्त्राव","झटके येणे","फिट येणे","मान आखडणे","पोटात तीव्र वेदना","लघवी न होणे","गरोदरपणात रक्तस्त्राव","गरोदरपणात तीव्र पोटदुखी"]

CRITICAL_EMERGENCY_PHRASES_EN = ["difficulty breathing","shortness of breath","can't breathe","cannot breathe","unable to breathe","hard to breathe","breathless","gasping","chest pain","pain in chest","tightness in chest","pressure in chest","unconscious","unconsciousness","fainted","fainting","passed out","collapsed","not waking","not responding","loss of consciousness","coughing blood","coughing up blood","vomiting blood","blood in vomit","severe bleeding","uncontrolled bleeding","seizure","seizures","convulsion","convulsions","blue lips","bluish lips","blue face","confusion","disoriented","very drowsy"]
CRITICAL_EMERGENCY_PHRASES_HI = ["सांस लेने में तकलीफ","सांस नहीं आ","सांस फूल","बेहोश","बेहोशी","सीने में दर्द","छाती में दर्द","खून की उल्टी","खून आ रहा","खून निकल","दौरा पड़","दौरे आ"]
CRITICAL_EMERGENCY_PHRASES_MR = ["श्वास घेण्यास त्रास",
    "श्वास घेण्यास खूप",
    "श्वास लागला",
    "श्वास घेऊ शकत नाही","दम लागणे","छातीत दुखणे","बेहोश","शुद्ध हरपणे","रक्ताची उलटी","रक्तस्त्राव","झटके येणे","फिट येणे"]

EXTRA_KEYWORDS = {
    "Dengue":["pain behind eyes","behind the eyes","behind my eyes","bleeding gums","joint pain","severe abdominal pain","persistent vomiting","fever not improving after 3 days"],
    "Malaria":["chills","shivering","sweating","fever with chills"],
    "Tuberculosis (TB)":["coughing blood","night sweats","cough more than 2 weeks","persistent cough"],
    "Diarrhea":["loose stools","watery stools","dehydrat","stomach pain","stomach cramps","cramps"],
    "Common Cold":["runny nose","blocked nose","sneezing","sore throat","cold","cough"],
    "Typhoid":["prolonged fever","stomach pain","loss of appetite"],
    "Chikungunya":["severe joint pain","joint pain","sudden fever"],
    "Influenza (Flu)":["body ache","muscle ache","muscle pain","congestion"],
    "Diabetes (Type 2) Awareness":["increased thirst","frequent urination","blurred vision","thirst and frequent urination"],
    "Hypertension (High BP) Awareness":["high bp","high blood pressure","nosebleed"],
    "Anemia":["pale skin","cold hands","dizziness","dizzy","tired","weakness","fatigue"],
    "Chickenpox":["fluid-filled","blisters","itchy rash"],
    "Conjunctivitis (Eye Flu)":["red eyes","itchy eyes","watery eyes","eye discharge","pink eye"],
    "Skin Infection (Fungal)":["itchy skin","skin folds","scaling"],
    "Malnutrition (Child Health Awareness)":["poor growth","low weight","irritability"],
    "Cholera":["rice water stools","rice-water stools","profuse watery diarrhea","watery diarrhea","cholera"],
    "Food Poisoning":["after eating","food poisoning","stale food","contaminated food"],
    "Viral Fever (Common Viral Illness)":["viral fever","viral","fever","high fever","mild fever","bukhar","बुखार","तेज बुखार"],
    "Pneumonia":["cough with phlegm","phlegm","rapid breathing","pneumonia"],
    "Asthma":["wheezing","chest tightness","asthma","inhaler"],
    "Bronchitis (Acute)":["cough with mucus","mucus","bronchitis"],
    "Tonsillitis (Sore Throat)":["swollen tonsils","tonsils","pain while swallowing","sore throat"],
    "Sinusitis":["facial pain","blocked nose","sinus","thick nasal discharge"],
    "Migraine":["throbbing headache","migraine","sensitivity to light","light and sound","head pain","sardardi","headache"],
    "Gastritis / Acidity (GERD)":["acidity","heartburn","burning pain in upper abdomen","gastritis","indigestion"],
    "Constipation":["constipation","hard stools","straining"],
    "Urinary Tract Infection (UTI)":["burning urination","burning while urinating","pain while urinating"],
    "Kidney Stones":["blood in urine","back pain","side pain","kidney stone","stones in kidney"],
    "Dehydration":["dehydration","dark urine","extreme thirst","less urine"],
    "Heat Stroke":["heat stroke","hot dry skin","no sweating","sunstroke"],
    "Japanese Encephalitis":["stiff neck","encephalitis","seizures","confusion"],
    "Leptospirosis":["calf pain","red eyes","leptospirosis","flood water"],
    "Scrub Typhus":["eschar","scab-like","scrub typhus","dark sore"],
    "Hepatitis A (Jaundice)":["jaundice","yellow eyes","yellow skin","dark urine"],
    "Measles":["measles","rash starting on face","red watery eyes","koplik"],
    "Intestinal Worms (Worm Infestation)":["worms in stool","worms","itchy anus","deworming"],
    "Scabies":["scabies","itching at night","night itching","between fingers","burrow"],
    "Osteoarthritis (Joint Pain)":["joint stiffness","osteoarthritis","knee pain","morning stiffness"],
    "Ear Infection (Otitis Media)":["ear pain","earache","fluid from ear","ear infection"],
    "Mumps":["swollen glands","mumps","pain while chewing","parotitis"],
    "Whooping Cough (Pertussis)":["whooping","coughing fits","whooping cough","pertussis"],
    "Appendicitis (Awareness)":["lower right abdomen","appendix","navel","appendicitis"],
    "Mental Health (Stress & Anxiety) Awareness":["anxiety","stress","worry","mental health","sleeplessness"],
}

ROMANIZED_HI_MAP = {"bukhar":"fever","bukhaar":"fever","khansi":"cough","khaansi":"cough","thandi":"cold","jukaam":"cold","sardardi":"headache","sar":"head","sir":"head","dard":"pain","peeda":"pain","pet":"stomach","peit":"stomach","chakkar":"dizzy","kamzor":"weak","thakan":"tired","thakaan":"tired","pyaas":"thirst","pyas":"thirst","dast":"diarrhea","daste":"diarrhea","ult":"vomit","ulti":"vomit","ultii":"vomit","jod":"joint","jodo":"joint","gala":"throat","gale":"throat","naak":"nose","aankh":"eye","ankh":"eye","aankhein":"eyes","chamdi":"skin","khoon":"blood","seena":"chest","seene":"chest","chhati":"chest","chhathi":"chest","saans":"breath","behosh":"unconscious","dawai":"medicine","aa":"","raha":"","rahe":"","rahi":"","rha":"","rhe":"","hua":"","hui":"","hue":"","ho":"","kar":"","karke":"","sakta":"","sakti":"","wala":"","wali":"","mujhe":"i","mera":"my","meri":"my","mere":"my","main":"i","mein":"in","hai":"","hain":"","ka":"","ki":"","ke":"","ko":"","me":"","aur":"and","nahi":"not","na":"not","bahut":"very","zyada":"much","bhi":"also"}
ROMANIZED_HI_STRONG = {"bukhar","bukhaar","khansi","khaansi","thandi","jukaam","sardardi","chakkar","kamzor","pyaas","dast","daste","ulti","ultii","saans","behosh","chhati","chhathi","seena","seene","dard","thakan","thakaan","peeda","aankh","ankh","aankhein","kamjori","sir","sar","pet","gala","naak","khoon","jod","jodo"}

def is_romanized_hindi(query): return bool(set(re.findall(r"[a-z]+", normalize_for_match(query))) & ROMANIZED_HI_STRONG)
def romanize_to_english(query):
    out = []
    for w in re.findall(r"[a-z]+", normalize_for_match(query)):
        if w in ROMANIZED_HI_MAP:
            mapped = ROMANIZED_HI_MAP[w]
            if mapped: out.append(mapped)
        else: out.append(w)
    return " ".join(out)

_DEVANAGARI_HI_MAP = [("सांस लेने में तकलीफ","difficulty breathing"),("सांस नहीं आ","cannot breathe"),("सांस फूल","shortness of breath"),("सीने में दर्द","chest pain"),("छाती में दर्द","chest pain"),("खून की उल्टी","vomiting blood"),("बेहोश","unconscious"),("दौरा पड़","seizure"),("दौरे आ","seizure"),("गर्दन अकड़","stiff neck"),("आँखों के पीछे दर्द","pain behind eyes"),("कंपकंपी","chills"),("ठंड लग","chills"),("कांप","shivering"),("रात को पसीना","night sweats"),("दो हफ्ते से खांसी","cough lasting more than 2 weeks"),("लंबे समय से खांसी","persistent cough"),("खांसी के साथ बलगम","cough with phlegm"),("बलगम","phlegm"),("चावल के पानी जैसे दस्त","rice water stools"),("पतले दस्त","loose stools"),("पानी जैसे दस्त","watery stools"),("दस्त हो रहे","diarrhea"),("दस्त हो रहा","diarrhea"),("आंखें लाल","red eyes"),("आँखें लाल","red eyes"),("आंख लाल","red eye"),("आँख लाल","red eye"),("त्वचा पीली","yellow skin"),("पेशाब में जलन","burning urination"),("बार बार पेशाब","frequent urination"),("बहुत प्यास","increased thirst"),("पेशाब में खून","blood in urine"),("जोड़ों में दर्द","joint pain"),("गले में दर्द","sore throat"),("गला खराब","sore throat"),("मांसपेशियों में दर्द","muscle pain"),("शरीर में दर्द","body ache"),("पीठ दर्द","back pain"),("कमर दर्द","back pain"),("पेट में दर्द","stomach pain"),("सिर में तेज दर्द","throbbing headache"),("सिर में दर्द","headache"),("रात में खुजली","itching at night"),("त्वचा पर खुजली","itchy skin"),("उंगलियों के बीच","between fingers"),("घरघराहट","wheezing"),("तेज बुखार","high fever"),("बुखार है","fever"),("बुखार","fever"),("खांसी","cough"),("सिर दर्द","headache"),("सिरदर्द","headache"),("पेट दर्द","stomach pain"),("पेट खराब","diarrhea"),("चक्कर","dizzy"),("कमजोरी","weakness"),("थकान","tiredness"),("उल्टी","vomiting"),("दस्त","diarrhea"),("जुकाम","cold"),("नाक बह","runny nose"),("नाक बंद","blocked nose"),("घबराहट","anxiety"),("चिंता","stress"),("तनाव","stress"),("खुजली","itching"),("दर्द","pain"),("प्यास","thirst"),("भूख","appetite"),("सिर","head"),("आँख","eye"),("आंख","eye"),("नाक","nose"),("गला","throat"),("कान","ear"),("पेट","stomach"),("छाती","chest"),("खून","blood"),("सांस","breath"),("जोड़","joint"),("त्वचा","skin")]

_DEVANAGARI_MR_MAP = [("श्वास घेण्यास त्रास", "difficulty breathing"),
    ("श्वास घेण्यास खूप", "difficulty breathing"),
    ("श्वास लागला", "difficulty breathing"),
    ("श्वास घेऊ शकत नाही", "difficulty breathing"),
    ("दम लागणे","shortness of breath"),("छातीत दुखणे","chest pain"),("रक्ताची उलटी","vomiting blood"),("शुद्ध हरपणे","unconscious"),("ताप आणि थंडी","fever with chills"),("खोकला","cough"),("ताप","fever"),("पोटदुखी","stomach pain"),("डोकेदुखी","headache"),("अतिसार","diarrhea"),("उलटी","vomiting"),("अशक्तपणा","weakness"),("खाज","itching"),("सांधेदुखी","joint pain"),("तोंड कोरडे पडणे","dehydration"),("गरोदरपणात रक्तस्त्राव","bleeding during pregnancy"),("गरोदरपणात तीव्र पोटदुखी","severe abdominal pain during pregnancy")]

def devanagari_to_english(query):
    if not query: return ""
    text = query
    for mr, en in _DEVANAGARI_MR_MAP: text = text.replace(mr, " " + en + " ")
    for hi, en in _DEVANAGARI_HI_MAP: text = text.replace(hi, " " + en + " ")
    return " ".join(re.findall(r"[a-z]+", text.lower()))

def normalize_for_match(text): return (text or "").lower().replace("'", "")


# --- SERVICE NORMALIZATION LAYER ---
# Canonical service names used in the facility dataset: services_list values
SERVICE_SYNONYMS = {
    # immunization / vaccination
    "immunization": "Immunization", "vaccination": "Immunization", "vaccine": "Immunization",
    "vaccines": "Immunization", "booster": "Immunization", "teeka": "Immunization",
    "tika": "Immunization", "tice": "Immunization", "lasikaran": "Immunization",
    "pratirodhak": "Immunization", "immunisation": "Immunization",
    "mission indradhanush": "Immunization",
    # maternity / pregnancy
    "maternity": "Maternity", "pregnancy": "Maternity", "delivery": "Maternity",
    "maternity ward": "Maternity", "anc": "Maternity", "prenatal": "Maternity",
    "garbhvati": "Maternity", "garbhavati": "Maternity", "garbhotpadan": "Maternity",
    "prasuti": "Maternity", "prasutikaran": "Maternity", "lasikaran": "Maternity",
    # pediatric / child
    "pediatric": "Pediatric", "paediatric": "Pediatric", "child care": "Pediatric",
    "children": "Pediatric", "child health": "Pediatric",
    "balchikitsa": "Pediatric", "baalrog": "Pediatric",
    # emergency
    "emergency": "Emergency", "urgent care": "Emergency", "casualty": "Emergency",
    "trauma": "Emergency", "emergency ops": "Emergency",
    "aapatkalin": "Emergency", "aapatkalin": "Emergency",
    # laboratory / diagnostics
    "laboratory": "Laboratory", "lab": "Laboratory", "blood test": "Laboratory",
    "diagnostic": "Laboratory", "x-ray": "X-Ray", "xray": "X-Ray",
    # general OPD
    "general opd": "General OPD", "opd": "General OPD", "consultation": "General OPD",
    "checkup": "General OPD", "check-up": "General OPD",
    # blood bank
    "blood bank": "Blood Bank", "blood": "Blood Bank",
    # telemedicine
    "telemedicine": "Telemedicine", "online consultation": "Telemedicine",
    "esanjeevani": "Telemedicine",
}

# Service topic detection — finds the service topic in a query regardless of language
SERVICE_TOPIC_PATTERNS = {
    "Immunization": [
        "immunization", "immunisation", "vaccination", "vaccinate", "vaccinated",
        "vaccine", "vaccines", "booster", "teeka", "tika", "tice",
        "mission indradhanush",
        "टीका", "लसीकरण",
        "प्रतिरोधक",
        "प्रतिरोधकक",
        "लस", "मिशन इंद्रधनुष",
    ],
    "Maternity": [
        "maternity", "pregnancy", "pregnant", "delivery", "prenatal", "anc",
        "garbhvati", "garbhavati", "garbhotpadan", "prasuti",
        "गर्भवती", "गरोदर",
        "प्रसूती", "लस",
    ],
    "Pediatric": [
        "pediatric", "paediatric", "child care", "balchikitsa",
        "बालचिकित्सा",
    ],
    "Emergency": [
        "emergency", "trauma", "casualty", "aapatkalin", "aapatkalin",
        "आपतकालीन",
    ],
    "Laboratory": [
        "laboratory", "lab test", "blood test", "diagnostic", "x-ray", "xray",
        "लैब",
    ],
    "Blood Bank": ["blood bank", "blood storage", "रक्तपेढ"],
    "Telemedicine": ["telemedicine", "online consultation", "esanjeevani", "e-sanjeevani"],
}

def detect_requested_service(combined_text):
    """Detect the healthcare service the user is requesting.
    Returns canonical service name or None."""
    c = combined_text.lower()
    for service, patterns in SERVICE_TOPIC_PATTERNS.items():
        for pat in patterns:
            if pat in c:
                return service
    return None

# --- INFORMATIONAL vs ACTION intent detection ---
# Words that signal the user wants INFORMATION, not a facility/location
_INFO_SEEKING_PATTERNS = [
    "ke baare mein", "ke bare mein", "kya hai", "kya hota", "kaise hota",
    "batao kya", "jankari", "jaankari", "information", "about", "tell me about",
    "what is", "how to", "why", "explain", "के बारे में",
    "क्या है", "जानकारी",
    "समजाणे", "संपूर्ण करा",
    "विषयी", "माहिती",
]

# Words that signal the user wants to FIND/GO TO a facility
_FACILITY_SEEKING_PATTERNS = [
    "hospital", "clinic", "phc", "chc", "center", "centre", "facility",
    "kahan", "kidhar", "kaha", "kutra", "kuthe", "nearest", "near me",
    "batao", "बताओ", "दिखाओ", "दिखवा", "dikhao", "dhundo", "chahiye", "chahiyan", "chahiyen", "find", "show me",
    "where can", "where to", "where is", "location",
    "nearest hospital", "closest hospital", "government hospital",
    "रुग्णालय", "अस्पताल",
    "सुविधा", "कुठे",
    "क्वाण", "साँगवा",
    "जवळचे", "जवळचा",
    "नजीक", "सबसे जवळ",
    "kareebi", "sabse kareeb", "kareeb wala",
    "mere paas", "paas wala", "gavat", "gavmadhe",
]

# Schedule/temporal patterns
_SCHEDULE_PATTERNS = [
    "kab", "kab hai", "kab lagega", "kab lagta", "schedule", "timing", "date",
    "kitne baje", "kaunse din", "कब", "कब है",
    "कदी", "वेळ", "तारीख",
]

def is_informational_query(combined_text):
    """Detect if user is asking for information, not seeking a facility."""
    c = combined_text.lower()
    return any(p in c for p in _INFO_SEEKING_PATTERNS)

def is_facility_seeking_query(combined_text):
    """Detect if user wants to find/visit a facility."""
    c = combined_text.lower()
    return any(p in c for p in _FACILITY_SEEKING_PATTERNS)

def is_schedule_query(combined_text):
    """Detect if user is asking about timing/schedule."""
    c = combined_text.lower()
    return any(p in c for p in _SCHEDULE_PATTERNS)



def has_red_flags(original_query, english_query):
    original, english = normalize_for_match(original_query), normalize_for_match(english_query)
    for phrase in RED_FLAG_PHRASES_EN:
        if phrase in english or phrase_hits(english, phrase, strict=True): return True
    for phrase in RED_FLAG_PHRASES_HI + RED_FLAG_PHRASES_MR:
        if phrase in original: return True
    return False

def is_critical_emergency(original_query, english_query):
    original, english = normalize_for_match(original_query), normalize_for_match(english_query)
    for phrase in CRITICAL_EMERGENCY_PHRASES_EN:
        if phrase in english or phrase_hits(english, phrase, strict=True): return True
    for phrase in CRITICAL_EMERGENCY_PHRASES_HI + CRITICAL_EMERGENCY_PHRASES_MR:
        if phrase in original: return True
    return False

_INFO_STARTERS = ("can ","could ","does ","do ","did ","is ","are ","will ","would ","should ","what ","which ","how ","why ","when ")
_INFO_KEYWORDS = (" cause"," causes"," mean"," means"," lead to"," symptom"," symptoms"," sign"," signs"," treatment"," treat"," prevent"," prevention"," avoid"," cure"," contagious")
def is_informational_question(query):
    q = (query or "").strip().lower()
    return q.startswith(_INFO_STARTERS) and any(k in q for k in _INFO_KEYWORDS)

def is_seasonal_prevention_query(query):
    q = (query or "").strip().lower()
    keywords = ["prevent seasonal","seasonal disease","seasonal illness","monsoon disease","seasonal prevention","protect from seasonal","avoid seasonal","prevent monsoon","मौसमी बीमारी","मौसमी बीमारियों","बरसात की बीमारी","बचाव के उपाय","पावसाळी आजार","हंगामी आजार","पावसाळ्यातील रोग","आजारांपासून बचाव"]
    return any(k in q for k in keywords)


# --- STRUCTURED INTENT ENUM (13 fixed intents) ---
INTENT_SYMPTOM_CHECK = "SYMPTOM_CHECK"
INTENT_EMERGENCY = "EMERGENCY"
INTENT_CHILD_HEALTH = "CHILD_HEALTH"
INTENT_PREGNANCY = "PREGNANCY"
INTENT_VACCINATION = "VACCINATION"
INTENT_FACILITY_SEARCH = "FACILITY_SEARCH"
INTENT_SCHEME_INFORMATION = "SCHEME_INFORMATION"
INTENT_MEDICINE_INFORMATION = "MEDICINE_INFORMATION"
INTENT_TELEMEDICINE = "TELEMEDICINE"
INTENT_ABHA = "ABHA"
INTENT_HELPLINE = "HELPLINE"
INTENT_HEALTH_PROGRAM = "HEALTH_PROGRAM"
INTENT_GENERAL_HEALTH = "GENERAL_HEALTH"

# Legacy aliases for backward compatibility with existing module routing
INTENT_HEALTH_QUERY = INTENT_SYMPTOM_CHECK
INTENT_FACILITY = INTENT_FACILITY_SEARCH
INTENT_SCHEME = INTENT_SCHEME_INFORMATION
INTENT_MATERNAL_CHILD = INTENT_PREGNANCY
INTENT_MEDICINE = INTENT_MEDICINE_INFORMATION
INTENT_DIGITAL_HEALTH = INTENT_ABHA
INTENT_GENERAL = INTENT_GENERAL_HEALTH

# --- CANONICAL INTENT TAXONOMY (15 intents per user spec) ---
# These are the PRIMARY intent codes. The router maps queries to these.
INTENT_IMMUNIZATION_FACILITY_SEARCH = "IMMUNIZATION_FACILITY_SEARCH"
INTENT_MATERNITY_FACILITY_SEARCH = "MATERNITY_FACILITY_SEARCH"
INTENT_PEDIATRIC_FACILITY_SEARCH = "PEDIATRIC_FACILITY_SEARCH"
INTENT_GENERAL_OPD_SEARCH = "GENERAL_OPD_SEARCH"
INTENT_IMMUNIZATION_INFORMATION = "IMMUNIZATION_INFORMATION"
INTENT_VACCINATION_SCHEDULE = "VACCINATION_SCHEDULE"
INTENT_VACCINATION_CAMP_INFORMATION = "VACCINATION_CAMP_INFORMATION"

# Canonical intent → module/routing intent mapping
# The 15 canonical intents all map to one of the13 routing intents
_CANONICAL_TO_ROUTING = {
    INTENT_IMMUNIZATION_FACILITY_SEARCH: INTENT_FACILITY_SEARCH,
    INTENT_MATERNITY_FACILITY_SEARCH: INTENT_FACILITY_SEARCH,
    INTENT_PEDIATRIC_FACILITY_SEARCH: INTENT_FACILITY_SEARCH,
    INTENT_GENERAL_OPD_SEARCH: INTENT_FACILITY_SEARCH,
    INTENT_IMMUNIZATION_INFORMATION: INTENT_VACCINATION,
    INTENT_VACCINATION_SCHEDULE: INTENT_VACCINATION,
    INTENT_VACCINATION_CAMP_INFORMATION: INTENT_HEALTH_PROGRAM,
}

VALID_INTENTS = frozenset([
    INTENT_SYMPTOM_CHECK, INTENT_EMERGENCY, INTENT_CHILD_HEALTH,
    INTENT_PREGNANCY, INTENT_VACCINATION, INTENT_FACILITY_SEARCH,
    INTENT_SCHEME_INFORMATION, INTENT_MEDICINE_INFORMATION,
    INTENT_TELEMEDICINE, INTENT_ABHA, INTENT_HELPLINE,
    INTENT_HEALTH_PROGRAM, INTENT_GENERAL_HEALTH,
    # Canonical sub-intents
    INTENT_IMMUNIZATION_FACILITY_SEARCH, INTENT_MATERNITY_FACILITY_SEARCH,
    INTENT_PEDIATRIC_FACILITY_SEARCH, INTENT_GENERAL_OPD_SEARCH,
    INTENT_IMMUNIZATION_INFORMATION, INTENT_VACCINATION_SCHEDULE,
    INTENT_VACCINATION_CAMP_INFORMATION,
])

# --- CARE LEVELS ---
CARE_EMERGENCY = "EMERGENCY"
CARE_URGENT = "URGENT"
CARE_PROMPT_REVIEW = "PROMPT_CLINICAL_REVIEW"
CARE_ROUTINE_PHC = "ROUTINE_PHC"
CARE_SELF_CARE = "SELF_CARE_AND_MONITOR"
CARE_INFO_ONLY = "INFORMATION_ONLY"

# --- ENTITY EXTRACTION ---
def extract_entities(query_en, original_query):
    """Extract age, duration, pregnancy context, location, severity from user query."""
    q = (query_en or "").lower().strip()
    orig = (original_query or "").lower().strip()
    combined = q + " " + orig
    entities = {}

    # Age extraction
    age_patterns = [
        (r"(\d+)\s*(?:year|yr|saal|varsh|sal)s?\s*(?:old)?", "years"),
        (r"(\d+)\s*(?:month|mahina|mahine|masik)s?", "months"),
        (r"(\d+)\s*(?:week|hafta|athvadya)s?", "weeks"),
        (r"(?:age|umar|vay)\s*(\d+)", "years"),
        (r"(\d+)\s*(?:yr|y)\b", "years"),
    ]
    for pat, unit in age_patterns:
        m = re.search(pat, combined)
        if m:
            val = m.group(1)
            entities["age"] = int(val)
            entities["age_unit"] = unit
            if val in ("0","1","2","3","4","5") and unit in ("years","months"):
                entities["age_group"] = "child"
            break

    # Child/baby/infant keywords — supports EN/HI/MR/romanized
    if any(k in combined for k in ["child","baby","infant","newborn","baccha","bachcha","bachche","bacche","bchcha","bachchi","bachchon",
                                     "mulga","mulgi","mulala","mulilaa","mula","mulya","mulansathi","baal","balak","shishu","navajat",
                                     "बच्चा","बाळ",
                                     "शिशु","नवजात",
                                     "मुलाला","मुलीला","मुलां","बाळाला","बाळाचा","बाळाची","बाळां"]):
        entities.setdefault("age_group", "child")

    # Elderly keywords
    if any(k in combined for k in ["elderly","old age","buzurg","vruddha","वृद्ध"]):
        entities["age_group"] = "elderly"

    # Duration extraction
    dur_patterns = [
        (r"(\d+)\s*(?:day|din)s?", "days"),
        (r"(\d+)\s*(?:week|hafta|athvadya)s?", "weeks"),
        (r"(\d+)\s*(?:month|mahina|mahine)s?", "months"),
        (r"(\d+)\s*(?:hour|ghanta|takas?)s?", "hours"),
        (r"(?:since|from|se|pasun)\s*(\d+)\s*(?:day|din)", "days"),
    ]
    for pat, unit in dur_patterns:
        m = re.search(pat, combined)
        if m:
            entities["duration"] = int(m.group(1))
            entities["duration_unit"] = unit
            break

    # Pregnancy context
    if any(k in combined for k in ["pregnant","pregnancy","garbhvati","garbhavati",
                                     "गर्भवती",
                                     "गरोदर",
                                     "गर्भ"]):
        entities["is_pregnant"] = True

    # Pregnancy week
    pw = re.search(r"(\d+)\s*(?:week|hafta|athvadya)\s*(?:pregnant|garbhvati)?", combined)
    if pw:
        entities["pregnancy_week"] = int(pw.group(1))

    # Location/district extraction — supports both Latin and Devanagari
    districts = ["nandurbar","gadchiroli","melghat","palghar","yavatmal",
                 "dharni","chikhaldara","jawhar","mokhada","hadgaon","aheri",
                 "bhamragad","shahada","pusad","kasansur","harisal","molgi"]
    for d in districts:
        if d in q or d in orig:
            entities["district"] = d.title()
            break
    # Devanagari district name extraction (when Latin transliteration not found)
    if not entities.get("district"):
        _devanagari_districts = {
            "नंदुरबार": "Nandurbar", "नंदुरबारमध्ये": "Nandurbar",
            "गडचिरोली": "Gadchiroli", "गडचिरोलीमध्ये": "Gadchiroli",
            "मेळघाट": "Melghat", "मेळघाटात": "Melghat",
            "पालघर": "Palghar", "पालघरमध्ये": "Palghat",
            "यवतमाळ": "Yavatmal", "यवतमाळमध्ये": "Yavatmal",
            "धरणी": "Dharni", "चिखलदरा": "Chikhaldara",
            "जव्हार": "Jawhar", "मोखाडा": "Mokhada",
            "शहादा": "Shahada", "पुसद": "Pusad",
            "अहेरी": "Aheri", "भामरगड": "Bhamragad",
            "हरिसळ": "Harisal", "मोळगी": "Molgi",
        }
        for dev_key, dist_name in _devanagari_districts.items():
            if dev_key in orig or dev_key in q:
                entities["district"] = dist_name
                break

    # Severity indicators
    if any(k in combined for k in ["severe","bahut","khup","bahot","zyada","tez","tivr",
                                     "bahut zyada","very bad","worst","intense","acute",
                                     "तीव्र","खूब"]):
        entities["severity_hint"] = "severe"
    elif any(k in combined for k in ["mild","halka","halke","thoda","slight","minor"]):
        entities["severity_hint"] = "mild"

    # Proximity / "nearest" detection
    _proximity_words = ["nearest", "near me", "nearby", "closest", "mere paas", "paas wala",
                        "sabse kareeb", "kareebi", "closest government",
                        "जवळचे", "जवळचा",
                        "नजीक", "सबसे जवळ"]
    if any(k in combined for k in _proximity_words):
        entities["proximity_request"] = True

    # "Government" facility request detection
    _govt_words = ["government", "sarkari", "sarkaari", "government hospital", "government facility",
                   "government centre", "government center", "sarkari hospital", "sarkari facility",
                   "सरकारी", "शासकीय"]
    if any(k in combined for k in _govt_words):
        entities["wants_government"] = True

    # Multi-symptom detection
    symptom_words = ["fever","pain","cough","cold","headache","vomiting","diarrhea",
                     "rash","weakness","fatigue","dizzy","nausea","bleeding","swelling",
                     "bukhar","dard","khansi","sardardi","ulti","dast","kamzori",
                     "ताप","दुखणे",
                     "खोकला","डोकेदुखी"]
    found_symptoms = [s for s in symptom_words if s in combined]
    if len(found_symptoms) >= 3:
        entities["multi_symptom"] = True

    return entities


# --- STRUCTURED ROUTING OBJECT ---
def build_routing_object(response_lang, intent, secondary_intent, entities, urgency, confidence, next_action, matched_facilities=None):
    """Build a validated JSON routing object. All fields present, null for unknown."""
    obj = {
        "language": response_lang or "en",
        "intent": intent if intent in VALID_INTENTS else INTENT_GENERAL_HEALTH,
        "patient_type": entities.get("patient_type"),
        "symptoms": entities.get("symptoms", []),
        "duration": (str(entities.get("duration","")) + " " + entities.get("duration_unit","")).strip() if entities.get("duration") else None,
        "severity": entities.get("severity_hint"),
        "pregnancy_status": "pregnant" if entities.get("is_pregnant") else None,
        "gestational_stage": str(entities["pregnancy_week"]) + " weeks" if entities.get("pregnancy_week") else None,
        "child_context": entities.get("age_group") == "child",
        "location": entities.get("district"),
        "district": entities.get("district"),
        "facility_type": entities.get("facility_type"),
        "required_service": entities.get("required_service"),
        "scheme_name": entities.get("scheme_name"),
        "medicine_name": entities.get("medicine_name"),
        "urgency": urgency,
        "confidence": round(confidence, 2),
        "next_action": next_action,
    }
    if matched_facilities:
        obj["matched_facility_count"] = len(matched_facilities)
    return obj


def _extract_symptoms_list(combined):
    """Extract symptom keywords found in the query."""
    symptom_map = {
        "fever": "fever", "bukhar": "fever", "ताप": "fever",
        "pain": "pain", "dard": "pain", "दुखण": "pain",
        "cough": "cough", "khansi": "cough", "खोकला": "cough",
        "cold": "cold", "sardi": "cold", "सर्दी": "cold",
        "headache": "headache", "sir dard": "headache", "दुखण": "headache",
        "vomiting": "vomiting", "ulti": "vomiting", "उल्टी": "vomiting",
        "diarrhea": "diarrhea", "dast": "diarrhea", "दस्त": "diarrhea",
        "rash": "rash", "weakness": "weakness", "kamzori": "weakness",
        "fatigue": "fatigue", "dizzy": "dizziness", "nausea": "nausea",
        "bleeding": "bleeding", "swelling": "swelling", "breathing": "breathing difficulty",
        "chest pain": "chest pain", "seene mein dard": "chest pain",
    }
    found = []
    for keyword, symptom in symptom_map.items():
        if keyword in combined and symptom not in found:
            found.append(symptom)
    return found


def classify_urgency(intent, entities, is_red_flag, is_critical):
    """Safety-first urgency classification. Runs before normal guidance."""
    if is_critical or is_red_flag or intent == INTENT_EMERGENCY:
        return "EMERGENCY"
    sev = entities.get("severity_hint")
    dur = entities.get("duration", 0)
    dur_unit = entities.get("duration_unit", "days")
    is_child = entities.get("age_group") == "child"
    is_pregnant = entities.get("is_pregnant", False)
    multi = entities.get("multi_symptom", False)

    if sev == "severe" or (is_pregnant and dur and dur >= 1):
        return "URGENT"
    if multi or (dur and dur_unit == "days" and dur >= 3) or (is_child and dur and dur >= 2):
        return "URGENT"
    if intent in (INTENT_SYMPTOM_CHECK, INTENT_CHILD_HEALTH):
        return "ROUTINE"
    return "INFORMATIONAL"


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


def assess_care_level(intent, entities, best_score, has_red_flags_result, is_critical):
    """Determine care level. NOT a diagnosis - only a healthcare access recommendation."""
    if has_red_flags_result or is_critical:
        return CARE_EMERGENCY
    if intent == INTENT_EMERGENCY:
        return CARE_EMERGENCY

    sev = entities.get("severity_hint")
    multi = entities.get("multi_symptom")
    dur = entities.get("duration", 0)
    dur_unit = entities.get("duration_unit", "days")
    is_child = entities.get("age_group") == "child"
    is_pregnant = entities.get("is_pregnant", False)

    if sev == "severe" or (is_pregnant and dur and dur >= 1):
        return CARE_URGENT
    if best_score >= 0.55 and (multi or (dur and dur_unit == "days" and dur >= 3) or is_child):
        return CARE_PROMPT_REVIEW
    if best_score >= 0.48:
        return CARE_ROUTINE_PHC
    if best_score >= 0.30:
        return CARE_SELF_CARE
    return CARE_INFO_ONLY


def build_structured_response(row, entities, care_level, response_lang, alternatives=None):
    """Build a structured, action-oriented health response."""
    disease = str(row.get("disease", "Unknown"))
    symptoms = str(row.get("symptoms", ""))
    prevention = str(row.get("prevention", ""))
    when_to_see = str(row.get("when_to_see_doctor", ""))
    home_care = str(row.get("home_care", ""))
    severity = str(row.get("severity", "N/A"))
    recommended_facility = str(row.get("recommended_facility", "PHC"))

    if "hospital" in recommended_facility.lower() or "district" in recommended_facility.lower():
        fac_type = "DH"
    elif "sdh" in recommended_facility.lower() or "sub-district" in recommended_facility.lower():
        fac_type = "SDH"
    elif "chc" in recommended_facility.lower() or "community" in recommended_facility.lower():
        fac_type = "CHC"
    else:
        fac_type = "PHC"

    context_parts = []
    if entities.get("age_group") == "child":
        context_parts.append("child" if response_lang == "en" else ("बच्चा" if response_lang == "hi" else "बाळ"))
    if entities.get("age"):
        context_parts.append(f"{entities['age']} {entities.get('age_unit','years')}")
    if entities.get("duration"):
        context_parts.append(f"{entities['duration']} {entities.get('duration_unit','days')}")
    if entities.get("is_pregnant"):
        context_parts.append("pregnant" if response_lang == "en" else ("गर्भवती" if response_lang == "hi" else "गरोदर"))
    context_str = ", ".join(context_parts) if context_parts else ""

    care_labels = {
        CARE_EMERGENCY: ("\U0001f6a8 EMERGENCY", "\U0001f6a8 आपातकाल", "\U0001f6a8 आणीबाणी"),
        CARE_URGENT: ("\u26a0\ufe0f URGENT", "\u26a0\ufe0f अतित्रिक्त", "\u26a0\ufe0f त्वरिक्त"),
        CARE_PROMPT_REVIEW: ("\U0001f7e1 PROMPT REVIEW ADVISED", "\U0001f7e1 शीघ्र देखभाल सूचित", "\U0001f7e1 लवकाळ तपासणी आवश्यक"),
        CARE_ROUTINE_PHC: ("\U0001f7e2 ROUTINE", "\U0001f7e2 सामान्य", "\U0001f7e2 सामान्य"),
        CARE_SELF_CARE: ("\U0001f7e2 SELF-CARE", "\U0001f7e2 स्वतःकाळजी", "\U0001f7e2 स्वतःकाळजी"),
        CARE_INFO_ONLY: ("\U0001f535 INFORMATION", "\U0001f535 जानकारी", "\U0001f535 माहिती"),
    }
    care_label = care_labels.get(care_level, care_labels[CARE_ROUTINE_PHC])
    cl = care_label[0] if response_lang == "en" else (care_label[1] if response_lang == "hi" else care_label[2])

    parts = []
    parts.append(f'<div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:10px 14px;margin-bottom:10px;font-size:0.88rem;"><strong>{cl}</strong></div>')

    desc_label = "YOU DESCRIBED" if response_lang == "en" else ("आपने बताया" if response_lang == "hi" else "तुम्ही साँगिता")
    desc_text = context_str if context_str else ("symptoms described" if response_lang == "en" else ("बताए गए लक्षण" if response_lang == "hi" else "साँगिलेले लक्षणे"))
    parts.append(f'<div style="margin-bottom:8px;"><strong style="color:#475569;font-size:0.82rem;">{desc_label}:</strong> <span style="color:#0F172A;">{html.escape(desc_text)}</span></div>')

    gen_label = "GENERAL AWARENESS" if response_lang == "en" else ("सामान्य जानकारी" if response_lang == "hi" else "सामान्य माहिती")
    disclaimer = "This information is for general awareness and does not confirm a diagnosis." if response_lang == "en" else ("यह जानकारी सामान्य जानकारी के लिए है, निदान नहीं है।" if response_lang == "hi" else "ही माहिती सामान्य जाण्यासाठी आहे, निदान नऺही।")
    parts.append(f'<div style="margin-bottom:8px;"><strong style="color:#475569;font-size:0.82rem;">{gen_label}:</strong> <span style="color:#64748B;font-size:0.88rem;font-style:italic;">{disclaimer}</span></div>')

    if home_care and home_care != "nan" and home_care.strip():
        do_label = "WHAT YOU CAN DO" if response_lang == "en" else ("आप क्या कर सकते हैं" if response_lang == "hi" else "तुम्ही काय करू शकता")
        parts.append(f'<div style="background:#F0FDF4;border:1px solid #86EFAC;border-radius:8px;padding:10px 14px;margin-bottom:8px;"><strong style="color:#16794C;font-size:0.82rem;">{do_label}:</strong><br><span style="font-size:0.88rem;color:#334155;">{home_care}</span></div>')

    if when_to_see and when_to_see != "nan" and when_to_see.strip():
        warn_label = "SEEK MEDICAL HELP IF" if response_lang == "en" else ("डॉक्टर को दिखाएं यदि" if response_lang == "hi" else "डॉक्टराका दिसावा")
        parts.append(f'<div style="background:#FEF3C7;border:1px solid #FDE68A;border-radius:8px;padding:10px 14px;margin-bottom:8px;"><strong style="color:#92400E;font-size:0.82rem;">{warn_label}:</strong><br><span style="font-size:0.88rem;color:#334155;">{when_to_see}</span></div>')

    if alternatives:
        alt_label = "Other possibilities" if response_lang == "en" else ("अन्य संभावना" if response_lang == "hi" else "इतर संभऺ्यवाणे")
        alt_str = ", ".join(alternatives[:2])
        parts.append(f'<div style="font-size:0.82rem;color:#64748B;margin-bottom:8px;"><strong>{alt_label}:</strong> {alt_str}</div>')

    return "".join(parts)


def build_clarifying_question(entities, intent, response_lang):
    """Ask only high-value clarifying questions. Max 1-2 at a time.
    Handles both legacy and canonical intents."""
    questions = []
    # Map canonical intents to legacy for district check
    _facility_intents = (INTENT_FACILITY, INTENT_FACILITY_SEARCH,
                         INTENT_IMMUNIZATION_FACILITY_SEARCH, INTENT_MATERNITY_FACILITY_SEARCH,
                         INTENT_PEDIATRIC_FACILITY_SEARCH, INTENT_GENERAL_OPD_SEARCH)
    if intent in _facility_intents and not entities.get("district"):
        if response_lang == "hi": questions.append("आप किस जिले में हैं?")
        elif response_lang == "mr": questions.append("तुम्ही कोणत्या जिल्ह्यात आहात?")
        else: questions.append("Which district are you in?")
        return questions
    if intent == INTENT_HEALTH_QUERY:
        if entities.get("age_group") == "child" and not entities.get("age"):
            if response_lang == "hi": questions.append("बच्चे की उम्र क्या है?")
            elif response_lang == "mr": questions.append("बाळाची वय कय आहे?")
            else: questions.append("How old is the child?")
        if not entities.get("duration") and not entities.get("age_group"):
            if response_lang == "hi": questions.append("यह कब से हो रहा है?")
            elif response_lang == "mr": questions.append("हे कयती दिवसापासून होत आहे?")
            else: questions.append("How long has this been happening?")
    return questions[:2]


def classify_intent(query_en, original_query):
    """Semantic intent classifier with 15 canonical intents.
    Returns (primary_intent, secondary_intent_or_None, confidence).
    Separates INTENT (action) from TOPIC (healthcare domain).
    Never invents intent names outside VALID_INTENTS."""
    q = (query_en or "").lower().strip()
    orig = (original_query or "").lower().strip()
    combined = q + " " + orig

    # --- EMERGENCY: highest priority, always runs first ---
    romanized_emergency = ["seene mein dard","chest pain","saans lene mein","saans nahi",
                           "behosh","bekhabar","bahut dard","tez dard","emergency help",
                           "need emergency","blood aa raha","khun aa raha","dil ka attack",
                           "heart attack","stroke","fits aa rahe","seizure",
                           "difficulty breathing","severe breathing","unconscious",
                           "severe chest pain","heavy bleeding","convulsions"]
    is_romanized_emerg = any(p in combined for p in romanized_emergency)
    if has_red_flags(original_query, query_en) or is_critical_emergency(original_query, query_en) or is_romanized_emerg:
        mat_kw = ["pregnant","pregnancy","bleeding","contraction","labor","labour","maternal",
                   "गरोदर","प्रसूती","रक्तस्त्राव","गर्भ"]
        if any(k in q or k in orig for k in mat_kw):
            return INTENT_EMERGENCY, INTENT_PREGNANCY, 0.95
        child_kw_emerg = ["child","baby","infant","bachcha","bachche","bacche","mulga","shishu","navajat",
                     "बच्चा","बच्चे","बच्चों","बाळ","शिशु","नवजात"]
        if any(k in q or k in orig for k in child_kw_emerg):
            return INTENT_EMERGENCY, INTENT_CHILD_HEALTH, 0.95
        return INTENT_EMERGENCY, None, 0.95

    # Pregnancy + danger signs = emergency
    if any(k in q or k in orig for k in ["pregnant","pregnancy","गरोदर","गर्भ"]):
        if any(k in q or k in orig for k in ["bleeding","severe pain","fits","convulsion","unconscious",
                                               "रक्तस्त्राव","फिट","बेहोश"]):
            return INTENT_EMERGENCY, INTENT_PREGNANCY, 0.95

    # --- TELEMEDICINE ---
    if any(k in combined for k in ["telemedicine","esanjeevani","e-sanjeevani","online doctor",
                                     "consult doctor","टेलीमेडिसिन"]):
        return INTENT_TELEMEDICINE, None, 0.90

    # --- HELPLINE ---
    if any(k in combined for k in ["asha","anm","community worker","helpline",
                                     "आशा","एनएम"]):
        return INTENT_HELPLINE, None, 0.85

    # --- SEMANTIC VACCINATION/IMMUNIZATION ROUTING ---
    _has_topic_vaccination = any(k in combined for k in [
        "vaccination","immunization","vaccine","vaccinate","vaccinated","booster",
        "teeka","tika","tice","lasikaran","tikakaran",
        "टीका","टीकाकरण","लसीकरण","वैक्सीनेशन","वॅक्सिनेशन","लस",
        "प्रतिरोधक","मिशन इंद्रधनुष","mission indradhanush",
    ])
    # Negation check: "vaccination nahi" = user is NOT asking about vaccination
    _has_vax_negation = False
    if _has_topic_vaccination:
        _vax_neg_patterns = ["nahi","nahin","nahi hai","nahi chahiye","not needed","not required","nako","नको","नहीं"]
        _has_vax_negation = any(neg in combined for neg in _vax_neg_patterns)
        # Only apply negation if there's no facility-seeking intent
        if _has_vax_negation and not is_facility_seeking_query(combined):
            _has_topic_vaccination = False  # Override: treat as non-vaccination query

    if _has_topic_vaccination:
        _is_info = is_informational_query(combined)
        _is_sched = is_schedule_query(combined)
        _has_hospital = any(k in combined for k in [
            "hospital","phc","chc","clinic","center","centre","facility",
            "केंद्र","सेंटर","रुग्णालय","अस्पताल",
        ])
        _is_fac = _has_hospital or any(k in combined for k in [
            "where can","where to","nearest","near me","kahan","kidhar","kaha",
            "find","dhundo","dikhao facility","facility batao","hospital batao",
            "center batao","centre batao","kutra","kuthe","lagega","lagna",
            "chahiye","chahiyen","chahiyan","lagwana","lagwayein","lagwaya","karani","karani hai","karana hai","karwana","karwaun","karwana hai",
            "कहाँ","कुठे","साँगवा","साँगवे","जवळचे","जवळचा",
            "हवे","हवं","हवेतो","लागेल","लागतो",
        ])
        _has_camp = any(k in combined for k in ["camp","शिबिर","camp"])

        # Case A: CAMP query — highest specificity
        if _has_camp:
            if _is_sched or _is_info:
                return INTENT_VACCINATION_CAMP_INFORMATION, None, 0.90
            if _is_fac or _has_hospital:
                return INTENT_IMMUNIZATION_FACILITY_SEARCH, None, 0.92
            return INTENT_VACCINATION_CAMP_INFORMATION, None, 0.85

        # Case B: SCHEDULE query
        if _is_sched and not _is_fac and not _has_hospital:
            return INTENT_VACCINATION_SCHEDULE, None, 0.88

        # Case C: INFORMATION query — strong info signals override facility signals
        _strong_info = any(k in combined for k in [
            "ke baare mein","ke bare mein","about","tell me about",
            "के बारे में","बद्दल","माहिती",
        ])
        if _strong_info:
            return INTENT_IMMUNIZATION_INFORMATION, None, 0.85
        if _is_info and not _has_hospital and not _is_fac:
            return INTENT_IMMUNIZATION_INFORMATION, None, 0.85

        # Case D: Pure info-like without facility signal
        _info_only = any(k in combined for k in [
            "ke baare mein","ke bare mein","kya hai","kya hota","information",
            "jankari","jaankari","about","tell me about","what is",
            "के बारे में","क्या है","जानकारी","समजाणे",
            "samjha","samjhao",
        ])
        if _info_only and not _has_hospital and not _is_fac:
            return INTENT_IMMUNIZATION_INFORMATION, None, 0.85

        # Case E: User wants to FIND a vaccination facility
        if _is_fac or _has_hospital:
            return INTENT_IMMUNIZATION_FACILITY_SEARCH, INTENT_VACCINATION, 0.92

        # Case F: Ambiguous — default to information
        return INTENT_IMMUNIZATION_INFORMATION, None, 0.78

    # --- SEMANTIC PREGNANCY/MATERNITY ROUTING ---
    _has_topic_pregnancy = any(k in combined for k in [
        "pregnant","pregnancy","maternity","delivery","anc","prenatal",
        "garbhvati","garbhavati","prasuti","garbhotpadan",
        "गर्भवती","गरोदर","प्रसूती","गर्भ",
    ])
    # Pregnancy negation: "maternity service nahi" = skip pregnancy routing
    if _has_topic_pregnancy:
        _preg_neg_patterns = ["nahi","nahin","not needed","not required","nako","नको","नहीं"]
        _has_preg_negation = any(neg in combined for neg in _preg_neg_patterns)
        if _has_preg_negation:
            # If user explicitly asks for "general"/"OPD" alongside negation, skip pregnancy
            _wants_general = any(k in combined for k in ["general","opd","सामान्य"])
            if _wants_general or not is_facility_seeking_query(combined):
                _has_topic_pregnancy = False

    if _has_topic_pregnancy:
        # Strong info signals override facility
        _strong_preg_info = any(k in combined for k in [
            "kya khana","kya kare","kya hota","ke bare mein","ke baare mein",
            "information","jankari","diet","food","khaana","khana",
            "क्या खाना","क्या करें","जानकारी","आहार",
        ])
        if not _strong_preg_info:
            _is_fac = is_facility_seeking_query(combined)
            _has_hospital = any(k in combined for k in [
                "hospital","phc","chc","clinic","center","centre","facility",
                "केंद्र","सेंटर","रुग्णालय","अस्पताल",
            ])
            if _is_fac or _has_hospital:
                return INTENT_MATERNITY_FACILITY_SEARCH, INTENT_PREGNANCY, 0.92
        return INTENT_PREGNANCY, None, 0.80

    # --- SEMANTIC CHILD HEALTH ROUTING ---
    _has_topic_child = any(k in combined for k in [
        "child","baby","infant","newborn","baccha","bachcha","bachche","bacche","bchcha","bachchi","bachchon",
        "mulga","mulgi","baal","balak","shishu","navajat","pediatric","paediatric",
        "बच्चा","बच्चे","बच्चों","बच्ची","बाळ","शिशु","नवजात",
    ])
    if _has_topic_child:
        # CRITICAL: Check explicit pediatric keywords FIRST
        _has_explicit_pediatric = any(k in combined for k in [
            "pediatric","paediatric","pediatrician","child specialist",
            "child doctor","बाल रोग","बालरोग","बाल रोग विशेषज्ञ",
            "children doctor","bachchon ka doctor","bacche ka doctor",
        ])
        _is_fac = is_facility_seeking_query(combined)
        _has_hospital = any(k in combined for k in [
            "hospital","phc","chc","clinic","center","centre","facility",
            "केंद्र","सेंटर","रुग्णालय","अस्पताल","डॉक्टर",
        ])

        # Explicit pediatric → PEDIATRIC_FACILITY_SEARCH
        if _has_explicit_pediatric:
            if _is_fac or _has_hospital:
                return INTENT_PEDIATRIC_FACILITY_SEARCH, None, 0.92
            return INTENT_PEDIATRIC_FACILITY_SEARCH, None, 0.85

        # Child + facility (no explicit pediatric) → pediatric facility search
        # Because the user is asking about a child's healthcare facility
        if _is_fac or _has_hospital:
            return INTENT_PEDIATRIC_FACILITY_SEARCH, None, 0.88

        # Has symptoms + child → symptom check
        symptom_words = ["fever","bukhar","cough","cold","pain","dard","vomiting","rash",
                         "breathing","saans","ताप","दुखणे"]
        if any(k in combined for k in symptom_words):
            return INTENT_SYMPTOM_CHECK, INTENT_CHILD_HEALTH, 0.75

        return INTENT_CHILD_HEALTH, None, 0.75

    # --- COMPOUND QUERY DETECTION (scheme + facility) ---
    _has_fac_word = any(k in q or k in orig for k in ["hospital","phc","chc","clinic","अस्पताल","रुग्णालय"])
    _has_sch_word = any(k in q or k in orig for k in ["scheme","yojana","kharcha","cover","insurance",
        "mjpjay","ayushman","pmjay","cashless","benefit","eligibility","free treatment","योजना"])
    if _has_fac_word and _has_sch_word:
        return INTENT_SCHEME_INFORMATION, None, 0.85

    # --- FACILITY_SEARCH (general, not topic-specific above) ---
    fac_long = ["hospital","clinic","nearest hospital","government hospital",
                "hospital list","civil hospital","district hospital","opd",
                "रुग्णालय","अस्पताल","सरकारी अस्पताल","जवळचे"]
    fac_short = ["phc","chc"]
    _fac_match = any(k in q or k in orig for k in fac_long)
    if not _fac_match:
        _words = set(combined.split())
        _fac_match = any(k in _words for k in fac_short)
    if _fac_match:
        return INTENT_GENERAL_OPD_SEARCH, None, 0.85

    # --- SCHEME_INFORMATION ---
    sch_kw = ["mjpjay","ayushman","pm-jay","cashless treatment","scheme","yojana",
              "aapla dawakhana","free treatment","insurance","rbsk","jsy","navsanjivan",
              "kharcha","cover","government se cover","benefit","eligibility","yojana ke",
              "योजना","मोफत उपचार","महात्मा फुले","आयुष्मान"]
    if any(k in q or k in orig for k in sch_kw):
        return INTENT_SCHEME_INFORMATION, None, 0.85

    # --- MEDICINE_INFORMATION ---
    med_kw = ["medicine price","jan aushadhi","generic medicine","cheap medicine",
              "medicine","drug","pharmacy","medical store",
              "औषध","जेनेरिक","दवा","दवाई"]
    if any(k in q or k in orig for k in med_kw):
        return INTENT_MEDICINE_INFORMATION, None, 0.85

    # --- ABHA ---
    dig_kw = ["abha","health id","health account","digital health",
              "आरोग्य आयडी","हेल्थ आयडी"]
    if any(k in q or k in orig for k in dig_kw):
        return INTENT_ABHA, None, 0.85

    # --- Default: SYMPTOM_CHECK ---
    return INTENT_SYMPTOM_CHECK, None, 0.60

def care_pathway_html(recommended_facility_type, lang="en"):
    """Append a care-pathway card after any health response."""
    fac_label = {
        "en": {"PHC":"Primary Health Centre (PHC)","CHC":"Community Health Centre (CHC)",
               "SDH":"Sub-District Hospital","DH":"District Hospital",
               "any":"nearest government health facility"},
        "hi": {"PHC":"प्राथमिक स्वास्थ्य केंद्र (PHC)","CHC":"सामुदायिक स्वास्थ्य केंद्र (CHC)",
               "SDH":"उप-जिला अस्पताल","DH":"जिला अस्पताल",
               "any":"निकटतम सरकारी स्वास्थ्य सुविधा"},
        "mr": {"PHC":"प्राथमिक आरोग्य केंद्र (PHC)","CHC":"सामुदायिक आरोग्य केंद्र (CHC)",
               "SDH":"उप-जिल्हा रुग्णालय","DH":"जिल्हा रुग्णालय",
               "any":"जवळची शासकीय आरोग्य सुविधा"}
    }
    ft = recommended_facility_type if recommended_facility_type in fac_label.get(lang, fac_label["en"]) else "any"
    fl = fac_label.get(lang, fac_label["en"]).get(ft, fac_label["en"]["any"])

    if lang == "hi":
        return (
            '<div style="background:#F0FDF4;border:1px solid #86EFAC;border-radius:12px;padding:14px 18px;margin-top:14px;">'
            f'<div style="font-weight:700;color:#16794C;font-size:0.95rem;margin-bottom:6px;">🏥 अगला कदम \u2014 {fl} पर जाएं</div>'
            f'<p style="font-size:0.88rem;color:#334155;margin:0 0 8px;line-height:1.5;">अपने नजदीकी <strong>{fl}</strong> पर जाएं। अपना आधार कार्ड और राशन कार्ड ले जाएं।</p>'
            '<p style="font-size:0.84rem;color:#64748B;margin:0;">\U0001f4de आपातकालीन में <a href="tel:108" style="color:#DC2626;font-weight:700;">108</a> पर कॉल करें | हेल्पलाइन: <a href="tel:104" style="color:#0B6BCB;font-weight:700;">104</a></p>'
            '</div>'
        )
    if lang == "mr":
        return (
            '<div style="background:#F0FDF4;border:1px solid #86EFAC;border-radius:12px;padding:14px 18px;margin-top:14px;">'
            f'<div style="font-weight:700;color:#16794C;font-size:0.95rem;margin-bottom:6px;">🏥 पुढचे पाऊल \u2014 {fl} ला जा</div>'
            f'<p style="font-size:0.88rem;color:#334155;margin:0 0 8px;line-height:1.5;">तुमच्या जवळच्या <strong>{fl}</strong> ला जा. आधार कार्ड आणि रेशन कार्ड घेऊन जा.</p>'
            '<p style="font-size:0.84rem;color:#64748B;margin:0;">\U0001f4de आणीबाणीत <a href="tel:108" style="color:#DC2626;font-weight:700;">108</a> वर कॉल करा | हेल्पलाइन: <a href="tel:104" style="color:#0B6BCB;font-weight:700;">104</a></p>'
            '</div>'
        )
    return (
        '<div style="background:#F0FDF4;border:1px solid #86EFAC;border-radius:12px;padding:14px 18px;margin-top:14px;">'
        f'<div style="font-weight:700;color:#16794C;font-size:0.95rem;margin-bottom:6px;">🏥 Next Step \u2014 Visit your {fl}</div>'
        f'<p style="font-size:0.88rem;color:#334155;margin:0 0 8px;line-height:1.5;">Visit your nearest <strong>{fl}</strong>. Carry your Aadhaar card and Ration card.</p>'
        '<p style="font-size:0.84rem;color:#64748B;margin:0;">\U0001f4de In emergency: <a href="tel:108" style="color:#DC2626;font-weight:700;">108</a> | Health helpline: <a href="tel:104" style="color:#0B6BCB;font-weight:700;">104</a></p>'
        '</div>'
    )

CAUTION_NOTE = "⚠️ Your question mentions a symptom that can be serious. Call **108** if experiencing it now.\n\n"
TRANSLATION_FAILED_NOTE = "⚠️ Automatic translation failed — answer shown in English:\n\n"
_GLOBAL_TRANSLATION_CACHE = {}

def emergency_banner_html(lang="en"):
    if lang == "hi":
        return """<div class="th-alert emerg"><div class="th-alert-icon">🚨</div><div class="th-alert-body"><h4>आपातकालीन स्थिति — तुरंत चिकित्सीय सहायता लें</h4><p>आपके संदेश में ऐसे लक्षण हैं जिन पर <strong>तत्काल चिकित्सा ध्यान</strong> की आवश्यकता है। तुरंत निकटतम अस्पताल जाएं।</p><div class="th-emerg-actions"><a href="tel:108" class="th-emerg-btn">🚑 एम्बुलेंस (MEMS): 108</a><a href="tel:104" class="th-emerg-btn-sub">🏥 आरोग्य हेल्पलाइन: 104</a><a href="tel:102" class="th-emerg-btn-sub">🤰 जननी एक्सप्रेस: 102</a></div></div></div>"""
    if lang == "mr":
        return """<div class="th-alert emerg"><div class="th-alert-icon">🚨</div><div class="th-alert-body"><h4>तात्काळ वैद्यकीय मदत घ्या — आणीबाणी</h4><p>तुमच्या लक्षणांवरून <strong>तातडीने वैद्यकीय उपचारांची</strong> गरज आहे. जवळच्या सरकारी रुग्णालयात जा.</p><div class="th-emerg-actions"><a href="tel:108" class="th-emerg-btn">🚑 रुग्णवाहिका (MEMS): 108</a><a href="tel:104" class="th-emerg-btn-sub">🏥 आरोग्य सल्ला: 104</a><a href="tel:102" class="th-emerg-btn-sub">🤰 जननी एक्सप्रेस: 102</a></div></div></div>"""
    return """<div class="th-alert emerg"><div class="th-alert-icon">🚨</div><div class="th-alert-body"><h4>Emergency — Seek Immediate Medical Help</h4><p>Your message mentions symptoms that may need <strong>urgent attention</strong>. Proceed to the nearest hospital immediately.</p><div class="th-emerg-actions"><a href="tel:108" class="th-emerg-btn">🚑 Ambulance (MEMS): 108</a><a href="tel:104" class="th-emerg-btn-sub">🏥 MH Health Line: 104</a><a href="tel:102" class="th-emerg-btn-sub">🤰 Janani Express: 102</a></div></div></div>"""

def caution_banner_html(lang="en"):
    if lang == "hi": return '<div class="th-alert caution"><div class="th-alert-icon">⚠️</div><div class="th-alert-body"><h4>महत्वपूर्ण सावधानी</h4><p>यदि लक्षण गंभीर हैं, तुरंत <strong>108</strong> पर कॉल करें।</p></div></div>'
    if lang == "mr": return '<div class="th-alert caution"><div class="th-alert-icon">⚠️</div><div class="th-alert-body"><h4>महत्त्वाची काळजी घ्या</h4><p>त्रास होत असल्यास त्वरित <strong>108</strong> ला कॉल करा.</p></div></div>'
    return '<div class="th-alert caution"><div class="th-alert-icon">⚠️</div><div class="th-alert-body"><h4>Important Caution</h4><p>If experiencing serious symptoms, call <strong>108</strong> immediately.</p></div></div>'

def tokenize(text):
    text = re.sub(r"[^a-z0-9\s]", " ", normalize_for_match(_merge_compound_aches(text)))
    return {_stem_word(w) for w in text.split() if w not in STOPWORDS and len(w) > 2}

def phrase_hits(query_text, phrase, strict=False):
    phrase = (phrase or "").strip().lower()
    if len(phrase) < 3: return False
    if phrase in (query_text or "").lower(): return True
    p_tokens, q_tokens = tokenize(phrase), tokenize(query_text)
    if not p_tokens: return False
    if not strict: return p_tokens.issubset(q_tokens)
    overlap = p_tokens & q_tokens
    if not overlap: return False
    if len(p_tokens) <= 2: return overlap == p_tokens
    return len(overlap) / len(p_tokens) >= 0.75

def keyword_bonus(query_text, row):
    bonus = 0.0
    disease = str(row["disease"])
    short_name = disease.split("(")[0].strip().lower()
    q = (query_text or "").lower()
    if short_name and short_name in q: bonus += 0.28
    elif any(p.strip().lower() in q for p in re.split(r"[()/,]", disease) if len(p.strip()) > 3): bonus += 0.16
    symptom_phrases = [p.strip().lower() for p in str(row["symptoms"]).split(",")]
    extra_phrases = [p.strip().lower() for p in EXTRA_KEYWORDS.get(disease, [])]
    extra_set = set(extra_phrases)
    seen = set()
    for phrase in symptom_phrases + extra_phrases:
        if not phrase or phrase in seen: continue
        seen.add(phrase)
        if not phrase_hits(query_text, phrase): continue
        tokens = tokenize(phrase)
        if not tokens: continue
        if phrase in extra_set: bonus += 0.22
        elif len(tokens) == 1:
            if next(iter(tokens)) in GENERIC_SYMPTOMS_STEMMED: bonus += 0.02
            else: bonus += 0.05
        else: bonus += min(0.22, 0.07 * len(tokens))
    return min(bonus, 0.40)

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

_CARD_I18N = {
    "en": {"badge":"Health Awareness Summary","symptoms":"Common Symptoms","prevention":"Prevention & Protection","home_care":"Home Care Guidance","doctor":"When to See a Doctor","related":"Other conditions to read about","disclaimer":"This is general awareness — not a clinical diagnosis. Always consult a doctor."},
    "hi": {"badge":"स्वास्थ्य जागरूकता","symptoms":"सामान्य लक्षण","prevention":"रोकथाम","home_care":"घरेलू देखभाल","doctor":"डॉक्टर से कब मिलें","related":"अन्य संबंधित स्थितियां","disclaimer":"यह सामान्य जानकारी है, चिकित्सकीय निदान नहीं। डॉक्टर से परामर्श लें।"},
    "mr": {"badge":"आरोग्य जागरूकता","symptoms":"सामान्य लक्षणे","prevention":"प्रतिबंध","home_care":"घरगुती काळजी","doctor":"डॉक्टरांचा सल्ला","related":"इतर संबंधित आजार","disclaimer":"ही सामान्य माहिती आहे, वैद्यकीय निदान नाही. डॉक्टरांचा सल्ला घ्या."},
}

def _severity_badge(row, lang):
    if "severity" not in row or pd.isna(row.get("severity", None)): return ""
    sev = str(row["severity"]).lower().strip()
    return f'<span class="th-meta-pill th-meta-severity-{sev}">{sev.upper()}</span>' if sev in ("mild","moderate","severe","critical") else ""

def _category_badge(row):
    if "category" not in row or pd.isna(row.get("category", None)): return ""
    cat = str(row["category"]).strip()
    return f'<span class="th-meta-pill th-meta-cat">📂 {cat.title()}</span>' if cat else ""

def _free_badge(row, lang):
    if "govt_free_treatment" not in row or pd.isna(row.get("govt_free_treatment", None)): return ""
    v = str(row["govt_free_treatment"]).lower().strip()
    labels = {"en":{"yes":"🎁 FREE at Govt Hospital","partial":"💰 Partially Free"},"hi":{"yes":"🎁 सरकारी अस्पताल में मुफ्त","partial":"💰 आंशिक मुफ्त"},"mr":{"yes":"🎁 शासकीय रुग्णालयात मोफत","partial":"💰 अंशतः मोफत"}}
    if v == "yes": return f'<span class="th-meta-pill th-meta-free">{labels[lang]["yes"]}</span>'
    if v == "partial": return f'<span class="th-meta-pill th-meta-partial">{labels[lang]["partial"]}</span>'
    return ""

def _facility_badge(row, lang):
    if "recommended_facility" not in row or pd.isna(row.get("recommended_facility", None)): return ""
    fac = str(row["recommended_facility"]).strip()
    labels = {"en":"🏥 Best treated at","hi":"🏥 सर्वोत्तम उपचार","mr":"🏥 सर्वोत्तम उपचार"}
    return f'<span class="th-meta-pill th-meta-facility">{labels[lang]}: {fac}</span>' if fac else ""

def format_disease_card_html(row, alternatives=None, lang="en", translated_row=None):
    labels = _CARD_I18N.get(lang, _CARD_I18N["en"])
    data = translated_row if translated_row else row
    disease = html.escape(str(data.get("disease", row.get("disease", ""))))
    meta_pills = _severity_badge(row, lang) + _category_badge(row) + _free_badge(row, lang) + _facility_badge(row, lang)
    meta_strip = f'<div class="th-meta-strip">{meta_pills}</div>' if meta_pills else ""
    def _row(icon, bg, color, label_key, val):
        if not val: return ""
        return f'<div class="th-dx-row"><div class="th-dx-icon-badge" style="background:{bg};color:{color};">{icon}</div><div style="flex:1;"><strong class="th-dx-label" style="color:{color};">{labels.get(label_key, label_key)}</strong><div class="th-dx-content">{html.escape(str(val))}</div></div></div>'
    body = _row("🩹","#EAF2FE","#0B6BCB","symptoms",data.get("symptoms","")) + _row("🛡️","#E6F7F5","#0E9F8F","prevention",data.get("prevention","")) + _row("🏠","#F3EFFE","#6941C6","home_care",data.get("home_care","")) + _row("👨‍⚕️","#FFF8E6","#D97706","doctor",data.get("when_to_see_doctor",""))
    alt_html = ""
    if alternatives:
        chips = " ".join(f'<span class="th-dx-alt-pill">{html.escape(a)}</span>' for a in alternatives)
        alt_html = f'<div class="th-dx-alt-box"><strong>💡 {labels["related"]}:</strong> {chips}</div>'
    return f"""<div class="th-dx-card"><div class="th-dx-header"><div class="th-dx-header-left"><div class="th-dx-header-icon">🩺</div><div><h4 class="th-dx-title">{disease}</h4><span style="font-size:0.75rem;color:#64748B;font-weight:600;">MahaArogya Setu Rural Triage</span></div></div><span class="th-dx-badge">{labels["badge"]}</span></div>{meta_strip}{body}{alt_html}<div class="th-dx-footer"><span>⚕️ {labels["disclaimer"]}</span></div></div>"""

def format_seasonal_prevention_card(lang="en"):
    if lang == "mr":
        return """<div class="th-dx-card"><div class="th-dx-header"><div class="th-dx-header-left"><div class="th-dx-header-icon">🛡️</div><div><h4 class="th-dx-title">हंगामी आणि पावसाळी आजार बचाव मार्गदर्शिका</h4><span style="font-size:0.75rem;color:#64748B;font-weight:600;">महाराष्ट्र सार्वजनिक आरोग्य विभाग</span></div></div><span class="th-dx-badge">प्रतिबंध</span></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#EAF2FE;color:#0B6BCB;">🦟</div><div style="flex:1;"><strong class="th-dx-label" style="color:#0B6BCB;">डासजन्य आजार (डेंग्यू, मलेरिया)</strong><div class="th-dx-content">• घराभोवती पाणी साठू देऊ नका
• मच्छरदाणी वापरा
• पूर्ण बाह्यांचे कपडे घाला</div></div></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#E6F7F5;color:#0E9F8F;">💧</div><div style="flex:1;"><strong class="th-dx-label" style="color:#0E9F8F;">पाण्याने होणारे आजार (कॉलरा, कावीळ)</strong><div class="th-dx-content">• उकळून थंड केलेले पाणी प्या
• जेवणापूर्वी हात धुवा
• रस्त्यावरचे उघडे अन्न टाळा</div></div></div><div class="th-dx-footer"><span>⚕️ गंभीर आजारात नजीकच्या PHC/CHC ला भेट द्या.</span></div></div>"""
    if lang == "hi":
        return """<div class="th-dx-card"><div class="th-dx-header"><div class="th-dx-header-left"><div class="th-dx-header-icon">🛡️</div><div><h4 class="th-dx-title">मौसमी बीमारियों से बचाव</h4><span style="font-size:0.75rem;color:#64748B;font-weight:600;">महाराष्ट्र स्वास्थ्य विभाग</span></div></div><span class="th-dx-badge">रोकथाम</span></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#EAF2FE;color:#0B6BCB;">🦟</div><div style="flex:1;"><strong class="th-dx-label" style="color:#0B6BCB;">मच्छर जनित रोग</strong><div class="th-dx-content">• पानी जमा न होने दें
• मच्छरदानी का प्रयोग करें
• पूरी बाजू के कपड़े पहनें</div></div></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#E6F7F5;color:#0E9F8F;">💧</div><div style="flex:1;"><strong class="th-dx-label" style="color:#0E9F8F;">जल जनित रोग</strong><div class="th-dx-content">• उबला पानी पिएं
• खाने से पहले हाथ धोएं
• बाहर के खाने से बचें</div></div></div><div class="th-dx-footer"><span>⚕️ गंभीर स्थिति में नजदीकी PHC जाएं।</span></div></div>"""
    return """<div class="th-dx-card"><div class="th-dx-header"><div class="th-dx-header-left"><div class="th-dx-header-icon">🛡️</div><div><h4 class="th-dx-title">Seasonal & Monsoon Disease Prevention</h4><span style="font-size:0.75rem;color:#64748B;font-weight:600;">Maharashtra Public Health Advisory</span></div></div><span class="th-dx-badge">Prevention</span></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#EAF2FE;color:#0B6BCB;">🦟</div><div style="flex:1;"><strong class="th-dx-label" style="color:#0B6BCB;">Vector-Borne (Dengue, Malaria)</strong><div class="th-dx-content">• Clear stagnant water around home
• Use insecticide-treated bed nets
• Wear full-sleeved clothes</div></div></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#E6F7F5;color:#0E9F8F;">💧</div><div style="flex:1;"><strong class="th-dx-label" style="color:#0E9F8F;">Water-Borne (Cholera, Jaundice)</strong><div class="th-dx-content">• Drink only boiled/filtered water
• Wash hands before meals
• Avoid roadside cut fruits</div></div></div><div class="th-dx-footer"><span>⚕️ Visit nearest PHC/CHC for serious symptoms.</span></div></div>"""

def format_disease_plain(row):
    text = f"{row['disease']}.\n\nCommon symptoms: {row['symptoms']}.\n\nPrevention: {row['prevention']}.\n\n"
    if row.get("home_care"): text += f"Home care: {row['home_care']}.\n\n"
    text += f"See a doctor if: {row['when_to_see_doctor']}.\n\nGeneral awareness only, not a diagnosis."
    return text

def _looks_like_translation_error(text):
    if not text or not text.strip(): return True
    t = text.strip().lower()
    return any(m in t for m in ("error 5","that's an error","please try again","too many requests","429","internal server","bad gateway","<!doctype","<html")) or (len(t) > 600 and ("<" in t or "google" in t))

def translate_safe(text, source, target):
    if not text or not str(text).strip(): return None
    if source == target: return text
    if st.session_state.get("low_bandwidth", False): return None
    key = (source, target, str(text).strip())
    if key in _GLOBAL_TRANSLATION_CACHE: return _GLOBAL_TRANSLATION_CACHE[key]
    for attempt in range(2):
        try:
            tr = GoogleTranslator(source=source, target=target).translate(str(text).strip())
            if tr and tr.strip() and not _looks_like_translation_error(tr) and tr.strip() != str(text).strip():
                _GLOBAL_TRANSLATION_CACHE[key] = tr.strip()
                return tr.strip()
        except Exception: pass
        if attempt < 1: time.sleep(0.3)
    _GLOBAL_TRANSLATION_CACHE[key] = None
    return None

def translate_row_fields(row, target_lang):
    if target_lang == "en": return row
    translated = {}
    for col in REQUIRED_COLUMNS:
        val = str(row.get(col, "") or "").strip()
        if not val: translated[col] = ""; continue
        tr = translate_safe(val, source="en", target=target_lang)
        translated[col] = tr if tr else val
    return translated

@st.cache_resource(show_spinner=False)
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

def detect_response_lang(query):
    q = (query or "").strip()
    if not q: return "en"
    if re.search(r"[ऀ-ॿ]", q):
        mr_keywords = ["आहे","नाही","त्रास","दुखत","खोकला","ताप","योजना","दवाखाना","रुग्णालय","गरोदर",
            "करावे","माझ्या","मुलाला","मध्ये","लसीकरण","कुठे","शोधा","पाहिजे","दाखवा","सांगा",
            "करतो","करते","होतो","होते","लागला","लागली","झाले","झाला","देऊ","घ्या",
            "आम्ही","तुम्ही","त्याला","तिला","मला","तुला"]
        if any(w in q for w in mr_keywords): return "mr"
        return "hi"
    if is_romanized_hindi(q): return "hi"
    if len(re.findall(r"[a-z]+", q.lower())) <= 3: return "en"
    try:
        lang = detect(q)
        if lang in ("hi","mr"): return lang
    except Exception: pass
    return "en"

# ============================================================================
# INTENT-SPECIFIC RESPONSE RENDERERS
# ============================================================================
def generate_telemedicine_guide(lang="en"):
    if lang == "mr":
        return """<div class="th-dx-card"><div class="th-dx-header"><div class="th-dx-header-left"><div class="th-dx-header-icon">📞</div><div><h4 class="th-dx-title">मोफत टेलिमेडिसिन मार्गदर्शक (ई-संजीवनी)</h4><span style="font-size:0.75rem;color:#64748B;font-weight:600;">घरी बसून डॉक्टरांचा सल्ला — esanjeevani.in किंवा 104 कॉल</span></div></div><span class="th-dx-badge">ONLINE</span></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#EAF2FE;color:#0B6BCB;">1️⃣</div><div style="flex:1;"><strong class="th-dx-label" style="color:#0B6BCB;">ई-संजीवनी OPD</strong><div class="th-dx-content">• 'eSanjeevaniOPD' अ‍ॅप डाऊनलोड करा किंवा <a href="https://esanjeevani.in" target="_blank" style="color:#0B6BCB;font-weight:700;">esanjeevani.in</a> ला भेट द्या
• मोबाईल OTP द्वारे नोंदणी करा
• टोकन घ्या → व्हिडिओ कॉलद्वारे शासकीय डॉक्टरांशी मोफत बोला</div></div></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#E6F7F5;color:#0E9F8F;">2️⃣</div><div style="flex:1;"><strong class="th-dx-label" style="color:#0E9F8F;">१०४ आरोग्य सल्ला हेल्पलाईन</strong><div class="th-dx-content">• थेट <strong>104</strong> डायल करा
• २४ तास मराठीत वैद्यकीय सल्ला
• आवश्यक असल्यास जवळच्या PHC ला रेफरल</div></div></div></div>"""
    if lang == "hi":
        return """<div class="th-dx-card"><div class="th-dx-header"><div class="th-dx-header-left"><div class="th-dx-header-icon">📞</div><div><h4 class="th-dx-title">मुफ्त टेलीमेडिसिन गाइड (eSanjeevani)</h4></div></div><span class="th-dx-badge">ONLINE</span></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#EAF2FE;color:#0B6BCB;">1️⃣</div><div style="flex:1;"><strong class="th-dx-label" style="color:#0B6BCB;">eSanjeevani OPD</strong><div class="th-dx-content">• <a href="https://esanjeevani.in" target="_blank" style="color:#0B6BCB;font-weight:700;">esanjeevani.in</a> पर जाएं या ऐप डाउनलोड करें
• मोबाइल OTP से पंजीकरण करें
• मुफ्त वीडियो कॉल पर डॉक्टर से बात करें</div></div></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#E6F7F5;color:#0E9F8F;">2️⃣</div><div style="flex:1;"><strong class="th-dx-label" style="color:#0E9F8F;">104 स्वास्थ्य हेल्पलाइन</strong><div class="th-dx-content">• 24×7 हिंदी में मुफ्त सलाह
• जरूरत पर PHC को रेफरल</div></div></div></div>"""
    return """<div class="th-dx-card"><div class="th-dx-header"><div class="th-dx-header-left"><div class="th-dx-header-icon">📞</div><div><h4 class="th-dx-title">Government Telemedicine (eSanjeevani)</h4><span style="font-size:0.75rem;color:#64748B;font-weight:600;">Free doctor consultation — visit esanjeevani.in or call 104</span></div></div><span class="th-dx-badge">ONLINE</span></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#EAF2FE;color:#0B6BCB;">1️⃣</div><div style="flex:1;"><strong class="th-dx-label" style="color:#0B6BCB;">eSanjeevani OPD</strong><div class="th-dx-content">• Visit <a href="https://esanjeevani.in" target="_blank" style="color:#0B6BCB;font-weight:700;">esanjeevani.in</a> or install eSanjeevaniOPD app
• Register with mobile OTP → get token
• Free video call with government specialists</div></div></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#E6F7F5;color:#0E9F8F;">2️⃣</div><div style="flex:1;"><strong class="th-dx-label" style="color:#0E9F8F;">104 Health Helpline</strong><div class="th-dx-content">• Dial 104 free from any phone
• 24×7 medical counseling in local languages
• Referral to nearest PHC when needed</div></div></div></div>"""

def generate_maternal_child_module(lang="en"):
    if lang == "mr":
        return """<div class="th-dx-card"><div class="th-dx-header"><div class="th-dx-header-left"><div class="th-dx-header-icon">🤰</div><div><h4 class="th-dx-title">माता व बाल आरोग्य पोर्टल</h4><span style="font-size:0.75rem;color:#64748B;font-weight:600;">शासकीय ANC, लसीकरण, JSY फायदे</span></div></div><span class="th-dx-badge">MCH</span></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#EAF2FE;color:#0B6BCB;">📋</div><div style="flex:1;"><strong class="th-dx-label" style="color:#0B6BCB;">४ मोफत ANC तपासण्या</strong><div class="th-dx-content">• १२ आठवड्यांच्या आत: नोंदणी, फॉलिक ऍसिड
• १४-२६ आठवडे: TT-१ इंजेक्शन, BP
• २८-३४ आठवडे: TT-२, अ‍ॅनिमिया तपासणी
• ३६+ आठवडे: प्रसूती नियोजन, 102 जननी एक्सप्रेस</div></div></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#E6F7F5;color:#0E9F8F;">💉</div><div style="flex:1;"><strong class="th-dx-label" style="color:#0E9F8F;">बाल लसीकरण वेळापत्रक</strong><div class="th-dx-content">• जन्म: BCG, OPV-0, Hep-B
• ६/१०/१४ आठवडे: पेंटाव्हॅलेंट, रोटा, OPV
• ९ महिने: MR-१, व्हिटॅमिन A</div></div></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#FEECEB;color:#DC2626;">🚨</div><div style="flex:1;"><strong class="th-dx-label" style="color:#DC2626;">गरोदरपणातील धोक्याची लक्षणे</strong><div class="th-dx-content">• अचानक रक्तस्त्राव
• तीव्र डोकेदुखी, फिट
• बाळाची हालचाल थांबणे → तात्काळ 108/102 कॉल</div></div></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#FFF8E6;color:#D97706;">🎁</div><div style="flex:1;"><strong class="th-dx-label" style="color:#D97706;">जननी सुरक्षा योजना (JSY)</strong><div class="th-dx-content">• शासकीय रुग्णालयात मोफत प्रसूती + <strong>₹७०० थेट बँक खात्यात</strong></div></div></div></div>"""
    if lang == "hi":
        return """<div class="th-dx-card"><div class="th-dx-header"><div class="th-dx-header-left"><div class="th-dx-header-icon">🤰</div><div><h4 class="th-dx-title">मातृ एवं शिशु स्वास्थ्य पोर्टल</h4></div></div><span class="th-dx-badge">MCH</span></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#EAF2FE;color:#0B6BCB;">📋</div><div style="flex:1;"><strong class="th-dx-label" style="color:#0B6BCB;">4 मुफ्त ANC जांच</strong><div class="th-dx-content">• 12 सप्ताह से पहले: पंजीकरण, फोलिक एसिड
• 14-26 सप्ताह: TT-1, BP जांच
• 28-34 सप्ताह: TT-2, एनीमिया स्क्रीनिंग
• 36+ सप्ताह: प्रसव योजना, 102 जननी एक्सप्रेस</div></div></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#E6F7F5;color:#0E9F8F;">💉</div><div style="flex:1;"><strong class="th-dx-label" style="color:#0E9F8F;">शिशु टीकाकरण अनुसूची</strong><div class="th-dx-content">• जन्म: BCG, OPV-0, Hep-B
• 6/10/14 सप्ताह: पेंटावैलेंट, रोटा
• 9 महीने: MR-1, विटामिन A</div></div></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#FEECEB;color:#DC2626;">🚨</div><div style="flex:1;"><strong class="th-dx-label" style="color:#DC2626;">गर्भावस्था में खतरे के संकेत</strong><div class="th-dx-content">• अचानक रक्तस्राव, तेज सिरदर्द, फिट → तुरंत 108/102</div></div></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#FFF8E6;color:#D97706;">🎁</div><div style="flex:1;"><strong class="th-dx-label" style="color:#D97706;">जननी सुरक्षा योजना</strong><div class="th-dx-content">• मुफ्त प्रसव + <strong>₹700 बैंक खाते में</strong></div></div></div></div>"""
    return """<div class="th-dx-card"><div class="th-dx-header"><div class="th-dx-header-left"><div class="th-dx-header-icon">🤰</div><div><h4 class="th-dx-title">Maternal & Child Health Portal</h4><span style="font-size:0.75rem;color:#64748B;font-weight:600;">Free ANC, Immunization & JSY Benefits</span></div></div><span class="th-dx-badge">MCH SERVICES</span></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#EAF2FE;color:#0B6BCB;">📋</div><div style="flex:1;"><strong class="th-dx-label" style="color:#0B6BCB;">4 Mandatory ANC Visits</strong><div class="th-dx-content">• <strong>Before 12 weeks:</strong> Registration, Folic Acid
• <strong>14-26 weeks:</strong> TT-1 vaccine, BP monitoring
• <strong>28-34 weeks:</strong> TT-2, anemia screening
• <strong>36+ weeks:</strong> Delivery planning, 102 Janani Express</div></div></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#E6F7F5;color:#0E9F8F;">💉</div><div style="flex:1;"><strong class="th-dx-label" style="color:#0E9F8F;">Child Immunization Schedule</strong><div class="th-dx-content">• <strong>At Birth:</strong> BCG, OPV-0, Hep-B
• <strong>6/10/14 Weeks:</strong> Pentavalent, Rotavirus, OPV
• <strong>9 Months:</strong> MR-1, Vitamin A</div></div></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#FEECEB;color:#DC2626;">🚨</div><div style="flex:1;"><strong class="th-dx-label" style="color:#DC2626;">Pregnancy Danger Signs</strong><div class="th-dx-content">• Sudden bleeding or spotting
• Severe headache, blurred vision, fits
• Reduced fetal movements → Call <strong>108/102 immediately</strong></div></div></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#FFF8E6;color:#D97706;">🎁</div><div style="flex:1;"><strong class="th-dx-label" style="color:#D97706;">Janani Suraksha Yojana</strong><div class="th-dx-content">• Free institutional delivery + <strong>₹700 direct bank transfer</strong> for rural women</div></div></div></div>"""

def generate_jan_aushadhi_guide(lang="en"):
    rows = "".join(
        f"<tr><td style='padding:8px;border:1px solid #E2E8F0;font-weight:700;'>{med}</td><td style='padding:8px;border:1px solid #E2E8F0;font-size:0.8rem;color:#64748B;'>{d['use']}</td><td style='padding:8px;border:1px solid #E2E8F0;color:#DC2626;'>{d['branded']}</td><td style='padding:8px;border:1px solid #E2E8F0;color:#16794C;font-weight:700;'>{d['generic']}</td><td style='padding:8px;border:1px solid #E2E8F0;'><span style='background:#EAF8EF;color:#16794C;padding:2px 8px;border-radius:999px;font-size:0.72rem;font-weight:700;'>{d['saving']}</span></td></tr>"
        for med, d in GENERIC_MEDS.items()
    )
    title = "पंतप्रधान जन औषधी - जेनेरिक औषध" if lang == "mr" else "प्रधानमंत्री जन औषधि - जेनेरिक दवा" if lang == "hi" else "Pradhan Mantri Jan Aushadhi Guide"
    headers = ["औषध"," वापर","ब्रँडेड","जन औषधी","बचत"] if lang == "mr" else ["दवा","उपयोग","ब्रांडेड","जन औषधि","बचत"] if lang == "hi" else ["Medicine","Use","Branded","Jan Aushadhi","Save"]
    tip = "'Jan Aushadhi Sugam' अ‍ॅप वापरून जवळचे केंद्र शोधा" if lang == "mr" else "'Jan Aushadhi Sugam' ऐप से नजदीकी केंद्र खोजें" if lang == "hi" else "Use 'Jan Aushadhi Sugam' app to find nearest store"
    return f"""<div class="th-dx-card"><div class="th-dx-header"><div class="th-dx-header-left"><div class="th-dx-header-icon">💊</div><div><h4 class="th-dx-title">{title}</h4><span style="font-size:0.75rem;color:#64748B;font-weight:600;">Reference prices — verify at local store</span></div></div><span class="th-dx-badge">GENERIC</span></div><div style="padding:15px 20px;"><table style="width:100%;border-collapse:collapse;font-size:0.85rem;margin-bottom:12px;"><thead><tr style="background:#F8FAFC;"><th style="padding:8px;border:1px solid #E2E8F0;text-align:left;">{headers[0]}</th><th style="padding:8px;border:1px solid #E2E8F0;text-align:left;">{headers[1]}</th><th style="padding:8px;border:1px solid #E2E8F0;text-align:left;">{headers[2]}</th><th style="padding:8px;border:1px solid #E2E8F0;text-align:left;">{headers[3]}</th><th style="padding:8px;border:1px solid #E2E8F0;text-align:left;">{headers[4]}</th></tr></thead><tbody>{rows}</tbody></table><div style="background:#F0F7FF;border:1px solid #BAE6FD;padding:12px;border-radius:10px;font-size:0.84rem;"><strong>📍 {tip}</strong></div></div></div>"""

def generate_asha_anm_guide(lang="en"):
    if lang == "mr":
        return """<div class="th-dx-card"><div class="th-dx-header"><div class="th-dx-header-left"><div class="th-dx-header-icon">👩‍⚕️</div><div><h4 class="th-dx-title">गावातील आशा सेविका आणि ANM</h4><span style="font-size:0.75rem;color:#64748B;font-weight:600;">ग्रामीण आरोग्य सेवा मार्गदर्शक</span></div></div><span class="th-dx-badge">FRONTLINE</span></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#EAF2FE;color:#0B6BCB;">🩸</div><div style="flex:1;"><strong class="th-dx-label" style="color:#0B6BCB;">आशा सेविका सेवा</strong><div class="th-dx-content">• गरोदर मातांची तपासणी + 102/108 जोडणी
• नवजात बालक वजन + मोफत लसी
• ORS, लोह गोळ्या, प्राथमिक औषधे मोफत
• TB DOTS, मलेरिया घरी उपचार</div></div></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#E6F7F5;color:#0E9F8F;">🏥</div><div style="flex:1;"><strong class="th-dx-label" style="color:#0E9F8F;">ANM आरोग्य सेविका</strong><div class="th-dx-content">• उपकेंद्रात प्रसूती + लसीकरण
• दरमहा लसीकरण दिवस
• गंभीर रुग्ण रेफरल</div></div></div></div>"""
    return """<div class="th-dx-card"><div class="th-dx-header"><div class="th-dx-header-left"><div class="th-dx-header-icon">👩‍⚕️</div><div><h4 class="th-dx-title">ASHA & ANM Frontline Workers</h4><span style="font-size:0.75rem;color:#64748B;font-weight:600;">Guide to rural healthcare worker services</span></div></div><span class="th-dx-badge">FRONTLINE</span></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#EAF2FE;color:#0B6BCB;">🩸</div><div style="flex:1;"><strong class="th-dx-label" style="color:#0B6BCB;">ASHA Worker Services</strong><div class="th-dx-content">• Maternal registration + 102 Janani Express coordination
• Newborn tracking, free immunization
• Free ORS, Iron-Folic Acid tablets, contraception
• Home TB DOTS therapy, malaria monitoring</div></div></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#E6F7F5;color:#0E9F8F;">🏥</div><div style="flex:1;"><strong class="th-dx-label" style="color:#0E9F8F;">ANM Services</strong><div class="th-dx-content">• Safe delivery setups at sub-centres
• Monthly village immunization drives
• High-risk case referral tracking</div></div></div></div>"""

def generate_district_locator_results(query_text, lang="en"):
    matched = None
    q = query_text.lower()
    for name in MAHARASHTRA_DISTRICTS:
        pure = re.sub(r"[\(\) ऀ-ॿ]", "", name).lower()
        if pure in q or name.split()[0].lower() in q: matched = name; break
    if not matched: matched = "Nandurbar (नंदुरबार)"
    facs = MAHARASHTRA_DISTRICTS[matched]
    cards = "".join(f"""<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:12px 16px;margin-bottom:8px;"><div style="display:flex;justify-content:space-between;align-items:center;"><strong style="color:#0B6BCB;font-size:0.92rem;">🏢 {f['name']}</strong><span style="font-size:0.7rem;background:#EAF2FE;color:#0B6BCB;padding:2px 8px;border-radius:999px;font-weight:700;">{f['type']}</span></div><p style="font-size:0.84rem;margin:6px 0 2px;color:#475569;">📍 {f['location']} | Beds: <strong>{f['beds']}</strong></p><p style="font-size:0.84rem;margin:0;color:#475569;">🔧 <em>{f['facilities']}</em></p><p style="font-size:0.78rem;margin:4px 0 0;color:#94A3B8;">ℹ️ Reference data — verify before visiting</p><p style="font-size:0.84rem;margin:4px 0 0;color:#0E9F8F;">📞 <a href="tel:{f['phone']}" style="color:inherit;text-decoration:none;"><strong>{f['phone']}</strong></a></p></div>""" for f in facs)
    title = f"{matched} शासकीय आरोग्य सुविधा" if lang == "mr" else f"{matched} स्वास्थ्य सुविधाएं" if lang == "hi" else f"Government Healthcare Directory - {matched}"
    return f"""<div class="th-dx-card"><div class="th-dx-header"><div class="th-dx-header-left"><div class="th-dx-header-icon">🏥</div><div><h4 class="th-dx-title">{title}</h4><span style="font-size:0.75rem;color:#64748B;font-weight:600;">Reference data — verify details before visiting</span></div></div><span class="th-dx-badge">DIRECTORY</span></div><div style="padding:15px 20px;">{cards}</div></div>"""

def _derive_required_services(entities, secondary_intent=None, requested_service=None):
    """Derive required healthcare services from extracted entities + semantic context.
    Uses requested_service from the semantic pipeline — the key attribute that was being lost."""
    services = []
    age_group = entities.get("age_group", "")
    is_pregnant = entities.get("is_pregnant", False)
    symptoms = entities.get("symptoms", [])
    severity = entities.get("severity_hint")

    # Priority 1: Explicit requested_service from semantic pipeline
    if requested_service:
        services.append(requested_service)
    # Priority 2: Secondary intent maps to a service
    if secondary_intent:
        _intent_service_map = {
            INTENT_VACCINATION: "Immunization",
            INTENT_PREGNANCY: "Maternity",
            INTENT_CHILD_HEALTH: "Pediatric",
        }
        svc = _intent_service_map.get(secondary_intent)
        if svc and svc not in services:
            services.append(svc)

    # Priority 3: Derive from patient attributes
    if age_group == "child":
        if "Pediatric" not in services:
            services.append("Pediatric")
    if is_pregnant:
        if "Maternity" not in services:
            services.append("Maternity")
    if severity == "severe" or "bleeding" in symptoms:
        if "Emergency" not in services:
            services.append("Emergency")

    # Always include General OPD as fallback if no specific service found
    if not services:
        services.append("General OPD")
    elif "General OPD" not in services and len(services) == 1:
        # If only one specific service, add General OPD as backup
        services.append("General OPD")

    return services


def generate_ranked_facility_results(ranked_facs, entities, lang="en", requested_service=None, secondary_intent=None, ranked_with_reasons=None):
    """Context-aware facility display using ranked results.
    Generates dynamic explanation based on ACTUAL extracted semantic attributes.
    Shows per-facility match reason tags from the scoring engine.
    """
    district = entities.get("district", "")
    age_group = entities.get("age_group", "")
    is_pregnant = entities.get("is_pregnant", False)
    symptoms = entities.get("symptoms", [])
    duration = entities.get("duration")
    duration_unit = entities.get("duration_unit", "days")
    severity = entities.get("severity_hint")

    # Build dynamic context string from ACTUAL semantic attributes
    ctx_parts = []
    if age_group == "child":
        ctx_parts.append("child" if lang == "en" else ("बच्चा" if lang == "hi" else "बाळ"))
    if age_group == "elderly":
        ctx_parts.append("elderly" if lang == "en" else "वृद्ध")
    if is_pregnant:
        ctx_parts.append("pregnant" if lang == "en" else ("गर्भवती" if lang == "hi" else "गरोदर"))
    if symptoms:
        ctx_parts.extend(symptoms[:3])
    if duration:
        ctx_parts.append(f"{duration} {duration_unit}")
    if severity == "severe":
        ctx_parts.append("severe" if lang == "en" else "गंभीर")
    if district:
        ctx_parts.append(district)

    # Build dynamic service priority message based on what was ACTUALLY requested
    # The key fix: use requested_service from semantic pipeline, not generic fallback
    if requested_service:
        priority_svc = requested_service
    elif secondary_intent:
        _intent_svc = {INTENT_VACCINATION: "Immunization", INTENT_PREGNANCY: "Maternity", INTENT_CHILD_HEALTH: "Pediatric"}
        priority_svc = _intent_svc.get(secondary_intent, "General OPD")
    else:
        required = _derive_required_services(entities, secondary_intent, requested_service)
        priority_svc = "/".join(required[:2]) if required else "General OPD"

    ctx_str = ", ".join(ctx_parts) if ctx_parts else ("general" if lang == "en" else "सामान्य")

    if lang == "hi":
        explanation = f"आपके विशलेसण के आधार पर: {ctx_str}. {priority_svc} सेवा वाली सुविधाएं पहले दिखाई गई हैं।"
    elif lang == "mr":
        explanation = f"तुम्हीच्या विशिष्टांच्या आधारावर: {ctx_str}. {priority_svc} सेवा असलेली सुविधा आधी दर्शवली आहेत."
    else:
        explanation = f"Based on your query: {ctx_str}. Showing facilities with {priority_svc} services first."

    explanation_html = f'<div style="background:#F0F7FF;border:1px solid #BAE6FD;border-radius:10px;padding:10px 14px;margin-bottom:10px;font-size:0.85rem;color:#1E40AF;">\U0001f50d {explanation}</div>'

    # Build facility cards with per-facility match reason tags
    cards = ""
    # Build a name→reasons map from ranked_with_reasons if available
    _reasons_map = {}
    if ranked_with_reasons:
        for fac, reasons in ranked_with_reasons:
            _reasons_map[fac.get("name", "")] = reasons

    for idx, f in enumerate(ranked_facs):
        # Use reasons from the scoring engine if available, otherwise fall back to service list match
        fac_reasons = _reasons_map.get(f.get("name", ""), [])
        if fac_reasons:
            match_badges = " ".join(
                f'<span style="font-size:0.65rem;background:#DCFCE7;color:#16794C;padding:1px 6px;border-radius:999px;margin-left:4px;font-weight:600;">{html.escape(r)}</span>'
                for r in fac_reasons
            )
        else:
            # Fallback: show which required services this facility has
            services_lower = [s.lower() for s in f.get("services_list", [])]
            required = _derive_required_services(entities, secondary_intent, requested_service)
            match_badges = ""
            for req in required:
                if req.lower() in " ".join(services_lower):
                    match_badges += f'<span style="font-size:0.65rem;background:#DCFCE7;color:#16794C;padding:1px 6px;border-radius:999px;margin-left:4px;font-weight:600;">\u2713 {req}</span>'

        rank_num = idx + 1
        rank_icon = "\U0001f947" if rank_num == 1 else ("\U0001f948" if rank_num == 2 else ("\U0001f949" if rank_num == 3 else f"#{rank_num}"))

        cards += f'<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:12px 16px;margin-bottom:8px;"><div style="display:flex;justify-content:space-between;align-items:center;"><strong style="color:#0B6BCB;font-size:0.92rem;">{rank_icon} {html.escape(f["name"])}</strong><span style="font-size:0.7rem;background:#EAF2FE;color:#0B6BCB;padding:2px 8px;border-radius:999px;font-weight:700;">{html.escape(f["type"])}</span></div><p style="font-size:0.84rem;margin:6px 0 2px;color:#475569;">\U0001f4cd {html.escape(f["location"])} | Beds: <strong>{html.escape(f["beds"])}</strong></p><p style="font-size:0.84rem;margin:0;color:#475569;">\U0001f527 <em>{html.escape(f["facilities"])}</em>{match_badges}</p><p style="font-size:0.78rem;margin:4px 0 0;color:#94A3B8;">\u2139\ufe0f Reference data \u2014 verify before visiting</p><p style="font-size:0.84rem;margin:4px 0 0;color:#0E9F8F;">\U0001f4de <a href="tel:{html.escape(f["phone"])}" style="color:inherit;text-decoration:none;"><strong>{html.escape(f["phone"])}</strong></a></p></div>'

    if lang == "mr":
        title = f"{district} शासकीय आरोग्य सुविधा" if district else "शासकीय आरोग्य सुविधा"
    elif lang == "hi":
        title = f"{district} स्वास्थ्य सुविधाएं" if district else "स्वास्थ्य सुविधाएं"
    else:
        title = f"Healthcare Facilities \u2014 {district}" if district else "Healthcare Facilities"

    return f'<div class="th-dx-card"><div class="th-dx-header"><div class="th-dx-header-left"><div class="th-dx-header-icon">\U0001f3e5</div><div><h4 class="th-dx-title">{title}</h4><span style="font-size:0.75rem;color:#64748B;font-weight:600;">Reference data \u2014 verify details before visiting</span></div></div><span class="th-dx-badge">RANKED</span></div><div style="padding:15px 20px;">{explanation_html}{cards}</div></div>'


def generate_schemes_guide(lang="en"):
    cards = "".join(f"""<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:12px 16px;margin-bottom:10px;"><strong style="color:#0B6BCB;font-size:0.95rem;display:block;margin-bottom:6px;">✨ {s['name']}</strong><p style="font-size:0.86rem;margin:0 0 6px 0;line-height:1.45;color:#334155;"><strong>🎁 Benefits:</strong> {s['benefits']}</p><p style="font-size:0.86rem;margin:0 0 6px 0;color:#334155;"><strong>🎯 Eligibility:</strong> {s['eligibility']}</p><p style="font-size:0.86rem;margin:0;color:#16794C;font-weight:700;">📌 How to claim: {s['apply_how']}</p></div>""" for s in MAHARASHTRA_SCHEMES)
    title = "महाराष्ट्र शासकीय आरोग्य योजना" if lang == "mr" else "महाराष्ट्र सरकारी स्वास्थ्य योजनाएं" if lang == "hi" else "Maharashtra Government Health Schemes"
    return f"""<div class="th-dx-card"><div class="th-dx-header"><div class="th-dx-header-left"><div class="th-dx-header-icon">📋</div><div><h4 class="th-dx-title">{title}</h4><span style="font-size:0.75rem;color:#64748B;font-weight:600;">Cashless treatment & free services</span></div></div><span class="th-dx-badge">BENEFITS</span></div><div style="padding:15px 20px;">{cards}</div></div>"""

# ============================================================================
# MAIN RESPONSE PIPELINE
# ============================================================================


def _render_next_camp_info(lang="en"):
    """Calculate and display next vaccination camp dates from recurring schedule.
    Clearly labels as reference schedule, not live confirmed events."""
    from datetime import datetime, timedelta
    today = datetime.now()
    
    # Find vaccination-related camps from HEALTH_CAMPS
    camp_html = ""
    for camp in HEALTH_CAMPS:
        camp_date_str = camp.get("date", "")
        next_date = None
        location = camp.get("location", "Contact your local PHC/CHC")
        services = camp.get("services", "")
        
        # Calculate next occurrence
        if "every wednesday" in camp_date_str.lower():
            # Find next Wednesday
            days_ahead = 2 - today.weekday()  # Wednesday = 2
            if days_ahead < 0:
                days_ahead += 7
            next_date = today + timedelta(days=days_ahead)
        elif "every 9th" in camp_date_str.lower() or "every 9" in camp_date_str.lower():
            # Next 9th of month
            if today.day <= 9:
                next_date = today.replace(day=9)
            else:
                next_month = today.replace(day=28) + timedelta(days=4)
                next_date = next_month.replace(day=9)
        elif "1st saturday" in camp_date_str.lower() or "first saturday" in camp_date_str.lower():
            # Find next 1st Saturday of month
            for month_offset in range(2):
                check_month = today.month + month_offset
                check_year = today.year
                if check_month > 12:
                    check_month -= 12
                    check_year += 1
                try:
                    first_day = datetime(check_year, check_month, 1)
                    # Saturday = 5
                    days_to_sat = (5 - first_day.weekday()) % 7
                    first_sat = first_day + timedelta(days=days_to_sat)
                    if first_sat >= today:
                        next_date = first_sat
                        break
                except ValueError:
                    pass
        elif "quarterly" in camp_date_str.lower():
            # Approximate: every 3 months from Jan/Apr/Jul/Oct
            quarter_months = [1, 4, 7, 10]
            for qm in quarter_months:
                try:
                    candidate = datetime(today.year, qm, 1)
                    if candidate >= today - timedelta(days=30):
                        next_date = candidate
                        break
                except ValueError:
                    pass
        
        next_date_str = next_date.strftime("%d %b %Y") if next_date else "Check locally"
        
        if lang == "hi":
            camp_html += f'<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:12px 16px;margin-bottom:10px;"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;"><strong style="color:#0B6BCB;font-size:0.95rem;">📅 {camp.get("name","")}</strong><span style="font-size:0.7rem;background:#FEF3C7;color:#92400E;padding:2px 8px;border-radius:999px;font-weight:700;">{camp_date_str}</span></div><p style="font-size:0.85rem;margin:0 0 4px;color:#334155;"><strong>📍 स्थान:</strong> {location}</p><p style="font-size:0.85rem;margin:0 0 4px;color:#334155;"><strong>🏥 सेवाएं:</strong> {services}</p><p style="font-size:0.85rem;margin:0 0 4px;color:#16794C;font-weight:600;"><strong>📅 अगली तारीख (अनुमानित):</strong> {next_date_str}</p><p style="font-size:0.78rem;color:#94A3B8;font-style:italic;">⚠️ संदर्भ अनुसूची — स्थानीय रूप से पुष्टि करें</p></div>'
        elif lang == "mr":
            camp_html += f'<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:12px 16px;margin-bottom:10px;"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;"><strong style="color:#0B6BCB;font-size:0.95rem;">📅 {camp.get("name","")}</strong><span style="font-size:0.7rem;background:#FEF3C7;color:#92400E;padding:2px 8px;border-radius:999px;font-weight:700;">{camp_date_str}</span></div><p style="font-size:0.85rem;margin:0 0 4px;color:#334155;"><strong>📍 ठिकाण:</strong> {location}</p><p style="font-size:0.85rem;margin:0 0 4px;color:#334155;"><strong>🏥 सेवा:</strong> {services}</p><p style="font-size:0.85rem;margin:0 0 4px;color:#16794C;font-weight:600;"><strong>📅 पुढची तारीख (अंदाजे):</strong> {next_date_str}</p><p style="font-size:0.78rem;color:#94A3B8;font-style:italic;">⚠️ संदर्भ वेळापत्रक — स्थानिक पडताळणी करा</p></div>'
        else:
            camp_html += f'<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:12px 16px;margin-bottom:10px;"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;"><strong style="color:#0B6BCB;font-size:0.95rem;">📅 {camp.get("name","")}</strong><span style="font-size:0.7rem;background:#FEF3C7;color:#92400E;padding:2px 8px;border-radius:999px;font-weight:700;">{camp_date_str}</span></div><p style="font-size:0.85rem;margin:0 0 4px;color:#334155;"><strong>📍 Where:</strong> {location}</p><p style="font-size:0.85rem;margin:0 0 4px;color:#334155;"><strong>🏥 Services:</strong> {services}</p><p style="font-size:0.85rem;margin:0 0 4px;color:#16794C;font-weight:600;"><strong>📅 Next expected date:</strong> {next_date_str}</p><p style="font-size:0.78rem;color:#94A3B8;font-style:italic;">⚠️ Reference schedule — verify locally before visiting</p></div>'

    if lang == "hi":
        title = "💉 टीकाकरण शिविर अनुसूची"
        subtitle = "आवर्ती मुफ्त टीकाकरण कार्यक्रम — स्थानीय पुष्टि आवश्यक"
    elif lang == "mr":
        title = "💉 लसीकरण शिबिर वेळापत्रक"
        subtitle = "आवर्ती मोफत लसीकरण कार्यक्रम — स्थानिक पडताळणी आवश्यक"
    else:
        title = "💉 Vaccination Camp Schedule"
        subtitle = "Recurring free immunization programs — verify locally before visiting"

    return f'<div class="th-dx-card"><div class="th-dx-header"><div class="th-dx-header-left"><div class="th-dx-header-icon">📅</div><div><h4 class="th-dx-title">{title}</h4><span style="font-size:0.75rem;color:#64748B;font-weight:600;">{subtitle}</span></div></div><span class="th-dx-badge">CAMPS</span></div><div style="padding:15px 20px;">{camp_html}</div></div>'

def generate_response(query, language, df, symptom_embeddings, name_embeddings, model):
    """Structured Healthcare Access Routing Engine.
    Pipeline: normalize -> detect lang -> classify intent -> extract entities ->
    classify urgency -> build routing object -> deterministic route -> facility match -> response."""
    try:
        return _generate_response_inner(query, language, df, symptom_embeddings, name_embeddings, model)
    except Exception as _route_err:
        # NEVER crash on valid user input — graceful fallback
        _lang = "en"
        try:
            _lang = detect_response_lang(query)
        except Exception:
            pass
        # Log error internally but don't expose to user
        import traceback
        traceback.print_exc()
        return _build_fallback_response(_lang)

def _generate_response_inner(query, language, df, symptom_embeddings, name_embeddings, model):
    """Inner routing engine — called by generate_response with exception safety."""
    # Stage 1+2: Input normalization + Language detection
    response_lang = "hi" if language == MODE_HINDI else "mr" if language == MODE_MARATHI else "en" if language == MODE_ENGLISH else detect_response_lang(query)
    romanized, has_devanagari = is_romanized_hindi(query), bool(re.search(r"[ऀ-ॿ]", query or ""))
    offline_parts = []
    if romanized: offline_parts.append(romanize_to_english(query))
    if response_lang in ("hi","mr") or has_devanagari: offline_parts.append(devanagari_to_english(query))
    offline_en = " ".join(p for p in offline_parts if p).strip()
    query_for_matching = query
    if response_lang != "en" or romanized:
        translated = translate_safe(query, source="auto", target="en")
        if translated and not (has_devanagari and re.search(r"[ऀ-ॿ]", translated)) and not _looks_like_translation_error(translated):
            query_for_matching = (translated + " " + offline_en).strip() if offline_en else translated
        else: query_for_matching = offline_en or query
    norm_q = query_for_matching.lower()

    # Stage 3: Intent classification
    primary_intent, secondary_intent, intent_confidence = classify_intent(query_for_matching, query)

    # Stage 5: Entity extraction
    entities = extract_entities(query_for_matching, query)
    # Add structured symptom list and patient type
    entities["symptoms"] = _extract_symptoms_list((query_for_matching or "").lower() + " " + (query or "").lower())
    entities["patient_type"] = entities.get("age_group", "adult")
    entities["required_service"] = None  # Set by routing below
    entities["facility_type"] = None

    # Conversational context: merge with session memory
    ctx = st.session_state.get("conversation_context", {})
    if entities.get("district"):
        ctx["last_district"] = entities["district"]
    if entities.get("age"):
        ctx["last_age"] = entities["age"]
        ctx["last_age_unit"] = entities.get("age_unit", "years")
    if entities.get("is_pregnant"):
        ctx["is_pregnant"] = True
    if entities.get("pregnancy_week"):
        ctx["pregnancy_week"] = entities["pregnancy_week"]
    st.session_state.conversation_context = ctx

    # Follow-up: use remembered district if user omits it
    _facility_intents_for_recall = (INTENT_FACILITY, INTENT_FACILITY_SEARCH,
        INTENT_IMMUNIZATION_FACILITY_SEARCH, INTENT_MATERNITY_FACILITY_SEARCH,
        INTENT_PEDIATRIC_FACILITY_SEARCH, INTENT_GENERAL_OPD_SEARCH)
    if primary_intent in _facility_intents_for_recall and not entities.get("district") and ctx.get("last_district"):
        entities["district"] = ctx["last_district"]

    # Stage 4: Safety-first urgency classification
    emergency_text = (query_for_matching or "") + (" " + offline_en if offline_en else "")
    _red_flag = has_red_flags(query, emergency_text)
    _critical = is_critical_emergency(query, emergency_text)
    urgency = classify_urgency(primary_intent, entities, _red_flag, _critical)

    # Seasonal prevention
    if is_seasonal_prevention_query(query):
        return format_seasonal_prevention_card(response_lang)

    # Stage 5: Deterministic routing engine
    # Store routing debug info
    _routing_debug = {
        "language": response_lang, "intent": primary_intent,
        "urgency": urgency, "confidence": intent_confidence,
        "entities": {k: v for k, v in entities.items() if v},
    }

    # --- EMERGENCY route (highest priority) ---
    if primary_intent == INTENT_EMERGENCY:
        entities["required_service"] = "Emergency"
        entities["facility_type"] = "District Hospital"
        matched_facs_with_reasons = match_and_rank_facilities(entities.get("district"), ["Emergency"], "District Hospital", urgency, entities=entities)
        matched_facs = [f for f, _ in matched_facs_with_reasons]
        _routing_debug["matched_facility_count"] = len(matched_facs)
        _routing_debug["route"] = "emergency"
        st.session_state["_routing_debug"] = _routing_debug

        # Emergency: show ONLY emergency action content. No routine disease cards.
        # Suppress "Viral Fever / MILD / PHC" and similar non-emergency interpretations.
        emerg_response = emergency_banner_html(response_lang)
        # Add 108 call action prominently
        if response_lang == "hi":
            emerg_response += '<div style="margin-top:12px;"><div class="th-alert info"><div class="th-alert-icon">\U0001f3e5</div><div class="th-alert-body"><h4>तुरंत अस्पताल जाएं</h4><p><a href="tel:108" style="color:#DC2626;font-weight:700;font-size:1.1rem;">108</a> पर तुरंत कॉल करें या <a href="tel:104" style="color:#0B6BCB;font-weight:700;">104</a> पर स्वास्थ्य सलाह लें</p></div></div></div>'
        elif response_lang == "mr":
            emerg_response += '<div style="margin-top:12px;"><div class="th-alert info"><div class="th-alert-icon">\U0001f3e5</div><div class="th-alert-body"><h4>त्वरित रुग्णालयात जा</h4><p><a href="tel:108" style="color:#DC2626;font-weight:700;font-size:1.1rem;">108</a> वर त्वरित कॉल करा किंवा <a href="tel:104" style="color:#0B6BCB;font-weight:700;">104</a> वर सल्लह घ्या</p></div></div></div>'
        else:
            emerg_response += '<div style="margin-top:12px;"><div class="th-alert info"><div class="th-alert-icon">\U0001f3e5</div><div class="th-alert-body"><h4>Seek emergency care immediately</h4><p>Call <a href="tel:108" style="color:#DC2626;font-weight:700;font-size:1.1rem;">108</a> now or <a href="tel:104" style="color:#0B6BCB;font-weight:700;">104</a> for health advice helpline.</p></div></div></div>'
        # If district known, show ranked emergency facilities
        if entities.get("district"):
            emerg_facs_with_reasons = match_and_rank_facilities(entities.get("district"), ["Emergency"], "District Hospital", "EMERGENCY", entities=entities)
            emerg_facs = [f for f, _ in emerg_facs_with_reasons]
            if emerg_facs:
                emerg_response += generate_ranked_facility_results(emerg_facs[:3], entities, response_lang, requested_service="Emergency")
        fac_type = "DH" if secondary_intent == INTENT_PREGNANCY else "any"
        emerg_response += care_pathway_html(fac_type, response_lang)
        return emerg_response

    # --- TELEMEDICINE route ---
    if primary_intent == INTENT_TELEMEDICINE:
        _routing_debug["route"] = "telemedicine"
        st.session_state["_routing_debug"] = _routing_debug
        return generate_telemedicine_guide(response_lang) + care_pathway_html("PHC", response_lang)

    # --- HELPLINE route ---
    if primary_intent == INTENT_HELPLINE:
        _routing_debug["route"] = "helpline"
        st.session_state["_routing_debug"] = _routing_debug
        return generate_asha_anm_guide(response_lang) + care_pathway_html("PHC", response_lang)

    # --- VACCINATION / HEALTH_PROGRAM route ---
    # =====================================================================
    # CANONICAL INTENT ROUTING — handles ALL 15 canonical intents
    # Maps each canonical intent to the correct service, then does
    # facility search or information display as appropriate.
    # =====================================================================

    # --- Canonical facility-search intents ---
    # These are the PRIMARY routing path for vaccination/maternity/pediatric/general queries.
    _CANONICAL_FACILITY_MAP = {
        INTENT_IMMUNIZATION_FACILITY_SEARCH: ("Immunization", "PHC"),
        INTENT_MATERNITY_FACILITY_SEARCH:    ("Maternity",    "District Hospital"),
        INTENT_PEDIATRIC_FACILITY_SEARCH:    ("Pediatric",    "PHC"),
        INTENT_GENERAL_OPD_SEARCH:           ("General OPD",  None),
    }

    if primary_intent in _CANONICAL_FACILITY_MAP:
        req_svc, fac_type = _CANONICAL_FACILITY_MAP[primary_intent]
        requested_service = req_svc
        required_services = _derive_required_services(entities, secondary_intent, requested_service)
        entities["required_service"] = requested_service
        entities["facility_type"] = fac_type
        _routing_debug["route"] = f"canonical_{req_svc.lower().replace(' ','_')}"
        _routing_debug["requested_service"] = requested_service
        _routing_debug["required_services"] = required_services
        _routing_debug["sub_intent"] = secondary_intent
        _routing_debug["nearest_requested"] = entities.get("proximity_request", False)
        st.session_state["_routing_debug"] = _routing_debug

        if entities.get("district"):
            ranked_facs_with_reasons = match_and_rank_facilities(
                entities.get("district"),
                required_services=required_services,
                facility_type=fac_type,
                urgency=urgency,
                requested_service=requested_service,
                entities=entities
            )
            ranked_facs = [f for f, _ in ranked_facs_with_reasons]
            _routing_debug["matched_facility_count"] = len(ranked_facs)
            st.session_state["_routing_debug"] = _routing_debug
            return generate_ranked_facility_results(
                ranked_facs, entities, response_lang,
                requested_service=requested_service,
                secondary_intent=secondary_intent,
                ranked_with_reasons=ranked_facs_with_reasons
            )

        # No district: ask for clarification
        clarifications = build_clarifying_question(entities, primary_intent, response_lang)
        if clarifications:
            hint = '<div style="background:#F0F7FF;border:1px solid #BAE6FD;border-radius:10px;padding:12px 16px;margin-bottom:10px;">' + "<br>".join(clarifications) + "</div>"
            return hint + generate_district_locator_results(norm_q, response_lang)
        return generate_district_locator_results(norm_q, response_lang)

    # --- Canonical information intents ---
    if primary_intent == INTENT_IMMUNIZATION_INFORMATION:
        _routing_debug["route"] = "immunization_info"
        st.session_state["_routing_debug"] = _routing_debug
        # Show vaccination/immunization information + camp schedule
        info_html = render_health_camps_html(response_lang)
        # Add next camp info if available
        camp_info = _render_next_camp_info(response_lang)
        if camp_info:
            info_html += camp_info
        return info_html + care_pathway_html("CHC", response_lang)

    if primary_intent == INTENT_VACCINATION_SCHEDULE:
        _routing_debug["route"] = "vaccination_schedule"
        st.session_state["_routing_debug"] = _routing_debug
        camp_info = _render_next_camp_info(response_lang)
        schedule_html = render_health_camps_html(response_lang)
        if camp_info:
            schedule_html += camp_info
        return schedule_html + care_pathway_html("CHC", response_lang)

    if primary_intent == INTENT_VACCINATION_CAMP_INFORMATION:
        _routing_debug["route"] = "vaccination_camp"
        st.session_state["_routing_debug"] = _routing_debug
        camp_html = render_health_camps_html(response_lang)
        camp_info = _render_next_camp_info(response_lang)
        if camp_info:
            camp_html += camp_info
        return camp_html + care_pathway_html("CHC", response_lang)

    # --- Legacy VACCINATION route (backward compat) ---
    if primary_intent == INTENT_VACCINATION:
        entities["required_service"] = "Immunization"
        entities["facility_type"] = "PHC"
        _routing_debug["route"] = "vaccination"
        st.session_state["_routing_debug"] = _routing_debug
        return render_health_camps_html(response_lang) + care_pathway_html("CHC", response_lang)

    # --- Legacy FACILITY_SEARCH route ---
    if primary_intent == INTENT_FACILITY_SEARCH:
        # Derive requested_service from semantic pipeline (secondary intent)
        requested_service = detect_requested_service(norm_q + " " + (query or "").lower())
        # Also map from secondary intent
        if not requested_service and secondary_intent:
            _intent_service_map = {
                INTENT_VACCINATION: "Immunization",
                INTENT_PREGNANCY: "Maternity",
                INTENT_CHILD_HEALTH: "Pediatric",
            }
            requested_service = _intent_service_map.get(secondary_intent)

        # Derive full required services list using entities + semantic context
        required_services = _derive_required_services(entities, secondary_intent, requested_service)
        entities["required_service"] = requested_service or (required_services[0] if required_services else "General OPD")
        _routing_debug["route"] = "facility_search"
        _routing_debug["requested_service"] = requested_service
        _routing_debug["required_services"] = required_services
        _routing_debug["sub_intent"] = secondary_intent
        st.session_state["_routing_debug"] = _routing_debug

        if entities.get("district"):
            # Use deterministic facility matching with entity context
            # CRITICAL FIX: pass requested_service so explicit service requests get top ranking
            ranked_facs_with_reasons = match_and_rank_facilities(
                entities.get("district"),
                required_services=required_services,
                facility_type=entities.get("facility_type"),
                urgency=urgency,
                requested_service=requested_service,
                entities=entities
            )
            ranked_facs = [f for f, _ in ranked_facs_with_reasons]
            _routing_debug["matched_facility_count"] = len(ranked_facs)
            st.session_state["_routing_debug"] = _routing_debug
            # Generate context-aware ranked display with dynamic explanation
            return generate_ranked_facility_results(
                ranked_facs, entities, response_lang,
                requested_service=requested_service,
                secondary_intent=secondary_intent,
                ranked_with_reasons=ranked_facs_with_reasons
            )

        # No district: ask for clarification
        clarifications = build_clarifying_question(entities, primary_intent, response_lang)
        if clarifications:
            hint = '<div style="background:#F0F7FF;border:1px solid #BAE6FD;border-radius:10px;padding:12px 16px;margin-bottom:10px;">' + "<br>".join(clarifications) + "</div>"
            return hint + generate_district_locator_results(norm_q, response_lang)
        return generate_district_locator_results(norm_q, response_lang)


    # --- SCHEME_INFORMATION route ---
    if primary_intent == INTENT_SCHEME_INFORMATION:
        _routing_debug["route"] = "scheme"
        st.session_state["_routing_debug"] = _routing_debug
        return generate_schemes_guide(response_lang)

    # --- PREGNANCY route (non-emergency) ---
    if primary_intent == INTENT_PREGNANCY:
        entities["required_service"] = "Maternity"
        entities["facility_type"] = "District Hospital"
        _routing_debug["route"] = "pregnancy"
        st.session_state["_routing_debug"] = _routing_debug
        return generate_maternal_child_module(response_lang) + care_pathway_html("PHC", response_lang)

    # --- CHILD_HEALTH route ---
    if primary_intent == INTENT_CHILD_HEALTH:
        entities["required_service"] = "Pediatric"
        _routing_debug["route"] = "child_health"
        st.session_state["_routing_debug"] = _routing_debug
        # Fall through to symptom check below for child symptom queries

    # --- MEDICINE_INFORMATION route ---
    if primary_intent == INTENT_MEDICINE_INFORMATION:
        _routing_debug["route"] = "medicine"
        st.session_state["_routing_debug"] = _routing_debug
        return generate_jan_aushadhi_guide(response_lang)

    # --- ABHA route ---
    if primary_intent == INTENT_ABHA:
        _routing_debug["route"] = "abha"
        st.session_state["_routing_debug"] = _routing_debug
        return render_abha_html(response_lang)

    # Stage 6+7+8+9: Symptom check pipeline
    if primary_intent in (INTENT_SYMPTOM_CHECK, INTENT_CHILD_HEALTH):
        informational = is_informational_question(query)
        caution = informational and (urgency == "EMERGENCY")
        ranked = rank_diseases(query_for_matching, df, symptom_embeddings, name_embeddings, model)
        best_score, best_idx, row = ranked[0]
        alternatives = [alt_row["disease"] for score, idx, alt_row in ranked[1:3] if score >= 0.43 and (best_score - score) <= 0.18] if best_score >= 0.48 else []
        good_match = best_score >= 0.48
        care_level = assess_care_level(primary_intent, entities, best_score, _red_flag, _critical)
        if good_match and "health_records" in st.session_state:
            st.session_state.health_records.append({"date": datetime.now().strftime("%d %b %Y, %I:%M %p"), "query": query[:80] + ("..." if len(query) > 80 else ""), "condition": str(row["disease"]), "severity": str(row.get("severity", "N/A")).upper() if pd.notna(row.get("severity")) else "N/A"})
        # Store routing debug
        _routing_debug["route"] = "symptom_check"
        _routing_debug["care_level"] = care_level
        _routing_debug["best_score"] = round(best_score, 3)
        _routing_debug["disease_matched"] = str(row["disease"]) if best_score >= 0.48 else None
        _routing_debug["matched_facility_count"] = 0
        if entities.get("district"):
            matched_facs_with_reasons = match_and_rank_facilities(entities.get("district"), [str(row.get("recommended_facility","PHC"))], entities=entities)
            _routing_debug["matched_facility_count"] = len(matched_facs_with_reasons)
        st.session_state["_routing_debug"] = _routing_debug

        if good_match:
            structured = build_structured_response(row, entities, care_level, response_lang, alternatives)
            rec_facility = str(row.get("recommended_facility", "PHC")) if pd.notna(row.get("recommended_facility")) else "PHC"
            if "hospital" in rec_facility.lower() or "district" in rec_facility.lower(): fac_type = "DH"
            elif "sdh" in rec_facility.lower() or "sub-district" in rec_facility.lower(): fac_type = "SDH"
            elif "chc" in rec_facility.lower() or "community" in rec_facility.lower(): fac_type = "CHC"
            else: fac_type = "PHC"
            caution_html = caution_banner_html(response_lang) if caution else ""
            if response_lang != "en":
                tr = translate_safe(format_disease_plain(row), source="en", target=response_lang)
                if tr: return caution_html + structured + care_pathway_html(fac_type, response_lang)
                translated_row = translate_row_fields(row, response_lang)
                return caution_html + format_disease_card_html(row, alternatives, lang=response_lang, translated_row=translated_row) + care_pathway_html(fac_type, response_lang)
            return caution_html + structured + care_pathway_html(fac_type, response_lang)
        clarifications = build_clarifying_question(entities, primary_intent, response_lang)
        if clarifications:
            hint = '<div style="background:#F0F7FF;border:1px solid #BAE6FD;border-radius:10px;padding:12px 16px;margin-bottom:10px;">' + "<br>".join(clarifications) + "</div>"
            return hint + _build_fallback_response(response_lang)
        return _build_fallback_response(response_lang)

    return _build_fallback_response(response_lang)


def render_debug_panel():
    """Optional debug panel showing structured routing decisions. Dev only.
    Shows the complete intent→service→facility pipeline for SIH demonstration."""
    debug = st.session_state.get("_routing_debug")
    if not debug:
        return
    with st.expander("\U0001f41b Routing Debug (dev)", expanded=False):
        # Row 1: Core routing signals
        cols = st.columns(5)
        cols[0].metric("Language", debug.get("language", "?"))
        cols[1].metric("Intent", debug.get("intent", "?"))
        sub = debug.get("sub_intent")
        cols[2].metric("Sub-intent", sub if sub else "—")
        cols[3].metric("Urgency", debug.get("urgency", "?"))
        cols[4].metric("Confidence", f"{debug.get('confidence', 0):.0%}")

        # Row 2: Service routing
        cols2 = st.columns(5)
        cols2[0].metric("Route", debug.get("route", "?"))
        cols2[1].metric("Requested Service", debug.get("requested_service") or "—")
        req_svcs = debug.get("required_services", [])
        cols2[2].metric("Required Services", ", ".join(req_svcs[:3]) if req_svcs else "—")
        cols2[3].metric("Facilities", debug.get("matched_facility_count", 0))
        cols2[4].metric("Nearest", "Yes" if debug.get("nearest_requested") else "No")

        if debug.get("care_level"):
            st.caption(f"Care Level: {debug['care_level']}")
        if debug.get("disease_matched"):
            st.caption(f"Matched: {debug['disease_matched']} (score: {debug.get('best_score', 0):.3f})")
        entities = debug.get("entities", {})
        if entities:
            # Show structured intent object (SIH demo)
            structured = {
                "intent": debug.get("intent"),
                "service": debug.get("requested_service"),
                "patient_type": entities.get("age_group"),
                "district": entities.get("district"),
                "urgency": debug.get("urgency"),
                "nearest_requested": entities.get("proximity_request", False),
                "government_only": entities.get("wants_government", False),
                "confidence": debug.get("confidence"),
            }
            st.caption("Structured Intent Object:")
            st.json(structured)


def _build_fallback_response(response_lang):
    """Safe fallback when intent is unclear."""
    if response_lang == "hi":
        return '<div class="th-alert info"><div class="th-alert-icon">\U0001f4a1</div><div class="th-alert-body"><h4>मुझे समझ नहीं आया</h4><p>मैं इनमें से मदद कर सकता हूं: रुग्णालय शोधक, MJPJAY/PM-JAY योजना, गर्भवती देखभाल, जेनेरिक दवा, टेलीमेडिसिन, आरोग्य शिबिर।</p></div></div>'
    if response_lang == "mr":
        return '<div class="th-alert info"><div class="th-alert-icon">\U0001f4a1</div><div class="th-alert-body"><h4>मला समजले नाही</h4><p>मी या मदत शकतो: रुग्णालय शोधक, MJPJAY/PM-JAY योजना, गरोदर देखभाल, स्वस्त औषधे, टेलिमेडिसिन, आरोग्य शिबिर।</p></div></div>'
    return '<div class="th-alert info"><div class="th-alert-icon">\U0001f4a1</div><div class="th-alert-body"><h4>Let&#39;s narrow it down</h4><p>I can help with: rural hospital locator, MJPJAY / PM-JAY schemes, pregnancy care, generic medicine costs, telemedicine, ASHA worker services, health camps, or common disease symptoms.</p></div></div>'

# ============================================================================
# NEW MODULE RENDERERS
# ============================================================================
def render_abha_html(lang="en"):
    info = ABHA_INFO.get(lang, ABHA_INFO["en"])
    benefits = "\n".join(info["benefits"])
    steps = "\n".join(info["how_to_create"])
    return f"""<div class="th-dx-card"><div class="th-dx-header"><div class="th-dx-header-left"><div class="th-dx-header-icon">🆔</div><div><h4 class="th-dx-title">ABHA - Digital Health ID</h4><span style="font-size:0.75rem;color:#64748B;font-weight:600;">Ayushman Bharat Health Account</span></div></div><span class="th-dx-badge">FREE</span></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#EAF2FE;color:#0B6BCB;">ℹ️</div><div style="flex:1;"><strong class="th-dx-label" style="color:#0B6BCB;">What is ABHA?</strong><div class="th-dx-content">{html.escape(info["what"])}</div></div></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#E6F7F5;color:#0E9F8F;">🎁</div><div style="flex:1;"><strong class="th-dx-label" style="color:#0E9F8F;">Key Benefits</strong><div class="th-dx-content">{benefits}</div></div></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#F3EFFE;color:#6941C6;">📝</div><div style="flex:1;"><strong class="th-dx-label" style="color:#6941C6;">How to Create (5 minutes)</strong><div class="th-dx-content">{steps}</div></div></div></div>"""

def render_health_camps_html(lang="en"):
    cards = "".join(f"""<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:12px 16px;margin-bottom:10px;"><div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:6px;"><strong style="color:#0B6BCB;font-size:0.95rem;">📅 {c['name']}</strong><span style="font-size:0.7rem;background:#FEF3C7;color:#92400E;padding:2px 8px;border-radius:999px;font-weight:700;">{c['date']}</span></div><p style="font-size:0.85rem;margin:0 0 4px 0;color:#334155;"><strong>📍 Where:</strong> {c['location']}</p><p style="font-size:0.85rem;margin:0 0 4px 0;color:#334155;"><strong>🏥 Services:</strong> {c['services']}</p><p style="font-size:0.85rem;margin:0;color:#16794C;font-weight:600;"><strong>🎯 Target:</strong> {c['target']}</p></div>""" for c in HEALTH_CAMPS)
    title = "आरोग्य कार्यक्रम माहिती" if lang == "mr" else "स्वास्थ्य कार्यक्रम जानकारी" if lang == "hi" else "Government Health Programs"
    return f"""<div class="th-dx-card"><div class="th-dx-header"><div class="th-dx-header-left"><div class="th-dx-header-icon">📅</div><div><h4 class="th-dx-title">{title}</h4><span style="font-size:0.75rem;color:#64748B;font-weight:600;">Regular free screening & vaccination camps</span></div></div><span class="th-dx-badge">CAMPS</span></div><div style="padding:15px 20px;">{cards}</div></div>"""

def render_helpline_guide(lang="en"):
    if lang == "mr":
        return """<div class="th-alert info"><div class="th-alert-icon">📱</div><div class="th-alert-body"><h4>आपत्कालीन हेल्पलाइन व संपर्क मार्गदर्शक</h4><p><strong>1. आपत्कालीन रुग्णवाहिका:</strong> <a href="tel:108" style="color:#DC2626;font-weight:700;">108</a> वर त्वरित कॉल करा (मोफत, 24x7)
<strong>2. आरोग्य सल्ला हेल्पलाइन:</strong> <a href="tel:104" style="color:#0B6BCB;font-weight:700;">104</a> वर कॉल करा (मोफत, 24x7)
<strong>3. जननी एक्सप्रेस:</strong> गरोदर आपत्कालीन <a href="tel:102" style="color:#0B6BCB;font-weight:700;">102</a> वर कॉल करा
<strong>4. बाल हेल्पलाइन:</strong> <a href="tel:1098" style="color:#0B6BCB;font-weight:700;">1098</a>
<strong>5. महिला हेल्पलाइन:</strong> <a href="tel:181" style="color:#0B6BCB;font-weight:700;">181</a></p></div></div>"""
    if lang == "hi":
        return """<div class="th-alert info"><div class="th-alert-icon">📱</div><div class="th-alert-body"><h4>आपातकालीन हेल्पलाइन और संपर्क मार्गदर्शक</h4><p><strong>1. एम्बुलेंस:</strong> <a href="tel:108" style="color:#DC2626;font-weight:700;">108</a> पर तुरंत कॉल करें (मुफ्त, 24x7)
<strong>2. स्वास्थ्य सलाह:</strong> <a href="tel:104" style="color:#0B6BCB;font-weight:700;">104</a> पर कॉल करें (मुफ्त, 24x7)
<strong>3. जननी एक्सप्रेस:</strong> <a href="tel:102" style="color:#0B6BCB;font-weight:700;">102</a> पर कॉल करें
<strong>4. बाल हेल्पलाइन:</strong> <a href="tel:1098" style="color:#0B6BCB;font-weight:700;">1098</a>
<strong>5. महिला हेल्पलाइन:</strong> <a href="tel:181" style="color:#0B6BCB;font-weight:700;">181</a></p></div></div>"""
    return """<div class="th-alert info"><div class="th-alert-icon">📱</div><div class="th-alert-body"><h4>Emergency Helplines & Contact Guide</h4><p><strong>1. Ambulance:</strong> Call <a href="tel:108" style="color:#DC2626;font-weight:700;">108</a> immediately (free, 24x7)
<strong>2. Health Advice Helpline:</strong> Call <a href="tel:104" style="color:#0B6BCB;font-weight:700;">104</a> (free, 24x7)
<strong>3. Janani Express:</strong> Call <a href="tel:102" style="color:#0B6BCB;font-weight:700;">102</a> for pregnancy emergencies
<strong>4. Child Helpline:</strong> <a href="tel:1098" style="color:#0B6BCB;font-weight:700;">1098</a>
<strong>5. Women Helpline:</strong> <a href="tel:181" style="color:#0B6BCB;font-weight:700;">181</a>
<strong>6. ASHA Worker:</strong> Contact your village Panchayat or Anganwadi center for ASHA worker details</p></div></div>"""

@st.cache_resource(show_spinner=False)
def load_model():
    try:
        from sentence_transformers import SentenceTransformer
        return SentenceTransformer("all-MiniLM-L6-v2")
    except Exception: return None

@st.cache_data(show_spinner=False)
def load_data():
    try: df = pd.read_csv("disease_dataset.csv")
    except Exception: st.error("⚠️ Could not read disease_dataset.csv."); st.stop()
    if missing := [col for col in REQUIRED_COLUMNS if col not in df.columns]:
        st.error(f"Missing required columns: {', '.join(missing)}"); st.stop()
    for col in ENHANCED_COLUMNS:
        if col not in df.columns:
            df[col] = None
    return df

df = load_data()

MODE_ENGLISH, MODE_HINDI, MODE_MARATHI, MODE_AUTO = "English", "हिंदी (Hindi)", "मराठी (Marathi)", "🌐 Auto-detect"
LANGUAGES = [MODE_ENGLISH, MODE_HINDI, MODE_MARATHI, MODE_AUTO]

# ============================================================================
# UI INTERNATIONALIZATION — ALL VISIBLE TEXT IN 3 LANGUAGES
# ============================================================================
UI_STRINGS = {
    "en": {
        "hero_badge": "Smart India Hackathon · Accessibility & Quality of Rural Public Healthcare",
        "hero_title": "MahaArogya Setu — Rural Healthcare Access Platform",
        "hero_sub": "Bridging the healthcare gap in Maharashtra\'s rural & tribal regions. Find hospitals, access government schemes (MJPJAY/PM-JAY), get maternal care, telemedicine consultations, and emergency support — all in your language.",
        "tag_facility": "🏥 Facility Locator", "tag_schemes": "📋 6 Health Schemes",
        "tag_mch": "🤰 Maternal & Child Health", "tag_tele": "📞 Telemedicine Guide",
        "tag_med": "💊 Jan Aushadhi Info", "tag_low": "📴 Low-Bandwidth Mode",
        "tab_chat": "💬 Consult AI", "tab_loc": "🏥 Facility Locator",
        "tab_sch": "📋 Schemes", "tab_mch": "🤰 Maternal & Child", "tab_more": "🎯 More Services",
        "st_abha": "🆔 ABHA ID", "st_camp": "📅 Health Programs", "st_med": "💊 Generic Meds",
        "st_help": "📱 Helpline Guide", "st_log": "📓 Session Log", "st_map": "🗺️ Roadmap",
        "welcome_title": "How can we help you today?",
        "welcome_sub": "Describe your symptoms in EN/HI/MR or ask about hospitals, schemes, or services.",
        "sec_quick": "💡 Popular Quick Actions", "sec_cont": "💡 Continue with",
        "btn_clear": "🗑️ Clear Chat", "btn_clear_rec": "🗑️ Clear All Records",
        "status_line": "💬 Active Consultation • {n} exchanges • {r} records saved",
        "analyzing": "Analyzing query & consulting rural healthcare database...",
        "voice_hint": "🎙️ <strong>Voice input available</strong> — click the mic icon inside the text box to speak your symptoms in EN / HI / MR",
        "sb_conn": "📶 Connectivity Mode", "sb_low": "📴 Low-Bandwidth Mode",
        "sb_low_help": "For 2G/weak network areas — bypasses AI models & translation APIs for faster response. Still requires server connection.",
        "sb_lang": "🌐 Language / भाषा", "sb_auto": "✨ Auto-detects EN/HI/MR/Hinglish",
        "sb_emerg": "🚑 24×7 Emergency Helplines",
        "sb_disc": "⚕️ <em>General awareness only — not a diagnosis.</em>",
        "loc_title": "🏥 Rural & Tribal Health Facility Reference Directory",
        "loc_desc": "Reference directory of District Hospitals, SDHs, CHCs & PHCs across Maharashtra\'s underserved regions — verify details before visiting",
        "loc_ref": "ℹ️ Facility data is for reference. Please verify phone numbers and services before visiting. Data sourced from public health directories.",
        "loc_sel": "📍 Select District / Region:", "loc_show": "Showing <strong>{c} reference facilities</strong> in <strong>{d}</strong>",
        "sch_title": "📋 Maharashtra Government Health Schemes",
        "sch_desc": "Reference information on cashless treatment schemes. Verify current details at your nearest government hospital or pmjay.gov.in.",
        "anc_title": "🤰 Antenatal Care (ANC) Schedule",
        "anc_desc": "Reference schedule — based on public health guidelines. Confirm with your local PHC/CHC.",
        "uip_title": "💉 Universal Immunization Programme (UIP)",
        "uip_desc": "Reference schedule based on UIP guidelines. Confirm with your local PHC/CHC for current availability.",
        "abha_sec": "🆔 Ayushman Bharat Health Account (ABHA) Guide",
        "abha_card": "🆔 Free 14-Digit Digital Health ID",
        "abha_ben": "🎁 Benefits:", "abha_how": "📝 How to Create (5 mins):",
        "camp_sec": "📅 Government Health Programs",
        "camp_desc": "Recurring free screening, immunization & specialist programs. Contact your local PHC/CHC for specific schedules and locations.",
        "med_sec": "💊 Jan Aushadhi Generic Medicine Guide",
        "med_desc": "Reference price comparison for essential medicines. Actual prices may vary — verify at your local Jan Aushadhi Kendra.",
        "med_loc": "📍 <strong>Locate stores:</strong> Download \'Jan Aushadhi Sugam\' app or visit <strong>janaushadhi.gov.in</strong>",
        "med_note": "ℹ️ Prices shown are indicative reference estimates (source: Jan Aushadhi price lists, may not reflect current MRP). Verify actual prices and availability at your local Jan Aushadhi Kendra. Prescription medicines require a doctor's prescription.",
        "help_sec": "📱 Emergency Helplines & Contact Guide",
        "help_desc": "How to reach emergency and public health services when internet access is limited",
        "low_card": "📴 Also Try: Low-Bandwidth Mode",
        "low_desc": "Toggle \"📴 Low-Bandwidth Offline Mode\" in the sidebar. It bypasses heavy AI models and translation APIs for faster response on 2G networks. Still requires a server connection.",
        "log_sec": "📓 Session Symptom Log",
        "log_desc": "Automatically logs symptom queries during this session. Data is ephemeral — lost on page refresh. Privacy-first: NOT stored on servers.",
        "log_empty": "📭 No records yet. Ask about symptoms in the <strong>💬 Consult AI</strong> tab and they\'ll appear here.",
        "map_sec": "🗺️ Feature Status & Roadmap",
        "map_desc": "Current implementation status of each feature module",
        "sys_err": "An unexpected error occurred. For urgent help, call <strong>108</strong>.",
    },
    "hi": {
        "hero_badge": "स्मार्ट इंडिया हैकाथॉन · ग्रामीण सार्वजनिक स्वास्थ्य सेवा की गुणवत्ता",
        "hero_title": "महाआरोग्य सेतु — ग्रामीण स्वास्थ्य सेवा प्लेटफॉर्म",
        "hero_sub": "महाराष्ट्र के ग्रामीण और आदिवासी क्षेत्रों में स्वास्थ्य सेवा की कमी को पूरा करना। अस्पताल खोजें, सरकारी योजनाओं (MJPJAY/PM-JAY) का लाभ लें, मातृ स्वास्थ्य, टेलीमेडिसिन और आपातकालीन सहायता — आपकी भाषा में।",
        "tag_facility": "🏥 अस्पताल खोजें", "tag_schemes": "📋 6 स्वास्थ्य योजनाएं",
        "tag_mch": "🤰 मातृ एवं शिशु स्वास्थ्य", "tag_tele": "📞 टेलीमेडिसिन गाइड",
        "tag_med": "💊 जन औषधि जानकारी", "tag_low": "📴 कम बैंडविड्थ मोड",
        "tab_chat": "💬 AI से पूछें", "tab_loc": "🏥 अस्पताल खोजें",
        "tab_sch": "📋 योजनाएं", "tab_mch": "🤰 मातृ एवं शिशु", "tab_more": "🎯 अन्य सेवाएं",
        "st_abha": "🆔 ABHA आईडी", "st_camp": "📅 स्वास्थ्य कार्यक्रम", "st_med": "💊 जेनेरिक दवाइयां",
        "st_help": "📱 हेल्पलाइन गाइड", "st_log": "📓 सत्र लॉग", "st_map": "🗺️ रोडमैप",
        "welcome_title": "आज हम आपकी कैसे मदद कर सकते हैं?",
        "welcome_sub": "अपने लक्षण हिंदी, मराठी या अंग्रेजी में टाइप करें या बोलें।",
        "sec_quick": "💡 लोकप्रिय त्वरित कार्य", "sec_cont": "💡 इनमें से पूछें",
        "btn_clear": "🗑️ चैट साफ़ करें", "btn_clear_rec": "🗑️ सभी रिकॉर्ड साफ़ करें",
        "status_line": "💬 सक्रिय परामर्श • {n} बातचीत • {r} रिकॉर्ड सहेजे गए",
        "analyzing": "प्रश्न का विश्लेषण हो रहा है और ग्रामीण स्वास्थ्य डेटाबेस देखा जा रहा है...",
        "voice_hint": "🎙️ <strong>वॉइस इनपुट उपलब्ध</strong> — टेक्स्ट बॉक्स के अंदर माइक आइकन पर क्लिक करके अपने लक्षण बोलें",
        "sb_conn": "📶 कनेक्टिविटी मोड", "sb_low": "📴 कम बैंडविड्थ मोड",
        "sb_low_help": "2G/कमज़ोर नेटवर्क के लिए — AI मॉडल और अनुवाद API को बायपास करता है। सर्वर कनेक्शन जरूरी।",
        "sb_lang": "🌐 भाषा चुनें", "sb_auto": "✨ स्वतः पहचान: EN/HI/MR/हिंगलिश",
        "sb_emerg": "🚑 24×7 आपातकालीन हेल्पलाइन",
        "sb_disc": "⚕️ <em>केवल सामान्य जानकारी — निदान नहीं।</em>",
        "loc_title": "🏥 ग्रामीण एवं आदिवासी सरकारी स्वास्थ्य सुविधा निर्देशिका",
        "loc_desc": "महाराष्ट्र के कम सेवा वाले क्षेत्रों में जिला अस्पताल, SDH, CHC और PHC की निर्देशिका",
        "loc_ref": "ℹ️ सुविधा डेटा संदर्भ के लिए है। कृपया जाने से पहले फोन नंबर और सेवाओं की पुष्टि करें।",
        "loc_sel": "📍 जिला / क्षेत्र चुनें:", "loc_show": "<strong>{d}</strong> में <strong>{c} संदर्भ सुविधाएं</strong> दिखा रहे हैं",
        "sch_title": "📋 महाराष्ट्र सरकारी स्वास्थ्य योजनाएं",
        "sch_desc": "कैशलेस उपचार योजनाओं की संदर्भ जानकारी। नवीनतम विवरण अपने नजदीकी सरकारी अस्पताल या pmjay.gov.in पर सत्यापित करें।",
        "anc_title": "🤰 प्रसवपूर्व देखभाल (ANC) अनुसूची",
        "anc_desc": "संदर्भ अनुसूची — सार्वजनिक स्वास्थ्य दिशानिर्देशों पर आधारित। अपने स्थानीय PHC/CHC से पुष्टि करें।",
        "uip_title": "💉 सार्वजनिक टीकाकरण कार्यक्रम (UIP)",
        "uip_desc": "UIP दिशानिर्देशों पर आधारित संदर्भ अनुसूची। अपने स्थानीय PHC/CHC से पुष्टि करें।",
        "abha_sec": "🆔 आयुष्मान भारत हेल्थ अकाउंट (ABHA) गाइड",
        "abha_card": "🆔 मुफ्त 14-अंकीय डिजिटल हेल्थ आईडी",
        "abha_ben": "🎁 फायदे:", "abha_how": "📝 कैसे बनाएं (5 मिनट):",
        "camp_sec": "📅 सरकारी स्वास्थ्य कार्यक्रम",
        "camp_desc": "नियमित मुफ्त स्क्रीनिंग, टीकाकरण और विशेषज्ञ कार्यक्रम। विशेष अनुसूची के लिए अपने स्थानीय PHC/CHC से संपर्क करें।",
        "med_sec": "💊 जन औषधि जेनेरिक दवा गाइड",
        "med_desc": "आवश्यक दवाओं की संदर्भ मूल्य तुलना। वास्तविक कीमतें भिन्न हो सकती हैं।",
        "med_loc": "📍 <strong>स्टोर खोजें:</strong> \'Jan Aushadhi Sugam\' ऐप डाउनलोड करें या <strong>janaushadhi.gov.in</strong> पर जाएं",
        "med_note": "ℹ️ दिखाए गए मूल्य सांकेतिक अनुमान हैं। वास्तविक कीमतें भिन्न हो सकती हैं।",
        "help_sec": "📱 आपातकालीन हेल्पलाइन और संपर्क मार्गदर्शक",
        "help_desc": "जब इंटरनेट सीमित हो तो आपातकालीन और सार्वजनिक स्वास्थ्य सेवाओं तक कैसे पहुंचें",
        "low_card": "📴 कम बैंडविड्थ मोड भी आज़माएं",
        "low_desc": "साइडबार में \"📴 कम बैंडविड्थ मोड\" टॉगल करें। यह 2G नेटवर्क पर तेज़ प्रतिक्रिया के लिए AI मॉडल को बायपास करता है।",
        "log_sec": "📓 सत्र लक्षण लॉग",
        "log_desc": "इस सत्र के दौरान लक्षण प्रश्न स्वचालित रूप से लॉग होते हैं। डेटा अस्थायी है — पेज रिफ्रेश पर खो जाता है।",
        "log_empty": "📭 अभी तक कोई रिकॉर्ड नहीं। <strong>💬 AI से पूछें</strong> टैब में लक्षण पूछें।",
        "map_sec": "🗺️ फीचर स्थिति और रोडमैप",
        "map_desc": "प्रत्येक फीचर मॉड्यूल की वर्तमान कार्यान्वयन स्थिति",
        "sys_err": "एक अप्रत्याशित त्रुटि हुई। तत्काल सहायता के लिए <strong>108</strong> पर कॉल करें।",
    },
    "mr": {
        "hero_badge": "स्मार्ट इंडिया हॅकाथॉन · ग्रामीण सार्वजनिक आरोग्य सेवा गुणवत्ता",
        "hero_title": "महाआरोग्य सेतु — ग्रामीण आरोग्य सेवा प्लॅटफॉर्म",
        "hero_sub": "महाराष्ट्रातील ग्रामीण आणि आदिवासी भागात आरोग्य सेवेच्या कमतरता भरून काढणे. रुग्णालये शोधा, सरकारी योजना (MJPJAY/PM-JAY) मिळवा, मातृ आरोग्य, टेलिमेडिसिन आणि आणीबाणी मदत — तुमच्या भाषेत.",
        "tag_facility": "🏥 रुग्णालय शोधा", "tag_schemes": "📋 ६ आरोग्य योजना",
        "tag_mch": "🤰 माता व बाल आरोग्य", "tag_tele": "📞 टेलिमेडिसिन मार्गदर्शक",
        "tag_med": "💊 जन औषधी माहिती", "tag_low": "📴 कमी बँडविड्थ मोड",
        "tab_chat": "💬 AI ला विचारा", "tab_loc": "🏥 रुग्णालय शोधा",
        "tab_sch": "📋 योजना", "tab_mch": "🤰 माता व बाल", "tab_more": "🎯 इतर सेवा",
        "st_abha": "🆔 ABHA आयडी", "st_camp": "📅 आरोग्य कार्यक्रम", "st_med": "💊 जेनेरिक औषधे",
        "st_help": "📱 हेल्पलाइन मार्गदर्शक", "st_log": "📓 सत्र लॉग", "st_map": "🗺️ रोडमॅप",
        "welcome_title": "आज आम्ही तुम्हाला कशी मदत करू शकतो?",
        "welcome_sub": "तुमची लक्षणे मराठी, हिंदी किंवा इंग्रजीत सांगा.",
        "sec_quick": "💡 लोकप्रिय जलद कृती", "sec_cont": "💡 यापैकी विचारा",
        "btn_clear": "🗑️ चॅट साफ करा", "btn_clear_rec": "🗑️ सर्व रेकॉर्ड साफ करा",
        "status_line": "💬 सक्रिय सल्ला • {n} संवाद • {r} रेकॉर्ड साठवले",
        "analyzing": "प्रश्नाचे विश्लेषण होत आहे आणि ग्रामीण आरोग्य डेटाबेस तपासला जात आहे...",
        "voice_hint": "🎙️ <strong>व्हॉइस इनपुट उपलब्ध</strong> — टेक्स्ट बॉक्समधील मायक आयकॉनवर क्लिक करून तुमची लक्षणे सांगा",
        "sb_conn": "📶 कनेक्टिव्हिटी मोड", "sb_low": "📴 कमी बँडविड्थ मोड",
        "sb_low_help": "2G/कमकुवत नेटवर्कसाठी — AI मॉडेल आणि अनुवाद API बायपास करतो. सर्व्हर कनेक्शन आवश्यक.",
        "sb_lang": "🌐 भाषा निवडा", "sb_auto": "✨ स्वयंओळख: EN/HI/MR/हिंगलिश",
        "sb_emerg": "🚑 24×7 आणीबाणी हेल्पलाइन",
        "sb_disc": "⚕️ <em>फक्त सामान्य माहिती — निदान नाही.</em>",
        "loc_title": "🏥 ग्रामीण व आदिवासी शासकीय आरोग्य सुविधा निर्देशिका",
        "loc_desc": "महाराष्ट्रातील कमी सेवा असलेल्या भागातील जिल्हा रुग्णालये, SDH, CHC आणि PHC",
        "loc_ref": "ℹ️ सुविधा डेटा संदर्भासाठी आहे. कृपया जाण्यापूर्वी फोन नंबर आणि सेवा तपासा.",
        "loc_sel": "📍 जिल्हा / क्षेत्र निवडा:", "loc_show": "<strong>{d}</strong> मध्ये <strong>{c} संदर्भ सुविधा</strong> दर्शवत आहे",
        "sch_title": "📋 महाराष्ट्र शासकीय आरोग्य योजना",
        "sch_desc": "कॅशलेस उपचार योजनांची संदर्भ माहिती. नवीनतम माहितीसाठी जवळच्या शासकीय रुग्णालयात तपासा.",
        "anc_title": "🤰 गरोदरपूर्व काळजी (ANC) वेळापत्रक",
        "anc_desc": "संदर्भ वेळापत्रक — सार्वजनिक आरोग्य मार्गदर्शक तत्त्वांवर आधारित. तुमच्या स्थानिक PHC/CHC शी पडताळणी करा.",
        "uip_title": "💉 सार्वजनिक लसीकरण कार्यक्रम (UIP)",
        "uip_desc": "UIP मार्गदर्शक तत्त्वांवर आधारित संदर्भ वेळापत्रक. तुमच्या स्थानिक PHC/CHC शी पडताळणी करा.",
        "abha_sec": "🆔 आयुष्मान भारत हेल्थ अकाउंट (ABHA) मार्गदर्शक",
        "abha_card": "🆔 विनामूल्य १४-अंकी डिजिटल आरोग्य ओळखपत्र",
        "abha_ben": "🎁 फायदे:", "abha_how": "📝 कसे तयार करायचे (५ मिनिटे):",
        "camp_sec": "📅 शासकीय आरोग्य कार्यक्रम",
        "camp_desc": "नियमित मोफत तपासणी, लसीकरण आणि तज्ञ कार्यक्रम. विशेष वेळापत्रकासाठी तुमच्या स्थानिक PHC/CHC शी संपर्क साधा.",
        "med_sec": "💊 जन औषधी जेनेरिक औषध मार्गदर्शक",
        "med_desc": "आवश्यक औषधांची संदर्भ किमत तुलना. प्रत्यक्ष किमती भिन्न असू शकतात.",
        "med_loc": "📍 <strong>स्टोर शोधा:</strong> \'Jan Aushadhi Sugam\' अॅप डाउनलोड करा किंवा <strong>janaushadhi.gov.in</strong> ला भेट द्या",
        "med_note": "ℹ️ दर्शवलेल्या किमती सांकेतिक अंदाज आहेत. प्रत्यक्ष किमती भिन्न असू शकतात.",
        "help_sec": "📱 आणीबाणी हेल्पलाइन आणि संपर्क मार्गदर्शक",
        "help_desc": "इंटरनेट मर्यादित असताना आणीबाणी आणि सार्वजनिक आरोग्य सेवा कशा मिळवाल",
        "low_card": "📴 कमी बँडविड्थ मोडही वापरा",
        "low_desc": "साइडबारमध्ये \"📴 कमी बँडविड्थ मोड\" टॉगल करा. हे 2G नेटवर्कवर जलद प्रतिसादासाठी AI मॉडेल बायपास करतो.",
        "log_sec": "📓 सत्र लक्षण लॉग",
        "log_desc": "या सत्रात लक्षण प्रश्न स्वयंचलितपणे लॉग होतात. डेटा तात्पुरता आहे — पृष्ठ रिफ्रेशवर नष्ट होतो.",
        "log_empty": "📭 अजून कोणतेही रेकॉर्ड नाहीत. <strong>💬 AI ला विचारा</strong> टॅबमध्ये लक्षणे विचारा.",
        "map_sec": "🗺️ फीचर स्थिती आणि रोडमॅप",
        "map_desc": "प्रत्येक फीचर मॉड्यूलची सध्याची कार्यान्वयन स्थिती",
        "sys_err": "एक अनपेक्षित त्रुटी आली. तात्काळ मदतीसाठी <strong>108</strong> वर कॉल करा.",
    }
}

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


# ============================================================================
# SIDEBAR
# ============================================================================
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
    if language.startswith("🌐"): st.caption(_ui("sb_auto"))
    st.session_state["_ui_lang"] = "hi" if language == MODE_HINDI else "mr" if language == MODE_MARATHI else "en"

    st.markdown("""<div class="th-sb-divider"></div><div class="th-sb-title">""" + _ui("sb_emerg") + """</div>
        <a href="tel:108" class="th-help-card critical"><span class="th-help-label">🚑 Ambulance (MEMS)</span><span class="th-help-num">108</span></a>
        <a href="tel:102" class="th-help-card critical"><span class="th-help-label">🤰 Janani Express</span><span class="th-help-num">102</span></a>
        <a href="tel:104" class="th-help-card"><span class="th-help-label">🏥 MH Health Line</span><span class="th-help-num">104</span></a>
        <a href="tel:1098" class="th-help-card"><span class="th-help-label">🧒 Child Helpline</span><span class="th-help-num">1098</span></a>
        <a href="tel:181" class="th-help-card"><span class="th-help-label">👩 Women Helpline</span><span class="th-help-num">181</span></a>
        <div class="th-sb-divider"></div><div style="font-size:0.74rem;color:#64748B;">""" + _ui("sb_disc") + """</div>""", unsafe_allow_html=True)

# ============================================================================
# REBRANDED HERO HEADER
# ============================================================================
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

if "history" not in st.session_state: st.session_state.history = []
if "prefill_query" not in st.session_state: st.session_state.prefill_query = None
if "health_records" not in st.session_state: st.session_state.health_records = []
if "conversation_context" not in st.session_state: st.session_state.conversation_context = {}

# ============================================================================
# MAIN TABBED INTERFACE — 5 TABS
# ============================================================================
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

# ============================================================================
# MICROPHONE JS COMPONENT
# ============================================================================
@st.cache_data(show_spinner=False)
def _mic_component(lang_code: str):
    return """<div id="mic-root" style="display:none"></div>
<script>
(function(){
  var host = window.parent.document;
  var win  = window.parent;
  var SR   = win.SpeechRecognition || win.webkitSpeechRecognition;
  if (!SR) return;

  if (!host.getElementById('th-mic-style')) {
    var s = host.createElement('style');
    s.id = 'th-mic-style';
    s.textContent = ''
      + '[data-testid="stChatInput"] form { position: relative !important; overflow: visible !important; }'
      + '[data-testid="stChatInput"] > div { overflow: visible !important; }'
      + '#th-mic-btn {'
      + '  position: absolute; right: 50px; top: 50%; transform: translateY(-50%);'
      + '  width: 32px; height: 32px; border-radius: 50%;'
      + '  border: 1.5px solid #CBD5E1; background: #FFFFFF; color: #0B6BCB;'
      + '  font-size: 15px; cursor: pointer; z-index: 99999; padding: 0;'
      + '  box-shadow: 0 1px 4px rgba(0,0,0,0.06);'
      + '  display: flex; align-items: center; justify-content: center;'
      + '  transition: background .15s, border-color .15s;'
      + '}'
      + '#th-mic-btn:hover { background: #EAF2FE; border-color: #0B6BCB; }'
      + '#th-mic-btn.listening {'
      + '  background: #DC2626; border-color: #DC2626; color: #FFFFFF;'
      + '  animation: th_pulse 1.2s infinite;'
      + '}'
      + '@keyframes th_pulse {'
      + '  0%  { box-shadow: 0 0 0 0 rgba(220,38,38,0.45); }'
      + '  70% { box-shadow: 0 0 0 10px rgba(220,38,38,0); }'
      + '  100%{ box-shadow: 0 0 0 0 rgba(220,38,38,0); }'
      + '}'
      + '#th-bubble {'
      + '  position: fixed; display: none; background: #FFFFFF; color: #0F172A;'
      + '  border: 1.5px solid #CBD5E1; border-radius: 12px;'
      + '  padding: 10px 16px; font-size: 14px; max-width: 320px;'
      + '  word-wrap: break-word;'
      + '  box-shadow: 0 8px 24px rgba(15,23,42,0.14); z-index: 999999;'
      + '}'
      + '#th-bubble.show { display: block; }';
    host.head.appendChild(s);
  }

  var btn = host.getElementById('th-mic-btn') || host.createElement('button');
  btn.id = 'th-mic-btn';
  btn.type = 'button';
  btn.innerHTML = '\U0001F399\uFE0F';
  btn.title = 'Speak your symptoms';

  var bubble = host.getElementById('th-bubble') || host.createElement('div');
  bubble.id = 'th-bubble';
  if (!bubble.parentNode) host.body.appendChild(bubble);

  var injected = false;
  function injectMic() {
    if (injected) return;
    var form = host.querySelector('[data-testid="stChatInput"] form');
    if (!form) form = host.querySelector('[data-testid="stChatInput"] > div');
    if (!form) return;
    form.appendChild(btn);
    injected = true;
    var ta = host.querySelector('[data-testid="stChatInput"] textarea');
    if (ta && ta.dataset.padded !== '1') {
      ta.dataset.padded = '1';
      ta.style.paddingRight = '88px';
    }
  }
  var injTimer = setInterval(function(){ injectMic(); if (injected) clearInterval(injTimer); }, 400);

  var listening = false, rec = null, ft = '';

  function deliver(t) {
    try {
      var ta = host.querySelector('[data-testid="stChatInput"] textarea');
      if (!ta) return;
      Object.getOwnPropertyDescriptor(win.HTMLTextAreaElement.prototype, 'value').set.call(ta, t);
      ta.dispatchEvent(new Event('input', { bubbles: true }));
      setTimeout(function(){
        var sendBtn = host.querySelector('[data-testid="stChatInputSubmitButton"]');
        if (sendBtn) sendBtn.click();
      }, 200);
    } catch (e) {}
  }

  btn.onclick = function (e) {
    e.preventDefault();
    e.stopPropagation();
    if (listening) { if (rec) rec.stop(); return; }

    ft = '';
    rec = new SR();
    rec.lang = '__LANG__';
    rec.interimResults = true;
    rec.continuous = false;

    rec.onstart = function () {
      listening = true;
      btn.classList.add('listening');
      btn.innerHTML = '\u23F9';
    };

    rec.onend = function () {
      listening = false;
      btn.classList.remove('listening');
      btn.innerHTML = '\U0001F399\uFE0F';
      bubble.classList.remove('show');
    };

    rec.onresult = function (ev) {
      var interim = '';
      for (var i = ev.resultIndex; i < ev.results.length; i++) {
        if (ev.results[i].isFinal) ft += ev.results[i][0].transcript;
        else interim += ev.results[i][0].transcript;
      }
      if (interim) {
        bubble.innerHTML = '\U0001F399\uFE0F ' + interim;
        bubble.classList.add('show');
        var inpRect = host.querySelector('[data-testid="stChatInput"]').getBoundingClientRect();
        bubble.style.bottom = (win.innerHeight - inpRect.top + 12) + 'px';
        bubble.style.right  = (win.innerWidth - inpRect.right + 16) + 'px';
      }
      if (ft.trim()) {
        deliver(ft.trim());
        rec.stop();
      }
    };

    rec.onerror = function () {
      listening = false;
      btn.classList.remove('listening');
      btn.innerHTML = '\U0001F399\uFE0F';
      bubble.classList.remove('show');
    };

    rec.start();
  };
})();
</script>""".replace("__LANG__", lang_code or "en-IN")

import streamlit.components.v1 as components
components.html(_mic_component(web_speech_lang(language)), height=0)

# ============================================================================
# CHAT INPUT & RESPONSE PIPELINE
# ============================================================================
placeholder_text = ("अपने लक्षण या स्वास्थ्य प्रश्न बताएं..." if language == MODE_HINDI else "तुमची लक्षणे किंवा आरोग्य प्रश्न सांगा..." if language == MODE_MARATHI else "Type your symptoms or ask about hospitals, schemes, ABHA...")
st.markdown(f"""<div style="text-align:center;margin-bottom:4px;padding:6px 0;">
    <span style="font-size:0.78rem;color:#64748B;background:#F8FAFC;border:1px solid #E2E8F0;padding:4px 14px;border-radius:999px;">
        {_ui("voice_hint")}
    </span>
</div>""", unsafe_allow_html=True)
query = st.chat_input(placeholder_text)

@st.cache_resource(show_spinner=False)
def _load_matcher_resources():
    """Cache-safe: loads model + embeddings without session_state dependency."""
    model = load_model()
    if not model: return None, None, None
    try: return model, model.encode(df["symptoms"].tolist(), convert_to_tensor=True), model.encode(df["disease"].tolist(), convert_to_tensor=True)
    except Exception: return None, None, None

def get_matcher():
    """Per-session wrapper: respects low_bandwidth toggle without polluting cache."""
    if st.session_state.get("low_bandwidth", False): return None, None, None
    return _load_matcher_resources()

used_voice, final_query = False, query

if final_query is None and st.session_state.prefill_query:
    final_query, st.session_state.prefill_query = st.session_state.prefill_query, None

if final_query:
    # Input validation
    if len(final_query) > 500:
        final_query = final_query[:500]
        st.toast("⚠️ Query truncated to 500 characters.", icon="⚠️")
    user_display = f"🎙️ *{html.escape(final_query)}*" if used_voice else html.escape(final_query)
    st.session_state.history.append(("user", user_display))
    with st.chat_message("user", avatar="🧑"): st.markdown(user_display)
    with st.chat_message("assistant", avatar="🩺"):
        with st.spinner(_ui("analyzing")):
            model, symptom_embeddings, name_embeddings = get_matcher()
            try:
                response = generate_response(final_query, language, df, symptom_embeddings, name_embeddings, model)
            except Exception as e:
                response = f'<div class="th-alert caution"><h4>{_ui("sys_err")}</h4></div>'
        st.session_state.history.append(("assistant", response))
        if len(st.session_state.history) > 50: st.session_state.history = st.session_state.history[-50:]
        st.markdown(response, unsafe_allow_html=True)
