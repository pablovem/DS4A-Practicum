#Basics Requirements
import pathlib
import dash
from dash.dependencies import Input, Output, State, ClientsideFunction
import dash_core_components as dcc
import dash_html_components as html

#Dash Bootstrap Components
import dash_bootstrap_components as dbc 
 
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime as dt
import json
import numpy as np
import pandas as pd


SE_df = pd.read_excel('data/SubsidioEmergencia.xlsx', sheet_name='IWvyio')
SE_df['Count'] = 1
#count_doc = SE_df.groupby(['Número de Documento'])['Count'].count().sort_values(ascending=False)
SE_df = SE_df.drop_duplicates(['Número de Documento'])


##############################################################
# Gender
###############################################################

count_gender = SE_df.groupby(['Género'])['Count'].count().sort_values(ascending=False)
g2_df = count_gender.to_frame(name=None)
fig2 = px.bar(g2_df, y='Count', title='Gender', color='Count')
#fig2.show()
fig2.update_layout(title='Gender',paper_bgcolor="#F8F9F9")

###############################################################
# Zone
###############################################################

count_zona = SE_df.groupby(['Zona'])['Count'].count().sort_values(ascending=False)
g3_df = count_zona.to_frame(name=None)
labels_zone = ['Urbana', 'Rural', 'No disponible']
fig3 = px.pie(g3_df, values = 'Count', title='Zone', names= labels_zone)
fig3.update_traces(textposition='inside', textinfo='percent+label')
fig3.update_layout(title='Zone',paper_bgcolor="#F8F9F9")

###############################################################
# Marital status
###############################################################

SE_df['Estado civil'] = SE_df['Estado civil'].fillna('No disponible')

SE_df[SE_df['Estado civil'].str.contains("Soltero/a", case=False)]
SE_df['Estado civil'] = SE_df['Estado civil'].apply(lambda x: x.replace('Soltero/a', 'Soltero'))

SE_df[SE_df['Estado civil'].str.contains("Casado/a", case=False)]
SE_df['Estado civil'] = SE_df['Estado civil'].apply(lambda x: x.replace('Casado/a', 'Casado'))

SE_df[SE_df['Estado civil'].str.contains("Unión Libre", case=False)]
SE_df['Estado civil'] = SE_df['Estado civil'].apply(lambda x: x.replace('Unión Libre', 'Unión libre'))

SE_df[SE_df['Estado civil'].str.contains("Separado/a", case=False)]
SE_df['Estado civil'] = SE_df['Estado civil'].apply(lambda x: x.replace('Separado/a', 'Separado'))

SE_df[SE_df['Estado civil'].str.contains("Viudo/a", case=False)]
SE_df['Estado civil'] = SE_df['Estado civil'].apply(lambda x: x.replace('Viudo/a', 'Viudo'))

count_estadoc = SE_df.groupby(['Estado civil'])['Count'].count().sort_values(ascending=False)
g4_df = count_estadoc.to_frame(name=None)
#fig4 = px.bar(g4_df, y='Count', title='Civil Status')
#fig4.show()
labels = ['Soltero', 'Unión libre', 'Casado', 'No disponible', 'Separado', 'Viudo']
fig4 = px.pie(g4_df, values = 'Count', title='Civil Status', names= labels)
fig4.update_traces(textposition='inside', textinfo='percent+label')
fig4.update_layout(title='Marital status',paper_bgcolor="#F8F9F9")


###############################################################
# Population
###############################################################
SE_df[SE_df['Población'].str.contains('Victima del conflicto armado y en condiciones de desplazamiento', case=False)]

SE_df['Población'] = SE_df['Población'].apply(lambda x: x.replace('Victima del conflicto armado y en condiciones de desplazamiento', 'Victima Conflicto/Desplazamiento'))

SE_df[SE_df['Población'].str.contains('Victima del conflicto armado y en condiciones de discapacidad', case=False)]
SE_df['Población'] = SE_df['Población'].apply(lambda x: x.replace('Victima del conflicto armado y en condiciones de discapacidad', 'Victima Conflicto/Discapacidad'))

SE_df[SE_df['Población'].str.contains('Victima del conflicto armado y en condiciones de desplazamiento', case=False)]
SE_df['Población'] = SE_df['Población'].apply(lambda x: x.replace('Victima del conflicto armado y en condiciones de discapacidad', 'Victima Conflicto/Discapacidad'))

SE_df[SE_df['Población'].str.contains('Victima del conflicto armado y en condiciones de desplazamiento', case=False)]
SE_df['Población'] = SE_df['Población'].apply(lambda x: x.replace('Victima del conflicto armado y en condiciones de discapacidad', 'Victima Conflicto/Discapacidad'))

count_population = SE_df.groupby(["Población"])['Count'].count().sort_values(ascending=False)
g6_df = count_population.to_frame(name=None)
fig6 = px.bar(g6_df, y='Count', title='Population')
#fig6.show()
fig6.update_layout(title='Population',paper_bgcolor="#F8F9F9")

###############################################################
# Ethnic group
###############################################################

count_petn = SE_df.groupby(["Pertenencia étnica"])['Count'].count().sort_values(ascending=False)
g7_df = count_petn.to_frame(name=None)
fig7 = px.bar(g7_df, y='Count', title='Ethnicity')
fig7.update_layout(title='Ethnic group',paper_bgcolor="#F8F9F9")

#################################################################################
# Here the layout for the plots to use.
#################################################################################
stats_se1=html.Div([ 
	    #Place the different graph components here.
        dbc.Row([
            dbc.Col(
                dcc.Graph(figure=fig3, id='zone')
            ),
            dbc.Col(
                dcc.Graph(figure=fig4, id='marital_status')
                ) 
        ]),
        dbc.Row([
            dbc.Col(
                dcc.Graph(figure=fig6, id='population')
            ),
            dbc.Col(
                dcc.Graph(figure=fig7, id='ethnic_group')
                ) 
        ])
	],className="ds4a-body")



