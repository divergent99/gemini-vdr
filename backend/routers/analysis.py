import json
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from backend.services.extractor import extract_from_folder, extract_from_uploads, scan_folder
from backend.services.analyser  import run_analysis, last_meta
from backend.logger import log

router = APIRouter(prefix="/api", tags=["analysis"])


# ── Request / Response models ─────────────────────────────────────
class FolderRequest(BaseModel):
    folder_path: str

class UploadRequest(BaseModel):
    contents:   list[str]   # base64 data URIs
    filenames:  list[str]

class ScanRequest(BaseModel):
    folder_path: str


# ── Endpoints ─────────────────────────────────────────────────────
@router.post("/scan")
def api_scan(req: ScanRequest):
    """Quick scan — return list of supported files in folder (no extraction)."""
    files = scan_folder(req.folder_path)
    return {"files": files, "count": len(files)}


@router.post("/analyse/folder")
def api_analyse_folder(req: FolderRequest):
    """Extract text from a local folder and run Gemini analysis."""
    try:
        doc_text, files = extract_from_folder(req.folder_path)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    analysis = run_analysis(doc_text, folder_path=req.folder_path)
    meta     = last_meta()

    return {
        "analysis":    analysis,
        "doc_text":    doc_text,
        "files":       files,
        "file_count":  len(files),
        "from_cache":  meta["from_cache"],
        "elapsed":     round(meta["elapsed"], 1),
    }


@router.post("/analyse/upload")
def api_analyse_upload(req: UploadRequest):
    """Extract text from uploaded base64 files and run Gemini analysis."""
    if not req.contents:
        raise HTTPException(status_code=400, detail="No files uploaded.")

    doc_text = extract_from_uploads(req.contents, req.filenames)
    analysis = run_analysis(doc_text)
    meta     = last_meta()

    return {
        "analysis":    analysis,
        "doc_text":    doc_text,
        "files":       req.filenames,
        "file_count":  len(req.filenames),
        "from_cache":  meta["from_cache"],
        "elapsed":     round(meta["elapsed"], 1),
    }
