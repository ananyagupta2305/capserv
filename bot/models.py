# bot/models.py
from pydantic import BaseModel
from typing import Optional, Dict, Any

class BotRequest(BaseModel):
    transcript: str
    metadata: Optional[Dict[str, Any]] = None

class ErrorDetail(BaseModel):
    type: str
    details: str

class BotResponse(BaseModel):
    intent: str
    entities: Dict[str, Any]
    crm_call: Dict[str, Any]
    result: Dict[str, Any]
