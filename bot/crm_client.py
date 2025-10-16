# bot/crm_client.py
import uuid
from typing import Any, Dict
from .settings import settings

class CRMError(Exception):
    def __init__(self, status_code: int, message: str):
        self.status_code = status_code
        self.message = message
        super().__init__(f"CRMError {status_code}: {message}")

class CRMClient:
    """
    Mock/in-memory CRM client for local testing.
    Stores leads in memory to allow sequential operations.
    """
    def __init__(self, base_url: str = None, timeout: int = 5):
        self.base_url = base_url or settings.CRM_BASE_URL
        self.timeout = timeout
        self.leads: Dict[str, Dict[str, Any]] = {}  # In-memory storage for leads

    def create_lead(self, name: str, phone: str, city: str, source: str = None) -> Dict[str, Any]:
        lead_id = str(uuid.uuid4())
        self.leads[lead_id] = {
            "name": name,
            "phone": phone,
            "city": city,
            "source": source,
            "status": "NEW"
        }
        return {"lead_id": lead_id, "status": "NEW"}

    def schedule_visit(self, lead_id: str, visit_time: str, notes: str = None) -> Dict[str, Any]:
        if lead_id not in self.leads:
            raise CRMError(404, '{"detail":"Lead not found"}')
        self.leads[lead_id]["visit_time"] = visit_time
        if notes:
            self.leads[lead_id]["notes"] = notes
        return {"visit_id": str(uuid.uuid4()), "status": "SCHEDULED"}

    def update_status(self, lead_id: str, status: str, notes: str = None) -> Dict[str, Any]:
        if lead_id not in self.leads:
            raise CRMError(404, '{"detail":"Lead not found"}')
        self.leads[lead_id]["status"] = status
        if notes:
            self.leads[lead_id]["notes"] = notes
        return {"lead_id": lead_id, "status": status}