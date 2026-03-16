from dash import html
from frontend.styles import C, MONO, BEBAS, DM


def right_panel() -> html.Div:
    """Loading screen + mic button + voice transcript panel."""
    return html.Div([

        # ── OG-style loading screen (hidden until analysis fires) ──
        html.Div([
            html.Div(className="spinner"),
            html.Div("ANALYSING DOCUMENTS", className="pulse", style={
                "fontFamily": BEBAS, "fontSize": "26px", "color": C["text"],
                "textAlign": "center", "letterSpacing": "0.1em", "marginBottom": "4px",
            }),
            html.Div("GEMINI FLASH · MULTI-DOMAIN ANALYSIS", style={
                "fontFamily": MONO, "fontSize": "9px", "color": C["cyan"],
                "textAlign": "center", "letterSpacing": "0.18em", "marginBottom": "28px",
            }),
            html.Div([
                *[html.Div([
                    html.Span(ic + "  ", style={"color": bc}),
                    html.Span(tx, style={"fontFamily": MONO, "fontSize": "11px", "color": C["text"]}),
                ], className="stepin", style={
                    "background": C["surf2"], "border": f"1px solid {bc}33",
                    "borderRadius": "8px", "padding": "10px 16px",
                    "marginBottom": "9px", "textAlign": "center",
                })
                for ic, bc, tx in [
                    ("📊", C["cyan"],   "Financial Health Analysis"),
                    ("🚩", C["high"],   "Contract Red Flag Detection"),
                    ("⚖",  C["medium"], "Regulatory Compliance Check"),
                    ("📝", C["accent"], "Synthesis & Report Generation"),
                ]],
            ], style={"maxWidth": "340px", "margin": "0 auto"}),
        ], id="loading-screen", style={"display": "none", "paddingTop": "80px"}),

        # ── Voice panel ───────────────────────────────────────────
        html.Div([

            # Mic button section
            html.Div([
                html.Div([
                    html.Span("▸ ", style={"color": C["accent"]}),
                    html.Span("VOICE INTERFACE", style={
                        "fontFamily": MONO, "fontSize": "9px",
                        "fontWeight": "700", "letterSpacing": "0.2em", "color": C["muted"],
                    }),
                ], style={"marginBottom": "20px"}),

                html.Div([
                    html.Button("🎤", id="mic-btn", n_clicks=0, className="mic-btn",
                        title="Click to start/stop recording"),
                    html.Div(id="mic-label", style={
                        "fontFamily": MONO, "fontSize": "10px", "color": C["muted"],
                        "textAlign": "center", "marginTop": "10px", "letterSpacing": "0.12em",
                    }),
                ], style={
                    "display": "flex", "flexDirection": "column",
                    "alignItems": "center", "marginBottom": "20px",
                }),

                html.Div([
                    *[html.Span(className="wave-bar", style={"height": "4px"}) for _ in range(7)]
                ], id="waveform-display", style={
                    "display": "flex", "alignItems": "flex-end", "justifyContent": "center",
                    "height": "24px", "marginBottom": "16px", "opacity": "0",
                }),

                html.Div(id="voice-status", style={
                    "fontFamily": MONO, "fontSize": "10px", "color": C["muted"],
                    "textAlign": "center", "minHeight": "18px",
                }),

            ], style={
                "display": "flex", "flexDirection": "column", "alignItems": "center",
                "borderBottom": f"1px solid {C['border']}",
                "paddingBottom": "20px", "marginBottom": "20px",
            }),

            # Conversation transcript
            html.Div([
                html.Div("▸ CONVERSATION", style={
                    "fontFamily": MONO, "fontSize": "9px",
                    "fontWeight": "700", "letterSpacing": "0.2em",
                    "color": C["muted"], "marginBottom": "14px",
                }),
                html.Div(
                    id="chat-display",
                    style={
                        "display": "flex", "flexDirection": "column",
                        "gap": "10px", "minHeight": "200px",
                    },
                    children=[
                        html.Div([
                            html.Div("GEMINI", style={
                                "fontFamily": MONO, "fontSize": "9px",
                                "color": C["cyan"], "letterSpacing": "0.15em",
                                "marginBottom": "4px",
                            }),
                            html.Div(
                                "Run document analysis first, then click the mic button to ask questions about the deal.",
                                style={"fontFamily": MONO, "fontSize": "11px",
                                       "color": C["muted"], "lineHeight": "1.7"},
                            ),
                        ], style={
                            "background": C["surf2"], "border": f"1px solid {C['border']}",
                            "borderRadius": "10px", "padding": "12px 14px",
                        }),
                    ],
                ),
            ]),

        ], id="voice-panel", style={
            "background": C["surf"], "border": f"1px solid {C['border']}",
            "borderRadius": "14px", "padding": "20px 22px",
        }),

    ], style={"flex": "1", "minWidth": "0"})
