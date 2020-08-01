import pathlib
import math
import numpy as np
import datetime as dt
import pandas as pd
import json

import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px

import dash_bootstrap_components as dbc 

#Recall app
# from app import app

###########################################################
#
#           APP LAYOUT:
#
###########################################################

#LOAD THE DIFFERENT FILES
# from lib import header, antioquia_map, stats_se1, stats_pac
from lib import header, stats_se1, stats_pac

app = dash.Dash(
    __name__, 
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    external_stylesheets = [dbc.themes.BOOTSTRAP],
    suppress_callback_exceptions=True
)

sidebar = html.Div(
  [
    html.H4("Reports"),
    html.Hr(),
    dbc.Nav(
        [
            dbc.NavLink("PAC", href="/pac", id="pac-link"),
            dbc.NavLink("SE", href="/se", id="se-link"),
            dbc.NavLink("Micro", href="/micro", id="micro-link"),
        ],
        vertical=True,
        pills=True,
    )
  ],
  id="sidebar"
)

app.layout = html.Div(
    [ 
      dcc.Location(id="url", refresh=False),
      header.header,
      html.Div(
        [
          html.Div(
            [
              sidebar
            ],
            id="app-sidebar",
            className="col"
          ),
          html.Div(id="app-main",className="col"),
        ],
        id="flex-grid",
      ),
    ],
    className="app-container",
)


@app.callback(
    Output("app-main", "children"),
    [Input("url", "pathname")]
)
def render_content(pathname):
    if pathname in ["/", "/pac"]:
        return stats_pac.stats_pac
    elif pathname == "/se":
        return stats_se1.stats_se1
    elif pathname == "/micro":
        return html.Div(html.P("MICRO"))
    return dbc.Jumbotron(
        [
            html.H1("404: Page not found", className="text-danger"),
        ]
    )   

if __name__ == "__main__":
    app.run_server(debug=True)
