# bot/nlu.py
import re
import json
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
try:
    import dateparser
except ImportError:
    dateparser = None

logger = logging.getLogger("bot_nlu")

UUID_RE = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")

PHONE_RE = re.compile(r"(?:\+91|0)?[\s-]*([6-9]\d[\d\s-]{8,})")

VALID_STATUSES = {"NEW", "IN_PROGRESS", "FOLLOW_UP", "WON", "LOST"}

ANALYTICS_FILE = "bot_analytics.jsonl"

def normalize_phone(raw: str) -> Optional[str]:
    if not raw:
        return None
    digits = re.sub(r"\D", "", raw)
    if len(digits) >= 10:
        return digits[-10:]
    return None

def parse_datetime(text: str) -> Optional[str]:
    if dateparser:
        dt = dateparser.parse(text, settings={"RETURN_AS_TIMEZONE_AWARE": True, "PREFER_DATES_FROM": "future"})
        if dt:
            return dt.isoformat()
    iso = re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(?:[+-]\d{2}:\d{2})?", text)
    if iso:
        return iso.group(0)
    return None

def extract_entities(transcript: str) -> Dict[str, Any]:
    t = transcript.strip()
    entities = {
        "name": None, "phone": None, "city": None, "source": None,
        "lead_id": None, "visit_time": None, "notes": None, "status": None
    }

    phone_match = PHONE_RE.search(t)
    if phone_match:
        entities["phone"] = normalize_phone(phone_match.group(0))

    uid = UUID_RE.search(t)
    if uid:
        entities["lead_id"] = uid.group(0)

    m = re.search(r"source\s+([A-Za-z0-9\s]+)", t, re.IGNORECASE)
    if m: entities["source"] = m.group(1).strip().strip(".,")

    m = re.search(r"(?:from|in)\s+([A-Za-z\s]+?)(?:,| phone| contact|$|\.)", t, re.IGNORECASE)
    if m: entities["city"] = m.group(1).strip()

    m = re.search(r"(?:lead[:]?|name[:]?|add a new lead[:]?|create lead[:]?)[\s\-]*([A-Za-z\s]{2,60}?)(?:from|,| phone| contact|$|\.)", t, re.IGNORECASE)
    if m:
        candidate = re.sub(r"^(a new|new)\s+", "", m.group(1).strip(), flags=re.IGNORECASE)
        entities["name"] = candidate

    if not entities["name"]:
        m = re.search(r"name\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)", t)
        if m: entities["name"] = m.group(1).strip()

    for s in VALID_STATUSES:
        if re.search(r"\b" + s.replace("_", " ") + r"\b", t, re.IGNORECASE) or re.search(r"\b" + s + r"\b", t, re.IGNORECASE):
            entities["status"] = s
            break

    vt = parse_datetime(t)
    if vt:
        entities["visit_time"] = vt

    m = re.search(r"notes?\s*[:\-]\s*(.+)$", t, re.IGNORECASE)
    if m:
        entities["notes"] = m.group(1).strip()

    return entities

def classify_intent(transcript: str) -> List[Dict[str, Any]]:
    """
    Returns a list of detected intents with optional confidence scores.
    """
    t = transcript.lower()
    intents = []

    # Simple confidence scoring heuristics
    def score(keyword_list):
        return max([1.0 if k in t else 0.0 for k in keyword_list])

    lead_keywords = ["create lead", "add a new lead", "add lead", "new lead"]
    visit_keywords = ["schedule", "site visit", "schedule a visit", "fix a site visit"]
    update_keywords = ["update lead", "mark lead", "set lead", "change lead", "mark as won"]

    if score(lead_keywords) > 0:
        intents.append({"intent": "LEAD_CREATE", "confidence": 1.0})
    if score(visit_keywords) > 0:
        intents.append({"intent": "VISIT_SCHEDULE", "confidence": 1.0})
    if score(update_keywords) > 0:
        intents.append({"intent": "LEAD_UPDATE", "confidence": 1.0})

    # fallback
    ent = extract_entities(transcript)
    if ent.get("phone") and ent.get("city") and not any(i["intent"]=="LEAD_CREATE" for i in intents):
        intents.append({"intent": "LEAD_CREATE", "confidence": 0.7})

    if not intents:
        intents.append({"intent": "UNKNOWN", "confidence": 0.0})

    return intents

def extract(transcript: str) -> Dict[str, Any]:
    entities = extract_entities(transcript)
    intents = classify_intent(transcript)
    result = {
        "intents": intents,      # list of intents (supports multi-action)
        "intent": intents[0]["intent"],  # primary intent for backward compatibility
        "entities": entities
    }

    # Analytics logging
    try:
        with open(ANALYTICS_FILE, "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "timestamp": datetime.now(timezone.utc).isoformat(),
                "transcript": transcript,
                "intents": intents,
                "entities": entities
            }) + "\n")
    except Exception as e:
        logger.warning("Failed to log analytics: %s", e)

    return result
