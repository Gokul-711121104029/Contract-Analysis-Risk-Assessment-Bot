from langdetect import detect
import argostranslate.translate as translate

def normalize_text(text: str):
    # Basic cleanup
    text = text.replace("\t", " ").replace("\r", "\n")
    text = "\n".join([line.strip() for line in text.split("\n") if line.strip()])

    # Detect language
    try:
        lang = detect(text[:1000])
    except:
        lang = "unknown"

    # Hindi → English (OFFLINE)
    if lang == "hi":
        try:
            translated = translate.translate(text, "hi", "en")
            return translated.strip(), "hi->en"
        except Exception as e:
            # If translation fails, return original
            return text.strip(), "hi-failed"

    # English or others
    return text.strip(), lang
