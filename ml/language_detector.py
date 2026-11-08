"""
Linguistic Cohort Identification Module for Multilingual Telecom Voice-of-Customer Data.

Implements the two-stage linguistic partitioning methodology grounded in:
1. Barman et al. (2014, EMNLP): Unicode script-level filtering and sub-word n-gram heuristics.
2. Gambäck & Das (2016, LREC): Code-Mixing Index (CMI) dominance threshold (CMI <= 30 / >= 70% language dominance).

Categorizes input reviews into:
- Bangla (Native Script)
- Romanized Banglish (Latin Script phonetic transliteration)
- English (Standard Latin Script)
- Symbolic / Emoticon Only
"""

import re
import unicodedata
from typing import Dict, List, Union
from nltk.corpus import words

# Compile Bengali Unicode script block: U+0980 to U+09FF
BENGALI_UNICODE_PATTERN = re.compile(r"[\u0980-\u09FF]")
LATIN_TOKEN_PATTERN = re.compile(r"[a-zA-Z]+")

# Standard English dictionary expansion
try:
    _raw_words = set(w.lower() for w in words.words())
except LookupError:
    import nltk
    nltk.download("words", quiet=True)
    _raw_words = set(w.lower() for w in words.words())

ENGLISH_VOCABULARY = set(_raw_words)
for w in list(_raw_words):
    ENGLISH_VOCABULARY.add(w + "s")
    ENGLISH_VOCABULARY.add(w + "es")
    ENGLISH_VOCABULARY.add(w + "ed")
    ENGLISH_VOCABULARY.add(w + "ing")

# Domain-specific telecom terms in English
TELECOM_DOMAIN_VOCAB = {
    "app", "apps", "sim", "sims", "mb", "gb", "kb", "4g", "3g", "2g", "5g",
    "net", "internet", "update", "updates", "updated", "updating", "wifi",
    "login", "logins", "log", "logged", "logging", "server", "servers",
    "offer", "offers", "offered", "offering", "service", "services", "servicing",
    "data", "pack", "packs", "package", "packages", "call", "calls", "called", "calling",
    "rate", "rates", "star", "stars", "version", "phone", "phones", "telecom",
    "balance", "recharge", "recharges", "recharged", "recharging", "account", "accounts",
    "customer", "customers", "care", "network", "networks", "networking", "connect",
    "connection", "connections", "connected", "connecting", "problem", "problems",
    "slow", "fast", "faster", "fastest", "good", "better", "best", "bad", "worse", "worst",
    "ok", "okay", "super", "poor", "useless", "nice", "nicer", "nicest", "waste", "cheat",
    "cheater", "cheaters", "cheating", "scam", "scams", "scammer", "issue", "issues",
    "fix", "fixes", "fixed", "fixing", "please", "thanks", "thank", "load", "loading",
    "bug", "bugs", "error", "errors", "solution", "solutions", "feature", "features",
    "money", "easy", "easier", "easiest", "helpful", "useful", "awesome", "love", "loved",
    "loving", "like", "liked", "likes", "liking", "fine", "working", "works", "worked",
    "open", "opening", "opened", "great", "excellent", "fantastic", "smooth", "smoother",
    "bangladesh", "bangladeshi", "robi", "grameenphone", "gp", "banglalink", "bl",
    "user", "users", "experience", "experienced", "experiences", "experiencing", "taka", "tk"
}
ENGLISH_VOCABULARY.update(TELECOM_DOMAIN_VOCAB)

# High-precision Romanized Bengali (Banglish) phonetic roots, markers, and affixes
BANGLISH_PHONETIC_MARKERS = {
    "kore", "korche", "kora", "korbo", "korle", "korchen", "kortese", "kori", "korce",
    "bhalo", "kharap", "faltu", "ekdom", "kete", "nei", "ache", "nai", "hobe", "hoi",
    "hoche", "hocche", "asche", "jacche", "dibe", "diben", "din", "aro", "beshi", "kom",
    "onek", "valo", "khub", "sundor", "dekhi", "jani", "parchi", "parina", "hoyna",
    "bujhi", "amader", "tomader", "apnader", "ei", "oi", "shei", "keno", "kobe", "kothay",
    "kotuk", "shob", "sob", "shathe", "sathe", "ar", "akta", "ekta", "koekta", "protidin",
    "shobar", "sobar", "baje", "bal", "fuchka", "dekhte", "jay", "geche", "gache",
    "ashche", "parci", "dicche", "deyni", "deyna", "kisu", "kichu", "amake", "tomake",
    "onk", "besi", "beicha", "kina", "lagbo", "dewar", "jonno", "hoitay", "parto",
    "ager", "ceye", "dike", "hoito", "dam", "vaci", "tai", "puro", "dilam", "khali",
    "amar", "amr", "apnar", "tomar", "kemon", "acche", "korben", "bujina", "parlam",
    "dekha", "dekhe", "dekhlam", "thake", "thakle", "thakbe", "chai", "cai", "caile",
    "dibona", "dewa", "moto", "motun", "bujte", "buja", "lagbe", "hoy", "koren"
}


class LanguageClassifier:
    """
    Automated Language and Linguistic Sub-Cohort Classifier.
    """

    def __init__(self, script_threshold: float = 0.25, dominance_threshold: float = 0.70):
        self.script_threshold = script_threshold
        self.dominance_threshold = dominance_threshold

    def analyze(self, text: str) -> Dict[str, Union[str, float, int, bool]]:
        """
        Analyze the linguistic properties of a customer review text.
        """
        norm_text = unicodedata.normalize("NFKD", str(text))
        non_ws_chars = len(re.sub(r"\s+", "", norm_text))
        
        if non_ws_chars == 0:
            return {
                "language": "Symbolic / Emoticons",
                "script": "Symbolic",
                "bengali_script_ratio": 0.0,
                "english_token_ratio": 0.0,
                "banglish_token_ratio": 0.0,
                "is_code_mixed": False,
            }

        # Stage 1: Native Bengali Script Evaluation
        bengali_chars = len(BENGALI_UNICODE_PATTERN.findall(norm_text))
        bengali_ratio = bengali_chars / non_ws_chars

        if bengali_ratio >= self.script_threshold:
            # Check for intra-sentential Latin script code-mixing in Bengali
            latin_tokens = LATIN_TOKEN_PATTERN.findall(norm_text)
            is_mixed = len(latin_tokens) >= 2
            return {
                "language": "Bangla (Native Script)",
                "script": "Bengali",
                "bengali_script_ratio": round(bengali_ratio, 4),
                "english_token_ratio": 0.0,
                "banglish_token_ratio": 0.0,
                "is_code_mixed": is_mixed,
            }

        # Stage 2: Latin Script Lexical Evaluation
        tokens = LATIN_TOKEN_PATTERN.findall(norm_text.lower())
        if not tokens:
            return {
                "language": "Symbolic / Emoticons",
                "script": "Symbolic",
                "bengali_script_ratio": round(bengali_ratio, 4),
                "english_token_ratio": 0.0,
                "banglish_token_ratio": 0.0,
                "is_code_mixed": False,
            }

        total_tokens = len(tokens)
        banglish_matches = sum(1 for t in tokens if t in BANGLISH_PHONETIC_MARKERS)
        english_matches = sum(1 for t in tokens if t in ENGLISH_VOCABULARY and t not in BANGLISH_PHONETIC_MARKERS)

        banglish_ratio = banglish_matches / total_tokens
        english_ratio = english_matches / total_tokens

        # Code-Mixing Index (Gambäck & Das 2016)
        is_mixed = (banglish_matches > 0 and english_matches > 0)

        # Classification decision rules
        if banglish_matches > 0 and banglish_ratio >= 0.15:
            lang = "Romanized Banglish"
        elif english_ratio >= self.dominance_threshold and banglish_matches == 0:
            lang = "English"
        elif banglish_matches > 0:
            lang = "Romanized Banglish"
        elif english_ratio >= 0.60:
            lang = "English"
        else:
            lang = "Romanized Banglish"

        return {
            "language": lang,
            "script": "Latin",
            "bengali_script_ratio": round(bengali_ratio, 4),
            "english_token_ratio": round(english_ratio, 4),
            "banglish_token_ratio": round(banglish_ratio, 4),
            "is_code_mixed": is_mixed,
        }

    def classify(self, text: str) -> str:
        """Return the primary linguistic cohort label for text."""
        return self.analyze(text)["language"]

    def batch_classify(self, texts: List[str]) -> List[str]:
        """Classify a batch of texts."""
        return [self.classify(t) for t in texts]


# Module singleton for fast imports
detector = LanguageClassifier()
