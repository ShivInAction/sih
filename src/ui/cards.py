"""HTML card generators, UI widgets, and dialog renderers."""
import html
import re
from datetime import datetime, timedelta
import pandas as pd
import streamlit as st
from src.config.constants import (
    _CARD_I18N,
    MAHARASHTRA_DISTRICTS,
    MAHARASHTRA_SCHEMES,
    GENERIC_MEDS,
    HEALTH_CAMPS,
    ABHA_INFO,
    CARE_EMERGENCY,
    CARE_URGENT,
    CARE_PROMPT_REVIEW,
    CARE_ROUTINE_PHC,
    CARE_SELF_CARE,
    CARE_INFO_ONLY,
    INTENT_FACILITY,
    INTENT_FACILITY_SEARCH,
    INTENT_IMMUNIZATION_FACILITY_SEARCH,
    INTENT_MATERNITY_FACILITY_SEARCH,
    INTENT_PEDIATRIC_FACILITY_SEARCH,
    INTENT_GENERAL_OPD_SEARCH,
    INTENT_HEALTH_QUERY,
    INTENT_VACCINATION,
    INTENT_PREGNANCY,
    INTENT_CHILD_HEALTH,
)
from src.ml.nlp_utils import _derive_required_services

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

    # Build symptoms text from entities
    symptom_list = entities.get("symptoms", [])
    symptom_text = ", ".join(symptom_list) if symptom_list else ""

    parts = []

    # Show disease name prominently
    disease_name = html.escape(disease)
    parts.append(f'<div style="background:#F8FAFC;border:1px solid #E2E8F0;border-radius:10px;padding:10px 14px;margin-bottom:10px;font-size:0.88rem;"><strong>{cl}</strong> — {disease_name}</div>')

    desc_label = "YOU DESCRIBED" if response_lang == "en" else ("आपने बताया" if response_lang == "hi" else "तुम्ही साँगिता")
    # Show actual symptoms from the query, not generic placeholder
    if context_str and symptom_text:
        desc_text = f"{context_str} — {symptom_text}"
    elif symptom_text:
        desc_text = symptom_text
    elif context_str:
        desc_text = context_str
    else:
        desc_text = "symptoms described" if response_lang == "en" else ("बताए गए लक्षण" if response_lang == "hi" else "साँगिलेले लक्षणे")
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



def format_trauma_emergency_card(trauma_type="TRAUMA_PENETRATING", query="", lang="en"):
    """Render a dedicated clinical trauma first-aid card for life-threatening emergencies."""
    tt = str(trauma_type or "").upper()
    q_lower = (query or "").lower()

    is_penetrating = "PENETRATING" in tt or any(w in q_lower for w in [
        "knife", "stab", "stabbed", "stabbing", "impaled", "bullet", "gunshot", "blade", "penetrating",
        "चाकू", "छुरा", "गोली", "सुरी", "वार"
    ])
    is_snake = "SNAKE" in tt or any(w in q_lower for w in [
        "snake", "snakebite", "cobra", "viper", "krait", "scorpion", "सांप", "साप", "सर्पदंश", "विंचू"
    ])
    is_poison = "POISON" in tt or any(w in q_lower for w in [
        "poison", "poisoning", "pesticide", "insecticide", "rat poison", "overdose", "chemical ingestion", "जहर", "विष", "विषबाधा", "कीटनाशक"
    ])
    is_burn = "BURN" in tt or any(w in q_lower for w in [
        "burn", "burns", "acid", "fire", "जल गया", "भाजले", "आगीत"
    ])

    if is_penetrating:
        if lang == "mr":
            return """
<div class="th-dx-card" style="border: 2.5px solid #DC2626; box-shadow: 0 10px 30px rgba(220, 38, 38, 0.22); margin-bottom: 14px;">
    <div class="th-dx-header" style="background: linear-gradient(135deg, #991B1B 0%, #DC2626 100%);">
        <div style="display:flex;align-items:center;gap:10px;">
            <span style="font-size:24px;">🚨</span>
            <div>
                <strong style="font-size:1.02rem;color:#FFFFFF;display:block;">अति-तातडीची सर्जिकल आणीबाणी: वार / पोटात सुरी किंवा शस्त्र</strong>
                <span style="font-size:0.75rem;color:#FEE2E2;font-weight:700;">CRITICAL TRAUMA · तातडीने शस्त्रक्रिया आवश्यक</span>
            </div>
        </div>
        <span style="background:rgba(255,255,255,0.25);color:#FFFFFF;padding:4px 10px;border-radius:999px;font-size:0.72rem;font-weight:700;">
            १०८ ला कॉल करा
        </span>
    </div>
    <div class="th-dx-body" style="padding:20px 24px;color:#0F172A;line-height:1.65;">
        <div style="background:#FEF2F2;border-left:5px solid #DC2626;border-radius:8px;padding:12px 16px;margin-bottom:14px;color:#991B1B;font-weight:700;font-size:0.95rem;">
            ⚠️ सर्वात महत्त्वाचा जीवनरक्षक नियम: पोटात घुसलेली सुरी किंवा वस्तू अजिबात बाहेर काढू नका!
        </div>
        <p style="font-size:0.90rem;color:#334155;margin-bottom:12px;">
            घुसलेली वस्तू बाहेर काढल्यास अंतर्गत रक्तवाहिन्या उघड्या पडून प्रचंड रक्तस्त्राव होतो आणि काही मिनिटांत मृत्यू होऊ शकतो. केवळ शस्त्रक्रियागृहातच (OT) सर्जन ती काढतील.
        </p>
        <h4 style="color:#991B1B;margin:12px 0 8px 0;font-size:0.95rem;">🩹 तातडीचे प्रथमोपचार (Immediate First Aid):</h4>
        <ul style="margin:0 0 14px 18px;padding:0;font-size:0.90rem;color:#1E293B;">
            <li><strong>सुरी स्थिर करा:</strong> सुरीच्या दोन्ही बाजूंना स्वच्छ कापडाच्या घड्या किंवा टॉवेल लावून ती हलणार नाही याची काळजी घ्या.</li>
            <li><strong>जखमेभोवती हलका दाब:</strong> सुरीवर दाब देऊ नका, जखमेच्या आजूबाजूला स्वच्छ कापडाने दाबून रक्तस्त्राव रोखा.</li>
            <li><strong>रुग्णाची स्थिती:</strong> रुग्णाला पाठीवर शांत झोपवा, पोटावरील ताण कमी करण्यासाठी गुडघे थोडे दुमडून ठेवा. पांघरूण घाला.</li>
            <li><strong>काहीही खाऊ किंवा पिऊ घालू नका (Nil by Mouth):</strong> तात्काळ भूल देऊन शस्त्रक्रिया करावी लागत असल्याने रुग्णाला पाणी किंवा अन्न अजिबात देऊ नका.</li>
            <li><strong>रुग्णालय:</strong> रक्तपेढी व शस्त्रक्रियागृह असलेल्या जवळच्या उपजिल्हा (SDH) किंवा जिल्हा रुग्णालयात (DH) त्वरित दाखल करा.</li>
        </ul>
    </div>
</div>"""
        if lang == "hi":
            return """
<div class="th-dx-card" style="border: 2.5px solid #DC2626; box-shadow: 0 10px 30px rgba(220, 38, 38, 0.22); margin-bottom: 14px;">
    <div class="th-dx-header" style="background: linear-gradient(135deg, #991B1B 0%, #DC2626 100%);">
        <div style="display:flex;align-items:center;gap:10px;">
            <span style="font-size:24px;">🚨</span>
            <div>
                <strong style="font-size:1.02rem;color:#FFFFFF;display:block;">अति-गंभीर सर्जिकल आपातकाल: पेट में चाकू / गहरा घाव (Stab Wound)</strong>
                <span style="font-size:0.75rem;color:#FEE2E2;font-weight:700;">CRITICAL TRAUMA · तत्काल सर्जरी आवश्यक</span>
            </div>
        </div>
        <span style="background:rgba(255,255,255,0.25);color:#FFFFFF;padding:4px 10px;border-radius:999px;font-size:0.72rem;font-weight:700;">
            108 पर कॉल करें
        </span>
    </div>
    <div class="th-dx-body" style="padding:20px 24px;color:#0F172A;line-height:1.65;">
        <div style="background:#FEF2F2;border-left:5px solid #DC2626;border-radius:8px;padding:12px 16px;margin-bottom:14px;color:#991B1B;font-weight:700;font-size:0.95rem;">
            ⚠️ सबसे महत्वपूर्ण जीवनरक्षक नियम: पेट में धंसे हुए चाकू या वस्तु को बिल्कुल बाहर न निकालें!
        </div>
        <p style="font-size:0.90rem;color:#334155;margin-bottom:12px;">
            चाकू बाहर निकालने की गलती कभी न करें। चाकू अभी आंतरिक रक्तवाहिकाओं को दबाए हुए है; निकालने पर आंतरिक खून का फव्वारा छूट सकता है और मरीज की कुछ ही मिनटों में जान जा सकती है। इसे केवल अस्पताल के ऑपरेशन थिएटर में सर्जन ही निकालेंगे।
        </p>
        <h4 style="color:#991B1B;margin:12px 0 8px 0;font-size:0.95rem;">🩹 तत्काल प्राथमिक उपचार (Immediate First Aid Steps):</h4>
        <ul style="margin:0 0 14px 18px;padding:0;font-size:0.90rem;color:#1E293B;">
            <li><strong>चाकू को स्थिर करें:</strong> चाकू के दोनों तरफ साफ कपड़ा या तौलिया मोड़कर रखें ताकि चाकू जरा भी न हिले-डुले।</li>
            <li><strong>घाव के आसपास दबाव बनाएं:</strong> चाकू पर दबाव न दें, घाव के चारों तरफ हल्के हाथ से साफ कपड़े से दबाएं ताकि खून का बहाव कम हो।</li>
            <li><strong>मरीज को सही लिटाएं:</strong> मरीज को पीठ के बल लिटाएं, पेट की मांसपेशियों का तनाव कम करने के लिए घुटनों को हल्का मोड़ें, और कंबल से ढकें ताकि शॉक न लगे।</li>
            <li><strong>पानी या खाना बिल्कुल न दें:</strong> मरीज को पानी, चाय या खाना बिल्कुल न दें, क्योंकि तुरंत इमरजेंसी ऑपरेशन (जनरल एनेस्थीसिया) करना पड़ सकता है।</li>
            <li><strong>सीधे जिला अस्पताल ले जाएं:</strong> मरीज को सीधे जिला अस्पताल (DH) या ट्रॉमा सेंटर ले जाएं जहां सर्जन और ब्लड बैंक उपलब्ध हो।</li>
        </ul>
    </div>
</div>"""

        return """
<div class="th-dx-card" style="border: 2.5px solid #DC2626; box-shadow: 0 10px 30px rgba(220, 38, 38, 0.22); margin-bottom: 14px;">
    <div class="th-dx-header" style="background: linear-gradient(135deg, #991B1B 0%, #DC2626 100%);">
        <div style="display:flex;align-items:center;gap:10px;">
            <span style="font-size:24px;">🚨</span>
            <div>
                <strong style="font-size:1.02rem;color:#FFFFFF;display:block;">CRITICAL SURGICAL EMERGENCY: PENETRATING ABDOMINAL TRAUMA / STAB WOUND</strong>
                <span style="font-size:0.75rem;color:#FEE2E2;font-weight:700;">IMMEDIATE SURGICAL ATTENTION REQUIRED</span>
            </div>
        </div>
        <span style="background:rgba(255,255,255,0.25);color:#FFFFFF;padding:4px 10px;border-radius:999px;font-size:0.72rem;font-weight:700;">
            CALL 108 NOW
        </span>
    </div>
    <div class="th-dx-body" style="padding:20px 24px;color:#0F172A;line-height:1.65;">
        <div style="background:#FEF2F2;border-left:5px solid #DC2626;border-radius:8px;padding:12px 16px;margin-bottom:14px;color:#991B1B;font-weight:700;font-size:0.95rem;">
            ⚠️ VITAL LIFE-SAVING RULE: DO NOT REMOVE OR PULL OUT THE KNIFE OR IMPALED OBJECT!
        </div>
        <p style="font-size:0.90rem;color:#334155;margin-bottom:12px;">
            Never attempt to remove the knife or impaled object. The object currently exerts a tamponade effect, plugging injured major blood vessels and internal organs. Removing it outside a surgical operating theater can cause fatal internal hemorrhagic shock within minutes.
        </p>
        <h4 style="color:#991B1B;margin:12px 0 8px 0;font-size:0.95rem;">🩹 Life-Saving Emergency First-Aid Protocol:</h4>
        <ul style="margin:0 0 14px 18px;padding:0;font-size:0.90rem;color:#1E293B;">
            <li><strong>Stabilize the Object:</strong> Pack bulky rolled towels, sterile dressings, or clean cloths on BOTH sides of the knife to firmly support it and prevent any movement or deeper penetration.</li>
            <li><strong>Control Bleeding Around Wound:</strong> Apply gentle, firm pressure AROUND the base of the wound with clean cloths (NEVER press down onto the knife itself).</li>
            <li><strong>Position the Patient:</strong> Keep the patient lying flat on their back. If conscious, slightly bending the knees helps relax abdominal wall tension. Cover with a warm blanket to prevent hypothermia and shock.</li>
            <li><strong>Nil by Mouth:</strong> Strictly DO NOT give any water, liquids, or food. Emergency surgical exploratory laparotomy under general anesthesia is required immediately.</li>
            <li><strong>Emergency Destination:</strong> Transport immediately via 108 Ambulance to the nearest Sub-District Hospital (SDH) or District Hospital (DH) equipped with a 24/7 Surgical Operation Theatre and Blood Bank.</li>
        </ul>
    </div>
</div>"""

    if is_snake:
        title = "सर्पदंश / विंचू चावल्याची आणीबाणी" if lang == "mr" else "सांप / बिच्छू के काटने की आपातकालीन स्थिति" if lang == "hi" else "CRITICAL EMERGENCY: SNAKEBITE / SCORPION ENVENOMATION"
        warning = "तातडीने अँटी-स्नेक व्हेनम (ASV) साठी शासकीय रुग्णालयात जा!" if lang == "mr" else "तुरंत एंटी-स्नेक वेनम (ASV) के लिए सरकारी अस्पताल पहुंचें!" if lang == "hi" else "Rush immediately to nearest Government Hospital for Anti-Snake Venom (ASV)!"
        return f"""
<div class="th-dx-card" style="border: 2px solid #DC2626; margin-bottom: 14px;">
    <div class="th-dx-header" style="background: linear-gradient(135deg, #7F1D1D 0%, #DC2626 100%);">
        <div style="display:flex;align-items:center;gap:10px;"><span style="font-size:24px;">🐍</span><div><strong style="color:#FFF;">{title}</strong></div></div>
    </div>
    <div class="th-dx-body" style="padding:18px 22px;">
        <div style="background:#FEF2F2;border-left:4px solid #DC2626;padding:10px 14px;margin-bottom:12px;color:#991B1B;font-weight:700;">⚠️ {warning}</div>
        <ul style="font-size:0.90rem;color:#334155;line-height:1.6;">
            <li>Keep the bitten limb still and positioned BELOW heart level.</li>
            <li>DO NOT cut, squeeze, suck venom, or tie tight tourniquets (causes tissue gangrene).</li>
            <li>Remove rings, watches, or tight clothing near the bite area before swelling begins.</li>
            <li>Anti-Snake Venom (ASV) is provided 100% FREE at all Maharashtra PHCs, CHCs, and District Hospitals.</li>
            <li>Call 108 immediately for an emergency ambulance.</li>
        </ul>
    </div>
</div>"""

    if is_poison:
        title = "विषबाधा / कीटकनाशक प्राशन आणीबाणी" if lang == "mr" else "विष / कीटनाशक की गंभीर आपातकालीन स्थिति" if lang == "hi" else "CRITICAL EMERGENCY: ACUTE POISONING / PESTICIDE INGESTION"
        return f"""
<div class="th-dx-card" style="border: 2px solid #DC2626; margin-bottom: 14px;">
    <div class="th-dx-header" style="background: linear-gradient(135deg, #7F1D1D 0%, #DC2626 100%);">
        <div style="display:flex;align-items:center;gap:10px;"><span style="font-size:24px;">☠️</span><div><strong style="color:#FFF;">{title}</strong></div></div>
    </div>
    <div class="th-dx-body" style="padding:18px 22px;">
        <div style="background:#FEF2F2;border-left:4px solid #DC2626;padding:10px 14px;margin-bottom:12px;color:#991B1B;font-weight:700;">⚠️ DO NOT induce vomiting unless explicitly directed by a physician!</div>
        <ul style="font-size:0.90rem;color:#334155;line-height:1.6;">
            <li>Keep the chemical bottle, pesticide packet, or medicine strip safely to show doctors.</li>
            <li>Keep the patient in the recovery position (on their side) so vomit cannot choke their airways.</li>
            <li>Call 108 Ambulance immediately for gastric lavage and ICU support at District Hospital.</li>
            <li>Call 104 National Health Helpline for immediate poison control advice.</li>
        </ul>
    </div>
</div>"""

    # General Emergency Card
    return ""


def format_general_clinical_triage_card(query="", entities=None, lang="en"):
    """Clinical triage evaluation for symptoms not matching specific known diseases in local dataset."""
    entities = entities or {}
    q_safe = html.escape(query[:120])
    
    if lang == "mr":
        return f"""
<div class="th-dx-card" style="border: 2px solid #00D2B4; box-shadow: 0 8px 26px rgba(0, 210, 180, 0.12); margin-bottom: 16px;">
    <div class="th-dx-header" style="background: linear-gradient(135deg, #0B2528 0%, #00A892 100%);">
        <div style="display:flex;align-items:center;gap:10px;">
            <span style="font-size:24px;">🩺</span>
            <div>
                <strong style="font-size:1.02rem;color:#FFFFFF;display:block;">महाआरोग्य प्राथमिक वैद्यकीय सल्ला</strong>
                <span style="font-size:0.72rem;color:#E0F8F4;font-weight:700;">क्लिनिकल मार्गदर्शन</span>
            </div>
        </div>
        <span style="font-size:0.72rem;background:rgba(255,255,255,0.2);color:#FFFFFF;padding:4px 10px;border-radius:999px;font-weight:700;">
            प्राथमिक मूल्यांकन
        </span>
    </div>
    <div class="th-dx-body" style="padding:20px 24px;color:#0B2528;line-height:1.65;">
        <p style="font-size:0.92rem;color:#334155;margin-bottom:12px;">
            तुम्ही नोंदवलेली लक्षणे: <em>"{q_safe}"</em>. प्राथमिक मूल्यांकनानुसार योग्य काळजी खालीलप्रमाणे आहे:
        </p>
        <h4 style="color:#00A892;margin:10px 0 6px 0;">🛡️ तात्काळ घरगुती काळजी व आराम:</h4>
        <ul style="font-size:0.88rem;color:#334155;margin:0 0 12px 18px;">
            <li>भरपूर पाणी किंवा ओआरएस (ORS) पाणी प्या आणि पूर्ण विश्रांती घ्या.</li>
            <li>हलका, पचायला सोपा आणि ताजा आहार घ्या.</li>
            <li>डॉक्टरांच्या प्रत्यक्ष सल्ल्याशिवाय तीव्र प्रतिजैविके (Antibiotics) स्वतःहून घेऊ नका.</li>
        </ul>
        <h4 style="color:#DC2626;margin:10px 0 6px 0;">⚠️ धोक्याची लक्षणे (तात्काळ रुग्णालयात जा):</h4>
        <p style="font-size:0.86rem;color:#991B1B;margin:0 0 12px 0;">
            अति तीव्र पोटदुखी, सतत उलट्या, रक्ताची उलटी, श्वास घेण्यास त्रास किंवा ३ दिवसांपेक्षा जास्त ताप असल्यास तात्काळ जवळच्या शासकीय रुग्णालयात जा.
        </p>
        <div style="background:#F0FDF4;border:1px solid #86EFAC;border-radius:8px;padding:10px 14px;font-size:0.84rem;color:#16794C;">
            🏥 <strong>शासकीय सुविधा:</strong> जवळच्या प्राथमिक आरोग्य केंद्रात (PHC) किंवा ग्रामीण रुग्णालयात मोफत तपासणी उपलब्ध आहे. मोफत सल्ला: १०४ | रुग्णवाहिका: १०८.
        </div>
    </div>
</div>"""

    if lang == "hi":
        return f"""
<div class="th-dx-card" style="border: 2px solid #00D2B4; box-shadow: 0 8px 26px rgba(0, 210, 180, 0.12); margin-bottom: 16px;">
    <div class="th-dx-header" style="background: linear-gradient(135deg, #0B2528 0%, #00A892 100%);">
        <div style="display:flex;align-items:center;gap:10px;">
            <span style="font-size:24px;">🩺</span>
            <div>
                <strong style="font-size:1.02rem;color:#FFFFFF;display:block;">महाआरोग्य प्राथमिक चिकित्सीय परामर्श</strong>
                <span style="font-size:0.72rem;color:#E0F8F4;font-weight:700;">क्लिनिकल मार्गदर्शन</span>
            </div>
        </div>
        <span style="font-size:0.72rem;background:rgba(255,255,255,0.2);color:#FFFFFF;padding:4px 10px;border-radius:999px;font-weight:700;">
            प्राथमिक मूल्यांकन
        </span>
    </div>
    <div class="th-dx-body" style="padding:20px 24px;color:#0B2528;line-height:1.65;">
        <p style="font-size:0.92rem;color:#334155;margin-bottom:12px;">
            आपके द्वारा बताए गए लक्षण: <em>"{q_safe}"</em>. प्राथमिक क्लिनिकल मूल्यांकन के आधार पर आवश्यक सुझाव:
        </p>
        <h4 style="color:#00A892;margin:10px 0 6px 0;">🛡️ तात्कालिक देखभाल एवं आराम:</h4>
        <ul style="font-size:0.88rem;color:#334155;margin:0 0 12px 18px;">
            <li>पर्याप्त मात्रा में पानी, ओआरएस (ORS) या तरल पदार्थ लें और पर्याप्त आराम करें।</li>
            <li>हल्का, ताजा और सुपाच्य भोजन लें।</li>
            <li>बिना डॉक्टर की सलाह के खुद से कोई एंटीबायोटिक या दर्द निवारक दवा न लें।</li>
        </ul>
        <h4 style="color:#DC2626;margin:10px 0 6px 0;">⚠️ खतरे के संकेत (तुरंत अस्पताल जाएं):</h4>
        <p style="font-size:0.86rem;color:#991B1B;margin:0 0 12px 0;">
            तेज असहनीय दर्द, लगातार उल्टी, खून आना, सांस लेने में कठिनाई या 3 दिन से अधिक तेज बुखार होने पर तुरंत सरकारी अस्पताल जाएं।
        </p>
        <div style="background:#F0FDF4;border:1px solid #86EFAC;border-radius:8px;padding:10px 14px;font-size:0.84rem;color:#16794C;">
            🏥 <strong>शासकीय सुविधा:</strong> अपने नजदीकी प्राथमिक स्वास्थ्य केंद्र (PHC) में मुफ्त जांच और दवाएं उपलब्ध हैं। स्वास्थ्य हेल्पलाइन: 104 | एम्बुलेंस: 108.
        </div>
    </div>
</div>"""

    return f"""
<div class="th-dx-card" style="border: 2px solid #00D2B4; box-shadow: 0 8px 26px rgba(0, 210, 180, 0.12); margin-bottom: 16px;">
    <div class="th-dx-header" style="background: linear-gradient(135deg, #0B2528 0%, #00A892 100%);">
        <div style="display:flex;align-items:center;gap:10px;">
            <span style="font-size:24px;">🩺</span>
            <div>
                <strong style="font-size:1.02rem;color:#FFFFFF;display:block;">MahaArogya Clinical Symptom Triage</strong>
                <span style="font-size:0.72rem;color:#E0F8F4;font-weight:700;">INITIAL EVALUATION</span>
            </div>
        </div>
        <span style="font-size:0.72rem;background:rgba(255,255,255,0.2);color:#FFFFFF;padding:4px 10px;border-radius:999px;font-weight:700;">
            CLINICAL GUIDANCE
        </span>
    </div>
    <div class="th-dx-body" style="padding:20px 24px;color:#0B2528;line-height:1.65;">
        <p style="font-size:0.92rem;color:#334155;margin-bottom:12px;">
            Evaluation for stated symptoms: <em>"{q_safe}"</em>.
        </p>
        <h4 style="color:#00A892;margin:10px 0 6px 0;">🛡️ Supportive Care & Comfort Measures:</h4>
        <ul style="font-size:0.88rem;color:#334155;margin:0 0 12px 18px;">
            <li>Maintain hydration with clean water, ORS fluids, or light broths. Rest adequately.</li>
            <li>Eat light, easily digestible meals. Avoid oily, spicy, or unhygienic foods.</li>
            <li>Avoid taking unprescribed schedule-H antibiotics without a doctor's examination.</li>
        </ul>
        <h4 style="color:#DC2626;margin:10px 0 6px 0;">⚠️ Danger Signs (Seek Immediate Medical Care):</h4>
        <p style="font-size:0.86rem;color:#991B1B;margin:0 0 12px 0;">
            Severe worsening pain, persistent vomiting, blood in vomit/stool, breathing difficulty, dizziness, or fever persisting beyond 3 days.
        </p>
        <div style="background:#F0FDF4;border:1px solid #86EFAC;border-radius:8px;padding:10px 14px;font-size:0.84rem;color:#16794C;">
            🏥 <strong>Public Healthcare:</strong> Visit your nearest Primary Health Centre (PHC) or Community Health Centre (CHC) for free clinical examination. Free Medical Advice: 104 | Ambulance: 108.
        </div>
    </div>
</div>"""


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


def generate_telemedicine_guide(lang="en"):
    if lang == "mr":
        return """<div class="th-dx-card"><div class="th-dx-header"><div class="th-dx-header-left"><div class="th-dx-header-icon">📞</div><div><h4 class="th-dx-title">मोफत टेलिमेडिसिन मार्गदर्शक (ई-संजीवनी)</h4><span style="font-size:0.75rem;color:#64748B;font-weight:600;">घरी बसून डॉक्टरांचा सल्ला — esanjeevani.mohfw.gov.in किंवा 104 कॉल</span></div></div><span class="th-dx-badge">ONLINE</span></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#EAF2FE;color:#0B6BCB;">1️⃣</div><div style="flex:1;"><strong class="th-dx-label" style="color:#0B6BCB;">ई-संजीवनी OPD</strong><div class="th-dx-content">• 'eSanjeevaniOPD' अ‍ॅप डाऊनलोड करा किंवा <a href="https://esanjeevani.mohfw.gov.in/#/" target="_blank" style="color:#0B6BCB;font-weight:700;">esanjeevani.mohfw.gov.in</a> ला भेट द्या
• मोबाईल OTP द्वारे नोंदणी करा
• टोकन घ्या → व्हिडिओ कॉलद्वारे शासकीय डॉक्टरांशी मोफत बोला</div></div></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#E6F7F5;color:#0E9F8F;">2️⃣</div><div style="flex:1;"><strong class="th-dx-label" style="color:#0E9F8F;">१०४ आरोग्य सल्ला हेल्पलाईन</strong><div class="th-dx-content">• थेट <strong>104</strong> डायल करा
• २४ तास मराठीत वैद्यकीय सल्ला
• आवश्यक असल्यास जवळच्या PHC ला रेफरल</div></div></div></div>"""
    if lang == "hi":
        return """<div class="th-dx-card"><div class="th-dx-header"><div class="th-dx-header-left"><div class="th-dx-header-icon">📞</div><div><h4 class="th-dx-title">मुफ्त टेलीमेडिसिन गाइड (eSanjeevani)</h4></div></div><span class="th-dx-badge">ONLINE</span></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#EAF2FE;color:#0B6BCB;">1️⃣</div><div style="flex:1;"><strong class="th-dx-label" style="color:#0B6BCB;">eSanjeevani OPD</strong><div class="th-dx-content">• <a href="https://esanjeevani.mohfw.gov.in/#/" target="_blank" style="color:#0B6BCB;font-weight:700;">esanjeevani.mohfw.gov.in</a> पर जाएं या ऐप डाउनलोड करें
• मोबाइल OTP से पंजीकरण करें
• मुफ्त वीडियो कॉल पर डॉक्टर से बात करें</div></div></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#E6F7F5;color:#0E9F8F;">2️⃣</div><div style="flex:1;"><strong class="th-dx-label" style="color:#0E9F8F;">104 स्वास्थ्य हेल्पलाइन</strong><div class="th-dx-content">• 24×7 हिंदी में मुफ्त सलाह
• जरूरत पर PHC को रेफरल</div></div></div></div>"""
    return """<div class="th-dx-card"><div class="th-dx-header"><div class="th-dx-header-left"><div class="th-dx-header-icon">📞</div><div><h4 class="th-dx-title">Government Telemedicine (eSanjeevani)</h4><span style="font-size:0.75rem;color:#64748B;font-weight:600;">Free doctor consultation — visit esanjeevani.mohfw.gov.in or call 104</span></div></div><span class="th-dx-badge">ONLINE</span></div><div class="th-dx-row"><div class="th-dx-icon-badge" style="background:#EAF2FE;color:#0B6BCB;">1️⃣</div><div style="flex:1;"><strong class="th-dx-label" style="color:#0B6BCB;">eSanjeevani OPD</strong><div class="th-dx-content">• Visit <a href="https://esanjeevani.mohfw.gov.in/#/" target="_blank" style="color:#0B6BCB;font-weight:700;">esanjeevani.mohfw.gov.in</a> or install eSanjeevaniOPD app
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

    if not matched:
        title = "स्वास्थ्य सुविधा खोज" if lang == "hi" else ("आरोग्य सुविधा शोध" if lang == "mr" else "Healthcare Locator")
        msg = (
            "आपल्या जवळचे रुग्णालय शोधण्यासाठी कृपया आपले शहर, परिसर किंवा जिल्हा नमूद करा (उदा. 'पुणे', 'मुंबई', किंवा 'नोएडा परी चौक'). तात्काळ आपत्कालीन मदतीसाठी १०८ क्रमांकावर संपर्क साधा."
            if lang == "mr"
            else (
                "निकटतम अस्पताल खोजने के लिए कृपया अपना शहर, इलाका या जिला बताएं (उदा. 'पुणे', 'मुंबई', या 'नोएडा परी चौक')। आपातकालीन स्थिति में तुरंत 108 या 112 डायल करें।"
                if lang == "hi"
                else "To locate hospitals near you, please specify your city, landmark, or district (e.g., 'Pune', 'Mumbai', or 'Pari Chowk Noida'). In an emergency, dial 108 or 112."
            )
        )
        return f"""<div class="th-dx-card"><div class="th-dx-header"><div class="th-dx-header-left"><div class="th-dx-header-icon">🏥</div><div><h4 class="th-dx-title">{title}</h4><span style="font-size:0.75rem;color:#64748B;font-weight:600;">Location Guidance</span></div></div><span class="th-dx-badge">HELPDESK</span></div><div style="padding:18px 20px;color:#0B2528;font-size:0.92rem;"><p style="margin:0 0 10px;">📍 {msg}</p><div style="padding:10px 14px;background:#F0FAF8;border-left:4px solid #00D2B4;border-radius:8px;font-size:0.82rem;color:#234745;">🚑 <strong>Emergency Response:</strong> Dial <strong>108</strong> (Ambulance) or <strong>112</strong> (Unified Emergency).</div></div></div>"""

    facs = MAHARASHTRA_DISTRICTS[matched]
    cards = "".join(f"""<div style="background:#FFFFFF;border:1px solid #E2E8F0;border-radius:12px;padding:12px 16px;margin-bottom:8px;"><div style="display:flex;justify-content:space-between;align-items:center;"><strong style="color:#0B6BCB;font-size:0.92rem;">🏢 {f['name']}</strong><span style="font-size:0.7rem;background:#EAF2FE;color:#0B6BCB;padding:2px 8px;border-radius:999px;font-weight:700;">{f['type']}</span></div><p style="font-size:0.84rem;margin:6px 0 2px;color:#475569;">📍 {f['location']} | Beds: <strong>{f['beds']}</strong></p><p style="font-size:0.84rem;margin:0;color:#475569;">🔧 <em>{f['facilities']}</em></p><p style="font-size:0.78rem;margin:4px 0 0;color:#94A3B8;">ℹ️ Reference data — verify before visiting</p><p style="font-size:0.84rem;margin:4px 0 0;color:#0E9F8F;">📞 <a href="tel:{f['phone']}" style="color:inherit;text-decoration:none;"><strong>{f['phone']}</strong></a></p></div>""" for f in facs)
    title = f"{matched} शासकीय आरोग्य सुविधा" if lang == "mr" else f"{matched} स्वास्थ्य सुविधाएं" if lang == "hi" else f"Government Healthcare Directory - {matched}"
    return f"""<div class="th-dx-card"><div class="th-dx-header"><div class="th-dx-header-left"><div class="th-dx-header-icon">🏥</div><div><h4 class="th-dx-title">{title}</h4><span style="font-size:0.75rem;color:#64748B;font-weight:600;">Reference data — verify details before visiting</span></div></div><span class="th-dx-badge">DIRECTORY</span></div><div style="padding:15px 20px;">{cards}</div></div>"""



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


def render_medicine_showcase_grid(lang="en"):
    """Showcases essential Jan Aushadhi generic medicines styled like the product bottles in the reference design."""
    import textwrap
    cards_html = ""
    for med, d in GENERIC_MEDS.items():
        use_text = d.get("use", "")
        saving_text = d.get("saving", "")
        branded_price = d.get("branded", "")
        generic_price = d.get("generic", "")
        cards_html += f"""
<div class="th-med-card">
    <div class="th-med-icon">💊</div>
    <div class="th-med-name">{html.escape(med)}</div>
    <div class="th-med-use">{html.escape(use_text)}</div>
    <div style="font-size:0.75rem;color:#7B9597;text-decoration:line-through;margin-bottom:2px;">Branded: {branded_price}</div>
    <div style="font-size:0.90rem;font-weight:800;color:#0B2528;margin-bottom:8px;">Jan Aushadhi: <span style="color:#00A892;">{generic_price}</span></div>
    <span class="th-med-saving">Save {saving_text}</span>
</div>
"""

    title = "सिद्ध वैद्यकीय दिलासा — विज्ञानावर आधारित" if lang == "mr" else ("सिद्ध चिकित्सीय राहत — विज्ञान आधारित" if lang == "hi" else "Proven Medical Relief, Backed By Science")
    subtitle = "Pradhan Mantri Bhartiya Janaushadhi Pariyojana (PMBJP) — Up to 85% Savings on Essential Drugs"

    full_html = f"""
<div class="th-med-showcase">
    <div style="text-align:center;margin-bottom:12px;">
        <span class="th-hero-badge" style="margin-bottom:8px;">💊 JAN AUSHADHI GENERIC ESSENTIALS</span>
        <h2 style="font-size:1.6rem;font-weight:800;color:var(--deep-slate);margin:6px 0 4px 0;">{title}</h2>
        <p style="font-size:0.88rem;color:var(--text-muted);margin:0;">{subtitle}</p>
    </div>
    <div class="th-med-grid">
        {cards_html}
    </div>
    <div style="text-align:center;margin-top:20px;">
        <a href="https://janaushadhi.gov.in" target="_blank" class="th-btn-teal" style="font-size:0.84rem;padding:10px 22px;">
            📍 Find Nearest Jan Aushadhi Kendra
        </a>
    </div>
</div>
"""
    return "\n".join(line.strip() for line in full_html.splitlines())


def render_clinical_search_loader(lang="en") -> str:
    """Renders a modern, animated clinical loading card with ECG heartbeat wave,
    concentric radar scanner, dynamic step checklist, and localized health status.
    """
    if lang == "mr":
        status_text = "AI क्लिनिकल ट्रायज इंजिन कार्यरत"
        badge_text = "⚡ Gemini Flash 3.5 · SIH कोर"
        heading_text = "आरोग्य लक्षणांचे विश्लेषण आणि वैद्यकीय सल्ला तपासणी सुरू आहे..."
        subtext = "गंभीरता पातळी, सुरक्षित प्रथमोपचार आणि महाराष्ट्रातील जवळच्या शासकीय रुग्णालयांची पडताळणी होत आहे."
        step1 = "१. लक्षणे व तीव्रता पडताळणी"
        step2 = "२. PHC / MJPJAY योजना तपासणी"
        step3 = "३. वैद्यकीय उपाय व औषध मार्गदर्शन"
    elif lang == "hi":
        status_text = "AI क्लिनिकल ट्रायज इंजन सक्रिय"
        badge_text = "⚡ Gemini Flash 3.5 · SIH कोर"
        heading_text = "स्वास्थ्य लक्षणों का विश्लेषण एवं चिकित्सा परामर्श जारी है..."
        subtext = "गंभीरता स्तर, सुरक्षित प्राथमिक उपचार और महाराष्ट्र के नजदीकी सरकारी अस्पतालों की जांच हो रही है।"
        step1 = "१. लक्षण एवं तात्कालिकता जांच"
        step2 = "२. PHC / MJPJAY प्रोटोकॉल मिलान"
        step3 = "३. चिकित्सकीय राहत एवं दवाएं"
    else:
        status_text = "AI CLINICAL TRIAGE ENGINE ACTIVE"
        badge_text = "⚡ Gemini Flash 3.5 · SIH Core"
        heading_text = "Analyzing Symptoms & Consulting Clinical Protocol..."
        subtext = "Evaluating urgency, safe home interventions, and nearest Maharashtra healthcare facilities."
        step1 = "1. Symptom & Triage Parsing"
        step2 = "2. PHC/MJPJAY Protocol Match"
        step3 = "3. Evidence-Based Synthesis"

    html_card = f"""
<div class="th-clinical-loader">
    <div class="th-loader-top-bar">
        <div class="th-loader-status-pill">
            <span class="th-pulse-dot"></span>
            <span>{status_text}</span>
        </div>
        <div class="th-loader-tech-badge">
            {badge_text}
        </div>
    </div>

    <div class="th-loader-main-body">
        <div class="th-loader-radar-wrapper">
            <div class="th-loader-ring-outer"></div>
            <div class="th-loader-ring-inner"></div>
            <div class="th-loader-icon-center">🩺</div>
        </div>
        <div class="th-loader-text-block">
            <div class="th-loader-heading">{heading_text}</div>
            <div class="th-loader-subtext">{subtext}</div>
        </div>
    </div>

    <!-- Animated ECG Heartbeat Wave -->
    <div class="th-loader-ecg-container">
        <svg class="th-loader-ecg-svg" viewBox="0 0 600 50" preserveAspectRatio="none">
            <path class="th-loader-ecg-bg" d="M0,25 L120,25 L135,25 L145,5 L155,45 L165,15 L175,32 L185,25 L320,25 L335,25 L345,5 L355,45 L365,15 L375,32 L385,25 L500,25 L515,25 L525,5 L535,45 L545,15 L555,32 L565,25 L600,25" />
            <path class="th-loader-ecg-pulse" d="M0,25 L120,25 L135,25 L145,5 L155,45 L165,15 L175,32 L185,25 L320,25 L335,25 L345,5 L355,45 L365,15 L375,32 L385,25 L500,25 L515,25 L525,5 L535,45 L545,15 L555,32 L565,25 L600,25" />
        </svg>
    </div>

    <!-- 3-Step Pipeline Tracker -->
    <div class="th-loader-steps-grid">
        <div class="th-loader-step th-step-active">
            <span class="th-step-icon">🔍</span>
            <span class="th-step-label">{step1}</span>
        </div>
        <div class="th-loader-step th-step-pulse">
            <span class="th-step-icon">🏥</span>
            <span class="th-step-label">{step2}</span>
        </div>
        <div class="th-loader-step th-step-wait">
            <span class="th-step-icon">💊</span>
            <span class="th-step-label">{step3}</span>
        </div>
    </div>

    <!-- Shimmer Progress Line -->
    <div class="th-loader-shimmer-progress">
        <div class="th-loader-shimmer-bar"></div>
    </div>
</div>
"""
    return "\n".join(line.strip() for line in html_card.splitlines())

