"""NLP tokenization, entity extraction, phrase matching, and intent classification."""
import re
from src.config.constants import (
    STOPWORDS,
    GENERIC_SYMPTOMS,
    _STEM_EXCEPTIONS,
    _COMPOUND_ACHE_WORDS,
    GENERIC_SYMPTOMS_STEMMED,
    RED_FLAG_PHRASES_EN,
    RED_FLAG_PHRASES_HI,
    RED_FLAG_PHRASES_MR,
    CRITICAL_EMERGENCY_PHRASES_EN,
    CRITICAL_EMERGENCY_PHRASES_HI,
    CRITICAL_EMERGENCY_PHRASES_MR,
    EXTRA_KEYWORDS,
    SERVICE_TOPIC_PATTERNS,
    _INFO_SEEKING_PATTERNS,
    _FACILITY_SEEKING_PATTERNS,
    _SCHEDULE_PATTERNS,
    _INFO_STARTERS,
    _INFO_KEYWORDS,
    INTENT_SYMPTOM_CHECK,
    INTENT_EMERGENCY,
    INTENT_CHILD_HEALTH,
    INTENT_PREGNANCY,
    INTENT_VACCINATION,
    INTENT_FACILITY_SEARCH,
    INTENT_SCHEME_INFORMATION,
    INTENT_MEDICINE_INFORMATION,
    INTENT_TELEMEDICINE,
    INTENT_ABHA,
    INTENT_HELPLINE,
    INTENT_HEALTH_PROGRAM,
    INTENT_GENERAL_HEALTH,
    INTENT_HEALTH_QUERY,
    INTENT_FACILITY,
    INTENT_SCHEME,
    INTENT_MATERNAL_CHILD,
    INTENT_MEDICINE,
    INTENT_DIGITAL_HEALTH,
    INTENT_GENERAL,
    INTENT_IMMUNIZATION_FACILITY_SEARCH,
    INTENT_MATERNITY_FACILITY_SEARCH,
    INTENT_PEDIATRIC_FACILITY_SEARCH,
    INTENT_GENERAL_OPD_SEARCH,
    INTENT_IMMUNIZATION_INFORMATION,
    INTENT_VACCINATION_SCHEDULE,
    INTENT_VACCINATION_CAMP_INFORMATION,
    VALID_INTENTS,
    CARE_EMERGENCY,
    CARE_URGENT,
    CARE_PROMPT_REVIEW,
    CARE_ROUTINE_PHC,
    CARE_SELF_CARE,
    CARE_INFO_ONLY,
)
from src.translation.translator import normalize_for_match

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



def detect_requested_service(combined_text):
    """Detect the healthcare service the user is requesting.
    Returns canonical service name or None."""
    c = combined_text.lower()
    for service, patterns in SERVICE_TOPIC_PATTERNS.items():
        for pat in patterns:
            if pat in c:
                return service
    return None



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



def extract_location(query_en: str, original_query: str) -> str:
    """Extract location, landmark, area, city or district from user query in EN, HI, or MR."""
    q = (query_en or "").strip()
    orig = (original_query or "").strip()

    # 1. Multi-tier Hindi patterns: e.g. 'अभी मैं परी चौक में नोएडा में हूं' or 'परी चौक, नोएडा'
    m_multi_hi = re.search(
        r'(?:अभी\s*मैं|मैं|हम|हमलोग)?\s*([ऀ-ॿA-Za-z0-9\s\-]+?)\s*(?:में|पे|पर)\s*([ऀ-ॿA-Za-z0-9\s\-]+?)\s*(?:में\s*हूं|में|हूँ|हैं|के\s*पास)',
        orig
    )
    if m_multi_hi:
        p1 = m_multi_hi.group(1).strip()
        p2 = m_multi_hi.group(2).strip()
        p1 = re.sub(r'^(अभी|मैं|हम|हमलोग)\s*', '', p1).strip()
        p2 = re.sub(r'^(अभी|मैं|हम|हमलोग)\s*', '', p2).strip()
        if p1 and p2 and len(p1) < 35 and len(p2) < 35:
            if not any(w in p1 for w in ["मुसीबत", "दर्द", "तकलीफ", "बीमारी", "इमरजेंसी", "समस्या"]):
                return f"{p1}, {p2}"

    # 2. English multi-tier: 'at X in Y' or 'in X, Y'
    m_multi_en = re.search(
        r'(?:at|in|near|around)\s+([A-Za-z0-9\s\-]{2,30}?)\s+(?:in|at|near)\s+([A-Za-z0-9\s\-]{2,30}?)(?:\s+where|\s+which|\s+and|\s+hospital|\.|\,|$)',
        q,
        re.I
    )
    if m_multi_en:
        p1 = m_multi_en.group(1).strip()
        p2 = m_multi_en.group(2).strip()
        if p1 and p2:
            return f"{p1}, {p2}"

    # 3. Known cities, NCR landmarks & districts dictionary lookup
    known_locs = [
        ("greater noida", "Greater Noida"), ("pari chowk", "Pari Chowk"),
        ("noida", "Noida"), ("gurugram", "Gurugram"), ("gurgaon", "Gurgaon"),
        ("delhi", "Delhi"), ("new delhi", "New Delhi"), ("ghaziabad", "Ghaziabad"),
        ("faridabad", "Faridabad"), ("meerut", "Meerut"), ("agra", "Agra"),
        ("lucknow", "Lucknow"), ("kanpur", "Kanpur"), ("varanasi", "Varanasi"),
        ("prayagraj", "Prayagraj"), ("allahabad", "Prayagraj"),
        ("mumbai", "Mumbai"), ("pune", "Pune"), ("nagpur", "Nagpur"),
        ("nashik", "Nashik"), ("thane", "Thane"), ("navi mumbai", "Navi Mumbai"),
        ("aurangabad", "Aurangabad"), ("chhatrapati sambhaji nagar", "Chhatrapati Sambhajinagar"),
        ("solapur", "Solapur"), ("kolhapur", "Kolhapur"), ("amravati", "Amravati"),
        ("nanded", "Nanded"), ("jalgaon", "Jalgaon"), ("akola", "Akola"),
        ("latur", "Latur"), ("dhule", "Dhule"), ("ahmednagar", "Ahmednagar"),
        ("chandrapur", "Chandrapur"), ("parbhani", "Parbhani"), ("jalna", "Jalna"),
        ("beed", "Beed"), ("satara", "Satara"), ("yavatmal", "Yavatmal"),
        ("osmanabad", "Dharashiv"), ("dharashiv", "Dharashiv"), ("nandurbar", "Nandurbar"),
        ("wardha", "Wardha"), ("bhandara", "Bhandara"), ("buldhana", "Buldhana"),
        ("gondia", "Gondia"), ("gadchiroli", "Gadchiroli"), ("washim", "Washim"),
        ("hingoli", "Hingoli"), ("palghar", "Palghar"), ("ratnagiri", "Ratnagiri"),
        ("sindhudurg", "Sindhudurg"), ("raigad", "Raigad"), ("melghat", "Melghat"),
        ("dharni", "Dharni"), ("chikhaldara", "Chikhaldara"), ("jawhar", "Jawhar"),
        ("mokhada", "Mokhada"), ("hadgaon", "Hadgaon"), ("aheri", "Aheri"),
        ("bhamragad", "Bhamragad"), ("shahada", "Shahada"), ("pusad", "Pusad"),
        ("kasansur", "Kasansur"), ("harisal", "Harisal"), ("molgi", "Molgi"),
        ("bengaluru", "Bengaluru"), ("bangalore", "Bengaluru"), ("hyderabad", "Hyderabad"),
        ("kolkata", "Kolkata"), ("chennai", "Chennai"), ("jaipur", "Jaipur"),
        ("indore", "Indore"), ("bhopal", "Bhopal"), ("patna", "Patna"),
        ("chandigarh", "Chandigarh"), ("dehradun", "Dehradun"), ("ranchi", "Ranchi"),
        ("ahmedabad", "Ahmedabad"), ("surat", "Surat"), ("vadodara", "Vadodara"),
    ]
    devanagari_locs = [
        ("ग्रेटर नोएडा", "Greater Noida"), ("परी चौक", "Pari Chowk"),
        ("नोएडा", "Noida"), ("गुड़गांव", "Gurugram"), ("गुरुग्राम", "Gurugram"),
        ("गाजियाबाद", "Ghaziabad"), ("फरीदाबाद", "Faridabad"), ("दिल्ली", "Delhi"),
        ("नई दिल्ली", "New Delhi"), ("लखनऊ", "Lucknow"), ("कानपुर", "Kanpur"),
        ("वाराणसी", "Varanasi"), ("आगरा", "Agra"), ("मेरठ", "Meerut"),
        ("मुंबई", "Mumbai"), ("पुणे", "Pune"), ("नागपुर", "Nagpur"),
        ("नासिक", "Nashik"), ("नाशिक", "Nashik"), ("ठाणे", "Thane"),
        ("नवी मुंबई", "Navi Mumbai"), ("औरंगाबाद", "Aurangabad"), ("संभाजीनगर", "Chhatrapati Sambhajinagar"),
        ("सोलापूर", "Solapur"), ("कोल्हापूर", "Kolhapur"), ("अमरावती", "Amravati"),
        ("नांदेड", "Nanded"), ("जळगाव", "Jalgaon"), ("अकोला", "Akola"),
        ("लातूर", "Latur"), ("धुळे", "Dhule"), ("अहमदनगर", "Ahmednagar"),
        ("चंद्रपूर", "Chandrapur"), ("परभणी", "Parbhani"), ("जालना", "Jalna"),
        ("बीड", "Beed"), ("सातारा", "Satara"), ("यवतमाळ", "Yavatmal"),
        ("उस्मानाबाद", "Dharashiv"), ("धाराशिव", "Dharashiv"), ("नंदुरबार", "Nandurbar"),
        ("वर्धा", "Wardha"), ("भंडारा", "Bhandara"), ("बुलढाणा", "Buldhana"),
        ("गोंदिया", "Gondia"), ("गडचिरोली", "Gadchiroli"), ("वाशीम", "Washim"),
        ("हिंगोली", "Hingoli"), ("पालघर", "Palghar"), ("रत्नागिरी", "Ratnagiri"),
        ("सिंधुदुर्ग", "Sindhudurg"), ("रायगड", "Raigad"), ("मेळघाट", "Melghat"),
        ("धरणी", "Dharni"), ("चिखलदरा", "Chikhaldara"), ("जव्हार", "Jawhar"),
        ("मोखाडा", "Mokhada"), ("शहादा", "Shahada"), ("पुसद", "Pusad"),
        ("अहेरी", "Aheri"), ("भामरगड", "Bhamragad"), ("हरिसळ", "Harisal"),
        ("मोळगी", "Molgi"), ("बंगलोर", "Bengaluru"), ("बेंगलुरु", "Bengaluru"),
        ("हैदराबाद", "Hyderabad"), ("कोलकाता", "Kolkata"), ("चेन्नई", "Chennai"),
        ("जयपुर", "Jaipur"), ("इंदौर", "Indore"), ("भोपाल", "Bhopal"),
        ("पटना", "Patna"), ("अहमदाबाद", "Ahmedabad"), ("सूरत", "Surat"),
    ]

    combined_lower = (q + " " + orig).lower()
    matched_parts = []
    for dev_k, canonical in devanagari_locs:
        if dev_k in orig:
            if canonical not in matched_parts:
                matched_parts.append(canonical)
    for eng_k, canonical in known_locs:
        if eng_k in combined_lower:
            if canonical not in matched_parts:
                matched_parts.append(canonical)

    if matched_parts:
        return ", ".join(matched_parts[:2])

    # 4. Generic single patterns: e.g. 'X में हूं', 'at X'
    m_single_hi = re.search(
        r'(?:अभी\s*मैं|मैं|हम)?\s*([ऀ-ॿA-Za-z0-9\s\-]{2,30}?)\s*(?:में\s*हूं|में\s*रहते|के\s*पास|जवळ)',
        orig
    )
    if m_single_hi:
        cand = m_single_hi.group(1).strip()
        cand = re.sub(r'^(अभी|मैं|हम|हमलोग)\s*', '', cand).strip()
        if cand and not any(w in cand for w in ["मुसीबत", "दर्द", "तकलीफ", "बीमारी", "इमरजेंसी", "समस्या", "घर"]):
            if len(cand) >= 2 and len(cand) <= 30:
                return cand

    return None


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

    # Location/district extraction — supports landmarks, cities, districts in Latin & Devanagari
    loc = extract_location(query_en, original_query)
    if loc:
        entities["location"] = loc
        entities["district"] = loc.split(",")[-1].strip() if "," in loc else loc

    # Legacy fallback district checks if extract_location returned None
    if not entities.get("district"):
        districts = ["nandurbar","gadchiroli","melghat","palghar","yavatmal",
                     "dharni","chikhaldara","jawhar","mokhada","hadgaon","aheri",
                     "bhamragad","shahada","pusad","kasansur","harisal","molgi"]
        for d in districts:
            if d in q or d in orig:
                entities["district"] = d.title()
                entities["location"] = d.title()
                break

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
                entities["location"] = dist_name
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
                        "sabse kareeb", "kareebi", "closest government", "paas", "ke paas",
                        "जवळचे", "जवळचा", "नजीक", "सबसे जवळ",
                        "आस पास", "आस-पास", "नियरेस्ट", "नजदीक", "नजदीकी", "पास में", "कहाँ है", "किधर है", "दिखा सकें", "कहाँ दिखाएं"]
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


def classify_intent(query_en, original_query):
    """Semantic intent classifier with 15 canonical intents.
    Returns (primary_intent, secondary_intent_or_None, confidence).
    Separates INTENT (action) from TOPIC (healthcare domain).
    Never invents intent names outside VALID_INTENTS."""
    q = (query_en or "").lower().strip()
    orig = (original_query or "").lower().strip()
    combined = q + " " + orig

    # --- EMERGENCY: highest priority, always runs first ---
    romanized_emergency = [
        "seene mein dard","chest pain","saans lene mein","saans nahi",
        "behosh","bekhabar","bahut dard","tez dard","emergency help",
        "need emergency","blood aa raha","khun aa raha","dil ka attack",
        "heart attack","stroke","fits aa rahe","seizure",
        "difficulty breathing","severe breathing","unconscious",
        "severe chest pain","heavy bleeding","convulsions",
        "pet mein chaku","chaku laga","chaku","stab","knife",
        "goli lagi","jahar","visha","saanp kata","saap chawla"
    ]
    is_romanized_emerg = any(p in combined for p in romanized_emergency)
    if has_red_flags(original_query, query_en) or is_critical_emergency(original_query, query_en) or is_romanized_emerg:
        # Specialized Trauma Classification
        penetrating_kw = ["knife","stab","stabbed","stabbing","impaled","bullet","gunshot","blade","penetrating",
                          "चाकू","छुरा","गोली","सुरी"]
        if any(k in combined for k in penetrating_kw):
            return INTENT_EMERGENCY, "TRAUMA_PENETRATING", 0.99

        snake_kw = ["snake","snakebite","cobra","viper","krait","scorpion","सांप","साप","सर्पदंश","बिच्छू","विंचू"]
        if any(k in combined for k in snake_kw):
            return INTENT_EMERGENCY, "TRAUMA_SNAKEBITE", 0.99

        poison_kw = ["poison","poisoning","pesticide","insecticide","rat poison","overdose","chemical ingestion",
                     "जहर","विष","विषबाधा","कीटनाशक"]
        if any(k in combined for k in poison_kw):
            return INTENT_EMERGENCY, "TRAUMA_POISON", 0.99

        burn_kw = ["burn","burns","acid","fire","जल गया","भाजले","एसिड"]
        if any(k in combined for k in burn_kw):
            return INTENT_EMERGENCY, "TRAUMA_BURNS", 0.99

        accident_kw = ["accident","crash","collision","fall from height","head injury","skull fracture",
                       "एक्सीडेंट","दुर्घटना","अपघात"]
        if any(k in combined for k in accident_kw):
            return INTENT_EMERGENCY, "TRAUMA_ACCIDENT", 0.99

        cardiac_kw = ["chest pain","heart attack","cardiac","stroke","paralysis",
                      "सीने में दर्द","छाती में दर्द","हार्ट अटैक","दिल का दौरा","पक्षाघात","लकवा"]
        if any(k in combined for k in cardiac_kw):
            return INTENT_EMERGENCY, "TRAUMA_CARDIAC", 0.99

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
    _has_fac_word = any(k in q or k in orig for k in ["hospital","phc","chc","clinic","अस्पताल","रुग्णालय","हॉस्पिटल","दवाखाना"])
    _has_sch_word = any(k in q or k in orig for k in ["scheme","yojana","kharcha","cover","insurance",
        "mjpjay","ayushman","pmjay","cashless","benefit","eligibility","free treatment","योजना"])
    if _has_fac_word and _has_sch_word:
        return INTENT_SCHEME_INFORMATION, None, 0.85

    # --- FACILITY_SEARCH (general, not topic-specific above) ---
    fac_long = ["hospital","clinic","nearest hospital","government hospital",
                "hospital list","civil hospital","district hospital","opd",
                "रुग्णालय","अस्पताल","सरकारी अस्पताल","जवळचे",
                "हॉस्पिटल","हॉस्पिटल्स","दवाखाना","चिकित्सालय","क्लिनिक","doctor","डॉक्टर",
                "दिखा सकें","दिखाना है","चेक कराना"]
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
