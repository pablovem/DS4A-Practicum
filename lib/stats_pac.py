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


df2 = pd.read_excel('5-311_MICRODATO_BENEFICIARIOS_MECANISMO_PROTECCIÓN_CESANTE_2.xlsx', sheet_name='5-311_MICRODATO_BENEFICIARIOS_M')

df2['subsidio_count']=1

#filtro_Antioquia=df2[df2['DIV_CNOM_DEPARTAMENTO'].str.contains('ANTIOQUIA', na=False,case=False)]

filtro_Antioquia= df2.loc[df2['DIV_CNOM_DEPARTAMENTO'] == 'ANTIOQUIA']

filtro_Antioquia['FEC_RADICA_SOLICITUD_BENEFICIARIO'] = pd.to_datetime(filtro_Antioquia['FEC_RADICA_SOLICITUD_BENEFICIARIO'], format = "%Y%m%d").dt.strftime('%Y-%m-%d')
filtro_Antioquia['FEC_RADICA_SOLICITUD_BENEFICIARIO'] = pd.to_datetime(filtro_Antioquia['FEC_RADICA_SOLICITUD_BENEFICIARIO'], errors='coerce')
filtro_Antioquia['year_month_SOLICITUD']= filtro_Antioquia['FEC_RADICA_SOLICITUD_BENEFICIARIO'].dt.strftime('%Y-%m')
#convert date to year
filtro_Antioquia['year_SOLICITUD']= filtro_Antioquia['FEC_RADICA_SOLICITUD_BENEFICIARIO'].dt.strftime('%Y')



##############################################################
# FIGURA 1
###############################################################


filtro_Antioquia['DIV_CNOM_MUNICIPIO'] = filtro_Antioquia['DIV_CNOM_MUNICIPIO'].str.lower()
count_barrio = filtro_Antioquia.groupby(['DIV_CNOM_MUNICIPIO'])['subsidio_count'].count().sort_values(ascending=False)
df3=count_barrio.nlargest(15).to_frame(name=None)

fig = px.bar(df3, y='subsidio_count',title="AMOUNT OF UNEMPLOYMENT BENEFIT PER BOROUGH")


###############################################################
# FIGURA 2
###############################################################


filtro_Antioquia['year_SOLICITUD'] = filtro_Antioquia['year_SOLICITUD'].str.lower()
count_year= filtro_Antioquia.groupby(['year_SOLICITUD'])['subsidio_count'].count().sort_values(ascending=False)
df6=count_year.nlargest(15).to_frame(name=None)
fig2 = px.bar(df6, y='subsidio_count',title="AMOUNT OF UNEMPLOYMENT BENEFIT PER YEAR")


#################################################################################
# Here the layout for the plots to use.
#################################################################################
stats_pac=html.Div([ 
	#Place the different graph components here.
    dbc.Row([
        dbc.Col(
            dcc.Graph(figure=fig2, id='fig2')
        ),
        dbc.Col(
            dcc.Graph(figure=fig, id='fig')
            )
    ])
	],className="ds4a-body")

