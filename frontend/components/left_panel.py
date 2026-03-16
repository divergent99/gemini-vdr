from dash import dcc, html
from frontend.styles import C, MONO, DM, BEBAS


def left_panel() -> html.Div:
    """VDR input panel — folder path / file upload toggle + analyse button."""
    file_icons = {"pdf": "📄", "docx": "📝", "xlsx": "📊", "xls": "📊"}

    return html.Div([

        # ── Input card ────────────────────────────────────────────
        html.Div([
            html.Div([
                html.Span("▸ ", style={"color": C["accent"]}),
                html.Span("VIRTUAL DATA ROOM", style={
                    "fontFamily": MONO, "fontSize": "9px",
                    "fontWeight": "700", "letterSpacing": "0.2em", "color": C["muted"],
                }),
            ], style={"marginBottom": "14px"}),

            # Mode toggle buttons
            html.Div([
                html.Button("FOLDER PATH", id="mode-folder-btn", n_clicks=0, style={
                    "flex": "1", "padding": "7px", "border": "none",
                    "borderRadius": "7px 0 0 7px",
                    "background": C["accent"], "color": "#07070f",
                    "fontFamily": MONO, "fontSize": "9px",
                    "letterSpacing": "0.1em", "cursor": "pointer", "fontWeight": "700",
                }),
                html.Button("FILE UPLOAD", id="mode-upload-btn", n_clicks=0, style={
                    "flex": "1", "padding": "7px", "border": "none",
                    "borderRadius": "0 7px 7px 0",
                    "background": C["border"], "color": C["muted"],
                    "fontFamily": MONO, "fontSize": "9px",
                    "letterSpacing": "0.1em", "cursor": "pointer", "fontWeight": "700",
                }),
            ], style={"display": "flex", "marginBottom": "12px"}),

            # Folder path input (default visible)
            html.Div([
                html.Div("FOLDER PATH", style={
                    "fontFamily": MONO, "fontSize": "9px",
                    "color": C["muted"], "letterSpacing": "0.12em", "marginBottom": "6px",
                }),
                dcc.Input(
                    id="folder-path-input", type="text",
                    placeholder="C:\\Users\\...\\Hackathon_VDR",
                    debounce=False,
                ),
                html.Div(id="folder-scan-info", style={"marginTop": "6px"}),
            ], id="folder-input-panel"),

            # File upload (hidden by default)
            html.Div([
                dcc.Upload(
                    id="upload-docs", multiple=True,
                    children=html.Div([
                        html.Div("⬆", style={"fontSize": "22px", "color": C["accent"], "marginBottom": "4px"}),
                        html.Div("Drop M&A Documents", style={
                            "fontFamily": DM, "fontWeight": "600",
                            "fontSize": "13px", "color": C["text"],
                        }),
                        html.Div("PDF · DOCX · XLSX", style={
                            "fontFamily": MONO, "fontSize": "9px",
                            "color": C["muted"], "letterSpacing": "0.1em",
                        }),
                    ], style={"textAlign": "center", "padding": "2px"}),
                    style={
                        "border": f"1.5px dashed {C['accent']}44",
                        "borderRadius": "10px", "padding": "18px 12px",
                        "cursor": "pointer", "background": "rgba(108,99,255,0.04)",
                    },
                ),
                html.Div(id="file-list", style={"marginTop": "8px"}),
            ], id="upload-input-panel", style={"display": "none"}),

            # Analyse button
            html.Button(
                [html.Span("◈  "), "ANALYSE DOCUMENTS"],
                id="analyse-btn", n_clicks=0,
                style={
                    "width": "100%",
                    "background": f"linear-gradient(135deg,{C['accent']},{C['cyan']})",
                    "border": "none", "borderRadius": "10px", "padding": "12px",
                    "color": "#07070f", "fontFamily": BEBAS, "fontSize": "15px",
                    "letterSpacing": "0.1em", "cursor": "pointer", "marginTop": "12px",
                },
            ),
            html.Div(id="analyse-status", style={"marginTop": "8px"}),

        ], style={
            "background": C["surf"], "border": f"1px solid {C['border']}",
            "borderRadius": "14px", "padding": "18px 20px", "marginBottom": "14px",
        }),

        # ── Analysis results card (populated by callback) ─────────
        html.Div(
            id="analysis-panel",
            style={
                "background": C["surf"], "border": f"1px solid {C['border']}",
                "borderRadius": "14px", "padding": "18px 20px", "display": "none",
            },
        ),

    ], style={"width": "360px", "flexShrink": "0"})
