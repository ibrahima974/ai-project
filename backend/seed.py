from database import SessionLocal, engine
from models import Base, Metric, Insight
from datetime import date

Base.metadata.create_all(bind=engine)

def seed():
    db = SessionLocal()

    existing = db.query(Metric).first()
    if existing:
        print("Seed déjà effectué, on skip.")
        db.close()
        return

    metrics = [
        # ── Sales ──────────────────────────────────────────
        Metric(name="Revenu mensuel",       value=42000, unit="€",     category="Sales",     recorded_at=date(2024, 1, 1)),
        Metric(name="Revenu mensuel",       value=45500, unit="€",     category="Sales",     recorded_at=date(2024, 2, 1)),
        Metric(name="Revenu mensuel",       value=39000, unit="€",     category="Sales",     recorded_at=date(2024, 3, 1)),
        Metric(name="Nouveaux clients",     value=18,    unit="clients",category="Sales",     recorded_at=date(2024, 1, 1)),
        Metric(name="Nouveaux clients",     value=24,    unit="clients",category="Sales",     recorded_at=date(2024, 2, 1)),
        Metric(name="Nouveaux clients",     value=20,    unit="clients",category="Sales",     recorded_at=date(2024, 3, 1)),
        Metric(name="Taux de churn",        value=3.2,   unit="%",     category="Sales",     recorded_at=date(2024, 1, 1)),
        Metric(name="Taux de churn",        value=4.1,   unit="%",     category="Sales",     recorded_at=date(2024, 2, 1)),
        Metric(name="Taux de churn",        value=3.8,   unit="%",     category="Sales",     recorded_at=date(2024, 3, 1)),

        # ── Marketing ──────────────────────────────────────
        Metric(name="Visiteurs uniques",    value=8200,  unit="users", category="Marketing", recorded_at=date(2024, 1, 1)),
        Metric(name="Visiteurs uniques",    value=9400,  unit="users", category="Marketing", recorded_at=date(2024, 2, 1)),
        Metric(name="Visiteurs uniques",    value=11200, unit="users", category="Marketing", recorded_at=date(2024, 3, 1)),
        Metric(name="Taux de conversion",   value=2.4,   unit="%",     category="Marketing", recorded_at=date(2024, 1, 1)),
        Metric(name="Taux de conversion",   value=2.1,   unit="%",     category="Marketing", recorded_at=date(2024, 2, 1)),
        Metric(name="Taux de conversion",   value=2.8,   unit="%",     category="Marketing", recorded_at=date(2024, 3, 1)),

        # ── Support ────────────────────────────────────────
        Metric(name="Tickets ouverts",      value=142,   unit="tickets",category="Support",  recorded_at=date(2024, 1, 1)),
        Metric(name="Tickets ouverts",      value=128,   unit="tickets",category="Support",  recorded_at=date(2024, 2, 1)),
        Metric(name="Tickets ouverts",      value=155,   unit="tickets",category="Support",  recorded_at=date(2024, 3, 1)),
        Metric(name="Temps de résolution",  value=4.2,   unit="heures", category="Support",  recorded_at=date(2024, 1, 1)),
        Metric(name="Temps de résolution",  value=3.8,   unit="heures", category="Support",  recorded_at=date(2024, 2, 1)),
        Metric(name="Temps de résolution",  value=5.1,   unit="heures", category="Support",  recorded_at=date(2024, 3, 1)),
        Metric(name="Satisfaction client",  value=87,    unit="%",      category="Support",  recorded_at=date(2024, 1, 1)),
        Metric(name="Satisfaction client",  value=91,    unit="%",      category="Support",  recorded_at=date(2024, 2, 1)),
        Metric(name="Satisfaction client",  value=85,    unit="%",      category="Support",  recorded_at=date(2024, 3, 1)),
    ]

    db.add_all(metrics)
    db.commit()
    print(f"{len(metrics)} métriques insérées avec succès.")
    db.close()

if __name__ == "__main__":
    seed()