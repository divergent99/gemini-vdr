"""
Analysis callbacks — call backend services directly (same process).
"""
import json
from dash import Input, Output, State, no_update, ctx, html

from frontend.styles import C, MONO, BEBAS, DM
from frontend.components.results_card import build_results_card
from backend.services.extractor import extract_from_folder, extract_from_uploads, scan_folder
from backend.services.analyser  import run_analysis, last_meta


def register(app):

    # ── Mode toggle ───────────────────────────────────────────────
    @app.callback(
        Output("input-mode",          "data"),
        Output("folder-input-panel",  "style"),
        Output("upload-input-panel",  "style"),
        Output("mode-folder-btn",     "style"),
        Output("mode-upload-btn",     "style"),
        Input("mode-folder-btn",  "n_clicks"),
        Input("mode-upload-btn",  "n_clicks"),
        prevent_initial_call=True,
    )
    def toggle_mode(f_clicks, u_clicks):
        triggered = ctx.triggered_id
        is_folder = triggered == "mode-folder-btn"
        base = {"flex": "1", "padding": "7px", "border": "none",
                "fontFamily": MONO, "fontSize": "9px",
                "letterSpacing": "0.1em", "cursor": "pointer", "fontWeight": "700"}
        active   = {**base, "background": C["accent"], "color": "#07070f",
                    "borderRadius": "7px 0 0 7px" if is_folder else "0 7px 7px 0"}
        inactive = {**base, "background": C["border"], "color": C["muted"],
                    "borderRadius": "0 7px 7px 0" if is_folder else "7px 0 0 7px"}
        if is_folder:
            return "folder", {"display": "block"}, {"display": "none"}, active, inactive
        return "upload", {"display": "none"}, {"display": "block"}, inactive, active


    # ── Folder scan preview ───────────────────────────────────────
    @app.callback(
        Output("folder-scan-info", "children"),
        Input("folder-path-input", "value"),
        prevent_initial_call=True,
    )
    def scan_folder_preview(path):
        if not path or len(path) < 3:
            return html.Div()
        files = scan_folder(path)
        if not files:
            return html.Div("⚠ No PDF/DOCX/XLSX files found", style={
                "fontFamily": MONO, "fontSize": "10px", "color": C["medium"]})
        icons = {"pdf": "📄", "docx": "📝", "xlsx": "📊", "xls": "📊"}
        return html.Div([
            html.Div(f"✓ {len(files)} document(s) found", style={
                "fontFamily": MONO, "fontSize": "10px",
                "color": C["low"], "marginBottom": "6px"}),
            *[html.Div([
                html.Span(icons.get(f.split(".")[-1].lower(), "📁") + "  "),
                html.Span(f, style={"fontFamily": MONO, "fontSize": "10px", "color": C["text"]}),
            ], style={"background": C["bg"], "border": f"1px solid {C['border']}",
                      "borderRadius": "6px", "padding": "4px 10px", "marginBottom": "3px"})
            for f in files],
        ])


    # ── Upload file list ──────────────────────────────────────────
    @app.callback(
        Output("file-list", "children"),
        Input("upload-docs", "filename"),
    )
    def show_files(fns):
        if not fns:
            return html.Div()
        icons = {"pdf": "📄", "docx": "📝", "xlsx": "📊", "xls": "📊"}
        return html.Div([html.Div([
            html.Span(icons.get(f.split(".")[-1].lower(), "📁") + "  "),
            html.Span(f, style={"fontFamily": MONO, "fontSize": "10px", "color": C["text"]}),
        ], style={"background": C["bg"], "border": f"1px solid {C['border']}",
                  "borderRadius": "6px", "padding": "5px 10px", "marginBottom": "4px"})
        for f in fns])


    # ── Show loading screen on button click ───────────────────────
    @app.callback(
        Output("loading-screen", "style", allow_duplicate=True),
        Input("analyse-btn", "n_clicks"),
        prevent_initial_call=True,
    )
    def show_loading(n):
        if not n:
            return no_update
        return {"display": "block", "paddingTop": "80px"}


    # ── Run analysis ──────────────────────────────────────────────
    @app.callback(
        Output("doc-text-store",    "data"),
        Output("analysis-store",    "data"),
        Output("analyse-status",    "children"),
        Output("analysis-panel",    "children"),
        Output("analysis-panel",    "style"),
        Output("loading-screen",    "style"),
        Input("analyse-btn",        "n_clicks"),
        State("input-mode",         "data"),
        State("folder-path-input",  "value"),
        State("upload-docs",        "contents"),
        State("upload-docs",        "filename"),
        prevent_initial_call=True,
    )
    def run_analysis_cb(n, mode, folder_path, contents, filenames):
        if not n:
            return no_update, no_update, no_update, no_update, no_update, no_update

        panel_style = {
            "background": C["surf"], "border": f"1px solid {C['border']}",
            "borderRadius": "14px", "padding": "18px 20px", "display": "block",
        }
        hide_loading = {"display": "none"}

        def _err(msg):
            return (no_update, no_update,
                    html.Div(f"✕ {msg}", style={"fontFamily": MONO, "fontSize": "11px",
                                                "color": C["critical"]}),
                    no_update, no_update, hide_loading)

        try:
            if mode == "folder":
                if not folder_path or not folder_path.strip():
                    return _err("Enter a folder path first.")
                doc_text, files = extract_from_folder(folder_path)
                file_count = len(files)
            else:
                if not contents:
                    return _err("Upload documents first.")
                doc_text   = extract_from_uploads(contents, filenames)
                file_count = len(filenames)

            analysis   = run_analysis(doc_text, folder_path=folder_path or "")
            meta       = last_meta()
            from_cache = meta["from_cache"]
            elapsed    = meta["elapsed"]
            cache_label = " · ⚡ cached" if from_cache else (f" · {elapsed:.0f}s" if elapsed else "")

            status = html.Div([
                html.Span("✓ ", style={"color": "var(--low)"}),
                html.Span(f"Analysis complete · {file_count} doc(s){cache_label}",
                    style={"fontFamily": MONO, "fontSize": "11px", "color": "var(--low)"}),
            ])

            store = json.dumps({"doc_text": doc_text, "analysis": analysis})
            return store, analysis, status, build_results_card(analysis), panel_style, hide_loading

        except Exception as e:
            return _err(str(e))
