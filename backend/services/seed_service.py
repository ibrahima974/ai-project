from datetime import date
from models import Metric
from sqlalchemy.orm import Session


def seed_user_metrics(db: Session, user_id: int):
    metrics = [
        # ── Sales ──────────────────────────────────────────
        Metric(name="Monthly Revenue",       value=42000, unit="€",       category="Sales",     recorded_at=date(2024,1,1), user_id=user_id),
        Metric(name="Monthly Revenue",       value=45500, unit="€",       category="Sales",     recorded_at=date(2024,2,1), user_id=user_id),
        Metric(name="Monthly Revenue",       value=39000, unit="€",       category="Sales",     recorded_at=date(2024,3,1), user_id=user_id),
        Metric(name="New Clients",           value=18,    unit="clients",  category="Sales",     recorded_at=date(2024,1,1), user_id=user_id),
        Metric(name="New Clients",           value=24,    unit="clients",  category="Sales",     recorded_at=date(2024,2,1), user_id=user_id),
        Metric(name="New Clients",           value=20,    unit="clients",  category="Sales",     recorded_at=date(2024,3,1), user_id=user_id),
        Metric(name="Churn Rate",            value=3.2,   unit="%",        category="Sales",     recorded_at=date(2024,1,1), user_id=user_id),
        Metric(name="Churn Rate",            value=4.1,   unit="%",        category="Sales",     recorded_at=date(2024,2,1), user_id=user_id),
        Metric(name="Churn Rate",            value=3.8,   unit="%",        category="Sales",     recorded_at=date(2024,3,1), user_id=user_id),

        # ── Marketing ──────────────────────────────────────
        Metric(name="Unique Visitors",       value=8200,  unit="users",    category="Marketing", recorded_at=date(2024,1,1), user_id=user_id),
        Metric(name="Unique Visitors",       value=9400,  unit="users",    category="Marketing", recorded_at=date(2024,2,1), user_id=user_id),
        Metric(name="Unique Visitors",       value=11200, unit="users",    category="Marketing", recorded_at=date(2024,3,1), user_id=user_id),
        Metric(name="Conversion Rate",       value=2.4,   unit="%",        category="Marketing", recorded_at=date(2024,1,1), user_id=user_id),
        Metric(name="Conversion Rate",       value=2.1,   unit="%",        category="Marketing", recorded_at=date(2024,2,1), user_id=user_id),
        Metric(name="Conversion Rate",       value=2.8,   unit="%",        category="Marketing", recorded_at=date(2024,3,1), user_id=user_id),

        # ── Support ────────────────────────────────────────
        Metric(name="Open Tickets",          value=142,   unit="tickets",  category="Support",   recorded_at=date(2024,1,1), user_id=user_id),
        Metric(name="Open Tickets",          value=128,   unit="tickets",  category="Support",   recorded_at=date(2024,2,1), user_id=user_id),
        Metric(name="Open Tickets",          value=155,   unit="tickets",  category="Support",   recorded_at=date(2024,3,1), user_id=user_id),
        Metric(name="Resolution Time",       value=4.2,   unit="hours",    category="Support",   recorded_at=date(2024,1,1), user_id=user_id),
        Metric(name="Resolution Time",       value=3.8,   unit="hours",    category="Support",   recorded_at=date(2024,2,1), user_id=user_id),
        Metric(name="Resolution Time",       value=5.1,   unit="hours",    category="Support",   recorded_at=date(2024,3,1), user_id=user_id),
        Metric(name="Customer Satisfaction", value=87,    unit="%",        category="Support",   recorded_at=date(2024,1,1), user_id=user_id),
        Metric(name="Customer Satisfaction", value=91,    unit="%",        category="Support",   recorded_at=date(2024,2,1), user_id=user_id),
        Metric(name="Customer Satisfaction", value=85,    unit="%",        category="Support",   recorded_at=date(2024,3,1), user_id=user_id),
    ]

    db.add_all(metrics)
    db.commit()