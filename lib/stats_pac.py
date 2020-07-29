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



#Convert date 20190315 to 2019-03-15
filtro_Antioquia['FEC_NACIMIENTO_BENEFICIARIO'] = pd.to_datetime(filtro_Antioquia['FEC_NACIMIENTO_BENEFICIARIO'], format = "%Y%m%d").dt.strftime('%Y-%m-%d')
# Eliminate the "Can only use .dt accessor with datetimelike values" error
filtro_Antioquia['FEC_NACIMIENTO_BENEFICIARIO'] = pd.to_datetime(filtro_Antioquia['FEC_NACIMIENTO_BENEFICIARIO'], errors='coerce')
#convert date to year
filtro_Antioquia['YEAR_BIRTH']= filtro_Antioquia['FEC_NACIMIENTO_BENEFICIARIO'].dt.strftime('%Y')
#convert integer
filtro_Antioquia['YEAR_BIRTH'] = filtro_Antioquia['YEAR_BIRTH'].astype(np.int64)


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


###############################################################
# FIGURA 3
###############################################################


filtro_Antioquia['NOMBRE_CCF'] = filtro_Antioquia['NOMBRE_CCF'].str.lower()
count_CCF= filtro_Antioquia.groupby(['NOMBRE_CCF'])['subsidio_count'].count().sort_values(ascending=False)
df7=count_CCF.nlargest(6).to_frame(name=None)
fig3 = px.bar(df7, y='subsidio_count',title="APPLICATIONS ACCORDING CCF")

###############################################################
# FIGURA 4
###############################################################

count_gender_year = filtro_Antioquia[['subsidio_count','GEN_CDESCRIPCION','year_SOLICITUD']].groupby(['GEN_CDESCRIPCION','year_SOLICITUD'],as_index=False).count()
count_gender_year.sort_values(by='year_SOLICITUD',inplace=True)
fig4 = px.bar(count_gender_year,x='GEN_CDESCRIPCION', y='subsidio_count', title='APPLICATIONS by gender', color="year_SOLICITUD", barmode="group")

###############################################################
# FIGURA 5
###############################################################


count_zona_year = filtro_Antioquia[['subsidio_count','ARG_CDESCRIPCION','year_SOLICITUD']].groupby(['ARG_CDESCRIPCION','year_SOLICITUD'],as_index=False).count()
count_zona_year.sort_values(by='year_SOLICITUD',inplace=True)
fig5 = px.bar(count_zona_year,x='ARG_CDESCRIPCION', y='subsidio_count', title='APPLICATIONS by zone', color="year_SOLICITUD", barmode="group")

###############################################################
# FIGURA 6
###############################################################
def transformar(x):
    
    if   2000<x<= 2020: return '<20 years'
    
    elif 1990<x<= 2000: return '20-30 years'
    elif 1980<x<= 1990: return '30-40 years'
    elif 1970<x<= 1980: return '40-50 years'
    elif 1960<x<= 1970: return '50-60 years'
   
    else: return '> 60 years'



filtro_Antioquia['age_range']=filtro_Antioquia['YEAR_BIRTH'].apply(transformar) 

count_year_range = filtro_Antioquia.groupby(['age_range'])['subsidio_count'].count().sort_values(ascending=False)
df11=count_year_range.nlargest(6).to_frame(name=None)
fig6 = px.bar(df11, y='subsidio_count',title="AMOUNT OF UNEMPLOYMENT BENEFIT PER AGE_RANGE")


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
            ),
        dbc.Col(
            dcc.Graph(figure=fig3, id='fig3')
        ),
        dbc.Col(
            dcc.Graph(figure=fig4, id='fig4')
            ),
        dbc.Col(
            dcc.Graph(figure=fig5, id='fig5')
        ),
        dbc.Col(
            dcc.Graph(figure=fig6, id='fig6')
            )
    ])
	],className="ds4a-body")

