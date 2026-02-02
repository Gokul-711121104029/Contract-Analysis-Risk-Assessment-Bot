from langdetect import detect

def normalize_text(text: str):
    # cleanup
    text = text.replace("\t", " ").replace("\r", "\n")
    text = "\n".join([line.strip() for line in text.split("\n") if line.strip()])

    # detect language
    try:
        lang = detect(text[:1000])
    except:
        lang = "unknown"

    # Hindi -> English (offline) using Argos Translate if installed
    if lang == "hi":
        try:
            import argostranslate.translate as translate
            translated = translate.translate(text, "hi", "en")
            return translated.strip(), "hi->en"
        except Exception:
            # If Argos isn't installed / model isn't installed, don't crash
            return text.strip(), "hi (translation unavailable)"

    return text.strip(), lang
