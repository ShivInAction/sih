import os
import sys

# Ensure UTF-8 output on Windows console
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = r"c:\Users\shiva\Desktop\Other Apps\Agent_updated"
sys.path.insert(0, BASE_DIR)

print("1. Testing config imports...")
from src.config.constants import (
    REQUIRED_COLUMNS,
    MAHARASHTRA_DISTRICTS,
    MAHARASHTRA_SCHEMES,
    HEALTH_CAMPS,
    GENERIC_MEDS,
    UI_STRINGS,
)
from src.config.theme import setup_page, CUSTOM_CSS
from src.config.settings import DATA_FILE, APP_NAME

print(f"   Config loaded. App: {APP_NAME}, Districts: {len(MAHARASHTRA_DISTRICTS)}, Schemes: {len(MAHARASHTRA_SCHEMES)}")

print("2. Testing data access...")
from src.data_access.loader import load_data
from src.data_access.geography import haversine_km, get_facility_coords

df = load_data()
print(f"   Data loaded. Total diseases in dataset: {len(df)}")

dist = haversine_km(19.0, 72.8, 19.1, 72.9)
print(f"   Haversine test distance: {dist:.2f} km")

print("3. Testing translation utilities...")
from src.translation.translator import (
    is_romanized_hindi,
    romanize_to_english,
    devanagari_to_english,
    normalize_for_match,
    detect_response_lang,
)

print(f"   is_romanized_hindi('mujhe bukhar hai'): {is_romanized_hindi('mujhe bukhar hai')}")
print(f"   romanize_to_english('mujhe bukhar hai'): {romanize_to_english('mujhe bukhar hai')}")
print(f"   devanagari_to_english('मला ताप आहे'): {devanagari_to_english('मला ताप आहे')}")
print(f"   detect_response_lang('मला ताप आहे'): {detect_response_lang('मला ताप आहे')}")

print("4. Testing ML and NLP utils...")
from src.ml.nlp_utils import (
    tokenize,
    classify_intent,
    extract_entities,
    has_red_flags,
    is_critical_emergency,
    classify_urgency,
)
from src.ml.engine import (
    match_and_rank_facilities,
    offline_keyword_matcher,
)

intent, sub_intent, conf = classify_intent("Show hospital near Nandurbar", "Show hospital near Nandurbar")
print(f"   Intent classification: {intent}, confidence: {conf}")

entities = extract_entities("Child 3 years old with high fever in Nandurbar", "Child 3 years old with high fever in Nandurbar")
print(f"   Extracted entities: {entities}")

ranked_facs = match_and_rank_facilities("Nandurbar", requested_service="Pediatric", entities=entities)
print(f"   Ranked facilities found in Nandurbar: {len(ranked_facs)}")
if ranked_facs:
    print(f"   Top facility: {ranked_facs[0][0]['name']} (Reasons: {ranked_facs[0][1]})")

score, idx, row = offline_keyword_matcher("high fever chills shivering", df)
print(f"   Offline keyword match: {row['disease']} (Score: {score:.2f})")

print("5. Testing UI cards and pipeline...")
from src.ui.cards import (
    generate_telemedicine_guide,
    generate_schemes_guide,
    format_disease_card_html,
)

tele_card = generate_telemedicine_guide("en")
print(f"   Telemedicine card generated: {len(tele_card)} chars")

print("\nALL UNIT TESTS PASSED SUCCESSFULLY!")
