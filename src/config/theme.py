"""Design system, CSS styling, and Streamlit page config matching modern clinical healthcare landing reference."""
import streamlit as st

CUSTOM_CSS = """
<style>
  @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

  :root {
    color-scheme: light !important;
    --primary-teal: #00D2B4;
    --primary-teal-dark: #00A892;
    --primary-teal-deep: #0B5C54;
    --primary-teal-light: #E0F8F4;
    --mint-soft: #F2FBF9;
    --deep-slate: #0B2528;
    --dark-forest: #071E20;
    --slate-subtle: #3D585B;
    --accent-amber: #D97706;
    --accent-red: #E53E3E;
    --bg-main: #F4FAF9;
    --card-bg: #FFFFFF;
    --text-main: #0B2528;
    --text-muted: #4E686A;
    --border-subtle: #D8EEE9;
    --border-card: #E1F2EE;
    --shadow-sm: 0 2px 8px rgba(11,37,40,0.03);
    --shadow-md: 0 6px 20px rgba(11,37,40,0.05);
    --shadow-lg: 0 12px 36px rgba(11,37,40,0.08);
  }

  html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif !important;
  }

  html, body {
    overflow-y: auto !important;
    overflow-x: hidden !important;
    scroll-behavior: smooth;
  }

  .stApp {
    overflow-y: auto !important;
  }

  [data-testid="stAppViewContainer"],
  section.main {
    overflow-y: auto !important;
    overflow-x: hidden !important;
    scroll-behavior: smooth;
  }

  .stApp, [data-testid="stAppViewContainer"], .main, .main .block-container {
    background-color: var(--bg-main) !important;
    color: var(--text-main) !important;
  }

  #MainMenu, footer, [data-testid="stDecoration"] { display: none !important; }
  
  /* ── Streamlit Top Header & Transparent Bar ── */
  header[data-testid="stHeader"],
  [data-testid="stHeader"],
  .stAppHeader {
    background: transparent !important;
    background-color: transparent !important;
    box-shadow: none !important;
    border: none !important;
    height: 3.5rem !important;
    position: fixed !important;
    top: 0 !important;
    left: 0 !important;
    right: 0 !important;
    z-index: 99999 !important;
    pointer-events: none !important;
  }
  header[data-testid="stHeader"] > div,
  .stAppHeader > div {
    background: transparent !important;
    background-color: transparent !important;
    box-shadow: none !important;
    border: none !important;
  }

  /* Hide ONLY Deploy button & Main Menu cleanly without hiding sidebar toggles or toolbar container */
  .stAppDeployButton,
  [data-testid="stAppDeployButton"],
  button[data-testid="stDeployButton"],
  header button[title="Deploy"],
  .stDeployButton,
  #stDeployButton,
  #MainMenu,
  [data-testid="stMainMenu"],
  [data-testid="manage-app-button"] {
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
  }

  /* Ensure toolbar stays transparent, active, and allows the expand sidebar button to be clicked */
  [data-testid="stToolbar"],
  .stAppToolbar {
    background: transparent !important;
    background-color: transparent !important;
    box-shadow: none !important;
    border: none !important;
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
  }

  /* ── Streamlit Sidebar Toggle Controls (Always Visible, Pinned & Accessible) ── */
  [data-testid="stExpandSidebarButton"],
  [data-testid="stExpandSidebarButton"] button,
  button[data-testid="stExpandSidebarButton"],
  [data-testid="collapsedControl"],
  [data-testid="collapsedControl"] button,
  button[aria-label="Open sidebar"],
  button[aria-label="Close sidebar"],
  [data-testid="stSidebarCollapseButton"],
  [data-testid="stSidebarCollapseButton"] button {
    display: inline-flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
  }

  [data-testid="stExpandSidebarButton"],
  button[data-testid="stExpandSidebarButton"],
  [data-testid="collapsedControl"] {
    position: fixed !important;
    top: 12px !important;
    left: 14px !important;
    z-index: 2147483646 !important;
    background: #FFFFFF !important;
    border: 2px solid #00D2B4 !important;
    border-radius: 12px !important;
    padding: 6px 14px !important;
    box-shadow: 0 4px 16px rgba(0, 210, 180, 0.35) !important;
    transition: all 0.2s ease !important;
    cursor: pointer !important;
    pointer-events: auto !important;
  }
  [data-testid="stExpandSidebarButton"]:hover,
  button[data-testid="stExpandSidebarButton"]:hover,
  [data-testid="collapsedControl"]:hover {
    background: #E0F8F4 !important;
    border-color: #00A892 !important;
    transform: scale(1.06) !important;
    box-shadow: 0 6px 22px rgba(0, 210, 180, 0.45) !important;
  }
  [data-testid="stExpandSidebarButton"] svg,
  [data-testid="collapsedControl"] svg {
    fill: #0B2528 !important;
    stroke: #0B2528 !important;
    color: #0B2528 !important;
  }

  #maha-maximize-sidebar-floating-btn {
    pointer-events: auto !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
  }
  .th-settings-badge:hover {
    background: #C6F6EC !important;
    border-color: #00A892 !important;
    transform: translateY(-1px);
    box-shadow: 0 4px 12px rgba(0,210,180,0.3) !important;
  }

  [data-testid="stSidebarCollapseButton"] {
    background: #F4FAF9 !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 10px !important;
    cursor: pointer !important;
  }
  [data-testid="stSidebarCollapseButton"]:hover {
    background: #E0F8F4 !important;
    border-color: #00D2B4 !important;
  }


  /* Eliminate empty gap at top of sidebar and page */
  .block-container {
    max-width: 1240px !important;
    padding-top: 1.2rem !important;
    padding-bottom: 8.5rem !important;
  }
  [data-testid="stSidebar"] [data-testid="stSidebarContent"],
  [data-testid="stSidebarContent"],
  [data-testid="stSidebarUserContent"] {
    padding-top: 1.0rem !important;
  }
  [data-testid="stStatusWidget"], .stStatusWidget { display: none !important; }

  /* ── Modern Top Navbar (Matching Reference Top Header) ── */
  .th-navbar {
    display: flex;
    justify-content: space-between;
    align-items: center;
    background: #FFFFFF;
    border: 1.5px solid var(--border-card);
    border-radius: 999px;
    padding: 10px 24px;
    margin-bottom: 20px;
    box-shadow: var(--shadow-sm);
  }
  .th-nav-brand {
    display: flex;
    align-items: center;
    gap: 10px;
    text-decoration: none !important;
  }

  /* ── Sidebar Styling ── */
  [data-testid="stSidebar"],
  [data-testid="stSidebar"] > div,
  [data-testid="stSidebarContent"],
  [data-testid="stSidebarUserContent"],
  section[data-testid="stSidebar"] {
    background-color: #FFFFFF !important;
    background: #FFFFFF !important;
    border-right: 1.5px solid var(--border-subtle) !important;
  }
  .th-sb-brand-box {
    display: flex; align-items: center; gap: 12px; padding: 6px 0; margin-bottom: 8px;
  }
  .th-sb-brand-icon {
    width: 44px; height: 44px; border-radius: 14px;
    background: linear-gradient(135deg, #0B2528 0%, #00BFA5 100%);
    display: flex; align-items: center; justify-content: center;
    font-size: 24px; color: #FFFFFF !important; box-shadow: 0 4px 12px rgba(0,191,165,0.25);
  }
  .th-sb-divider { height: 1.5px; background: var(--border-subtle); margin: 14px 0; }
  .th-sb-title {
    font-size: 0.72rem; font-weight: 800; color: #5C7678;
    letter-spacing: 0.09em; text-transform: uppercase; margin-bottom: 8px;
  }
  [data-testid="stSidebar"] [role="radiogroup"] > label {
    background: #FFFFFF !important; border: 1.5px solid var(--border-subtle) !important;
    border-radius: 12px !important; padding: 10px 14px !important; margin-bottom: 6px !important;
    transition: all 0.2s ease !important;
  }
  [data-testid="stSidebar"] [role="radiogroup"] > label:hover {
    background: var(--primary-teal-light) !important;
    border-color: var(--primary-teal) !important;
  }
  [data-testid="stSidebar"] [role="radiogroup"] > label p,
  [data-testid="stSidebar"] [role="radiogroup"] > label span,
  [data-testid="stSidebar"] [role="radiogroup"] > label div {
    color: #0B2528 !important; -webkit-text-fill-color: #0B2528 !important; font-weight: 700 !important; font-size: 0.92rem !important;
  }
  [data-testid="stSidebar"] [role="radiogroup"] > label[data-checked="true"] {
    background: var(--primary-teal-light) !important;
    border-color: var(--primary-teal) !important;
  }

  .th-help-card {
    display: flex !important; align-items: center !important; justify-content: space-between !important;
    padding: 10px 14px !important; background: #FAFDFD !important; border: 1.5px solid var(--border-subtle) !important;
    border-radius: 12px !important; margin-bottom: 8px !important; text-decoration: none !important;
    transition: all 0.2s ease !important; width: 100% !important; box-sizing: border-box !important;
  }
  .th-help-card:hover {
    transform: translateX(4px);
    border-color: var(--primary-teal) !important;
    background: #FFFFFF !important;
    box-shadow: 0 4px 12px rgba(0,191,165,0.12) !important;
  }
  .th-help-label { font-size: 0.86rem !important; font-weight: 700 !important; color: #0B2528 !important; }
  .th-help-num {
    font-size: 0.95rem !important; font-weight: 800 !important; color: var(--primary-teal-deep) !important;
    background: var(--primary-teal-light) !important; padding: 3px 9px !important; border-radius: 8px !important;
  }
  .th-help-card.critical {
    background: #FFF5F5 !important; border-color: #FED7D7 !important;
  }
  .th-help-card.critical .th-help-num {
    color: #DC2626 !important; background: #FEE2E2 !important;
  }

  .th-nav-logo {
    width: 36px;
    height: 36px;
    border-radius: 10px;
    background: linear-gradient(135deg, #0B2528 0%, #00D2B4 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    color: #FFFFFF;
  }
  .th-nav-title {
    font-size: 1.12rem;
    font-weight: 800;
    color: var(--deep-slate);
    letter-spacing: -0.02em;
  }
  .th-nav-links {
    display: flex;
    align-items: center;
    gap: 20px;
  }
  .th-nav-link {
    color: var(--text-muted);
    font-size: 0.88rem;
    font-weight: 600;
    text-decoration: none !important;
    transition: color 0.2s;
  }
  .th-nav-link:hover { color: var(--primary-teal-dark); }
  .th-nav-btn {
    background: var(--deep-slate);
    color: #FFFFFF !important;
    font-size: 0.82rem;
    font-weight: 700;
    padding: 8px 18px;
    border-radius: 999px;
    text-decoration: none !important;
    display: inline-flex;
    align-items: center;
    gap: 6px;
    box-shadow: 0 4px 12px rgba(11,37,40,0.15);
    transition: all 0.2s ease;
  }
  .th-nav-btn:hover {
    background: var(--primary-teal-dark);
    transform: translateY(-1px);
  }

  /* ── Modern Hero Section (Matching Reference Hero) ── */
  .th-hero-wrap {
    background: #FFFFFF;
    border: 1.5px solid var(--border-card);
    border-radius: 28px;
    padding: 36px 40px 32px;
    margin-bottom: 24px;
    box-shadow: var(--shadow-md);
    position: relative;
    overflow: hidden;
  }
  .th-hero-wrap::before {
    content: "";
    position: absolute;
    top: -60px; right: -60px;
    width: 240px; height: 240px;
    background: radial-gradient(circle, rgba(0,210,180,0.18) 0%, rgba(244,250,249,0) 70%);
    border-radius: 50%;
    pointer-events: none;
  }
  .th-hero-badge {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-size: 0.74rem;
    font-weight: 700;
    color: var(--primary-teal-deep);
    background: var(--primary-teal-light);
    border: 1px solid #B8ECE2;
    padding: 5px 15px;
    border-radius: 999px;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 14px;
  }
  .th-hero-title {
    font-size: 2.35rem !important;
    font-weight: 800 !important;
    color: var(--deep-slate) !important;
    letter-spacing: -0.03em;
    line-height: 1.22;
    margin: 0 0 12px 0 !important;
  }
  .th-hero-title span {
    background: linear-gradient(135deg, #00A892 0%, #00D2B4 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
  }
  .th-hero-sub {
    font-size: 1.02rem;
    color: var(--text-muted);
    line-height: 1.6;
    margin: 0 0 22px 0;
    max-width: 820px;
  }
  .th-hero-cta-row {
    display: flex;
    align-items: center;
    gap: 14px;
    flex-wrap: wrap;
    margin-bottom: 24px;
  }
  .th-btn-teal {
    background: linear-gradient(135deg, #00D2B4 0%, #00BFA5 100%);
    color: var(--deep-slate) !important;
    font-weight: 800;
    font-size: 0.92rem;
    padding: 12px 26px;
    border-radius: 999px;
    text-decoration: none !important;
    box-shadow: 0 6px 18px rgba(0,210,180,0.32);
    display: inline-flex;
    align-items: center;
    gap: 8px;
    transition: all 0.2s ease;
  }
  .th-btn-teal:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 22px rgba(0,210,180,0.42);
  }
  .th-btn-outline {
    background: #FFFFFF;
    color: var(--deep-slate) !important;
    border: 1.5px solid var(--border-subtle);
    font-weight: 700;
    font-size: 0.92rem;
    padding: 11px 24px;
    border-radius: 999px;
    text-decoration: none !important;
    display: inline-flex;
    align-items: center;
    gap: 8px;
    transition: all 0.2s ease;
  }
  .th-btn-outline:hover {
    border-color: var(--primary-teal);
    background: var(--mint-soft);
    transform: translateY(-2px);
  }
  .th-hero-trust {
    display: flex;
    align-items: center;
    gap: 12px;
    padding-top: 14px;
    border-top: 1px solid #EEF6F4;
    font-size: 0.84rem;
    color: var(--text-muted);
  }

  /* ── 3-Card Feature Highlights Bar (Matching Reference Row) ── */
  .th-highlights-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 16px;
    margin-bottom: 24px;
  }
  .th-highlight-card {
    background: #FFFFFF;
    border: 1.5px solid var(--border-card);
    border-radius: 20px;
    padding: 20px 22px;
    display: flex;
    align-items: flex-start;
    gap: 16px;
    box-shadow: var(--shadow-sm);
    transition: all 0.2s ease;
  }
  .th-highlight-card:hover {
    transform: translateY(-3px);
    border-color: var(--primary-teal);
    box-shadow: var(--shadow-md);
  }
  .th-highlight-icon {
    width: 48px;
    height: 48px;
    flex: 0 0 48px;
    border-radius: 14px;
    background: var(--primary-teal-light);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    color: var(--primary-teal-deep);
  }
  .th-highlight-title {
    font-size: 0.98rem;
    font-weight: 800;
    color: var(--deep-slate);
    margin: 0 0 4px 0;
  }
  .th-highlight-desc {
    font-size: 0.84rem;
    color: var(--text-muted);
    line-height: 1.5;
    margin: 0;
  }

  /* ── Dark Statistics Ribbon (Matching Reference Dark Banner) ── */
  .th-stats-ribbon {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    background: var(--deep-slate);
    border-radius: 22px;
    padding: 24px 30px;
    color: #FFFFFF;
    margin-bottom: 30px;
    box-shadow: 0 10px 30px rgba(11,37,40,0.16);
  }
  .th-stat-item {
    text-align: center;
    border-right: 1px solid rgba(255,255,255,0.12);
    padding: 4px 10px;
  }
  .th-stat-item:last-child { border-right: none; }
  .th-stat-val {
    font-size: 2.1rem;
    font-weight: 800;
    color: var(--primary-teal);
    line-height: 1.1;
    margin-bottom: 4px;
    letter-spacing: -0.02em;
  }
  .th-stat-lbl {
    font-size: 0.78rem;
    font-weight: 700;
    color: #B3D1D3;
    text-transform: uppercase;
    letter-spacing: 0.06em;
  }

  /* ── "Why Choose Us" / Core Capabilities 4-Grid ── */
  .th-why-section {
    text-align: center;
    margin: 30px 0 20px;
  }
  .th-why-badge {
    display: inline-block;
    font-size: 0.75rem;
    font-weight: 800;
    color: var(--primary-teal-deep);
    background: var(--primary-teal-light);
    border: 1px solid #B8ECE2;
    padding: 4px 14px;
    border-radius: 999px;
    text-transform: uppercase;
    margin-bottom: 8px;
    letter-spacing: 0.05em;
  }
  .th-why-title {
    font-size: 1.7rem;
    font-weight: 800;
    color: var(--deep-slate);
    margin: 0 0 20px 0;
    letter-spacing: -0.02em;
  }
  .th-why-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-bottom: 30px;
  }
  .th-why-card {
    background: #FFFFFF;
    border: 1.5px solid var(--border-card);
    border-radius: 20px;
    padding: 22px 18px;
    text-align: left;
    box-shadow: var(--shadow-sm);
    transition: all 0.2s ease;
  }
  .th-why-card:hover {
    transform: translateY(-3px);
    border-color: var(--primary-teal);
    box-shadow: var(--shadow-md);
  }
  .th-why-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: var(--primary-teal-light);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 20px;
    margin-bottom: 12px;
  }
  .th-why-card-title {
    font-size: 0.95rem;
    font-weight: 800;
    color: var(--deep-slate);
    margin: 0 0 6px 0;
  }
  .th-why-card-desc {
    font-size: 0.82rem;
    color: var(--text-muted);
    line-height: 1.5;
    margin: 0;
  }

  /* ── "Proven Medical Relief" Generic Medicine Showcase Grid ── */
  .th-med-showcase {
    background: #FFFFFF;
    border: 1.5px solid var(--border-card);
    border-radius: 24px;
    padding: 28px 30px;
    margin: 24px 0;
    box-shadow: var(--shadow-sm);
  }
  .th-med-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-top: 18px;
  }
  .th-med-card {
    background: var(--mint-soft);
    border: 1px solid var(--border-subtle);
    border-radius: 16px;
    padding: 16px;
    text-align: center;
    transition: all 0.2s ease;
  }
  .th-med-card:hover {
    transform: translateY(-2px);
    border-color: var(--primary-teal);
    box-shadow: var(--shadow-sm);
  }
  .th-med-icon {
    width: 46px;
    height: 46px;
    border-radius: 12px;
    background: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 22px;
    margin: 0 auto 10px;
    border: 1px solid var(--border-subtle);
  }
  .th-med-name {
    font-size: 0.92rem;
    font-weight: 800;
    color: var(--deep-slate);
    margin: 0 0 4px 0;
  }
  .th-med-use {
    font-size: 0.78rem;
    color: var(--text-muted);
    margin: 0 0 8px 0;
  }
  .th-med-saving {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 800;
    color: #16794C;
    background: #DCFCE7;
    padding: 3px 10px;
    border-radius: 999px;
  }

  /* ── Testimonial Spotlight Section ── */
  .th-testimonial-box {
    background: linear-gradient(135deg, #FFFFFF 0%, #F4FAF9 100%);
    border: 1.5px solid var(--border-card);
    border-radius: 24px;
    padding: 28px 32px;
    margin: 26px 0;
    display: flex;
    align-items: center;
    gap: 28px;
    box-shadow: var(--shadow-sm);
  }
  .th-test-quote {
    flex: 1;
  }
  .th-test-text {
    font-size: 1.05rem;
    font-weight: 600;
    color: var(--deep-slate);
    line-height: 1.6;
    margin: 0 0 12px 0;
    font-style: italic;
  }
  .th-test-author {
    font-size: 0.86rem;
    font-weight: 800;
    color: var(--primary-teal-deep);
  }
  .th-test-role {
    font-size: 0.78rem;
    color: var(--text-muted);
  }
  .th-test-avatar {
    width: 90px;
    height: 90px;
    border-radius: 20px;
    background: linear-gradient(135deg, #00D2B4 0%, #0B2528 100%);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 42px;
    color: #FFFFFF;
    flex: 0 0 90px;
    box-shadow: 0 6px 18px rgba(0,210,180,0.25);
  }

  /* ── Tabs (Pill Category Selector matching reference) ── */
  .stTabs {
    margin-top: 10px;
    margin-bottom: 24px;
  }
  .stTabs [data-baseweb="tab-list"] {
    display: flex !important;
    gap: 8px !important;
    background: #FFFFFF !important;
    padding: 6px 8px !important;
    border-radius: 999px !important;
    border: 1.5px solid var(--border-card) !important;
    margin-bottom: 20px !important;
    box-shadow: var(--shadow-sm) !important;
    width: fit-content !important;
    max-width: 100% !important;
    overflow-x: auto !important;
    align-items: center !important;
  }
  .stTabs [data-baseweb="tab-highlight"],
  .stTabs [data-baseweb="tab-border"] {
    display: none !important;
    height: 0 !important;
    opacity: 0 !important;
  }
  .stTabs [data-baseweb="tab"] {
    background: transparent !important;
    border-radius: 999px !important;
    padding: 8px 18px !important;
    color: #4E686A !important;
    font-weight: 700 !important;
    font-size: 0.90rem !important;
    border: none !important;
    transition: all 0.2s ease !important;
    white-space: nowrap !important;
  }
  .stTabs [data-baseweb="tab"]:hover {
    background: var(--primary-teal-light) !important;
    color: var(--primary-teal-deep) !important;
  }
  .stTabs [data-baseweb="tab"] p,
  .stTabs [data-baseweb="tab"] span {
    color: #4E686A !important;
    -webkit-text-fill-color: #4E686A !important;
    font-weight: 700 !important;
  }
  .stTabs [data-baseweb="tab"][aria-selected="true"],
  .stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, #00D2B4 0%, #00BFA5 100%) !important;
    color: #0B2528 !important;
    font-weight: 800 !important;
    box-shadow: 0 4px 14px rgba(0,210,180,0.32) !important;
  }
  .stTabs [data-baseweb="tab"][aria-selected="true"] p,
  .stTabs [data-baseweb="tab"][aria-selected="true"] span {
    color: #0B2528 !important;
    -webkit-text-fill-color: #0B2528 !important;
    font-weight: 800 !important;
  }

  /* ── Chat Welcome & Action Grid ── */
  .th-welcome-box {
    background: #FFFFFF;
    border: 1.5px solid var(--border-card);
    border-radius: 24px;
    padding: 30px 28px 24px;
    text-align: center;
    margin: 10px 0 22px 0;
    box-shadow: var(--shadow-sm);
  }
  .th-welcome-icon {
    width: 52px;
    height: 52px;
    border-radius: 16px;
    background: var(--primary-teal-light);
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 26px;
    margin-bottom: 12px;
    box-shadow: 0 4px 12px rgba(0,210,180,0.18);
  }
  .th-welcome-box h2 {
    color: var(--deep-slate) !important;
    font-size: 1.45rem !important;
    font-weight: 800 !important;
    margin: 0 0 8px 0 !important;
  }
  .th-welcome-box p {
    color: var(--text-muted) !important;
    font-size: 0.95rem !important;
    line-height: 1.5 !important;
    margin: 0 auto !important;
  }
  .th-section-heading {
    font-size: 0.88rem;
    font-weight: 800;
    color: var(--primary-teal-deep);
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin: 20px 0 12px 0;
  }

  /* ── Chat Input ── */
  [data-testid="stBottom"] {
    background: linear-gradient(180deg, rgba(244,250,249,0) 0%, rgba(244,250,249,0.96) 24%, #F4FAF9 100%) !important;
    backdrop-filter: blur(12px) !important;
    padding: 16px 0 12px !important;
    z-index: 100 !important;
  }
  div[data-testid="stChatInput"] > div, div[data-testid="stChatInput"] form {
    background-color: #FFFFFF !important;
    border: 1.5px solid var(--border-subtle) !important;
    border-radius: 999px !important;
    box-shadow: 0 4px 20px rgba(11,37,40,0.06) !important;
  }
  div[data-testid="stChatInput"] > div:focus-within {
    border-color: var(--primary-teal) !important;
    box-shadow: 0 0 0 4px rgba(0,210,180,0.18) !important;
  }
  div[data-testid="stChatInput"] textarea {
    background-color: #FFFFFF !important;
    color: var(--text-main) !important;
    -webkit-text-fill-color: var(--text-main) !important;
    font-size: 0.98rem !important;
    font-weight: 500 !important;
    caret-color: var(--primary-teal) !important;
    padding-left: 20px !important;
  }
  div[data-testid="stChatInput"] textarea::placeholder { color: #7B9597 !important; }
  div[data-testid="stChatInputSubmitButton"] {
    background-color: var(--deep-slate) !important;
    border-radius: 999px !important;
    margin: 4px !important;
    transition: all 0.2s ease !important;
  }
  div[data-testid="stChatInputSubmitButton"]:hover {
    background-color: var(--primary-teal-dark) !important;
    transform: scale(1.04) !important;
  }
  div[data-testid="stChatInputSubmitButton"] svg { fill: #FFFFFF !important; }

  /* ── Buttons ── */
  div[data-testid="stButton"] > button {
    background-color: #FFFFFF !important;
    color: var(--deep-slate) !important;
    border: 1.5px solid var(--border-subtle) !important;
    border-radius: 14px !important;
    padding: 12px 16px !important;
    font-weight: 700 !important;
    font-size: 0.92rem !important;
    transition: all 0.2s ease !important;
    display: flex !important;
    align-items: center !important;
    justify-content: flex-start !important;
    text-align: left !important;
    width: 100% !important;
    min-height: 52px !important;
    box-shadow: var(--shadow-sm) !important;
  }
  div[data-testid="stButton"] > button:hover {
    background-color: #FFFFFF !important;
    border-color: var(--primary-teal) !important;
    color: var(--primary-teal-dark) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 18px rgba(0,210,180,0.18) !important;
  }
  div[data-testid="stButton"] > button p { color: inherit !important; font-weight: 700 !important; }

  .th-clear-btn div[data-testid="stButton"] > button {
    min-height: 36px !important; padding: 6px 14px !important; border-radius: 999px !important;
    font-size: 0.82rem !important; background: #FFFFFF !important; color: #64748B !important;
    justify-content: center !important;
  }
  .th-clear-btn div[data-testid="stButton"] > button:hover {
    background: #FEECEB !important; border-color: #F8D5D1 !important; color: var(--accent-red) !important;
  }

  /* ── Chat Messages ── */
  [data-testid="stChatMessage"] { background: transparent !important; padding: 6px 0 !important; border: none !important; }
  [data-testid="stChatMessage"] [data-testid="stChatMessageContent"] {
    background: #FFFFFF !important;
    border: 1.5px solid var(--border-card) !important;
    border-radius: 18px !important;
    padding: 16px 20px !important;
    box-shadow: var(--shadow-sm) !important;
    color: var(--text-main) !important;
    max-width: 920px;
    line-height: 1.6 !important;
  }
  [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) { flex-direction: row-reverse !important; }
  [data-testid="stChatMessage"]:has([data-testid="chatAvatarIcon-user"]) [data-testid="stChatMessageContent"] {
    background: #E8F9F5 !important;
    border-color: #BDEEE4 !important;
    border-radius: 18px 18px 4px 18px !important;
  }
  [data-testid="stChatMessageAvatar"] {
    background: #FFFFFF !important;
    border: 1.5px solid var(--border-subtle) !important;
    border-radius: 14px !important;
  }

  /* ── Disease & Content Cards ── */
  .th-dx-card {
    background: #FFFFFF;
    border: 1.5px solid var(--border-card);
    border-radius: 20px;
    overflow: hidden;
    box-shadow: var(--shadow-md);
    margin: 8px 0;
  }
  .th-dx-header {
    background: linear-gradient(135deg, #0B2528 0%, #133D41 100%);
    padding: 16px 22px;
    color: #FFFFFF;
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 12px;
  }
  .th-dx-header-left { display: flex; align-items: center; gap: 12px; }
  .th-dx-header-icon {
    width: 44px;
    height: 44px;
    border-radius: 12px;
    background: rgba(255,255,255,0.12);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 24px;
  }
  .th-dx-title {
    margin: 0 !important;
    font-size: 1.22rem !important;
    font-weight: 800 !important;
    color: #FFFFFF !important;
  }
  .th-dx-badge {
    font-size: 0.72rem;
    font-weight: 800;
    color: var(--deep-slate);
    background: var(--primary-teal);
    padding: 4px 12px;
    border-radius: 999px;
    text-transform: uppercase;
    letter-spacing: 0.04em;
  }
  .th-dx-row {
    display: flex;
    gap: 14px;
    padding: 16px 22px;
    border-bottom: 1px solid #F0F6F5;
    align-items: flex-start;
  }
  .th-dx-icon-badge {
    width: 38px;
    height: 38px;
    flex: 0 0 38px;
    border-radius: 10px;
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 18px;
  }
  .th-dx-label {
    display: block;
    font-size: 0.76rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin-bottom: 4px;
    font-weight: 800;
  }
  .th-dx-content {
    font-size: 0.95rem;
    color: #334A4D;
    line-height: 1.55;
  }
  .th-dx-footer {
    padding: 12px 22px;
    background: #F8FCFB;
    border-top: 1px solid #E6F2EE;
    font-size: 0.8rem;
    color: #627E80;
    font-style: italic;
  }

  /* ── Modern Alerts ── */
  .th-alert {
    border-radius: 16px;
    padding: 18px 20px;
    border-left: 5px solid;
    display: flex;
    gap: 16px;
    margin-bottom: 14px;
    box-shadow: var(--shadow-sm);
  }
  .th-alert-icon { font-size: 26px; flex: 0 0 32px; padding-top: 2px; }
  .th-alert-body { flex: 1; }
  .th-alert h4 { margin: 0 0 6px 0 !important; font-weight: 800 !important; font-size: 1.05rem !important; }
  .th-alert.emerg {
    background: #FFF5F5;
    border-left-color: var(--accent-red);
    border: 1.5px solid #FED7D7;
    border-left-width: 6px;
  }
  .th-alert.emerg h4, .th-alert.emerg p, .th-alert.emerg li { color: #9B1C1C !important; }
  .th-emerg-actions { display: flex; gap: 10px; margin-top: 12px; flex-wrap: wrap; }
  .th-emerg-btn {
    display: inline-flex; align-items: center; gap: 6px;
    background: var(--accent-red); color: #FFFFFF !important;
    font-weight: 700; font-size: 0.88rem; padding: 8px 16px;
    border-radius: 999px; text-decoration: none !important;
  }
  .th-emerg-btn-sub {
    display: inline-flex; align-items: center; gap: 6px;
    background: #FFFFFF; color: #9B1C1C !important;
    font-weight: 700; font-size: 0.88rem; padding: 8px 16px;
    border-radius: 999px; border: 1px solid #FED7D7; text-decoration: none !important;
  }
  .th-alert.caution {
    background: #FFFBEB; border-left-color: var(--accent-amber);
    border: 1.5px solid #FDE68A; border-left-width: 6px;
  }
  .th-alert.caution h4 { color: #92400E !important; }
  .th-alert.caution p { color: #B45309 !important; }
  .th-alert.info {
    background: #F0FDF9; border-left-color: var(--primary-teal-dark);
    border: 1.5px solid #C6F6EC; border-left-width: 6px;
  }
  .th-alert.info h4 { color: var(--primary-teal-deep) !important; }
  .th-alert.info p { color: #234E48 !important; }

  /* ── Deep Slate Footer (Matching Reference Bottom) ── */
  .th-footer {
    background: var(--deep-slate) !important;
    border-radius: 24px !important;
    padding: 38px 38px 24px !important;
    margin-top: 40px !important;
    color: #FFFFFF !important;
    box-shadow: 0 10px 30px rgba(11,37,40,0.16) !important;
  }
  .th-footer-grid {
    display: grid !important;
    grid-template-columns: 2fr 1.1fr 1.2fr 1.1fr !important;
    gap: 28px !important;
    margin-bottom: 24px !important;
  }
  .th-footer-title {
    font-size: 0.96rem !important;
    font-weight: 800 !important;
    color: #00D2B4 !important;
    -webkit-text-fill-color: #00D2B4 !important;
    text-transform: uppercase !important;
    letter-spacing: 0.08em !important;
    margin-bottom: 14px !important;
  }
  .th-footer p {
    color: #D1E7E5 !important;
    -webkit-text-fill-color: #D1E7E5 !important;
    line-height: 1.6 !important;
  }
  .th-footer a,
  .th-footer a:link,
  .th-footer a:visited,
  .th-footer-link {
    display: flex !important;
    align-items: center !important;
    gap: 6px !important;
    color: #E0F8F4 !important;
    -webkit-text-fill-color: #E0F8F4 !important;
    text-decoration: none !important;
    font-size: 0.88rem !important;
    font-weight: 600 !important;
    margin-bottom: 10px !important;
    transition: all 0.2s ease !important;
  }
  .th-footer a:hover,
  .th-footer-link:hover {
    color: #00D2B4 !important;
    -webkit-text-fill-color: #00D2B4 !important;
    transform: translateX(4px) !important;
  }
  .th-footer span.th-footer-link {
    color: #FFFFFF !important;
    -webkit-text-fill-color: #FFFFFF !important;
    font-weight: 600 !important;
  }
  .th-footer-bottom {
    border-top: 1px solid rgba(255,255,255,0.16) !important;
    padding-top: 18px !important;
    text-align: center !important;
    font-size: 0.84rem !important;
    color: #B2D8D6 !important;
    -webkit-text-fill-color: #B2D8D6 !important;
  }

  /* ── Contrast & Visibility Safeguards ── */
  [data-testid="stSidebar"] p,
  [data-testid="stSidebar"] span,
  [data-testid="stSidebar"] small,
  [data-testid="stSidebar"] label,
  [data-testid="stSidebar"] div[data-testid="stCaptionContainer"],
  [data-testid="stSidebar"] .stCaption p {
    color: #496366 !important;
    -webkit-text-fill-color: #496366 !important;
  }
  div[data-testid="stRadio"] label p,
  div[data-testid="stRadio"] label span,
  div[data-testid="stRadio"] [role="radiogroup"] label p,
  div[data-testid="stRadio"] [role="radiogroup"] label span {
    color: var(--text-main) !important;
    -webkit-text-fill-color: var(--text-main) !important;
    opacity: 1 !important;
  }

  /* ── Modern Clinical Search Loading Screen Styles ── */
  .th-clinical-loader {
    background: linear-gradient(135deg, #FFFFFF 0%, #F2FBF9 50%, #E8F9F5 100%) !important;
    border: 2px solid #00D2B4 !important;
    border-radius: 20px !important;
    padding: 24px 28px !important;
    margin: 18px auto 26px auto !important;
    max-width: 900px !important;
    box-shadow: 0 16px 40px rgba(0, 210, 180, 0.22), 0 4px 16px rgba(11, 37, 40, 0.05) !important;
    position: relative !important;
    overflow: hidden !important;
    animation: clinicalCardPulse 2.4s ease-in-out infinite alternate !important;
    font-family: 'Plus Jakarta Sans', system-ui, sans-serif !important;
  }

  @keyframes clinicalCardPulse {
    0% {
      box-shadow: 0 10px 30px rgba(0, 210, 180, 0.16);
      border-color: #00D2B4;
      transform: translateY(0);
    }
    100% {
      box-shadow: 0 18px 46px rgba(0, 210, 180, 0.32);
      border-color: #00A892;
      transform: translateY(-2px);
    }
  }

  .th-loader-top-bar {
    display: flex !important;
    align-items: center !important;
    justify-content: space-between !important;
    margin-bottom: 16px !important;
    padding-bottom: 12px !important;
    border-bottom: 1px solid rgba(0, 210, 180, 0.2) !important;
  }

  .th-loader-status-pill {
    display: inline-flex !important;
    align-items: center !important;
    gap: 8px !important;
    background: rgba(0, 210, 180, 0.12) !important;
    color: #007A6C !important;
    font-size: 0.72rem !important;
    font-weight: 800 !important;
    letter-spacing: 0.8px !important;
    padding: 4px 12px !important;
    border-radius: 20px !important;
    border: 1px solid rgba(0, 210, 180, 0.35) !important;
  }

  .th-pulse-dot {
    width: 8px !important;
    height: 8px !important;
    background-color: #00D2B4 !important;
    border-radius: 50% !important;
    display: inline-block !important;
    box-shadow: 0 0 10px #00D2B4 !important;
    animation: pulseDotAnim 1.2s infinite ease-in-out !important;
  }

  @keyframes pulseDotAnim {
    0% { transform: scale(0.85); opacity: 0.6; box-shadow: 0 0 4px #00D2B4; }
    50% { transform: scale(1.3); opacity: 1; box-shadow: 0 0 12px #00D2B4; }
    100% { transform: scale(0.85); opacity: 0.6; box-shadow: 0 0 4px #00D2B4; }
  }

  .th-loader-tech-badge {
    font-size: 0.74rem !important;
    font-weight: 700 !important;
    color: #5C7678 !important;
    background: #FFFFFF !important;
    border: 1px solid #D8EEE9 !important;
    padding: 4px 12px !important;
    border-radius: 14px !important;
  }

  .th-loader-main-body {
    display: flex !important;
    align-items: center !important;
    gap: 20px !important;
    margin-bottom: 16px !important;
  }

  .th-loader-radar-wrapper {
    position: relative !important;
    width: 58px !important;
    height: 58px !important;
    min-width: 58px !important;
    display: flex !important;
    align-items: center !important;
    justify-content: center !important;
  }

  .th-loader-ring-outer {
    position: absolute !important;
    inset: 0 !important;
    border: 3px dashed #00D2B4 !important;
    border-radius: 50% !important;
    animation: spinClockwise 4s linear infinite !important;
  }

  .th-loader-ring-inner {
    position: absolute !important;
    inset: 6px !important;
    border: 2px solid transparent !important;
    border-top-color: #007A6C !important;
    border-bottom-color: #00A892 !important;
    border-radius: 50% !important;
    animation: spinCounterClockwise 2s linear infinite !important;
  }

  @keyframes spinClockwise {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
  }

  @keyframes spinCounterClockwise {
    from { transform: rotate(360deg); }
    to { transform: rotate(0deg); }
  }

  .th-loader-icon-center {
    font-size: 24px !important;
    animation: heartbeatBounce 1.5s ease-in-out infinite !important;
  }

  @keyframes heartbeatBounce {
    0% { transform: scale(1); }
    14% { transform: scale(1.2); }
    28% { transform: scale(1); }
    42% { transform: scale(1.15); }
    70% { transform: scale(1); }
  }

  .th-loader-text-block {
    flex: 1 !important;
  }

  .th-loader-heading {
    font-size: 1.12rem !important;
    font-weight: 800 !important;
    color: #0B2528 !important;
    line-height: 1.4 !important;
    margin-bottom: 4px !important;
  }

  .th-loader-subtext {
    font-size: 0.84rem !important;
    color: #4E686A !important;
    line-height: 1.5 !important;
  }

  /* ECG Wave Line */
  .th-loader-ecg-container {
    width: 100% !important;
    height: 36px !important;
    margin: 10px 0 16px 0 !important;
    background: rgba(0, 210, 180, 0.04) !important;
    border-radius: 8px !important;
    overflow: hidden !important;
  }

  .th-loader-ecg-svg {
    width: 100% !important;
    height: 100% !important;
    display: block !important;
  }

  .th-loader-ecg-bg {
    stroke: rgba(0, 210, 180, 0.22) !important;
    stroke-width: 2 !important;
    fill: none !important;
  }

  .th-loader-ecg-pulse {
    stroke: #00D2B4 !important;
    stroke-width: 3 !important;
    stroke-linecap: round !important;
    stroke-linejoin: round !important;
    fill: none !important;
    stroke-dasharray: 100, 500 !important;
    animation: ecgFlow 2s linear infinite !important;
    filter: drop-shadow(0 0 5px #00D2B4) !important;
  }

  @keyframes ecgFlow {
    0% { stroke-dashoffset: 600; }
    100% { stroke-dashoffset: 0; }
  }

  /* Step Badges */
  .th-loader-steps-grid {
    display: grid !important;
    grid-template-columns: repeat(3, 1fr) !important;
    gap: 10px !important;
    margin-bottom: 16px !important;
  }

  @media (max-width: 768px) {
    .th-loader-steps-grid {
      grid-template-columns: 1fr !important;
    }
  }

  .th-loader-step {
    display: flex !important;
    align-items: center !important;
    gap: 8px !important;
    padding: 8px 12px !important;
    border-radius: 12px !important;
    font-size: 0.78rem !important;
    font-weight: 700 !important;
    background: #FFFFFF !important;
    border: 1px solid #D8EEE9 !important;
    color: #3D585B !important;
  }

  .th-loader-step.th-step-active {
    background: linear-gradient(135deg, #E0F8F4 0%, #FFFFFF 100%) !important;
    border-color: #00D2B4 !important;
    color: #007A6C !important;
    box-shadow: 0 2px 8px rgba(0, 210, 180, 0.18) !important;
  }

  .th-loader-step.th-step-pulse {
    border-color: #7BE3D5 !important;
    color: #0B5C54 !important;
    animation: pulseSubtle 1.8s infinite ease-in-out !important;
  }

  @keyframes pulseSubtle {
    0% { opacity: 0.7; }
    50% { opacity: 1; }
    100% { opacity: 0.7; }
  }

  .th-loader-step.th-step-wait {
    opacity: 0.65 !important;
  }

  /* Shimmer Progress Line */
  .th-loader-shimmer-progress {
    width: 100% !important;
    height: 5px !important;
    background: #D8EEE9 !important;
    border-radius: 10px !important;
    overflow: hidden !important;
    position: relative !important;
  }

  .th-loader-shimmer-bar {
    position: absolute !important;
    top: 0 !important;
    left: 0 !important;
    height: 100% !important;
    width: 35% !important;
    background: linear-gradient(90deg, #00D2B4 0%, #007A6C 50%, #2DD4BF 100%) !important;
    border-radius: 10px !important;
    box-shadow: 0 0 10px #00D2B4 !important;
    animation: shimmerSweep 1.6s ease-in-out infinite !important;
  }

  @keyframes shimmerSweep {
    0% { left: -35%; width: 25%; }
    50% { width: 50%; }
    100% { left: 100%; width: 25%; }
  }

  /* ── Fallback Streamlit Native Spinner Modern Styling ── */
  [data-testid="stSpinner"],
  .stSpinner {
    background: linear-gradient(135deg, #FFFFFF 0%, #F2FBF9 50%, #E8F9F5 100%) !important;
    border: 1.5px solid #00D2B4 !important;
    border-radius: 16px !important;
    padding: 18px 24px !important;
    margin: 16px auto !important;
    max-width: 860px !important;
    box-shadow: 0 10px 30px rgba(0, 210, 180, 0.18), 0 2px 8px rgba(11,37,40,0.04) !important;
    display: flex !important;
    align-items: center !important;
    position: relative !important;
    overflow: hidden !important;
    animation: clinicalCardPulse 2.4s ease-in-out infinite alternate !important;
  }

  [data-testid="stSpinner"]::after,
  .stSpinner::after {
    content: "" !important;
    position: absolute !important;
    bottom: 0 !important;
    left: 0 !important;
    height: 3px !important;
    width: 100% !important;
    background: linear-gradient(90deg, #00D2B4, #007A6C, #2DD4BF) !important;
    background-size: 200% 100% !important;
    animation: shimmerBorder 2s linear infinite !important;
  }

  @keyframes shimmerBorder {
    0% { background-position: 100% 0; }
    100% { background-position: -100% 0; }
  }

  [data-testid="stSpinner"] svg,
  [data-testid="stSpinner"] span {
    color: #00A892 !important;
    fill: #00A892 !important;
    filter: drop-shadow(0 0 8px rgba(0, 210, 180, 0.5)) !important;
  }

  [data-testid="stSpinner"] div[role="status"],
  [data-testid="stSpinner"] p {
    font-family: 'Plus Jakarta Sans', system-ui, sans-serif !important;
    font-size: 1.02rem !important;
    font-weight: 700 !important;
    color: #0B2528 !important;
    -webkit-text-fill-color: #0B2528 !important;
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
