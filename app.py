import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

df = pd.read_excel('5-311_MICRODATO_BENEFICIARIOS_MECANISMO_PROTECCIÓN_CESANTE_2.xlsx', sheet_name='5-311_MICRODATO_BENEFICIARIOS_M')



df2=df.copy()
df2['subsidio_count']=1
filtro_Antioquia=df2[df2['DIV_CNOM_DEPARTAMENTO'].str.contains('ANTIOQUIA', na=False,case=False)]

filtro_Antioquia['FEC_RADICA_SOLICITUD_BENEFICIARIO'] = pd.to_datetime(filtro_Antioquia['FEC_RADICA_SOLICITUD_BENEFICIARIO'], format = "%Y%m%d").dt.strftime('%Y-%m-%d')
filtro_Antioquia['FEC_RADICA_SOLICITUD_BENEFICIARIO'] = pd.to_datetime(filtro_Antioquia['FEC_RADICA_SOLICITUD_BENEFICIARIO'], errors='coerce')
filtro_Antioquia['year_month_SOLICITUD']= filtro_Antioquia['FEC_RADICA_SOLICITUD_BENEFICIARIO'].dt.strftime('%Y-%m')
#convert date to year
filtro_Antioquia['year_SOLICITUD']= filtro_Antioquia['FEC_RADICA_SOLICITUD_BENEFICIARIO'].dt.strftime('%Y')


#Grafica 1


filtro_Antioquia['DIV_CNOM_MUNICIPIO'] = filtro_Antioquia['DIV_CNOM_MUNICIPIO'].str.lower()
count_barrio = filtro_Antioquia.groupby(['DIV_CNOM_MUNICIPIO'])['subsidio_count'].count().sort_values(ascending=False)
df3=count_barrio.nlargest(15).to_frame(name=None)

fig = px.bar(df3, y='subsidio_count',title="AMOUNT OF UNEMPLOYMENT BENEFIT PER BOROUGH")









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
            dcc.Graph(
        id='example-graph',
        figure=fig
    )    
            ],
            id="report",
            className="row",
        )
    ],
    id="report-container",
)

if __name__ == '__main__':
    app.run_server(debug=True)