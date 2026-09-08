"""End-to-end response generation and triage pipeline."""
import re
from datetime import datetime
import pandas as pd
import streamlit as st
from src.config.constants import (
    MODE_HINDI,
    MODE_MARATHI,
    MODE_ENGLISH,
    INTENT_EMERGENCY,
    INTENT_PREGNANCY,
    INTENT_TELEMEDICINE,
    INTENT_HELPLINE,
    INTENT_IMMUNIZATION_FACILITY_SEARCH,
    INTENT_MATERNITY_FACILITY_SEARCH,
    INTENT_PEDIATRIC_FACILITY_SEARCH,
    INTENT_GENERAL_OPD_SEARCH,
    INTENT_IMMUNIZATION_INFORMATION,
    INTENT_VACCINATION_SCHEDULE,
    INTENT_VACCINATION_CAMP_INFORMATION,
    INTENT_VACCINATION,
    INTENT_FACILITY_SEARCH,
    INTENT_SCHEME_INFORMATION,
    INTENT_CHILD_HEALTH,
    INTENT_MEDICINE_INFORMATION,
    INTENT_ABHA,
    INTENT_SYMPTOM_CHECK,
    INTENT_FACILITY,
)
from src.translation.translator import (
    is_romanized_hindi,
    romanize_to_english,
    devanagari_to_english,
    translate_safe,
    translate_row_fields,
    detect_response_lang,
    _looks_like_translation_error,
)
from src.ml.nlp_utils import (
    classify_intent,
    extract_entities,
    _extract_symptoms_list,
    has_red_flags,
    is_critical_emergency,
    classify_urgency,
    is_seasonal_prevention_query,
    is_informational_question,
    assess_care_level,
    detect_requested_service,
    _derive_required_services,
)
from src.ml.engine import (
    match_and_rank_facilities,
    rank_diseases,
)
from src.ml.gemini_client import (
    query_gemini_flash,
    query_gemini_facility_search,
    is_gemini_available,
)
from src.ui.cards import (
    format_seasonal_prevention_card,
    emergency_banner_html,
    generate_ranked_facility_results,
    care_pathway_html,
    generate_telemedicine_guide,
    generate_asha_anm_guide,
    render_health_camps_html,
    _render_next_camp_info,
    build_clarifying_question,
    generate_district_locator_results,
    generate_schemes_guide,
    generate_maternal_child_module,
    generate_jan_aushadhi_guide,
    render_abha_html,
    build_structured_response,
    caution_banner_html,
    format_disease_plain,
    format_disease_card_html,
    format_trauma_emergency_card,
    format_general_clinical_triage_card,
    _build_fallback_response,
)

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
    is_emergency_case = (
        primary_intent == INTENT_EMERGENCY
        or urgency == "EMERGENCY"
        or _critical
        or _red_flag
    )

    if is_emergency_case:
        primary_intent = INTENT_EMERGENCY
        urgency = "EMERGENCY"
        care_level = "EMERGENCY"
        entities["required_service"] = "Emergency"
        entities["facility_type"] = "District Hospital"
        matched_facs_with_reasons = match_and_rank_facilities(entities.get("district"), ["Emergency"], "District Hospital", "EMERGENCY", entities=entities)
        matched_facs = [f for f, _ in matched_facs_with_reasons]
        _routing_debug["matched_facility_count"] = len(matched_facs)
        _routing_debug["route"] = "emergency"
        _routing_debug["intent"] = INTENT_EMERGENCY
        _routing_debug["sub_intent"] = secondary_intent or "TRAUMA"
        _routing_debug["urgency"] = "EMERGENCY"
        _routing_debug["care_level"] = "EMERGENCY"
        st.session_state["_routing_debug"] = _routing_debug

        # Specialized trauma first aid card (knife, stab, gunshot, snakebite, poisoning, burns)
        trauma_first_aid = format_trauma_emergency_card(secondary_intent or "TRAUMA_PENETRATING", query, response_lang)
        emerg_response = (trauma_first_aid + "\n" if trauma_first_aid else "") + emergency_banner_html(response_lang)

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

        loc_key = entities.get("location") or entities.get("district") or ""
        ranked_facs = []
        ranked_facs_with_reasons = []
        if loc_key:
            ranked_facs_with_reasons = match_and_rank_facilities(
                loc_key,
                required_services=required_services,
                facility_type=fac_type,
                urgency=urgency,
                requested_service=requested_service,
                entities=entities
            )
            ranked_facs = [f for f, _ in ranked_facs_with_reasons]

        if ranked_facs:
            _routing_debug["matched_facility_count"] = len(ranked_facs)
            st.session_state["_routing_debug"] = _routing_debug
            return generate_ranked_facility_results(
                ranked_facs, entities, response_lang,
                requested_service=requested_service,
                secondary_intent=secondary_intent,
                ranked_with_reasons=ranked_facs_with_reasons
            )

        # If not matched in static local DB (e.g. Pari Chowk, Noida, Delhi, etc.) or no district:
        # Gemini Flash resolves nearest facilities across India dynamically!
        if is_gemini_available():
            ai_fac_result = query_gemini_facility_search(
                query=query,
                location=loc_key,
                service_needed=requested_service,
                urgency=urgency,
                response_lang=response_lang,
                entities=entities,
            )
            if ai_fac_result:
                _routing_debug["route"] = "gemini_facility_locator"
                _routing_debug["location"] = loc_key
                st.session_state["_routing_debug"] = _routing_debug
                return ai_fac_result

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

        loc_key = entities.get("location") or entities.get("district") or ""
        ranked_facs = []
        ranked_facs_with_reasons = []
        if loc_key:
            ranked_facs_with_reasons = match_and_rank_facilities(
                loc_key,
                required_services=required_services,
                facility_type=entities.get("facility_type"),
                urgency=urgency,
                requested_service=requested_service,
                entities=entities
            )
            ranked_facs = [f for f, _ in ranked_facs_with_reasons]

        if ranked_facs:
            _routing_debug["matched_facility_count"] = len(ranked_facs)
            st.session_state["_routing_debug"] = _routing_debug
            return generate_ranked_facility_results(
                ranked_facs, entities, response_lang,
                requested_service=requested_service,
                secondary_intent=secondary_intent,
                ranked_with_reasons=ranked_facs_with_reasons
            )

        # Dynamic AI locator fallback across India for custom locations & landmarks
        if is_gemini_available():
            ai_fac_result = query_gemini_facility_search(
                query=query,
                location=loc_key,
                service_needed=requested_service,
                urgency=urgency,
                response_lang=response_lang,
                entities=entities,
            )
            if ai_fac_result:
                _routing_debug["route"] = "gemini_facility_locator"
                _routing_debug["location"] = loc_key
                st.session_state["_routing_debug"] = _routing_debug
                return ai_fac_result

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

    # Stage 6+7+8+9: Symptom check & clinical query resolution
    if primary_intent in (INTENT_SYMPTOM_CHECK, INTENT_CHILD_HEALTH):
        informational = is_informational_question(query)
        caution = informational and (urgency == "EMERGENCY")
        ranked = rank_diseases(query_for_matching, df, symptom_embeddings, name_embeddings, model)
        best_score, best_idx, row = ranked[0]
        alternatives = [alt_row["disease"] for score, idx, alt_row in ranked[1:3] if score >= 0.43 and (best_score - score) <= 0.18] if best_score >= 0.48 else []
        good_match = best_score >= 0.48
        care_level = assess_care_level(primary_intent, entities, best_score, _red_flag, _critical)

        matched_facs = []
        loc_key = entities.get("location") or entities.get("district") or ""
        if loc_key:
            rec_fac_str = str(row.get("recommended_facility", "PHC")) if good_match else "PHC"
            matched_facs_with_reasons = match_and_rank_facilities(loc_key, [rec_fac_str], entities=entities)
            matched_facs = [f for f, _ in matched_facs_with_reasons]
            _routing_debug["matched_facility_count"] = len(matched_facs)

        # If user explicitly asked for nearest hospital/doctor for their condition and specified location:
        _wants_nearest_hosp = entities.get("proximity_request", False) or any(
            k in (norm_q + " " + (query or "").lower())
            for k in ["hospital", "clinic", "हॉस्पिटल", "अस्पताल", "दवाखाना", "doctor", "डॉक्टर", "दिखा सकें", "दिखाना"]
        )
        if _wants_nearest_hosp and loc_key and not matched_facs and is_gemini_available():
            ai_fac = query_gemini_facility_search(
                query=query,
                location=loc_key,
                service_needed=str(row["disease"]) if good_match else "Fever / General OPD",
                urgency=urgency,
                response_lang=response_lang,
                entities=entities,
            )
            if ai_fac:
                _routing_debug["route"] = "gemini_facility_locator"
                _routing_debug["location"] = loc_key
                st.session_state["_routing_debug"] = _routing_debug
                return ai_fac

        # ── GEMINI FLASH CLINICAL AI RESOLUTION ──

        if is_gemini_available():
            try:
                gemini_output = query_gemini_flash(
                    query=query,
                    response_lang=response_lang,
                    entities=entities,
                    matched_disease_row=(row if good_match else None),
                    matched_facilities=matched_facs,
                )
                if gemini_output:
                    _routing_debug["route"] = "gemini_flash_triage"
                    _routing_debug["ai_model"] = "gemini_flash"
                    _routing_debug["care_level"] = care_level
                    _routing_debug["disease_matched"] = str(row["disease"]) if good_match else "AI Clinical Synthesis"
                    st.session_state["_routing_debug"] = _routing_debug

                    if "health_records" in st.session_state:
                        rec_cond = str(row["disease"]) if good_match else "General Health Consultation"
                        rec_sev = str(row.get("severity", "N/A")).upper() if pd.notna(row.get("severity")) else "N/A"
                        st.session_state.health_records.append({
                            "date": datetime.now().strftime("%d %b %Y, %I:%M %p"),
                            "query": query[:80] + ("..." if len(query) > 80 else ""),
                            "condition": rec_cond,
                            "severity": rec_sev,
                        })

                    result_html = gemini_output
                    if caution:
                        result_html = caution_banner_html(response_lang) + result_html
                    if matched_facs:
                        result_html += generate_ranked_facility_results(matched_facs[:3], entities, response_lang)
                    return result_html
            except Exception as _gemini_err:
                import traceback
                traceback.print_exc()

        # Fallback to local embedding matcher and translated structured cards
        if good_match and "health_records" in st.session_state:
            st.session_state.health_records.append({"date": datetime.now().strftime("%d %b %Y, %I:%M %p"), "query": query[:80] + ("..." if len(query) > 80 else ""), "condition": str(row["disease"]), "severity": str(row.get("severity", "N/A")).upper() if pd.notna(row.get("severity")) else "N/A"})
        # Store routing debug
        _routing_debug["route"] = "symptom_check"
        _routing_debug["care_level"] = care_level
        _routing_debug["best_score"] = round(best_score, 3)
        _routing_debug["disease_matched"] = str(row["disease"]) if best_score >= 0.48 else None
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
        # Intelligent triage for symptoms not matched to a specific CSV disease
        if is_gemini_available():
            try:
                general_ai_resp = query_gemini_flash(query=query, response_lang=response_lang, entities=entities)
                if general_ai_resp:
                    _routing_debug["route"] = "gemini_symptom_synthesis"
                    _routing_debug["care_level"] = care_level
                    st.session_state["_routing_debug"] = _routing_debug
                    return general_ai_resp
            except Exception:
                pass

        # Local intelligent clinical triage card
        triage_card = format_general_clinical_triage_card(query, entities, response_lang)
        _routing_debug["route"] = "clinical_symptom_triage"
        _routing_debug["care_level"] = care_level
        st.session_state["_routing_debug"] = _routing_debug

        clarifications = build_clarifying_question(entities, primary_intent, response_lang)
        hint = ""
        if clarifications:
            hint = '<div style="background:#F0F7FF;border:1px solid #BAE6FD;border-radius:10px;padding:12px 16px;margin-bottom:10px;">' + "<br>".join(clarifications) + "</div>"

        return hint + triage_card + care_pathway_html("PHC", response_lang)

    # General / Unstructured query fallback with Gemini Flash or intelligent card
    if is_gemini_available():
        try:
            general_ai_resp = query_gemini_flash(query=query, response_lang=response_lang, entities=entities)
            if general_ai_resp:
                _routing_debug["route"] = "gemini_general_query"
                st.session_state["_routing_debug"] = _routing_debug
                return general_ai_resp
        except Exception:
            pass

    return format_general_clinical_triage_card(query, entities, response_lang) + care_pathway_html("PHC", response_lang)
