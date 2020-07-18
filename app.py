import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

app = dash.Dash(
    __name__, 
    meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

app.layout = html.Div(
    [
        html.Div(
            [
                html.Div(
                    [
                        html.H3("Team 10 - SuperSubsidio"),
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
        ),
        html.Div(
            [
                
            ],
            id="report",
            className="row",
        )
    ],
    id="report-container",
)

if __name__ == '__main__':
    app.run_server(debug=True)