from dash_extensions.enrich import html, dcc

def render_main_layout() -> html.Div:
    """Рендер главной страницы"""

    return html.Div([
        dcc.Location(id="url", refresh=False),
        dcc.Location(id="redirect", refresh=True),
        html.Div(id="page-content"),
    ])
