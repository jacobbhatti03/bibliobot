import re

BIBLE_KEYWORDS = [
    "bible", "scripture", "verse", "chapter", "psalm", "proverb", "gospel",
    "jesus", "christ", "moses", "paul", "israel", "sin", "faith", "prayer",
    "genesis", "exodus", "matthew", "mark", "luke", "john", "romans", "acts",
]

OUT_OF_SCOPE = [
    "code", "program", "hack", "cheat", "password", "crack",
    "politics", "stock", "crypto", "dating", "explicit",
]

def is_allowed(question: str) -> bool:
    q = question.lower().strip()

    # Block obvious non-bible content
    if any(word in q for word in OUT_OF_SCOPE):
        return False

    # Allow if bible-related keywords OR verse pattern (e.g., John 3:16)
    if any(word in q for word in BIBLE_KEYWORDS):
        return True

    if re.search(r"\b\d{1,3}:\d{1,3}\b", q):
        return True

    return False
