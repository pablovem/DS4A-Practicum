#Basics Requirements
import pathlib
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

import urllib

import warnings
warnings.filterwarnings('ignore')

#Recall app
#from app import app


#############################
# Load map data
#############################

url = 'https://opendata.arcgis.com/datasets/6dca7a12295f4d76b328827729a54d82_0.geojson'

uh = urllib.request.urlopen(url)
datastring = uh.read()

import json
data = json.loads(datastring)
for item in data["features"]:
        item["id"]=item["properties"]["COD_MPIO"]

import unicodedata
def elimina_tildes(cadena):
    s = ''.join((c for c in unicodedata.normalize('NFD',cadena) if unicodedata.category(c) != 'Mn'))
    return s


municipios_df = pd.read_csv('data/municipios.csv')

mun_antioquia = municipios_df.loc[municipios_df['CÓDIGO DANE DEL DEPARTAMENTO'] == 5][['MUNICIPIO','CÓDIGO DANE DEL MUNICIPIO']]

mun_antioquia['MUNICIPIO'] = mun_antioquia['MUNICIPIO'].apply(lambda x: elimina_tildes(x.lower()))
mun_antioquia['CÓDIGO DANE DEL MUNICIPIO'] = mun_antioquia['CÓDIGO DANE DEL MUNICIPIO'].apply(lambda x: str(x).zfill(5))

xls_2=pd.ExcelFile('Data/Lote AB-06 Enviados para tablero.xlsx')
lote_df=xls_2.parse('Lote 01 AB06(3448)')
lote_df['Municipio'].unique()

lote_df['Municipio'] = lote_df['Municipio'].apply(lambda x: elimina_tildes(x.lower()))

sub_df = lote_df[['Tipo de Documento','Género', 'Estado civil', 'Departamento', 'Municipio']]

temp_df = sub_df.merge(mun_antioquia, left_on='Municipio', right_on='MUNICIPIO')

agg_mun_df = temp_df.groupby('CÓDIGO DANE DEL MUNICIPIO').size().reset_index(name='SUBSIDIOS')
        
#############################
# Load map data
#############################
#df = pd.read_csv('data/superstore.csv', parse_dates=['Order Date', 'Ship Date'])
#
#with open('Data/us.json') as geo:
#    geojson = json.loads(geo.read())
#
#with open('Data/states.json') as f:
#    states_dict = json.loads(f.read())

#df['State_abbr'] = df['State'].map(states_dict)


#Create the map:
#dff=df.groupby('State_abbr').sum().reset_index()
#Map_Fig=px.choropleth_mapbox(dff,                         
#        locations='State_abbr',                   
#        color='Sales',                            
#        geojson=geojson,                          
#        zoom=3,                                   
#        mapbox_style="carto-positron",            
#        center={"lat": 37.0902, "lon": -95.7129}, 
#        color_continuous_scale="Viridis",         
#        opacity=0.5,                              
#        )
#Map_Fig.update_layout(title='US map',paper_bgcolor="#F8F9F9")


Map_Fig=px.choropleth_mapbox(agg_mun_df,                        
        locations='CÓDIGO DANE DEL MUNICIPIO',                  
        color='SUBSIDIOS',                           
        geojson=data,                          
        zoom=6,                                  
        mapbox_style="carto-positron",           
        center={"lat": 6.25184 , "lon": -75.56359}, 
        color_continuous_scale="Viridis",         
        opacity=0.5,                             
        )
Map_Fig.update_layout(title='Antioquia map',paper_bgcolor="#F8F9F9")


##############################
#Map Layout
##############################
ant_map = html.Div([
 #Place the main graph component here:
  dcc.Graph(figure=Map_Fig, id='ant_map')
], className="ds4a-body")
    