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

    if any(word in q for word in OUT_OF_SCOPE):
        return False

    if any(word in q for word in BIBLE_KEYWORDS):
        return True

    # verse pattern like 3:16
    if re.search(r"\b\d{1,3}:\d{1,3}\b", q):
        return True

    return False


def refusal_message() -> str:
    return (
        "🙏 **BiblioBot stays scripture-focused**\n\n"
        "I can only help with Bible/scripture-based questions.\n\n"
        "**Try asking:**\n"
        "- Explain John 3:16\n"
        "- What does Romans 8 teach?\n"
        "- Give Bible verses about anxiety\n"
        "- Summarize Psalm 23"
    )
