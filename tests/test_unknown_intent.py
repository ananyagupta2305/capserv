# tests/test_unknown_intent_multi.py
import pytest
from fastapi.testclient import TestClient
from bot.app import app

client = TestClient(app)

def test_unknown_intent():
    """
    Test that the bot returns UNKNOWN intent for ambiguous transcripts
    """
    payload = {"transcript": "Can you help me with something?"}
    resp = client.post("/bot/handle", json=payload)
    assert resp.status_code == 200
    data = resp.json()
    assert data["intent"] == "UNKNOWN"
    assert "Could not determine intent" in data["result"]["message"]

def test_multiple_intents_in_same_transcript():
    """
    Test a transcript containing both lead creation and visit scheduling
    """
    # Step 1: Add a new lead dynamically
    payload = {"transcript": "Add a new lead Test User from Pune phone 9876543210 source Referral"}
    create_resp = client.post("/bot/handle", json=payload)
    lead_id = create_resp.json()["result"]["lead_id"]

    # Step 2: Single transcript containing both intents
    multi_transcript = f"Update lead {lead_id} to IN_PROGRESS and schedule a visit at 2025-10-05T17:00:00+05:30"
    resp = client.post("/bot/handle", json={"transcript": multi_transcript})
    assert resp.status_code == 200
    data = resp.json()
    
    # The bot should pick the primary intent (e.g., LEAD_UPDATE) and extract relevant entities
    assert data["intent"] in ["LEAD_UPDATE", "VISIT_SCHEDULE"]
    assert "lead_id" in data["entities"]
    # Optional: Check CRM call info is included
    assert "crm_call" in data
