from database import SessionLocal, engine
from models import Base, Metric, Insight, User
from services.auth_service import hash_password
from datetime import date


Base.metadata.create_all(bind=engine)


def seed():
    db = SessionLocal()

    existing_user = db.query(User).filter(User.email == "demo@insightiq.com").first()

    if existing_user:
        existing_metrics = db.query(Metric).filter(Metric.user_id == existing_user.id).first()
        if existing_metrics:
            print("Seed déjà effectué, on skip.")
            db.close()
            return
        user = existing_user
    else:
        user = User(
            email    = "demo@insightiq.com",
            username = "Demo User",
            password = hash_password("demo1234")
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    metrics = [
        # ── Sales ─────────────────────────────────────────
        Metric(name="Monthly Revenue",    value=42000, unit="€",      category="Sales",     recorded_at=date(2024,1,1), user_id=user.id),
        Metric(name="Monthly Revenue",    value=45500, unit="€",      category="Sales",     recorded_at=date(2024,2,1), user_id=user.id),
        Metric(name="Monthly Revenue",    value=39000, unit="€",      category="Sales",     recorded_at=date(2024,3,1), user_id=user.id),
        Metric(name="New Clients",        value=18,    unit="clients", category="Sales",     recorded_at=date(2024,1,1), user_id=user.id),
        Metric(name="New Clients",        value=24,    unit="clients", category="Sales",     recorded_at=date(2024,2,1), user_id=user.id),
        Metric(name="New Clients",        value=20,    unit="clients", category="Sales",     recorded_at=date(2024,3,1), user_id=user.id),
        Metric(name="Churn Rate",         value=3.2,   unit="%",       category="Sales",     recorded_at=date(2024,1,1), user_id=user.id),
        Metric(name="Churn Rate",         value=4.1,   unit="%",       category="Sales",     recorded_at=date(2024,2,1), user_id=user.id),
        Metric(name="Churn Rate",         value=3.8,   unit="%",       category="Sales",     recorded_at=date(2024,3,1), user_id=user.id),

        # ── Marketing ──────────────────────────────────────
        Metric(name="Unique Visitors",    value=8200,  unit="users",   category="Marketing", recorded_at=date(2024,1,1), user_id=user.id),
        Metric(name="Unique Visitors",    value=9400,  unit="users",   category="Marketing", recorded_at=date(2024,2,1), user_id=user.id),
        Metric(name="Unique Visitors",    value=11200, unit="users",   category="Marketing", recorded_at=date(2024,3,1), user_id=user.id),
        Metric(name="Conversion Rate",    value=2.4,   unit="%",       category="Marketing", recorded_at=date(2024,1,1), user_id=user.id),
        Metric(name="Conversion Rate",    value=2.1,   unit="%",       category="Marketing", recorded_at=date(2024,2,1), user_id=user.id),
        Metric(name="Conversion Rate",    value=2.8,   unit="%",       category="Marketing", recorded_at=date(2024,3,1), user_id=user.id),

        # ── Support ────────────────────────────────────────
        Metric(name="Open Tickets",       value=142,   unit="tickets", category="Support",   recorded_at=date(2024,1,1), user_id=user.id),
        Metric(name="Open Tickets",       value=128,   unit="tickets", category="Support",   recorded_at=date(2024,2,1), user_id=user.id),
        Metric(name="Open Tickets",       value=155,   unit="tickets", category="Support",   recorded_at=date(2024,3,1), user_id=user.id),
        Metric(name="Resolution Time",    value=4.2,   unit="hours",   category="Support",   recorded_at=date(2024,1,1), user_id=user.id),
        Metric(name="Resolution Time",    value=3.8,   unit="hours",   category="Support",   recorded_at=date(2024,2,1), user_id=user.id),
        Metric(name="Resolution Time",    value=5.1,   unit="hours",   category="Support",   recorded_at=date(2024,3,1), user_id=user.id),
        Metric(name="Customer Satisfaction", value=87, unit="%",       category="Support",   recorded_at=date(2024,1,1), user_id=user.id),
        Metric(name="Customer Satisfaction", value=91, unit="%",       category="Support",   recorded_at=date(2024,2,1), user_id=user.id),
        Metric(name="Customer Satisfaction", value=85, unit="%",       category="Support",   recorded_at=date(2024,3,1), user_id=user.id),
    ]

    db.add_all(metrics)
    db.commit()
    print(f"Seed : {len(metrics)} métriques insérées pour {user.email}")
    db.close()


if __name__ == "__main__":
    seed()