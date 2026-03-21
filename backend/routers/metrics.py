from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from database import get_db
from models import Metric
from schemas import MetricCreate, MetricUpdate, MetricResponse

router = APIRouter(prefix="/api/metrics", tags=["Metrics"])


@router.get("/", response_model=List[MetricResponse])
def get_metrics(
    category: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Metric)
    if category:
        query = query.filter(Metric.category == category)
    return query.order_by(Metric.recorded_at.desc()).all()


@router.post("/", response_model=MetricResponse, status_code=201)
def create_metric(
    metric: MetricCreate,
    db: Session = Depends(get_db)
):
    db_metric = Metric(**metric.model_dump())
    db.add(db_metric)
    db.commit()
    db.refresh(db_metric)
    return db_metric


@router.put("/{metric_id}", response_model=MetricResponse)
def update_metric(
    metric_id: int,
    metric: MetricUpdate,
    db: Session = Depends(get_db)
):
    db_metric = db.query(Metric).filter(Metric.id == metric_id).first()
    if not db_metric:
        raise HTTPException(status_code=404, detail="Métrique introuvable")

    updated_data = metric.model_dump(exclude_unset=True)
    for key, value in updated_data.items():
        setattr(db_metric, key, value)

    db.commit()
    db.refresh(db_metric)
    return db_metric


@router.delete("/{metric_id}", status_code=204)
def delete_metric(
    metric_id: int,
    db: Session = Depends(get_db)
):
    db_metric = db.query(Metric).filter(Metric.id == metric_id).first()
    if not db_metric:
        raise HTTPException(status_code=404, detail="Métrique introuvable")

    db.delete(db_metric)
    db.commit()
    return None