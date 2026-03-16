from fastapi import APIRouter
from pydantic import BaseModel

from backend.services.voice_agent import (
    voice_state,
    start_recording,
    stop_recording_and_query,
)
from backend.logger import log

router = APIRouter(prefix="/api/voice", tags=["voice"])


class StopPayload(BaseModel):
    doc_context: str = ""


@router.post("/start")
def api_start():
    start_recording()
    return {"status": "recording"}


@router.post("/stop")
def api_stop(payload: StopPayload):
    stop_recording_and_query(payload.doc_context)
    return {"status": "processing"}


@router.get("/result")
def api_result():
    if not voice_state.result_ready.is_set():
        return {"ready": False}
    result = voice_state.last_result or {}
    voice_state.result_ready.clear()
    voice_state.last_result = None
    log("Result consumed via API", "OK")
    return {"ready": True, "result": result}
