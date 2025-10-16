# import pytest
# from fastapi.testclient import TestClient
# from bot.app import app  # Make sure your FastAPI app is in main.py

# client = TestClient(app)

# # --- Test LEAD_CREATE ---
# def test_lead_create():
#     payload = {"transcript": "Add a new lead: Rohan Sharma from Gurgaon, phone 9876543210"}
#     response = client.post("/bot/handle", json=payload)
#     data = response.json()
    
#     assert response.status_code == 200
#     assert data["intent"] == "LEAD_CREATE"
#     assert data["entities"]["name"] == "Rohan Sharma"
#     assert data["result"]["status"] == "NEW"

# # --- Test VISIT_SCHEDULE ---
# def test_visit_schedule():
#     payload = {"transcript": "Schedule a visit for lead 65ce1c14 at 3 pm tomorrow"}
#     response = client.post("/bot/handle", json=payload)
#     data = response.json()
    
#     assert response.status_code == 200
#     assert data["intent"] == "VISIT_SCHEDULE"
#     assert data["result"]["status"] == "SCHEDULED"
#     assert "visit_time" in data["entities"]

# # --- Test LEAD_UPDATE ---
# def test_lead_update():
#     payload = {"transcript": "Update lead 65ce1c14 to in progress"}
#     response = client.post("/bot/handle", json=payload)
#     data = response.json()
    
#     assert response.status_code == 200
#     assert data["intent"] == "LEAD_UPDATE"
#     assert data["result"]["status"] == "UPDATED"

# # --- Test UNKNOWN intent ---
# def test_unknown_intent():
#     payload = {"transcript": "Can you help me?"}
#     response = client.post("/bot/handle", json=payload)
#     data = response.json()
    
#     assert response.status_code == 200
#     assert data["intent"] == "UNKNOWN"
#     assert data["result"]["status"] == "FAILED"
#     assert data["fallback"] is not None

# # --- Test multiple transcripts ---
# def test_multiple_transcripts():
#     payload = {
#         "transcripts": [
#             "Add a new lead: Priya Nair from Mumbai, phone 91234-56789",
#             "Schedule a visit for lead 65ce1c14 at 5 pm tomorrow"
#         ]
#     }
#     response = client.post("/bot/handle", json=payload)
#     data = response.json()
    
#     assert response.status_code == 200
#     assert "responses" in data
#     assert len(data["responses"]) == 2
#     intents = [r["intent"] for r in data["responses"]]
#     assert "LEAD_CREATE" in intents
#     assert "VISIT_SCHEDULE" in intents

# # --- Test fallback for low confidence ---
# def test_low_confidence_fallback(monkeypatch):
#     # Force classify_intent to return low confidence
#     def low_confidence(*args, **kwargs):
#         return "LEAD_CREATE", 0.5
#     monkeypatch.setattr("main.classify_intent", low_confidence)
    
#     payload = {"transcript": "Add a new lead: Someone"}
#     response = client.post("/bot/handle", json=payload)
#     data = response.json()
    
#     assert data["fallback"] is not None
#     assert "Could you please rephrase" in data["fallback"]
import pytest
from fastapi.testclient import TestClient
from bot.app import app  # Make sure your FastAPI app is in main.py

client = TestClient(app)

# --- Test LEAD_CREATE ---
def test_lead_create():
    payload = {"transcript": "Add a new lead: Rohan Sharma from Gurgaon, phone 9876543210"}
    response = client.post("/bot/handle", json=payload)
    data = response.json()
    
    assert response.status_code == 200
    assert data["intent"] == "LEAD_CREATE"
    assert data["entities"]["name"] == "Rohan Sharma"
    assert data["result"]["status"] == "NEW"

# --- Test VISIT_SCHEDULE ---
def test_visit_schedule():
    payload = {"transcript": "Schedule a visit for lead 65ce1c14 at 3 pm tomorrow"}
    response = client.post("/bot/handle", json=payload)
    data = response.json()
    
    assert response.status_code == 200
    assert data["intent"] == "VISIT_SCHEDULE"
    assert data["result"]["status"] == "SCHEDULED"
    assert "visit_time" in data["entities"]

# --- Test LEAD_UPDATE ---
def test_lead_update():
    payload = {"transcript": "Update lead 65ce1c14 to in progress"}
    response = client.post("/bot/handle", json=payload)
    data = response.json()
    
    assert response.status_code == 200
    assert data["intent"] == "LEAD_UPDATE"
    assert data["result"]["status"] == "UPDATED"

# --- Test UNKNOWN intent ---
def test_unknown_intent():
    payload = {"transcript": "Can you help me?"}
    response = client.post("/bot/handle", json=payload)
    data = response.json()
    
    assert response.status_code == 200
    assert data["intent"] == "UNKNOWN"
    assert data["result"]["status"] == "FAILED"
    assert data["fallback"] is not None

# --- Test multiple transcripts ---
def test_multiple_transcripts():
    payload = {
        "transcripts": [
            "Add a new lead: Priya Nair from Mumbai, phone 91234-56789",
            "Schedule a visit for lead 65ce1c14 at 5 pm tomorrow"
        ]
    }
    response = client.post("/bot/handle", json=payload)
    data = response.json()
    
    assert response.status_code == 200
    assert "responses" in data
    assert len(data["responses"]) == 2
    intents = [r["intent"] for r in data["responses"]]
    assert "LEAD_CREATE" in intents
    assert "VISIT_SCHEDULE" in intents

# --- Test fallback for low confidence ---
def test_low_confidence_fallback(monkeypatch):
    # Force classify_intent to return low confidence
    def low_confidence(*args, **kwargs):
        return "LEAD_CREATE", 0.5
    
    # Fix the import path to match your actual module structure
    monkeypatch.setattr("bot.app.classify_intent", low_confidence)
    
    payload = {"transcript": "Add a new lead: Someone"}
    response = client.post("/bot/handle", json=payload)
    data = response.json()
    
    assert data["fallback"] is not None
    assert "Could you please rephrase" in data["fallback"]