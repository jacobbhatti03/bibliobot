import re

BIBLE_KEYWORDS = {
    "bible","scripture","verse","chapter","psalm","psalms","proverb","proverbs","gospel",
    "jesus","christ","holy spirit","moses","paul","peter","john","mark","luke","matthew",
    "genesis","exodus","romans","acts","corinthians","galatians","ephesians","philippians",
    "hebrews","james","revelation","isaiah","jeremiah","daniel","apologetics","trinity",
    "resurrection","salvation","atonement","grace","faith"
}

VERSE_PATTERNS = [
    r"\b\d{1,3}:\d{1,3}(-\d{1,3})?\b",          # 3:16, 1:1-3
    r"\bpsalm\s*\d+\b",                         # Psalm 23
    r"\b(1|2|3)\s*(john|peter|timothy|cor)\b",  # 1 John, 2 Peter, 1 Cor
]

HARD_BLOCK = {"hack","crack","pirate","porn","explicit"}  # keep short

def is_scripture_related(text: str) -> bool:
    t = text.lower().strip()
    if any(w in t for w in HARD_BLOCK):
        return False
    if any(k in t for k in BIBLE_KEYWORDS):
        return True
    return any(re.search(p, t) for p in VERSE_PATTERNS)

def gentle_redirect(user_question: str) -> str:
    # Not “you’re wrong” — just a friendly boundary + offer alternatives
    return (
        "I can help best with **Bible, scripture, and apologetics** questions.\n\n"
        "If you want, I can:\n"
        "• connect your question to a **biblical perspective**\n"
        "• share **relevant verses** and a short explanation\n"
        "• help you form an **apologetics-style answer**\n\n"
        "Try asking like:\n"
        f"• “What does the Bible say about {user_question[:60]}?”\n"
        "• “Give verses + explanation about this topic.”"
    )

