"""ML and NLP processing package."""
from src.ml.nlp_utils import (
    _merge_compound_aches,
    _stem_word,
    tokenize,
    phrase_hits,
    keyword_bonus,
    has_red_flags,
    is_critical_emergency,
    is_informational_query,
    is_facility_seeking_query,
    is_schedule_query,
    is_informational_question,
    is_seasonal_prevention_query,
    detect_requested_service,
    extract_location,
    extract_entities,
    _extract_symptoms_list,
    classify_intent,
    classify_urgency,
    assess_care_level,
    build_routing_object,
    _derive_required_services,
)
from src.ml.engine import (
    match_and_rank_facilities,
    offline_keyword_matcher,
    rank_diseases,
    load_whisper,
    transcribe_audio,
    asr_language_code,
    web_speech_lang,
    load_model,
)
from src.ml.gemini_client import (
    query_gemini_flash,
    query_gemini_facility_search,
    is_gemini_available,
    get_gemini_api_key,
)

