# from fastapi.testclient import TestClient
# from bot.app import app
# from bot import app as bot_app

# client = TestClient(app)

# def test_lead_update_happy():
#     # Step 1: Create a new lead dynamically
#     create_resp = client.post("/bot/handle", json={
#         "transcript": "Add a new lead Test User from Delhi phone 9876543210 source Instagram."
#     })
#     assert create_resp.status_code == 200
#     lead_id = create_resp.json()["result"]["lead_id"]

#     # Step 2: Update the status of that lead
#     update_resp = client.post("/bot/handle", json={
#         "transcript": f"Update lead {lead_id} to IN_PROGRESS"
#     })
#     assert update_resp.status_code == 200
#     data = update_resp.json()
#     assert data["intent"] == "LEAD_UPDATE"
#     assert data["entities"]["lead_id"] == lead_id
#     assert data["entities"]["status"] == "IN_PROGRESS"
#     assert "result" in data

# def test_lead_update_crm_error(monkeypatch):
#     # Create a custom CRMClient that raises errors
#     class FailingCRMClient:
#         def __init__(self):
#             self.leads = {}
        
#         def create_lead(self, name, phone, city=None, source=None):
#             # This works fine for creating leads
#             lead_id = "test-lead-id"
#             return {"lead_id": lead_id, "status": "NEW"}
        
#         def update_status(self, lead_id, status, notes=None):
#             # This always fails
#             raise bot_app.CRMError(500, "Internal")
    
#     # Replace the global CRM client instance
#     monkeypatch.setattr(bot_app, "crm_client_instance", FailingCRMClient())

#     # Create lead to get a valid UUID
#     create_resp = client.post("/bot/handle", json={
#         "transcript": "Add a new lead Test User from Delhi phone 9876543210 source Instagram."
#     })
#     lead_id = create_resp.json()["result"]["lead_id"]

#     resp = client.post("/bot/handle", json={
#         "transcript": f"Update lead {lead_id} to WON notes booked unit A2"
#     })
#     assert resp.status_code == 502
#     data = resp.json()
#     assert data["error"]["type"] == "CRM_ERROR"




from fastapi.testclient import TestClient
from bot.app import app, CRMError
from bot import app as bot_app

client = TestClient(app)

def test_lead_update_happy():
    # Step 1: Create a new lead dynamically
    create_resp = client.post("/bot/handle", json={
        "transcript": "Add a new lead Test User from Delhi phone 9876543210 source Instagram."
    })
    assert create_resp.status_code == 200
    lead_id = create_resp.json()["result"]["lead_id"]

    # Step 2: Update the status of that lead
    update_resp = client.post("/bot/handle", json={
        "transcript": f"Update lead {lead_id} to IN_PROGRESS"
    })
    assert update_resp.status_code == 200
    data = update_resp.json()
    assert data["intent"] == "LEAD_UPDATE"
    assert data["entities"]["lead_id"] == lead_id
    assert data["entities"]["status"] == "IN_PROGRESS"
    assert "result" in data

def test_lead_update_crm_error(monkeypatch):
    # Monkeypatch the update_status method to always fail
    def failing_update_status(self, lead_id, status, notes=None):
        raise CRMError(500, "Internal")
    
    # Replace the update_status method
    monkeypatch.setattr(bot_app.CRMClient, "update_status", failing_update_status)

    # Test with any lead ID since the method will fail anyway
    resp = client.post("/bot/handle", json={
        "transcript": "Update lead 12345678 to WON notes booked unit A2"
    })
    assert resp.status_code == 502
    data = resp.json()
    assert data["error"]["type"] == "CRM_ERROR"
    assert "Internal" in data["error"]["details"]