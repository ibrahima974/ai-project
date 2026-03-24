from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database import engine, Base
import models
from routers import metrics, insights, auth
from seed import seed
from sqlalchemy import text

Base.metadata.create_all(bind=engine)

app = FastAPI(title="InsightIQ API", version="1.0.0")


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "https://ai-project-steel-psi.vercel.app"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)

app.include_router(auth.router)
app.include_router(metrics.router)
app.include_router(insights.router)



with engine.connect() as conn:
    conn.execute(text("DROP TABLE IF EXISTS insights CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS metrics CASCADE"))
    conn.execute(text("DROP TABLE IF EXISTS users CASCADE"))
    conn.commit()

Base.metadata.create_all(bind=engine)
seed()

seed()

@app.get("/")
def root():
    return {"message": "InsightIQ API is running"}