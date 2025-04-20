# utils/schemas.py

from pydantic import BaseModel, Field
from typing import Optional

class WebhookRequest(BaseModel):
    action: str
    amount: Optional[float] = Field(default=None, gt=0)
    source: Optional[str] = "live"
