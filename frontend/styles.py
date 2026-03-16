from dash import html

# ── Fonts ─────────────────────────────────────────────────────────
MONO  = "'JetBrains Mono',monospace"
BEBAS = "'Bebas Neue',sans-serif"
DM    = "'DM Sans',sans-serif"

# ── Colour aliases (all reference CSS custom properties) ──────────
C = {
    "bg":       "var(--bg)",
    "surf":     "var(--surf)",
    "surf2":    "var(--surf2)",
    "border":   "var(--border)",
    "accent":   "var(--accent)",
    "cyan":     "var(--cyan)",
    "text":     "var(--text)",
    "muted":    "var(--muted)",
    "critical": "var(--critical)",
    "high":     "var(--high)",
    "medium":   "var(--medium)",
    "low":      "var(--low)",
    "red":      "var(--critical)",
    "green":    "var(--low)",
}

# ── index_string: full HTML shell with CSS + theme JS ─────────────
INDEX_STRING = """<!DOCTYPE html><html data-theme="dark"><head>{%metas%}<title>{%title%}</title>{%favicon%}{%css%}
<style>
/* ── THEME VARIABLES ── */
:root,[data-theme="dark"]{
  --bg:#07070f;--surf:#0d0d1a;--surf2:#13132a;--border:#1c1c3a;
  --text:#e8e8f8;--muted:#5a5a7a;--accent:#6c63ff;--cyan:#00e5cc;
  --critical:#ff3b5c;--high:#ff8c42;--medium:#ffd166;--low:#06d6a0;
  --shadow:0 2px 12px rgba(0,0,0,0.4);
  --input-placeholder:#2a2a4a;
}
[data-theme="light"]{
  --bg:#f0f2f8;--surf:#ffffff;--surf2:#e8eaf4;--border:#d0d4e8;
  --text:#0d0d2b;--muted:#4a4a6a;--accent:#5046e5;--cyan:#0088aa;
  --critical:#cc1133;--high:#c05800;--medium:#8a6000;--low:#007a55;
  --shadow:0 2px 12px rgba(0,0,0,0.10);
  --input-placeholder:#9090b0;
}

*{box-sizing:border-box;margin:0;padding:0}
body{background:var(--bg);color:var(--text);font-family:'DM Sans',sans-serif;overflow-x:hidden;transition:background .2s,color .2s}
::-webkit-scrollbar{width:4px}
::-webkit-scrollbar-track{background:var(--surf)}
::-webkit-scrollbar-thumb{background:var(--accent);opacity:0.4;border-radius:2px}

.t-bg    {background:var(--bg)!important}
.t-surf  {background:var(--surf)!important}
.t-surf2 {background:var(--surf2)!important}
.t-card  {background:var(--surf)!important;border:1px solid var(--border)!important;border-radius:14px!important;padding:18px 20px!important;box-shadow:var(--shadow)!important;transition:background .2s,border .2s}
.t-card2 {background:var(--surf2)!important;border:1px solid var(--border)!important;border-radius:10px!important;padding:12px 14px!important;transition:background .2s,border .2s}
.t-header{background:var(--surf)!important;border-bottom:1px solid var(--border)!important;transition:background .2s,border .2s}
.t-sec   {font-family:'JetBrains Mono',monospace;font-size:9px;font-weight:700;letter-spacing:0.2em;text-transform:uppercase;color:var(--muted)!important}
.t-label {font-family:'JetBrains Mono',monospace;font-size:9px;letter-spacing:0.12em;color:var(--muted)!important}
.t-text  {color:var(--text)!important}
.t-muted {color:var(--muted)!important}
.t-accent{color:var(--accent)!important}
.t-cyan  {color:var(--cyan)!important}
.t-border{border-color:var(--border)!important}
.t-divider{border-top:1px solid var(--border)!important}

.t-btn-mode-active  {background:var(--accent)!important;color:#fff!important;border:none!important}
.t-btn-mode-inactive{background:var(--border)!important;color:var(--muted)!important;border:none!important}
.t-btn-run{background:linear-gradient(135deg,var(--accent),var(--cyan))!important;border:none!important;color:#07070f!important;border-radius:10px!important;padding:12px!important;width:100%!important;font-family:'Bebas Neue',sans-serif!important;font-size:16px!important;letter-spacing:0.1em!important;cursor:pointer!important;transition:filter .15s!important}
.t-btn-run:hover{filter:brightness(1.1)!important}
.t-btn-theme{background:rgba(108,99,255,0.12)!important;border:1px solid rgba(108,99,255,0.3)!important;border-radius:6px!important;padding:4px 10px!important;color:var(--accent)!important;font-family:'JetBrains Mono',monospace!important;font-size:9px!important;letter-spacing:0.14em!important;cursor:pointer!important}

.t-upload{border:1.5px dashed var(--accent)!important;border-opacity:0.4!important;border-radius:10px!important;background:transparent!important}
.t-file  {background:var(--bg)!important;border:1px solid var(--border)!important;border-radius:6px!important}
.t-bubble-you {background:color-mix(in srgb,var(--accent) 12%,transparent)!important;border:1px solid color-mix(in srgb,var(--accent) 33%,transparent)!important;border-radius:10px!important;padding:10px 13px!important}
.t-bubble-gem {background:var(--surf2)!important;border:1px solid var(--border)!important;border-radius:10px!important;padding:10px 13px!important}
.t-score-row  {background:var(--surf2)!important;border-radius:10px!important;padding:14px!important}

@keyframes spin{to{transform:rotate(360deg)}}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:.2}}
@keyframes fadein{from{opacity:0;transform:translateY(8px)}to{opacity:1;transform:translateY(0)}}
@keyframes stepin{from{opacity:0;transform:translateX(-16px)}to{opacity:1;transform:translateX(0)}}
@keyframes waveform{0%,100%{height:4px}50%{height:20px}}
@keyframes glow-pulse{0%,100%{box-shadow:0 0 20px rgba(108,99,255,0.3)}50%{box-shadow:0 0 40px rgba(108,99,255,0.7),0 0 60px rgba(0,229,204,0.3)}}
@keyframes pulse-ring{0%{transform:scale(0.9);opacity:1}70%{transform:scale(1.4);opacity:0}100%{transform:scale(1.4);opacity:0}}

.spinner{width:50px;height:50px;border:2px solid var(--border);border-top:2px solid var(--accent);
  border-right:2px solid var(--cyan);border-radius:50%;animation:spin .75s linear infinite;margin:0 auto 18px}
.pulse{animation:pulse 2s ease infinite}
.stepin{animation:stepin .4s ease forwards;opacity:0}
.stepin:nth-child(1){animation-delay:.1s}.stepin:nth-child(2){animation-delay:.5s}
.stepin:nth-child(3){animation-delay:.9s}.stepin:nth-child(4){animation-delay:1.3s}

.mic-btn{width:80px;height:80px;border-radius:50%;border:none;cursor:pointer;
  background:linear-gradient(135deg,var(--accent),var(--cyan));
  display:flex;align-items:center;justify-content:center;font-size:28px;
  transition:all .2s;position:relative;box-shadow:0 4px 20px rgba(108,99,255,0.4)}
.mic-btn:hover{transform:scale(1.05);box-shadow:0 6px 28px rgba(108,99,255,0.6)}
.mic-btn.recording{background:linear-gradient(135deg,#ff3b5c,#ff8c42);animation:glow-pulse 1.5s ease infinite}
.mic-btn.recording::before{content:'';position:absolute;width:100%;height:100%;border-radius:50%;
  border:2px solid rgba(255,59,92,0.6);animation:pulse-ring 1.5s ease infinite}
.mic-btn.processing{background:linear-gradient(135deg,var(--border),var(--surf2));cursor:not-allowed;opacity:0.7}

.wave-bar{display:inline-block;width:3px;border-radius:2px;
  background:linear-gradient(to top,var(--accent),var(--cyan));
  animation:waveform 0.6s ease infinite;margin:0 1px}
.wave-bar:nth-child(2){animation-delay:.1s;height:8px}.wave-bar:nth-child(3){animation-delay:.2s;height:12px}
.wave-bar:nth-child(4){animation-delay:.3s;height:6px}.wave-bar:nth-child(5){animation-delay:.4s;height:14px}
.wave-bar:nth-child(6){animation-delay:.15s;height:9px}.wave-bar:nth-child(7){animation-delay:.25s;height:5px}

.chat-bubble{animation:fadein .3s ease forwards}
.score-bar-fill{transition:width 1s cubic-bezier(0.4,0,0.2,1)}

.typing-dot{display:inline-block;width:6px;height:6px;border-radius:50%;
  background:var(--cyan);margin:0 2px;animation:typing-bounce .9s infinite ease-in-out}
.typing-dot:nth-child(2){animation-delay:.2s}.typing-dot:nth-child(3){animation-delay:.4s}
@keyframes typing-bounce{0%,80%,100%{transform:translateY(0);opacity:.4}40%{transform:translateY(-5px);opacity:1}}

input,input:focus{
  background:var(--bg)!important;color:var(--text)!important;
  border:1px solid var(--border)!important;border-radius:8px!important;
  padding:9px 12px!important;font-family:'JetBrains Mono',monospace!important;
  font-size:11px!important;width:100%!important;outline:none!important;
  transition:background .2s,color .2s,border .2s!important}
input::placeholder{color:var(--input-placeholder)!important}
input:focus{border-color:color-mix(in srgb,var(--accent) 40%,transparent)!important}

.risk-tag{display:inline-block;padding:2px 8px;border-radius:4px;
  font-family:'JetBrains Mono',monospace;font-size:9px;font-weight:700;
  letter-spacing:0.14em;text-transform:uppercase;margin-right:6px}
</style>
<script>
function setTheme(t){
  document.documentElement.setAttribute('data-theme',t);
  var btn=document.getElementById('theme-toggle');
  if(btn) btn.textContent = t==='dark' ? '☀ LIGHT' : '🌙 DARK';
}
</script>
</head><body>{%app_entry%}<footer>{%config%}{%scripts%}{%renderer%}</footer></body></html>"""


# ── Helper functions ──────────────────────────────────────────────
def score_color(s: int) -> str:
    if s >= 75: return "var(--low)"
    if s >= 50: return "var(--medium)"
    if s >= 25: return "var(--high)"
    return "var(--critical)"


def rec_label(r: str) -> tuple[str, str]:
    return {
        "proceed":                 ("PROCEED",               "var(--low)"),
        "proceed_with_conditions": ("PROCEED W/ CONDITIONS", "var(--medium)"),
        "do_not_proceed":          ("DO NOT PROCEED",        "var(--critical)"),
    }.get(r, ("UNKNOWN", "var(--muted)"))


def score_bar(label: str, score: int):
    col = score_color(score)
    return html.Div([
        html.Div([
            html.Span(label, style={"fontFamily": MONO, "fontSize": "9px",
                "color": C["muted"], "letterSpacing": "0.12em"}),
            html.Span(str(score), style={"fontFamily": BEBAS, "fontSize": "18px", "color": col}),
        ], style={"display": "flex", "justifyContent": "space-between",
                  "alignItems": "center", "marginBottom": "4px"}),
        html.Div(
            html.Div(className="score-bar-fill", style={
                "height": "100%", "width": f"{score}%",
                "background": col, "borderRadius": "3px",
            }),
            style={"height": "6px", "background": C["border"],
                   "borderRadius": "3px", "overflow": "hidden"},
        ),
    ], style={"marginBottom": "12px"})


def risk_tag(severity: str):
    col_map = {
        "critical": ("var(--critical)", "rgba(255,59,92,0.1)",   "rgba(255,59,92,0.27)"),
        "high":     ("var(--high)",     "rgba(255,140,66,0.1)",  "rgba(255,140,66,0.27)"),
        "medium":   ("var(--medium)",   "rgba(255,209,102,0.1)", "rgba(255,209,102,0.27)"),
        "low":      ("var(--low)",      "rgba(6,214,160,0.1)",   "rgba(6,214,160,0.27)"),
    }
    col, bg, border = col_map.get(
        severity.lower(),
        ("var(--muted)", "rgba(90,90,122,0.1)", "rgba(90,90,122,0.27)"),
    )
    return html.Span(severity.upper(), className="risk-tag",
        style={"color": col, "background": bg, "border": f"1px solid {border}"})
