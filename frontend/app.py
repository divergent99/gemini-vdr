from dash import Dash, dcc, html
import dash_bootstrap_components as dbc

from frontend.styles   import C, MONO, BEBAS, INDEX_STRING
from frontend.components.left_panel  import left_panel
from frontend.components.right_panel import right_panel
from frontend.callbacks import analysis_cb, voice_cb, theme_cb

# ── App init ──────────────────────────────────────────────────────
dash_app = Dash(
    __name__,
    requests_pathname_prefix="/",
    external_stylesheets=[
        dbc.themes.BOOTSTRAP,
        "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700"
        "&family=Bebas+Neue&family=DM+Sans:wght@300;400;500;600&display=swap",
    ],
    suppress_callback_exceptions=True,
    title="VDR Voice Intelligence",
)

dash_app.index_string = INDEX_STRING

# ── Layout ────────────────────────────────────────────────────────
dash_app.layout = html.Div([

    dcc.Store(id="doc-text-store",      data=""),
    dcc.Store(id="analysis-store",      data=None),
    dcc.Store(id="chat-history-store",  data=[]),
    dcc.Store(id="recording-state",     data=False),
    dcc.Store(id="processing-state",    data=False),
    dcc.Store(id="input-mode",          data="folder"),
    dcc.Store(id="theme-store",         data="dark"),
    dcc.Interval(id="record-ticker",    interval=50,   disabled=True),
    dcc.Interval(id="result-poller",    interval=1000, disabled=False),

    # ── Header ────────────────────────────────────────────────────
    html.Div([
        html.Div([
            html.Div([
                html.Span("VDR ", style={"fontFamily": BEBAS, "fontSize": "22px",
                    "color": C["accent"], "letterSpacing": "0.06em"}),
                html.Span("VOICE", style={"fontFamily": BEBAS, "fontSize": "22px",
                    "color": C["cyan"], "letterSpacing": "0.06em"}),
                html.Div("GEMINI LIVE · M&A DUE DILIGENCE VOICE AGENT", style={
                    "fontFamily": MONO, "fontSize": "8px",
                    "letterSpacing": "0.2em", "color": C["muted"],
                }),
            ]),
            html.Div([
                html.Span("Gemini Live Agent Challenge 2026", style={
                    "fontFamily": MONO, "fontSize": "9px", "color": C["muted"]}),
                html.Span(" · ", style={"color": C["border"], "margin": "0 6px"}),
                html.Span("gemini-2.5-flash-native-audio", style={
                    "fontFamily": MONO, "fontSize": "9px", "color": C["cyan"]}),
                html.Span(" · ", style={"color": C["border"], "margin": "0 6px"}),
                html.Button("☀ LIGHT", id="theme-toggle", n_clicks=0, style={
                    "background": "rgba(108,99,255,0.12)",
                    "border": "1px solid rgba(108,99,255,0.3)",
                    "borderRadius": "6px", "padding": "4px 10px",
                    "color": C["accent"], "fontFamily": MONO,
                    "fontSize": "9px", "letterSpacing": "0.14em", "cursor": "pointer",
                }),
            ], style={"display": "flex", "alignItems": "center"}),
        ], style={
            "display": "flex", "justifyContent": "space-between", "alignItems": "center",
            "maxWidth": "1400px", "margin": "0 auto", "padding": "0 24px",
        }),
    ], id="app-header", style={
        "background": C["surf"], "borderBottom": f"1px solid {C['border']}",
        "padding": "12px 0", "position": "sticky", "top": "0", "zIndex": "100",
    }),

    # ── Main ──────────────────────────────────────────────────────
    html.Div([
        left_panel(),
        right_panel(),
    ], style={
        "display": "flex", "gap": "18px", "padding": "20px 24px",
        "maxWidth": "1400px", "margin": "0 auto", "alignItems": "flex-start",
    }),

], style={"background": C["bg"], "minHeight": "100vh"})

# ── Register callbacks ────────────────────────────────────────────
analysis_cb.register(dash_app)
voice_cb.register(dash_app)
theme_cb.register(dash_app)

# Flask WSGI server — mounted into FastAPI via WSGIMiddleware
server = dash_app.server
