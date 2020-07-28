#Basics Requirements
import pathlib
import plotly.graph_objects as go
import plotly.express as px

#Dash
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash.exceptions import PreventUpdate
import dash_bootstrap_components as dbc 

#Data 
import math
import numpy as np
import datetime as dt
import pandas as pd
import json

#Recall app
# from app import app

app = dash.Dash(__name__, external_stylesheets = [dbc.themes.BOOTSTRAP])
server = app.server

###########################################################
#
#           APP LAYOUT:
#
###########################################################

#LOAD THE DIFFERENT FILES
# from lib import title, stats_pac
# from lib import title, sidebar, stats_pac
from lib import title

#PLACE THE COMPONENTS IN THE LAYOUT
app.layout =html.Div(
    [ 
      # stats_pac.stats_pac,
      html.H1(children="Hola Mundo!"),
      # stats_pac.stats_pac,
      # title.title,
    ],
    className="ds4a-app",
)

if __name__ == "__main__":
    app.run_server(debug=True)