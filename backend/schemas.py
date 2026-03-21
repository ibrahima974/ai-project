from pydantic import BaseModel, Field
from datetime import date, datetime
from typing import Optional

# ─── METRIC ───────────────────────────────────────────

class MetricCreate(BaseModel):
    name:        str   = Field(..., min_length=1, max_length=100)
    value:       float = Field(..., description="Valeur numérique de la métrique")
    unit:        str   = Field(..., min_length=1, max_length=20)
    category:    str   = Field(..., min_length=1, max_length=50)
    recorded_at: date

class MetricUpdate(BaseModel):
    name:        Optional[str]   = Field(None, min_length=1, max_length=100)
    value:       Optional[float] = None
    unit:        Optional[str]   = Field(None, min_length=1, max_length=20)
    category:    Optional[str]   = Field(None, min_length=1, max_length=50)
    recorded_at: Optional[date]  = None

class MetricResponse(BaseModel):
    id:          int
    name:        str
    value:       float
    unit:        str
    category:    str
    recorded_at: date
    created_at:  datetime

    class Config:
        from_attributes = True

# ─── INSIGHT ──────────────────────────────────────────

class InsightRequest(BaseModel):
    category: str = Field(..., min_length=1, max_length=50)

class InsightResponse(BaseModel):
    id:           int
    title:        str
    content:      str
    category:     str
    generated_at: datetime

    class Config:
        from_attributes = True