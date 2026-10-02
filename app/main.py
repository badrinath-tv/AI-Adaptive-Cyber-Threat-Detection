from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi import Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.api.alerts import router as alerts_router
from app.api.events import router as events_router
from app.api.feedback import router as feedback_router
from app.api.health import router as health_router


PROJECT_ROOT = Path(__file__).resolve().parents[1]

DASHBOARD_DIR = PROJECT_ROOT / "dashboard"
TEMPLATES_DIR = DASHBOARD_DIR / "templates"
STATIC_DIR = DASHBOARD_DIR / "static"


app = FastAPI(
    title="AI-Powered Adaptive Cyber Threat Detection & Response System",
    description=(
        "AI-based cybersecurity detection, anomaly analysis, "
        "risk assessment, and simulated response system."
    ),
    version="1.0.0",
)


app.mount(
    "/static",
    StaticFiles(directory=STATIC_DIR),
    name="static",
)


templates = Jinja2Templates(
    directory=TEMPLATES_DIR,
)


app.include_router(health_router)
app.include_router(events_router)
app.include_router(alerts_router)
app.include_router(feedback_router)


@app.get("/dashboard")
def dashboard(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "request": request,
        },
    )


@app.get("/dashboard/incident")
def incident(request: Request):
    return templates.TemplateResponse(
        request=request,
        name="incident.html",
        context={
            "request": request,
        },
    )


@app.get("/")
def root():
    return {
        "service": (
            "AI-Powered Adaptive Cyber Threat "
            "Detection & Response System"
        ),
        "status": "running",
    }