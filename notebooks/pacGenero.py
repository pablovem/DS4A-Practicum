#Basics Requirements
import pathlib
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
from dash.exceptions import PreventUpdate
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

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
from lib import title, sidebar, us_map, stats

#PLACE THE COMPONENTS IN THE LAYOUT
app.layout =html.Div(
    [ 
      us_map.map,
      stats.stats,
      title.title,
      sidebar.sidebar,
    ],
    className="ds4a-app", #You can also add your own css files by locating them into the assets folder
)

###############################################   
#
#           APP INTERACTIVITY:
#
###############################################

###############################################################
#Load and modify the data that will be used in the app.
#################################################################

dfSE = pd.read_csv(r'data/pac/SE.csv', sep=';',encoding='latin1')
dfPAC = pd.read_csv(r'data/pac/pac.txt', sep='\t',encoding='latin1')
varFilterMunicipio = ''

df = pd.read_csv('data/superstore.csv', parse_dates=['Order Date', 'Ship Date'])

with open('data/us.json') as geo:
    geojson = json.loads(geo.read())

with open('data/states.json') as f:
    states_dict = json.loads(f.read())

df['State_abbr'] = df['State'].map(states_dict)
df['Order_Month'] = pd.to_datetime(df['Order Date'].map(lambda x: "{}-{}".format(x.year, x.month)))

#############################################################
# SCATTER & LINE PLOT : Add sidebar interaction here
#############################################################
@app.callback(
    [Output("Line", "figure"),Output("Scatter","figure")],
    [Input("state_dropdown", "value"),Input("date_picker", "start_date"),Input("date_picker", "end_date")],
)
def make_line_plot(state_dropdown, start_date, end_date):
    # se filtran los datos de acuerdo con las variables filtro
    if len(varFilterMunicipio) > 1:
        dfSE_1 = dfSE[dfSE['Municipio'].isin(varFilterMunicipio)]
        dfPAC_1 = dfPAC[dfPAC['DIV_CNOM_MUNICIPIO'].isin(varFilterMunicipio)]
    else:
        dfSE_1 = dfSE
        dfPAC_1 = dfPAC
    dfSE_1['Año/mes terminación laboral'] = [("_" + i[0:4] + i[5:7]) for i in dfSE_1['Fecha de terminación laboral']]
    dfSE_genero1 = dfSE_1
    dfSE_genero1["Año/mes terminación laboral int"] = [int(i[1:]) for i in dfSE_genero1["Año/mes terminación laboral"]]
    dfSE_genero2 = dfSE_genero1[dfSE_genero1["Año/mes terminación laboral int"] >= 201902]
    dfSE_genero2 = dfSE_genero2.groupby(['Año/mes terminación laboral', 'Genero']).count().reset_index().sort_values(
        by=["Año/mes terminación laboral"], ascending=True, ignore_index=True)
    Line_fig = px.bar(dfSE_genero2, x="Año/mes terminación laboral", y="numeroDocumento", color="Genero")
    Line_fig.update_layout(title='SE Genero', paper_bgcolor="#F8F9F9").update_xaxes(categoryorder="category ascending")
    dfPAC_genero = dfPAC_1
    dfPAC_genero['Año/mes radicación solicitud beneficiario'] = [int(int(i) / 100) for i in dfPAC_genero['FEC_RADICA_SOLICITUD_BENEFICIARIO']]
    dfPAC_genero = dfPAC_genero[dfPAC_genero['Año/mes radicación solicitud beneficiario'] >= 201712]
    dfPAC_genero['Año/mes radicación solicitud beneficiario'] = ["_" + str(i) for i in dfPAC_genero[
        'Año/mes radicación solicitud beneficiario']]
    dfPAC_genero = dfPAC_genero.groupby(
        ['Año/mes radicación solicitud beneficiario', 'GEN_CDESCRIPCION']).count().reset_index().sort_values(
        by=['Año/mes radicación solicitud beneficiario'], ascending=True, ignore_index=True)
    Scatter_fig = px.bar(dfPAC_genero, x="Año/mes radicación solicitud beneficiario", y="MPC_NID",color="GEN_CDESCRIPCION")
    Scatter_fig.update_layout(title='PaC Genero', paper_bgcolor="#F8F9F9")
    return [Line_fig, Scatter_fig]

#############################################################
# MAP : Add interactions here
#############################################################

#MAP date interaction
@app.callback(
    Output("US_map", "figure"),
    [
        Input("date_picker", "start_date"),
        Input("date_picker", "end_date")
    ],
)
def update_map(start_date,end_date):
    dff = df[(df['Order Date'] >= start_date) & (df['Order Date'] < end_date)] # We filter our dataset for the daterange
    dff=dff.groupby("State_abbr").sum().reset_index()
    fig_map2=px.choropleth_mapbox(dff,
        locations='State_abbr',
        color='Sales',
        geojson=geojson, 
        zoom=3, 
        mapbox_style="carto-positron", 
        center={"lat": 37.0902, "lon": -95.7129},
        color_continuous_scale="Viridis",
        opacity=0.5,
        title='US Sales'
        )
    fig_map2.update_layout(title="US State Sales",margin={"r":0,"t":0,"l":0,"b":0}, paper_bgcolor="#F8F9F9", plot_bgcolor="#F8F9F9",)
    return fig_map2

#MAP click interaction
@app.callback(
    Output('state_dropdown','value'),
    [Input('US_map','clickData')],
    [State('state_dropdown','value')]
)
def click_saver(clickData,state):
    if clickData is None:
        raise PreventUpdate
    #print(clickData)
    state.append(clickData['points'][0]['location'])
    return state

if __name__ == "__main__":
    app.run_server(debug=True)
