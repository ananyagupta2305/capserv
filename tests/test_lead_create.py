# tests/test_lead_create.py
from fastapi.testclient import TestClient
import pytest
from bot import app
from bot import crm_client

client = TestClient(app.app)

def test_lead_create_happy(monkeypatch):
    def fake_create_lead(name, phone, city, source=None):
        return {"lead_id": "1111-1111", "status": "NEW"}
    monkeypatch.setattr(crm_client.CRMClient, "create_lead", staticmethod(lambda *args, **kw: fake_create_lead(*args, **kw)))
    payload = {"transcript": "Add a new lead: Rohan Sharma from Gurgaon, phone 9876543210, source Instagram."}
    resp = client.post("/bot/handle", json=payload)
    assert resp.status_code == 200
    j = resp.json()
    assert j["intent"] == "LEAD_CREATE"
    assert j["entities"]["name"] is not None
    assert j["result"]["status"] == "NEW"

def test_lead_create_missing_phone(monkeypatch):
    payload = {"transcript": "Create lead name Priya Nair, city Mumbai."}
    resp = client.post("/bot/handle", json=payload)
    assert resp.status_code == 400
    j = resp.json()
    assert j["error"]["type"] == "VALIDATION_ERROR"
