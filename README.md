# 🩺 MahaArogya Setu — Rural Healthcare Access Platform

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue.svg)](https://www.python.org/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B.svg)](https://streamlit.io/)
[![Smart India Hackathon](https://img.shields.io/badge/SIH-Rural%20Healthcare-green.svg)](https://www.sih.gov.in/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**MahaArogya Setu** is an intelligent, multilingual rural healthcare triage and access platform built for underserved and tribal communities in Maharashtra (Nandurbar, Gadchiroli, Melghat/Amravati, Palghar, Yavatmal). 

It connects citizens to primary and tertiary healthcare, helps navigate government health insurance schemes (MJPJAY, PM-JAY), provides maternal and child health guidance, locates nearby public health facilities, and offers instant AI-assisted symptom triage with voice support in English, Hindi (हिंदी), and Marathi (मराठी).

---

## 🏛️ Architecture & Project Structure

The project is structured according to industrial modular software architecture:

```text
mahaarogya_setu/
├── main.py                     # Streamlit application entry point
├── requirements.txt            # Project dependencies
├── .gitignore                  # Git ignore rules for virtualenvs & secrets
├── data/
│   └── disease_dataset.csv     # Rural disease, symptom, prevention & care dataset
├── src/
│   ├── config/                 # Configuration, themes, constants & UI strings
│   │   ├── __init__.py
│   │   ├── constants.py        # Districts, schemes, schedules, intent taxomony
│   │   ├── settings.py         # Application settings and paths
│   │   └── theme.py            # Clinical design system CSS & page config
│   ├── data_access/            # Data layer and geolocation services
│   │   ├── __init__.py
│   │   ├── loader.py           # Cached CSV data loading & validation
│   │   └── geography.py        # Haversine distance & facility coordinate engine
│   ├── ml/                     # NLP, triage algorithms & ML services
│   │   ├── __init__.py
│   │   ├── nlp_utils.py        # Entity extraction, tokenization, intent classifier
│   │   └── engine.py           # Sentence-transformers semantic search & ASR
│   ├── translation/            # Multilingual layer
│   │   ├── __init__.py
│   │   └── translator.py       # Devanagari/Romanized transliteration & translation
│   └── ui/                     # Presentation components & views
│       ├── __init__.py
│       ├── audio.py            # Browser Web Speech API JavaScript mic component
│       ├── cards.py            # Clinical alert banners, disease cards, scheme widgets
│       ├── pipeline.py         # End-to-end user query routing & response pipeline
│       └── views.py            # Sidebar, hero header, and 5 interactive tabs
```

---

## ✨ Key Features

1. **🩺 AI Symptom Triage & Red-Flag Detection**:
   - Semantic NLP matching using `sentence-transformers` (`all-MiniLM-L6-v2`) against 40+ rural conditions.
   - Immediate red-flag and critical emergency triage triggering clickable 108/102/104 call actions.

2. **🌐 Trilingual Voice & Text Interface**:
   - Full support for **English**, **हिंदी (Hindi)**, **मराठी (Marathi)**, and phonetic Hinglish.
   - Injected browser-native microphone component for hands-free symptom reporting.

3. **🏥 Smart Rural Facility Locator & Geo-Ranking**:
   - District-wise directory of PHCs, CHCs, SDHs, and District Hospitals in tribal regions.
   - Context-aware ranking matching patient attributes (pediatric, maternal, emergency, nearest HQ).

4. **📋 Government Health Schemes Navigator**:
   - Detailed guides for **MJPJAY**, **Ayushman Bharat (PM-JAY)**, **Aapla Dawakhana**, **JSY**, **RBSK**, and **Navsanjivan Yojana**.
   - Direct information on eligibility, documentation, and empanelled hospital desks.

5. **🤰 Maternal & Child Health (MCH) Portal**:
   - 4-stage ANC visit timeline with danger sign detection.
   - Universal Immunization Programme (UIP) infant vaccination schedule.

6. **💊 Pradhan Mantri Jan Aushadhi Guide**:
   - Generic medicine cost comparison displaying up to 85% savings on essential drugs.

7. **⚡ Low-Bandwidth Mode**:
   - Bypasses heavy neural models in favor of deterministic offline keyword matching for weak 2G network areas.

---

## 🚀 Quickstart & Installation

### 1. Prerequisites
- Python 3.10+
- Virtual environment tool (`venv` or `conda`)

### 2. Setup Virtual Environment
```bash
# Clone the repository
git clone https://github.com/ShivInAction/sih.git
cd sih

# Create and activate virtual environment
python -m venv venv

# On Windows:
venv\Scripts\activate
# On Linux/macOS:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run Application
```bash
streamlit run main.py
```
Open your browser and navigate to `http://localhost:8501`.

---

## 🧪 Running Tests

Run the built-in validation suite to verify all modules and pipelines:
```bash
python test_refactored_modules.py
```

---

## 👥 Authors & Acknowledgements
- Developed for the **Smart India Hackathon (SIH)**.
- Data & public healthcare references sourced from the **Maharashtra Public Health Department** and **National Health Mission (NHM)**.
