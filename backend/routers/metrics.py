from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Metric, User
from schemas import MetricCreate, MetricUpdate, MetricResponse
from services.auth_service import get_current_user

router = APIRouter(prefix="/api/metrics", tags=["Metrics"])


@router.get("/", response_model=List[MetricResponse])
def get_metrics(
    category:     Optional[str] = None,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user)
):
    query = db.query(Metric).filter(Metric.user_id == current_user.id)
    if category:
        query = query.filter(Metric.category == category)
    return query.order_by(Metric.recorded_at.desc()).all()


@router.post("/", response_model=MetricResponse, status_code=201)
def create_metric(
    metric:       MetricCreate,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user)
):
    db_metric = Metric(**metric.model_dump(), user_id=current_user.id)
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric


@router.put("/{metric_id}", response_model=MetricResponse)
def update_metric(
    metric_id:    int,
    metric:       MetricUpdate,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user)
):
    db_metric = db.query(Metric).filter(
        Metric.id == metric_id,
        Metric.user_id == current_user.id
    ).first()
    if not db_metric:
        raise HTTPException(status_code=404, detail="Metric not found")

    for key, value in metric.model_dump(exclude_unset=True).items():
        setattr(db_metric, key, value)
    db.commit()
    db.refresh(db_metric)
    return db_metric


@router.delete("/{metric_id}", status_code=204)
def delete_metric(
    metric_id:    int,
    db:           Session = Depends(get_db),
    current_user: User    = Depends(get_current_user)
):
    db_metric = db.query(Metric).filter(
        Metric.id == metric_id,
        Metric.user_id == current_user.id
    ).first()
    if not db_metric:
        raise HTTPException(status_code=404, detail="Metric not found")
    db.delete(db_metric)
    db.commit()
    return None