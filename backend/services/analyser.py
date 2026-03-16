import json
import time
from google import genai
from google.genai import types as gtypes

from backend.config import GEMINI_API_KEY
from backend.logger import log
from backend.services.cache import cache_get, cache_put, doc_hash

ANALYSIS_MODEL = "gemini-2.5-flash"
PROMPT_TEMPLATE = """\
You are a senior M&A due diligence analyst.
Analyse the following documents and return a JSON object with this exact structure.
No markdown, no preamble — raw JSON only.

{{
  "deal_score": 62,
  "recommendation": "proceed_with_conditions",
  "financial_summary": "2-3 sentence summary of financial health",
  "legal_summary": "2-3 sentence summary of legal/contract risks",
  "compliance_summary": "2-3 sentence summary of regulatory risks",
  "top_risks": [
    {{"risk": "risk name", "severity": "critical|high|medium|low", "area": "financial|legal|compliance"}}
  ],
  "scores": {{
    "financial": 65,
    "legal": 55,
    "compliance": 70
  }},
  "key_facts": [
    "fact 1 about the deal",
    "fact 2 about the deal"
  ],
  "executive_summary": "3-4 sentence executive summary for C-suite"
}}

DOCUMENTS:
{doc_text}
"""

# Function-level flags so the router can report cache hit + elapsed
_last_from_cache: bool  = False
_last_elapsed:    float = 0.0


def run_analysis(doc_text: str, folder_path: str = "") -> dict:
    global _last_from_cache, _last_elapsed
    _last_from_cache = False
    _last_elapsed    = 0.0

    key    = doc_hash(doc_text)
    cached = cache_get(key)
    if cached:
        log("Returning cached analysis (skipping Gemini call)", "OK")
        _last_from_cache = True
        return cached

    log("Connecting to Gemini Flash for analysis...")
    client = genai.Client(
        api_key=GEMINI_API_KEY,
        http_options=gtypes.HttpOptions(api_version="v1alpha"),
    )

    prompt = PROMPT_TEMPLATE.format(doc_text=doc_text[:20_000])
    log("Sending documents to Gemini Flash (this may take 15-30s)...")
    t0 = time.time()
    response = client.models.generate_content(model=ANALYSIS_MODEL, contents=prompt)
    elapsed  = time.time() - t0
    _last_elapsed = elapsed
    log(f"Gemini analysis returned in {elapsed:.1f}s", "OK")

    raw    = response.text.replace("```json", "").replace("```", "").strip()
    result = json.loads(raw)
    log(f"Deal score: {result.get('deal_score')} | Rec: {result.get('recommendation')}", "OK")

    cache_put(key, result, folder_path)
    return result


def last_meta() -> dict:
    """Return cache/elapsed metadata from the most recent run_analysis call."""
    return {"from_cache": _last_from_cache, "elapsed": _last_elapsed}
