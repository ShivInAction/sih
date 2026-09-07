"""Translation and multilingual detection layer."""
import re
import time
import streamlit as st
from deep_translator import GoogleTranslator
from langdetect import detect, LangDetectException
from src.config.constants import (
    ROMANIZED_HI_MAP,
    ROMANIZED_HI_STRONG,
    _DEVANAGARI_HI_MAP,
    _DEVANAGARI_MR_MAP,
    REQUIRED_COLUMNS,
    MODE_HINDI,
    MODE_MARATHI,
    MODE_ENGLISH,
)

def is_romanized_hindi(query): return bool(set(re.findall(r"[a-z]+", normalize_for_match(query))) & ROMANIZED_HI_STRONG)
def romanize_to_english(query):
    out = []
    for w in re.findall(r"[a-z]+", normalize_for_match(query)):
        if w in ROMANIZED_HI_MAP:
            mapped = ROMANIZED_HI_MAP[w]
            if mapped: out.append(mapped)
        else: out.append(w)
    return " ".join(out)


def devanagari_to_english(query):
    if not query: return ""
    text = query
    for mr, en in _DEVANAGARI_MR_MAP: text = text.replace(mr, " " + en + " ")
    for hi, en in _DEVANAGARI_HI_MAP: text = text.replace(hi, " " + en + " ")
    return " ".join(re.findall(r"[a-z]+", text.lower()))

def normalize_for_match(text): return (text or "").lower().replace("'", "")



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
