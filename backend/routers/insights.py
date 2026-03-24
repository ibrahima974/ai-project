from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Metric, Insight, User
from schemas import InsightRequest, InsightResponse
from services.claude_service import generate_insight, generate_insight_stream
from services.auth_service import get_current_user
import json

router = APIRouter(prefix="/api/insights", tags=["Insights"])


@router.post("/generate", response_model=InsightResponse, status_code=201)
def generate(
    request:      InsightRequest,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user)
):
    metrics = db.query(Metric).filter(
        Metric.category == request.category,
        Metric.user_id  == current_user.id
    ).order_by(Metric.recorded_at.asc()).all()

    if not metrics:
        raise HTTPException(status_code=404, detail=f"No metrics found for '{request.category}'")

    metrics_data = [{"name": m.name, "value": m.value, "unit": m.unit, "recorded_at": str(m.recorded_at)} for m in metrics]

    try:
        result = generate_insight(metrics_data, request.category)
    except ValueError as e:
        raise HTTPException(status_code=503, detail=str(e))

    db_insight = Insight(
        title    = result["title"],
        content  = result["content"],
        category = result["category"],
        user_id  = current_user.id
    )
    db.add(db_insight)
    db.commit()
    db.refresh(db_insight)
    return db_insight


@router.post("/stream")
def stream_insight(
    request:      InsightRequest,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user)
):
    metrics = db.query(Metric).filter(
        Metric.category == request.category,
        Metric.user_id  == current_user.id
    ).order_by(Metric.recorded_at.asc()).all()

    if not metrics:
        raise HTTPException(status_code=404, detail=f"No metrics found for '{request.category}'")

    metrics_data = [{"name": m.name, "value": m.value, "unit": m.unit, "recorded_at": str(m.recorded_at)} for m in metrics]
    full_content = []

    def event_stream():
        try:
            for chunk in generate_insight_stream(metrics_data, request.category):
                full_content.append(chunk)
                yield f"data: {json.dumps({'text': chunk})}\n\n"

            content = "".join(full_content)
            title   = f"Analysis {request.category} — {metrics_data[0]['recorded_at'][:7]}"

            db_insight = Insight(title=title, content=content, category=request.category, user_id=current_user.id)
            db.add(db_insight)
            db.commit()
            db.refresh(db_insight)

            yield f"data: {json.dumps({'done': True, 'insight': {'id': db_insight.id, 'title': db_insight.title, 'category': db_insight.category}})}\n\n"
        except ValueError as e:
            yield f"data: {json.dumps({'error': str(e)})}\n\n"

    return StreamingResponse(event_stream(), media_type="text/event-stream",
        headers={"Cache-Control": "no-cache", "X-Accel-Buffering": "no"})


@router.get("/", response_model=List[InsightResponse])
def get_insights(
    category:     str     = None,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user)
):
    query = db.query(Insight).filter(Insight.user_id == current_user.id)
    if category:
        query = query.filter(Insight.category == category)
    return query.order_by(Insight.generated_at.desc()).all()