"""
Voice callbacks — call voice_state directly (same process as FastAPI).
No httpx needed for voice operations.
"""
import json
from dash import Input, Output, State, no_update, html

from frontend.styles import C, MONO
from backend.services.voice_agent import (
    voice_state,
    start_recording,
    stop_recording_and_query,
)

WAVEFORM_ON  = {"display": "flex", "alignItems": "flex-end", "justifyContent": "center",
                "height": "24px", "marginBottom": "16px", "opacity": "1"}
WAVEFORM_OFF = {**WAVEFORM_ON, "opacity": "0"}


def _build_bubbles(history: list) -> list:
    bubbles = []
    for turn in history:
        bubbles.append(html.Div([
            html.Div("YOU", style={"fontFamily": MONO, "fontSize": "9px",
                "color": C["accent"], "letterSpacing": "0.15em", "marginBottom": "4px"}),
            html.Div(turn["you"], style={"fontFamily": MONO, "fontSize": "11px",
                "color": C["text"], "lineHeight": "1.6"}),
        ], className="chat-bubble", style={
            "background": "rgba(108,99,255,0.08)",
            "border": "1px solid rgba(108,99,255,0.2)",
            "borderRadius": "10px", "padding": "10px 13px", "alignSelf": "flex-end",
        }))
        bubbles.append(html.Div([
            html.Div("GEMINI", style={"fontFamily": MONO, "fontSize": "9px",
                "color": C["cyan"], "letterSpacing": "0.15em", "marginBottom": "4px"}),
            html.Div(turn["gemini"], style={"fontFamily": MONO, "fontSize": "11px",
                "color": C["text"], "lineHeight": "1.7"}),
        ], className="chat-bubble", style={
            "background": C["surf2"], "border": f"1px solid {C['border']}",
            "borderRadius": "10px", "padding": "10px 13px",
        }))
    return bubbles


def register(app):

    # ── Mic button: start / stop ──────────────────────────────────
    @app.callback(
        Output("recording-state",           "data"),
        Output("processing-state",          "data"),
        Output("record-ticker",             "disabled"),
        Output("result-poller",             "disabled"),
        Output("mic-btn",                   "className"),
        Output("mic-label",                 "children"),
        Output("waveform-display",          "style"),
        Output("voice-status",              "children"),
        Output("chat-display", "children",  allow_duplicate=True),
        Input("mic-btn",                    "n_clicks"),
        State("recording-state",            "data"),
        State("processing-state",           "data"),
        State("doc-text-store",             "data"),
        State("chat-history-store",         "data"),
        prevent_initial_call=True,
    )
    def toggle_mic(n, is_recording, is_processing, doc_store_json, history):
        if is_processing:
            return (no_update,) * 9

        if not is_recording:
            # ── START ────────────────────────────────────────────
            start_recording()
            return (True, False, False, True,
                    "mic-btn recording", "RECORDING — click to stop",
                    WAVEFORM_ON, "Listening...", no_update)

        else:
            # ── STOP ─────────────────────────────────────────────
            doc_context = ""
            if doc_store_json:
                try:
                    stored      = json.loads(doc_store_json)
                    analysis    = stored.get("analysis", {})
                    doc_text    = stored.get("doc_text", "")
                    doc_context = (
                        f"ANALYSIS:\n{json.dumps(analysis)[:2000]}"
                        f"\n\nDOCUMENTS:\n{doc_text[:2000]}"
                    )
                except Exception:
                    pass

            stop_recording_and_query(doc_context)

            bubbles = _build_bubbles(history)
            bubbles.append(html.Div([
                html.Div("GEMINI", style={"fontFamily": MONO, "fontSize": "9px",
                    "color": C["cyan"], "letterSpacing": "0.15em", "marginBottom": "6px"}),
                html.Div([
                    html.Span(className="typing-dot"),
                    html.Span(className="typing-dot"),
                    html.Span(className="typing-dot"),
                ], style={"display": "flex", "alignItems": "center", "height": "20px"}),
            ], style={
                "background": C["surf2"], "border": f"1px solid {C['border']}",
                "borderRadius": "10px", "padding": "10px 13px",
            }))

            return (False, True, True, False,
                    "mic-btn processing", "Processing...",
                    WAVEFORM_OFF, "Sending to Gemini...", bubbles)


    # ── Poller: check voice_state directly ────────────────────────
    @app.callback(
        Output("chat-display",        "children",  allow_duplicate=True),
        Output("chat-history-store",  "data"),
        Output("processing-state",    "data",      allow_duplicate=True),
        Output("mic-btn",             "className", allow_duplicate=True),
        Output("mic-label",           "children",  allow_duplicate=True),
        Output("voice-status",        "children",  allow_duplicate=True),
        Input("result-poller",        "n_intervals"),
        State("processing-state",     "data"),
        State("chat-history-store",   "data"),
        prevent_initial_call=True,
    )
    def poll_result(n, is_processing, history):
        if not is_processing:
            return (no_update,) * 6

        # Direct in-process check — no httpx, no network
        if not voice_state.result_ready.is_set():
            return (no_update,) * 6

        result = voice_state.last_result or {}
        voice_state.result_ready.clear()
        voice_state.last_result = None

        you_said      = result.get("you_said", "(unclear)")
        response_text = result.get("response_text", "(no response)")
        error         = result.get("error", "")

        new_history = list(history) + [{"you": you_said, "gemini": response_text}]
        bubbles     = _build_bubbles(new_history)
        status_col  = C["low"] if not error else C["critical"]
        status_msg  = (
            f"✓ Response received{' · audio played' if result.get('has_audio') else ''}"
            if not error else f"✕ {error}"
        )

        return (
            bubbles,
            new_history,
            False,   # processing done — gates poller
            "mic-btn",
            "READY — click to speak",
            html.Span(status_msg, style={"color": status_col}),
        )
