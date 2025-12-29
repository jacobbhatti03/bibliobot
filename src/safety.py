def is_scripture_related(text):
    if not text:
        return False

    t = text.lower().strip()
    keywords = [
        "bible", "jesus", "christ", "god", "scripture",
        "verse", "psalm", "paul", "gospel", "sin",
        "faith", "church", "pray", "prayer", "holy"
    ]
    return any(k in t for k in keywords)


