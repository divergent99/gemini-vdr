import re
import threading
import asyncio
from google import genai
from google.genai import types as gtypes

from backend.config import (
    GEMINI_API_KEY, GEMINI_MODEL,
    pya, FORMAT, CHANNELS,
    SEND_SAMPLE_RATE, RECV_SAMPLE_RATE,
    CHUNK_SIZE, INPUT_DEVICE, OUTPUT_DEVICE,
)
from backend.logger import log


# ── State ─────────────────────────────────────────────────────────
class VoiceState:
    def __init__(self):
        self.is_recording = False
        self.frames:  list = []
        self.stream         = None
        self.lock           = threading.Lock()
        self.result_ready   = threading.Event()
        self.last_result: dict | None = None


voice_state = VoiceState()


# ── Recording controls ────────────────────────────────────────────
def start_recording() -> None:
    with voice_state.lock:
        voice_state.frames = []
        voice_state.is_recording = True
        voice_state.result_ready.clear()
        voice_state.last_result = None
        voice_state.stream = pya.open(
            format=FORMAT, channels=CHANNELS,
            rate=SEND_SAMPLE_RATE, input=True,
            input_device_index=INPUT_DEVICE,
            frames_per_buffer=CHUNK_SIZE,
        )

    # Self-contained recording loop — no Dash ticker needed
    def _record_loop():
        log("Recording loop started", "OK")
        while True:
            with voice_state.lock:
                if not voice_state.is_recording or not voice_state.stream:
                    break
                try:
                    data = voice_state.stream.read(CHUNK_SIZE, exception_on_overflow=False)
                    voice_state.frames.append(data)
                except Exception:
                    break
        log("Recording loop ended", "OK")

    threading.Thread(target=_record_loop, daemon=True).start()


def stop_recording_and_query(doc_context: str) -> None:
    with voice_state.lock:
        voice_state.is_recording = False
        if voice_state.stream:
            voice_state.stream.stop_stream()
            voice_state.stream.close()
            voice_state.stream = None
        frames = list(voice_state.frames)

    log(f"Recording stopped — {len(frames)} chunks "
        f"({len(frames) * CHUNK_SIZE / SEND_SAMPLE_RATE:.1f}s of audio)")

    def _run():
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            result = loop.run_until_complete(_gemini_voice_query(frames, doc_context))
        except Exception as e:
            log(f"Voice query failed: {e}", "ERR")
            result = {"error": str(e), "you_said": "(unclear)", "response_text": f"Error: {e}"}
        finally:
            loop.close()
        voice_state.last_result = result
        voice_state.result_ready.set()
        log("Result stored and ready flag set", "OK")

    threading.Thread(target=_run, daemon=True).start()


def record_chunk() -> None:
    """Legacy — no longer needed, kept for API compat."""
    pass


# ── Gemini Live query ─────────────────────────────────────────────
async def _gemini_voice_query(frames: list, doc_context: str) -> dict:
    if not frames:
        log("No audio frames captured", "WARN")
        return {"error": "no_audio", "you_said": "", "response_text": "No audio recorded."}

    audio_bytes = b"".join(frames)
    log(f"Sending {len(audio_bytes):,} bytes "
        f"({len(frames) * CHUNK_SIZE / SEND_SAMPLE_RATE:.1f}s) to Gemini Live API...")

    client = genai.Client(
        api_key=GEMINI_API_KEY,
        http_options=gtypes.HttpOptions(api_version="v1alpha"),
    )

    system_instruction = (
        "You are a senior M&A voice analyst embedded in VDR Intelligence.\n"
        "Answer questions concisely and clearly based ONLY on the due diligence data below.\n"
        "Always respond in English. If asked something outside this data, say so briefly.\n\n"
        f"DUE DILIGENCE CONTEXT:\n{doc_context[:6000]}"
    )

    audio_chunks:  list[bytes] = []
    input_chunks:  list[str]   = []
    output_chunks: list[str]   = []
    text_parts:    list[str]   = []

    try:
        async with client.aio.live.connect(
            model=GEMINI_MODEL,
            config={
                "response_modalities":      ["AUDIO"],
                "input_audio_transcription":  {},
                "output_audio_transcription": {},
                "system_instruction":         system_instruction,
            },
        ) as session:
            log("Gemini Live session connected", "OK")
            await session.send_realtime_input(
                audio=gtypes.Blob(data=audio_bytes, mime_type="audio/pcm;rate=16000")
            )
            log("Audio sent — awaiting response...")

            async for response in session.receive():
                sc = response.server_content
                if not sc:
                    continue

                it = getattr(sc, "input_transcription", None)
                if it:
                    txt = getattr(it, "text", "") or ""
                    if txt:
                        input_chunks.append(txt)
                        log(f"  [YOU] {txt.strip()}")

                mt = getattr(sc, "model_turn", None)
                if mt:
                    for part in mt.parts or []:
                        if getattr(part, "inline_data", None):
                            audio_chunks.append(part.inline_data.data)
                        txt     = getattr(part, "text", "") or ""
                        thought = getattr(part, "thought", False)
                        if txt and not thought:
                            text_parts.append(txt)
                            log(f"  [TEXT PART] {txt.strip()[:80]}")

                ot = getattr(sc, "output_transcription", None)
                if ot:
                    txt = getattr(ot, "text", "") or ""
                    if txt:
                        output_chunks.append(txt)
                        log(f"  [GEMINI] {txt.strip()[:80]}")

                if getattr(sc, "turn_complete", False):
                    log(f"Turn complete — {len(audio_chunks)} audio chunks", "OK")
                    break

    except Exception as e:
        log(f"Gemini Live error: {e}", "ERR")
        return {
            "error":         str(e),
            "you_said":      "".join(input_chunks) or "(unclear)",
            "response_text": f"Error: {e}",
        }

    # ── Playback ──────────────────────────────────────────────────
    if audio_chunks:
        log(f"Playing audio ({len(audio_chunks)} chunks)...")
        out_stream = pya.open(
            format=FORMAT, channels=CHANNELS,
            rate=RECV_SAMPLE_RATE, output=True,
            output_device_index=OUTPUT_DEVICE,
        )
        for chunk in audio_chunks:
            out_stream.write(chunk)
        out_stream.stop_stream()
        out_stream.close()
        log("Playback complete", "OK")

    you_said      = re.sub(r"\s+", " ", "".join(input_chunks)).strip()  or "(unclear)"
    response_text = re.sub(r"\s+", " ", "".join(output_chunks)).strip() \
                    or " ".join(text_parts).strip()                      \
                    or "(audio response — no transcript)"

    log(f"YOU:    {you_said[:100]}")
    log(f"GEMINI: {response_text[:100]}")

    return {
        "you_said":      you_said,
        "response_text": response_text,
        "has_audio":     bool(audio_chunks),
    }
