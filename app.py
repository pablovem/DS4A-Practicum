import math
import numpy as np
import datetime as dt
import pandas as pd
import json

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

from lib import header, stats_pac

app = dash.Dash(
    __name__, 
    meta_tags=[{"name": "viewport", "content": "width=device-width"}]
)

app.layout = html.Div(
    [
        header.header,
        html.Div(
            [
                stats_pac.stats_pac,
            ],
            id="report",
            className="row",
        )
    ],
    id="report-container",
)

if __name__ == '__main__':
    app.run_server(debug=True)