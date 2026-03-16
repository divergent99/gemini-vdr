from dash import html
from frontend.styles import C, MONO, BEBAS, DM, score_bar, risk_tag, score_color, rec_label


def build_results_card(analysis: dict) -> html.Div:
    """
    Build the full analysis results panel from a Gemini analysis dict.
    Used by the run_analysis callback to populate #analysis-panel.
    """
    deal_score = analysis.get("deal_score", 50)
    scores     = analysis.get("scores", {})
    rec_txt, rec_col = rec_label(analysis.get("recommendation", "unknown"))
    top_risks  = analysis.get("top_risks", [])
    key_facts  = analysis.get("key_facts", [])
    exec_sum   = analysis.get("executive_summary", "")

    return html.Div([

        # Section header
        html.Div([
            html.Span("▸ ", style={"color": C["accent"]}),
            html.Span("ANALYSIS RESULTS", style={
                "fontFamily": MONO, "fontSize": "9px",
                "fontWeight": "700", "letterSpacing": "0.2em", "color": C["muted"],
            }),
        ], style={"marginBottom": "16px"}),

        # Deal score + recommendation hero row
        html.Div([
            html.Div([
                html.Div(str(deal_score), style={
                    "fontFamily": BEBAS, "fontSize": "56px",
                    "color": score_color(deal_score),
                    "lineHeight": "1", "letterSpacing": "0.02em",
                }),
                html.Div("DEAL SCORE", style={
                    "fontFamily": MONO, "fontSize": "8px",
                    "color": C["muted"], "letterSpacing": "0.15em",
                }),
            ], style={"textAlign": "center", "marginRight": "20px"}),
            html.Div([
                html.Div(rec_txt, style={
                    "fontFamily": BEBAS, "fontSize": "16px",
                    "color": rec_col, "letterSpacing": "0.05em", "marginBottom": "4px",
                }),
                html.Div(exec_sum[:180] + ("..." if len(exec_sum) > 180 else ""), style={
                    "fontFamily": DM, "fontSize": "11px",
                    "color": C["muted"], "lineHeight": "1.6",
                }),
            ], style={"flex": "1"}),
        ], style={
            "display": "flex", "alignItems": "center",
            "background": C["surf2"], "borderRadius": "10px",
            "padding": "14px", "marginBottom": "14px",
        }),

        # Score bars
        score_bar("FINANCIAL",  scores.get("financial",  50)),
        score_bar("LEGAL",      scores.get("legal",      50)),
        score_bar("COMPLIANCE", scores.get("compliance", 50)),

        # Top risks
        html.Div([
            html.Div("TOP RISKS", style={
                "fontFamily": MONO, "fontSize": "9px", "color": C["muted"],
                "letterSpacing": "0.15em", "marginBottom": "8px",
            }),
            *[html.Div([
                risk_tag(r.get("severity", "medium")),
                html.Span(r.get("risk", ""), style={
                    "fontFamily": DM, "fontSize": "11px", "color": C["text"],
                }),
            ], style={"marginBottom": "7px"}) for r in top_risks[:5]],
        ], style={"marginBottom": "14px"}),

        # Key facts
        html.Div([
            html.Div("KEY FACTS", style={
                "fontFamily": MONO, "fontSize": "9px", "color": C["muted"],
                "letterSpacing": "0.15em", "marginBottom": "8px",
            }),
            *[html.Div([
                html.Span("◆ ", style={"color": C["accent"]}),
                html.Span(f, style={
                    "fontFamily": MONO, "fontSize": "10px",
                    "color": C["text"], "lineHeight": "1.6",
                }),
            ], style={"marginBottom": "5px"}) for f in key_facts[:5]],
        ]),

    ])
