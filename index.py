#Basics Requirements
import pathlib
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px

#Dash Bootstrap Components
import dash_bootstrap_components as dbc 

#Data 
import math
import numpy as np
import datetime as dt
import pandas as pd
import json

#Recall app
from app import app



###########################################################
#
#           APP LAYOUT:
#
###########################################################

#LOAD THE DIFFERENT FILES
from lib import header, antioquia_map, stats_se1, stats_pac

#PLACE THE COMPONENTS IN THE LAYOUT
app.layout =html.Div(
    [ 
      header.header,
      #sidebar.sidebar,
      antioquia_map.ant_map,
      #stats_se1.stats_se1,
      stats_pac.stats_pac

    ],
    className="ds4a-app", #You can also add your own css files by locating them into the assets folder
)

   

if __name__ == "__main__":
    app.run_server(debug=True)
