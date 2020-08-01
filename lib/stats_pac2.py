import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc 
import plotly.graph_objects as go
import plotly.express as px


from datetime import datetime as dt
import json
import numpy as np
import pandas as pd

#Recall app
from app import app

dfSE = pd.read_excel('data/SubsidioEmergencia.xlsx', sheet_name='IWvyio')
dfPAC =pd.read_excel('data/5-311_MICRODATO_BENEFICIARIOS_MECANISMO_PROTECCIÓN_CESANTE_2.xlsx', sheet_name='5-311_MICRODATO_BENEFICIARIOS_M')

varFilterMunicipio = ''

if len(varFilterMunicipio) > 1:
    dfSE_1 = dfSE[dfSE['Municipio'].isin(varFilterMunicipio)]
    dfPAC_1 = dfPAC[dfPAC['DIV_CNOM_MUNICIPIO'].isin(varFilterMunicipio)]
else:
    dfSE_1 = dfSE
    dfPAC_1 = dfPAC

##############################################################
# FIGURA 1
###############################################################

dfPAC_1['fecha_nacimiento'] = (dfPAC_1['FEC_NACIMIENTO_BENEFICIARIO'] / 100)
dfPAC_1['fecha_nacimiento'] = [int(i) for i in dfPAC_1['fecha_nacimiento']]
dfPAC_1['edad'] = [2020-int(i/100)+(1 if int(i/100) >= 7 else 0) for i in dfPAC_1['fecha_nacimiento']]

dfPAC_edad = dfPAC_1.groupby(['edad', 'BEM_CDESCRIPCION']).count().reset_index()
dfPAC_edad.head()

fig1 = px.box(dfPAC_edad, x="BEM_CDESCRIPCION", y="edad", points="all") # , color="fecha_nacimiento"
fig1.update_layout(title='PaC Edad x Tipo Beneficiario', paper_bgcolor="#F8F9F9")

###############################################################
# FIGURA 2
###############################################################

dfPAC_edad3 = dfPAC_1.groupby(['edad','POB_CDESCRIPCION']).count().reset_index()
fig2 = px.box(dfPAC_edad3, x="POB_CDESCRIPCION", y="edad", points="all")
fig2.update_layout(title='PaC Poblacion x Edad', paper_bgcolor="#F8F9F9")

###############################################################
# FIGURA 3
###############################################################


dfPAC_1['Núnero de usuarios'] = dfPAC_1['MPC_NID']
dfPAC_1['Zona'] = dfPAC_1['ARG_CDESCRIPCION']
dfPAC_edad2 = dfPAC_1.groupby(['edad']).count().reset_index()
fig3 = px.bar(dfPAC_edad2, x="edad", y="Núnero de usuarios") # , color="fecha_nacimiento"
fig3.update_layout(title='PaC Edad', paper_bgcolor="#F8F9F9")

###############################################################
# FIGURA 4
###############################################################

dfPAC_zona = dfPAC_1
dfPAC_1['Número de usuarios'] = dfPAC_1['MPC_NID']
dfPAC_1['beneficio'] = dfPAC_1['MPC_CDESCRIPCION']
dfPAC_1['Zona'] = dfPAC_1['ARG_CDESCRIPCION']

dfPAC_Zona = dfPAC_1.groupby(['beneficio', 'Zona']).count().reset_index()

fig4 = px.bar(dfPAC_Zona, x="beneficio", y="Número de usuarios", color="Zona")
fig4.update_layout(title='PaC Zona', paper_bgcolor="#F8F9F9")

#################################################################################
# Here the layout for the plots to use.
#################################################################################

stats_pac2=html.Div([ 
        dbc.Row([
            dbc.Col(
                dcc.Graph(figure=fig1, id='zone')
            ),
            dbc.Col(
                dcc.Graph(figure=fig2, id='marital_status')
                ) 
        ]),
        dbc.Row([
            dbc.Col(
                dcc.Graph(figure=fig3, id='population')
            ),
            dbc.Col(
                dcc.Graph(figure=fig4, id='ethnic_group')
                ) 
        ])
	],className="ds4a-body")