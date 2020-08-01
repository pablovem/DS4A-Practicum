import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import dash_bootstrap_components as dbc 


from lib import header, antioquia_map, stats_se1

app = dash.Dash(
    __name__, 
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    suppress_callback_exceptions=True
)

app.layout = html.Div(
    [
        dcc.Location(id="url", refresh=False),
        header.header,
        html.Div(id="report",className="row"),
    ],
    id="report-container",
)

index_page = html.Div([
        antioquia_map.ant_map,
        stats_se1.stats_se1
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
