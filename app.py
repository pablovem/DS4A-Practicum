import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State

from lib import header, stats_pac

app = dash.Dash(
    __name__, 
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    suppress_callback_exceptions=True
)

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        header.header,
        html.Div(id="report",className="row")
    ],
    id="report-container",
)

index_page = html.Div([
    html.H1('DS4A')
])

@app.callback(
    dash.dependencies.Output('report','children'),
    [dash.dependencies.Input('url','pathname')]
)
def render_page(pathname):
    if pathname == '/daniel':
        return stats_pac.stats_pac,
    else:
        return index_page

if __name__ == '__main__':
    app.run_server(debug=True)
