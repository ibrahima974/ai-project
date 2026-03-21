from sqlalchemy import Column, Integer, String, Float, Date, Text, DateTime
from sqlalchemy.sql import func
from database import Base

class Metric(Base):
    __tablename__ = "metrics"

    id          = Column(Integer, primary_key=True, index=True)
    name        = Column(String(100), nullable=False)
    value       = Column(Float, nullable=False)
    unit        = Column(String(20), nullable=False)
    category    = Column(String(50), nullable=False)
    recorded_at = Column(Date, nullable=False)
    created_at  = Column(DateTime, server_default=func.now())


class Insight(Base):
    __tablename__ = "insights"

    id           = Column(Integer, primary_key=True, index=True)
    title        = Column(String(200), nullable=False)
    content      = Column(Text, nullable=False)
    category     = Column(String(50), nullable=False)
    generated_at = Column(DateTime, server_default=func.now())