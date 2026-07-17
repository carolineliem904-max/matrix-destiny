from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.matrix import router as matrix_router
from app.core.config import settings

app = FastAPI(
    title="Matrix Destiny API",
    version="0.1.0",
    description="Deterministic Destiny Matrix calculation and interpretation API.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(matrix_router, prefix="/api")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}
