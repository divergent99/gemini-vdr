from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware

from backend.routers.analysis import router as analysis_router
from backend.routers.voice    import router as voice_router
from backend.logger import log

# ── FastAPI ───────────────────────────────────────────────────────
app = FastAPI(
    title="VDR Voice Intelligence",
    description="Gemini Live Agent Challenge 2026",
    version="1.0.0",
)

app.include_router(analysis_router)
app.include_router(voice_router)

@app.get("/health")
def health():
    return {"status": "ok"}

# ── Mount Dash under / ────────────────────────────────────────────
# Import AFTER FastAPI routes so /api/* is matched first
from frontend.app import server as dash_server  # noqa: E402
app.mount("/", WSGIMiddleware(dash_server))

log("VDR Voice Intelligence ready — http://localhost:8052", "OK")
