from fastapi import FastAPI
from src.auth.router import router as auth_router

app = FastAPI(
    title="SidiWeb Backend - Auth Module (B1)",
    description="Authentication & User Management API",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.include_router(auth_router)

@app.get("/")
async def root():
    return {"message": "SidiWeb Auth API - B1"}


