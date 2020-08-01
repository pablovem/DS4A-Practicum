#Basics Requirements
import pathlib
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html

#Dash Bootstrap Components
import dash_bootstrap_components as dbc 

header = html.Div(
            children = [
                html.Div(
                    [
                        html.H3("Team 10 - SuperSubsidio & Comfama"),
                    ],
                    id="title",
                    className="two-thirds column",
                ),
                html.Div(
                    [],
                    id="logo",
                    className="one-third column",
                ),
            ],
            id="header",
        )