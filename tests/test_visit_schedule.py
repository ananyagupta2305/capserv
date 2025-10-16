# tests/test_visit_schedule.py
import pytest
from fastapi.testclient import TestClient
from bot.app import app

client = TestClient(app)

def test_visit_schedule_happy():
    # Step 1: Create a lead
    create_resp = client.post("/bot/handle", json={
        "transcript": "Add a new lead Visit User from Mumbai phone 9876543210 source Instagram."
    })
    lead_id = create_resp.json()["result"]["lead_id"]

    # Step 2: Schedule a visit for that lead
    visit_resp = client.post("/bot/handle", json={
        "transcript": f"Schedule a visit for lead {lead_id} at 2025-10-02T17:00:00+05:30"
    })
    assert visit_resp.status_code == 200
    data = visit_resp.json()
    assert data["intent"] == "VISIT_SCHEDULE"
    assert data["result"]["status"] == "SCHEDULED"
