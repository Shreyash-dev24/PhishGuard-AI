from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.app.api.predict import router as predict_router
from backend.app.api.history import router as history_router


# --------------------------------------------------
# FastAPI Application
# --------------------------------------------------

app = FastAPI(
    title="PhishGuard AI",
    description=(
        "AI-powered URL phishing detection using "
        "Machine Learning, Deep Learning, and "
        "a rule-based expert system."
    ),
    version="1.0.0",
)


# --------------------------------------------------
# CORS Configuration
# --------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# --------------------------------------------------
# Register API routers
# --------------------------------------------------

app.include_router(
    predict_router
)

app.include_router(
    history_router
)


# --------------------------------------------------
# Root endpoint
# --------------------------------------------------

@app.get("/")
def root():
    """
    Basic API health message.
    """

    return {
        "message": "PhishGuard AI API is running",
        "status": "ok",
    }


# --------------------------------------------------
# Health endpoint
# --------------------------------------------------

@app.get("/health")
def health():
    """
    Backend health check.
    """

    return {
        "status": "healthy"
    }