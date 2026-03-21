from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Metric, Insight
from schemas import InsightRequest, InsightResponse
from services.claude_service import generate_insight

router = APIRouter(prefix="/api/insights", tags=["Insights"])


@router.post("/generate", response_model=InsightResponse, status_code=201)
def generate(
    request: InsightRequest,
    db: Session = Depends(get_db)
):
    metrics = db.query(Metric).filter(
        Metric.category == request.category
    ).order_by(Metric.recorded_at.asc()).all()

    if not metrics:
        raise HTTPException(
            status_code=404,
            detail=f"Aucune métrique trouvée pour la catégorie '{request.category}'"
        )

    metrics_data = [
        {
            "name":        m.name,
            "value":       m.value,
            "unit":        m.unit,
            "recorded_at": str(m.recorded_at)
        }
        for m in metrics
    ]

    try:
        result = generate_insight(metrics_data, request.category)
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))

    db_insight = Insight(
        title=result["title"],
        content=result["content"],
        category=result["category"]
    )
    db.add(db_insight)
    db.commit()
    db.refresh(db_insight)
    return db_insight


@router.get("/", response_model=List[InsightResponse])
def get_insights(
    category: str = None,
    db: Session = Depends(get_db)
):
    query = db.query(Insight)
    if category:
        query = query.filter(Insight.category == category)
    return query.order_by(Insight.generated_at.desc()).all()