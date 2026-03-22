from services.claude_service import generate_insight

metrics_test = [
    {"name": "Revenu mensuel", "value": 42000, "unit": "€", "recorded_at": "2024-01-01"},
    {"name": "Revenu mensuel", "value": 45500, "unit": "€", "recorded_at": "2024-02-01"},
    {"name": "Nouveaux clients", "value": 18, "unit": "clients", "recorded_at": "2024-01-01"},
    {"name": "Taux de churn", "value": 4.1, "unit": "%", "recorded_at": "2024-02-01"},
]

result = generate_insight(metrics_test, "Sales")
print("TITRE :", result["title"])
print("CONTENU :\n", result["content"])