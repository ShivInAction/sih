"""Constants, dictionaries, schedules, and language maps for MahaArogya Setu."""
import re

# Columns and dataset metadata
REQUIRED_COLUMNS = ["disease", "symptoms", "prevention", "when_to_see_doctor", "home_care"]
ENHANCED_COLUMNS = ["severity", "age_group", "category", "rural_prevalence", "govt_free_treatment", "recommended_facility"]

STOPWORDS = {"a","an","the","and","or","in","of","with","for","to","my","me","i","i'm","im","have","has","had","is","are","was","were","am","it","this","that","some","someone","feeling","feel","got","get"}
GENERIC_SYMPTOMS = {"fever","pain","cough","fatigue","headache","weakness","rash","nausea","vomiting","cold","ache","tired","tiredness","sick"}
_STEM_EXCEPTIONS = {"aches":"ache","headaches":"headache","stomachaches":"stomachache"}
_COMPOUND_ACHE_WORDS = ("head","body","ear","stomach","tooth","back","neck","belly")



# Districts and Facility Data
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



# Government Schemes and Schedules
MAHARASHTRA_SCHEMES = [
    {"name":"Mahatma Jyotirao Phule Jan Arogya Yojana (MJPJAY)","benefits":"Cashless treatment up to ₹5,00,000/family/year for 996 identified procedures.","eligibility":"Yellow, Orange, AAY, Annapurna Ration cards. Farmers in 14 distressed districts. Eligibility depends on scheme rules — verify through official channel.","apply_how":"Visit any empanelled hospital → 'Arogyamitra' desk with Ration Card + Aadhaar.","what_to_carry":"Yellow/Orange/AAY Ration Card, Aadhaar Card","verify_at":"Visit arogyamitra desk at empanelled hospital or call 1800-233-2085","source":"maha.gov.in","status":"LIVE"},
    {"name":"Ayushman Bharat - PMJAY (Integrated with MJPJAY)","benefits":"Cashless cover up to ₹5,00,000/family/year for secondary & tertiary care.","eligibility":"SECC 2011 identified poor & vulnerable families. Eligibility depends on scheme rules — verify through official channel.","apply_how":"Verify at abdm.gov.in or contact Arogyamitra at any empanelled facility.","what_to_carry":"Aadhaar Card, Ration Card","verify_at":"abdm.gov.in or call 14555","source":"abdm.gov.in","status":"LIVE"},
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


# NLP stemming helpers & Keyword lists
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

RED_FLAG_PHRASES_EN = [
    "difficulty breathing","shortness of breath","can't breathe","cannot breathe","unable to breathe","hard to breathe","breathless","gasping",
    "chest pain","pain in chest","tightness in chest","pressure in chest",
    "knife in stomach","knife in abdomen","knife in chest","knife wound","knife cut","knife","stab in stomach","stab wound","stabbed","stabbing","stab","impaled","penetrating wound","blade wound",
    "gunshot","bullet wound","bullet","shot in",
    "severe bleeding","uncontrolled bleeding","heavy bleeding","profuse bleeding","bleeding stomach","bleeding from ear","arterial bleed","deep cut","slashed",
    "unconscious","unconsciousness","fainted","fainting","passed out","collapsed","not waking","not responding","loss of consciousness",
    "coughing blood","coughing up blood","vomiting blood","blood in vomit","blood in stool","bloody stool","black stool",
    "seizure","seizures","convulsion","convulsions","stiff neck","neck stiffness","blue lips","bluish lips","blue face",
    "severe abdominal pain","severe stomach pain","confusion","disoriented","very drowsy","difficulty swallowing","cannot swallow",
    "snake bite","snakebite","cobra bite","viper bite","scorpion sting",
    "poison","poisoning","swallowed poison","consumed poison","drank poison","rat poison","pesticide","insecticide","chemical ingestion","overdose",
    "severe burn","third degree burn","fire burn","acid burn","acid attack",
    "electric shock","electrocution","electrocuted","choking","choked","drowning","near drowning","hanging","strangulation",
    "road accident","car accident","car crash","bike accident","vehicle collision","fall from height","head injury","skull fracture","severe accident",
    "heart attack","cardiac arrest","stroke","paralysis","facial drooping","slurred speech",
    "no urine","not passing urine","sunken eyes","high fever not improving","fever not improving after 3 days","hot dry skin","not sweating"
]

RED_FLAG_PHRASES_HI = [
    "सांस लेने में तकलीफ","सांस नहीं आ","सांस फूल","सांस लेने में दिक्कत","सांस लेने में बहुत","सांस में तकलीफ","सांस में दिक्कत",
    "बेहोश","बेहोशी","सीने में दर्द","छाती में दर्द","खून की उल्टी","खून आ रहा","खून निकल","दौरा पड़","दौरे आ","गर्दन अकड़",
    "पेट में चाकू","चाकू लगा","चाकू घोंप","चाकू मार","चाकू पेट","चाकू","छुरा","गोली लगी","गोली मार",
    "जहर खा","जहर पी","जहर","कीटनाशक","दवा ज्यादा खा ली",
    "सांप काट","सांप ने काटा","सांप का डस","बिच्छू","बिच्छू काट",
    "जल गया","आग लग","एसिड गिर","एसिड",
    "करंट लग","बिजली का झटका","गला घुट","सांस घुट","डूब गया",
    "एक्सीडेंट","दुर्घटना","गाड़ी से टकरा","सिर में चोट","सिर फट गया",
    "खून बह रहा","खून रुक नहीं","गंभीर घाव","गहरा घाव",
    "हार्ट अटैक","दिल का दौरा","लकवा","स्ट्रोक"
]

RED_FLAG_PHRASES_MR = [
    "श्वास घेण्यास त्रास","श्वास घेण्यास खूप","श्वास लागला","श्वास घेऊ शकत नाही","दम लागणे","छातीत दुखणे",
    "बेहोश","शुद्ध हरपणे","रक्ताची उलटी","रक्तस्त्राव","झटके येणे","फिट येणे","मान आखडणे","पोटात तीव्र वेदना","लघवी न होणे",
    "गरोदरपणात रक्तस्त्राव","गरोदरपणात तीव्र पोटदुखी",
    "पोटात सुरी","पोटात चाकू","सुरी खुपसली","चाकू लागला","चाकू मारला","सुरी","चाकू","गोळी लागली",
    "विष प्राशन","विष घेतले","विषबाधा","कीटकनाशक",
    "साप चावला","सर्पदंश","विंचू चावला",
    "भाजले","गंभीर भाजले","आगीत","एसिड",
    "विजेचा धक्का","करंट बसला","श्वास गुदमरतोय","घशात अडकले","बुडाला",
    "अपघात झाला","गंभीर अपघात","डोक्याला मार","रक्तस्त्राव थांबत नाही","खूप रक्त",
    "हार्ट अटॅक","हृदयविकाराचा झटका","पक्षाघात","लकवा"
]

CRITICAL_EMERGENCY_PHRASES_EN = [
    "difficulty breathing","shortness of breath","can't breathe","cannot breathe","unable to breathe","hard to breathe","breathless","gasping",
    "chest pain","pain in chest","tightness in chest","pressure in chest",
    "knife in stomach","knife in abdomen","knife in chest","knife wound","knife cut","knife","stab in stomach","stab wound","stabbed","stabbing","stab","impaled","penetrating wound",
    "gunshot","bullet wound","bullet","shot in",
    "unconscious","unconsciousness","fainted","fainting","passed out","collapsed","not waking","not responding","loss of consciousness",
    "coughing blood","coughing up blood","vomiting blood","blood in vomit",
    "severe bleeding","uncontrolled bleeding","heavy bleeding","profuse bleeding","arterial bleed",
    "snake bite","snakebite","cobra bite","viper bite","poison","poisoning","pesticide","rat poison","chemical ingestion",
    "severe burn","third degree burn","acid burn","electric shock","electrocution","choking","drowning","hanging",
    "road accident","car crash","bike crash","head injury","skull fracture",
    "heart attack","cardiac arrest","stroke","paralysis",
    "seizure","seizures","convulsion","convulsions","blue lips","bluish lips","blue face","confusion","disoriented","very drowsy"
]

CRITICAL_EMERGENCY_PHRASES_HI = [
    "सांस लेने में तकलीफ","सांस नहीं आ","सांस फूल","बेहोश","बेहोशी","सीने में दर्द","छाती में दर्द","खून की उल्टी","खून आ रहा","खून निकल","दौरा पड़","दौरे आ",
    "पेट में चाकू","चाकू लगा","चाकू घोंप","चाकू","छुरा","गोली लगी","जहर खा","जहर पी","जहर","कीटनाशक",
    "सांप काट","सांप ने काटा","बिच्छू","जल गया","एसिड","करंट लग","गला घुट","डूब गया","एक्सीडेंट","दुर्घटना","सिर में चोट","खून रुक नहीं रहा","हार्ट अटैक","दिल का दौरा","लकवा","स्ट्रोक"
]

CRITICAL_EMERGENCY_PHRASES_MR = [
    "श्वास घेण्यास त्रास","श्वास घेण्यास खूप","श्वास लागला","श्वास घेऊ शकत नाही","दम लागणे","छातीत दुखणे",
    "बेहोश","शुद्ध हरपणे","रक्ताची उलटी","रक्तस्त्राव","झटके येणे","फिट येणे",
    "पोटात सुरी","पोटात चाकू","सुरी खुपसली","चाकू लागला","सुरी","चाकू","गोळी लागली",
    "विष प्राशन","विष घेतले","विषबाधा","कीटकनाशक","साप चावला","सर्पदंश","विंचू चावला",
    "भाजले","एसिड","विजेचा धक्का","श्वास गुदमरतोय","बुडाला","अपघात झाला","गंभीर अपघात","डोक्याला मार","रक्तस्त्राव थांबत नाही",
    "हार्ट अटॅक","हृदयविकाराचा झटका","पक्षाघात"
]

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



# Devanagari translation maps
_DEVANAGARI_HI_MAP = [("सांस लेने में तकलीफ","difficulty breathing"),("सांस नहीं आ","cannot breathe"),("सांस फूल","shortness of breath"),("सीने में दर्द","chest pain"),("छाती में दर्द","chest pain"),("खून की उल्टी","vomiting blood"),("बेहोश","unconscious"),("दौरा पड़","seizure"),("दौरे आ","seizure"),("गर्दन अकड़","stiff neck"),("आँखों के पीछे दर्द","pain behind eyes"),("कंपकंपी","chills"),("ठंड लग","chills"),("कांप","shivering"),("रात को पसीना","night sweats"),("दो हफ्ते से खांसी","cough lasting more than 2 weeks"),("लंबे समय से खांसी","persistent cough"),("खांसी के साथ बलगम","cough with phlegm"),("बलगम","phlegm"),("चावल के पानी जैसे दस्त","rice water stools"),("पतले दस्त","loose stools"),("पानी जैसे दस्त","watery stools"),("दस्त हो रहे","diarrhea"),("दस्त हो रहा","diarrhea"),("आंखें लाल","red eyes"),("आँखें लाल","red eyes"),("आंख लाल","red eye"),("आँख लाल","red eye"),("त्वचा पीली","yellow skin"),("पेशाब में जलन","burning urination"),("बार बार पेशाब","frequent urination"),("बहुत प्यास","increased thirst"),("पेशाब में खून","blood in urine"),("जोड़ों में दर्द","joint pain"),("गले में दर्द","sore throat"),("गला खराब","sore throat"),("मांसपेशियों में दर्द","muscle pain"),("शरीर में दर्द","body ache"),("पीठ दर्द","back pain"),("कमर दर्द","back pain"),("पेट में दर्द","stomach pain"),("सिर में तेज दर्द","throbbing headache"),("सिर में दर्द","headache"),("रात में खुजली","itching at night"),("त्वचा पर खुजली","itchy skin"),("उंगलियों के बीच","between fingers"),("घरघराहट","wheezing"),("तेज बुखार","high fever"),("बुखार है","fever"),("बुखार","fever"),("खांसी","cough"),("सिर दर्द","headache"),("सिरदर्द","headache"),("पेट दर्द","stomach pain"),("पेट खराब","diarrhea"),("चक्कर","dizzy"),("कमजोरी","weakness"),("थकान","tiredness"),("उल्टी","vomiting"),("दस्त","diarrhea"),("जुकाम","cold"),("नाक बह","runny nose"),("नाक बंद","blocked nose"),("घबराहट","anxiety"),("चिंता","stress"),("तनाव","stress"),("खुजली","itching"),("दर्द","pain"),("प्यास","thirst"),("भूख","appetite"),("सिर","head"),("आँख","eye"),("आंख","eye"),("नाक","nose"),("गला","throat"),("कान","ear"),("पेट","stomach"),("छाती","chest"),("खून","blood"),("सांस","breath"),("जोड़","joint"),("त्वचा","skin")]

_DEVANAGARI_MR_MAP = [("श्वास घेण्यास त्रास", "difficulty breathing"),
    ("श्वास घेण्यास खूप", "difficulty breathing"),
    ("श्वास लागला", "difficulty breathing"),
    ("श्वास घेऊ शकत नाही", "difficulty breathing"),
    ("दम लागणे","shortness of breath"),("छातीत दुखणे","chest pain"),("रक्ताची उलटी","vomiting blood"),("शुद्ध हरपणे","unconscious"),("ताप आणि थंडी","fever with chills"),("खोकला","cough"),("ताप","fever"),("पोटदुखी","stomach pain"),("डोकेदुखी","headache"),("अतिसार","diarrhea"),("उलटी","vomiting"),("अशक्तपणा","weakness"),("खाज","itching"),("सांधेदुखी","joint pain"),("तोंड कोरडे पडणे","dehydration"),("गरोदरपणात रक्तस्त्राव","bleeding during pregnancy"),("गरोदरपणात तीव्र पोटदुखी","severe abdominal pain during pregnancy")]


# Service Synonyms & Topic Patterns
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


# Query intent pattern sets
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

_INFO_STARTERS = ("can ","could ","does ","do ","did ","is ","are ","will ","would ","should ","what ","which ","how ","why ","when ")
_INFO_KEYWORDS = (" cause"," causes"," mean"," means"," lead to"," symptom"," symptoms"," sign"," signs"," treatment"," treat"," prevent"," prevention"," avoid"," cure"," contagious")


# Structured Intent Enums
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


# Care levels
# --- CARE LEVELS ---
CARE_EMERGENCY = "EMERGENCY"
CARE_URGENT = "URGENT"
CARE_PROMPT_REVIEW = "PROMPT_CLINICAL_REVIEW"
CARE_ROUTINE_PHC = "ROUTINE_PHC"
CARE_SELF_CARE = "SELF_CARE_AND_MONITOR"
CARE_INFO_ONLY = "INFORMATION_ONLY"


# Caution Notes & Warnings
CAUTION_NOTE = "⚠️ Your question mentions a symptom that can be serious. Call **108** if experiencing it now.\n\n"
TRANSLATION_FAILED_NOTE = "⚠️ Automatic translation failed — answer shown in English:\n\n"
_GLOBAL_TRANSLATION_CACHE = {}


# Card UI I18N
_CARD_I18N = {
    "en": {"badge":"Health Awareness Summary","symptoms":"Common Symptoms","prevention":"Prevention & Protection","home_care":"Home Care Guidance","doctor":"When to See a Doctor","related":"Other conditions to read about","disclaimer":"This is general awareness — not a clinical diagnosis. Always consult a doctor."},
    "hi": {"badge":"स्वास्थ्य जागरूकता","symptoms":"सामान्य लक्षण","prevention":"रोकथाम","home_care":"घरेलू देखभाल","doctor":"डॉक्टर से कब मिलें","related":"अन्य संबंधित स्थितियां","disclaimer":"यह सामान्य जानकारी है, चिकित्सकीय निदान नहीं। डॉक्टर से परामर्श लें।"},
    "mr": {"badge":"आरोग्य जागरूकता","symptoms":"सामान्य लक्षणे","prevention":"प्रतिबंध","home_care":"घरगुती काळजी","doctor":"डॉक्टरांचा सल्ला","related":"इतर संबंधित आजार","disclaimer":"ही सामान्य माहिती आहे, वैद्यकीय निदान नाही. डॉक्टरांचा सल्ला घ्या."},
}


# Language Modes
MODE_ENGLISH = "English"
MODE_HINDI = "हिंदी (Hindi)"
MODE_MARATHI = "मराठी (Marathi)"
MODE_AUTO = "🌐 Auto-detect"
LANGUAGES = [MODE_ENGLISH, MODE_HINDI, MODE_MARATHI, MODE_AUTO]

# UI Strings
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
        "sch_desc": "Reference information on cashless treatment schemes. Verify current details at your nearest government hospital or abdm.gov.in.",
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
        "sch_desc": "कैशलेस उपचार योजनाओं की संदर्भ जानकारी। नवीनतम विवरण अपने नजदीकी सरकारी अस्पताल या abdm.gov.in पर सत्यापित करें।",
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
