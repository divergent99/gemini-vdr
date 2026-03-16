import os
import pyaudio
from dotenv import load_dotenv
from backend.logger import log

load_dotenv()

# ── Gemini ────────────────────────────────────────────────
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL   = os.getenv("GEMINI_MODEL", "gemini-2.5-flash-native-audio-preview-12-2025")
CACHE_DIR      = os.getenv("CACHE_DIR", "./gemini_vdr_cache")

# ── Server ports ──────────────────────────────────────────
BACKEND_PORT  = int(os.getenv("BACKEND_PORT",  8000))
FRONTEND_PORT = int(os.getenv("FRONTEND_PORT", 8052))

# ── Audio ─────────────────────────────────────────────────
FORMAT           = pyaudio.paInt16
CHANNELS         = 1
SEND_SAMPLE_RATE = 16000
RECV_SAMPLE_RATE = 24000
CHUNK_SIZE       = 1024

log("Initialising PyAudio...")
pya = pyaudio.PyAudio()

INPUT_DEVICE  = None
OUTPUT_DEVICE = None

for i in range(pya.get_device_count()):
    info = pya.get_device_info_by_index(i)
    if "Jabra" in info["name"]:
        if info["maxInputChannels"] > 0 and INPUT_DEVICE is None:
            INPUT_DEVICE = i
            log(f"Jabra input  → device {i}: {info['name']}", "OK")
        if info["maxOutputChannels"] > 0 and OUTPUT_DEVICE is None:
            OUTPUT_DEVICE = i
            log(f"Jabra output → device {i}: {info['name']}", "OK")

if INPUT_DEVICE is None:
    log("No Jabra found — using system default input", "WARN")
if OUTPUT_DEVICE is None:
    log("No Jabra found — using system default output", "WARN")
