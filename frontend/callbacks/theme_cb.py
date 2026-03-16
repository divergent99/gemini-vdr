from dash import Output, Input, State


def register(app):
    app.clientside_callback(
        """
        function(n, current) {
            if (!n) return window.dash_clientside.no_update;
            var newTheme = (current === 'dark') ? 'light' : 'dark';
            setTheme(newTheme);
            return newTheme;
        }
        """,
        Output("theme-store",       "data"),
        Input("theme-toggle",       "n_clicks"),
        State("theme-store",        "data"),
        prevent_initial_call=True,
    )
