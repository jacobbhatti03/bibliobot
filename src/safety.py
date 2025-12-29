# src/safety.py

SCRIPTURE_KEYWORDS = [
    "bible", "jesus", "christ", "god", "scripture",
    "verse", "psalm", "paul", "gospel", "sin",
    "faith", "church", "pray", "prayer", "holy",
    "moses", "abraham", "john", "romans", "corinthians"
]


def is_scripture_related(text):
    if not text:
        return False

    t = text.lower().strip()
    return any(k in t for k in SCRIPTURE_KEYWORDS)


def gentle_redirect(text):
    """
    Used when a question is not scripture-related.
    Polite, non-offensive, apologetic tone.
    """
    return (
        "I’m here to help with Bible, Scripture, and Christian apologetics questions 📖✨\n\n"
        "If you’d like, you can ask about a verse, a teaching of Jesus, theology, "
        "or how Scripture speaks to life’s questions."
    )


def is_allowed(text):
    """
    Optional: simple safety gate (expand later)
    """
    return True


def refusal_message():
    return (
        "I’m not able to help with that request, but I’m always happy to discuss "
        "Scripture, theology, or questions of faith 📖"
    )


