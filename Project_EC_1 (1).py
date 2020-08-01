#!/usr/bin/env python
# coding: utf-8

# ## Project EC

# **Problema**
# 
# En esta sección buscamos dar una descripción de la problematica y una descripción de la estructura del tablero.

# **Filtros Globales**
# 
# Caja de Compensación \
# Año \
# Departamento

# **Subsidio de Emergencia** (Manuela)
# 
# El Subsidio de emergencia es un beneficio que otorga la Caja de Compensación Familiar Colsubsidio, con recursos que provienen de los aportes de las empresas afiliadas, destinados a los trabajadores que quedaron desempleados a causa de la pandemia COVID - 19, como una medida de orden laboral, dentro del Estado de emergencia, económica, social y ecológica, a partir del decreto 488 de 27 de marzo de 2020 y el decreto 770 del 03 de junio de 2020.

# En esta sección buscamos entender el comportamiento de la asignación de subsidios de emergencia \
# 
# Indicadores 
# 
# Número de formularios / Número de personas / Subsidios asignados
# 
# Análisis por estado: Aprobado, Negado, Pendiente de análisis, Pérdida de derecho, Retiro voluntario
# 
# Postulados por genero
# 
# Postulados por zona o región
# 
# Postulados por municipio
# 
# Postulados por categoría salarial
# 
# Postulados por sector económico
# 
# Postulados por rango de edad
# 
# 
# Datasets: BD Subsidio Emergencia-1, PAGO DE BENEFICIOS_Corte20200618, **Lote AB-06 Enviados para tablero**
# 

# **Protección al Cesante** (Daniel)
# 
# El Fondo de Solidaridad y Fomento al Empleo y Protección al Cesante es un componente del Mecanismo de Protección al Cesante, el cual será administrado por las Cajas de Compensación Familiar y se encargará de otorgar beneficios a la población
# cesante que cumpla con los requisitos de acceso, con el fin de proteger a los trabajadores de los riesgos producidos por las fluctuaciones en los ingresos en periodos de desempleo.

# Cobertura por genero por año
# 
# Cobertura por zona o región por año
# 
# Cobertura por municipio por año
# 
# Cobertura por categoría salarial por año
# 
# Cobertura por rango de edad por año
# 
# Datasets: 5-311_MICRODATO_BENEFICIARIOS_MECANISMO_PROTECCIÓN_CESANTE, 5-395A_EJECUCIÓN_FOSFEC_ESTRUCTURA A_CANTIDAD_VALOR, 5-396A_EJECUCIÓN_FOSFECESTRUCTURA_B_(VALOR), 5-397A_EJECUCIÓN_FOSFEC_ESTRUCTURA_C_(CANTIDAD)
# 

# **Análisis Comparativo** (Johanna)
# 
# En esta sección buscamos identificar las variaciones de los indicadores considerados en las secciones anteriores. Se pueden presentar como tasas (ratas) y/o porcentajes.
# 
# 
# PaC vs SE por genero \
# PaC vs SE por zona o región \
# PaC vs SE por municipio \
# PaC vs SE Cobertura por categoría salarial \
# PaC vs SE Cobertura por rango de edad 

# **Opcional** (Hernán y Pablo V.)
# 
# Comparación del comportamiento proyectado (modelo predictivo) respecto al comportamiento real

# **Opcional** **Análisis Ingreso Solidario** (Pablo N.)
# 
# El Ingreso Solidario, subsidio creado por el Gobierno Nacional y entregado por el Departamento Nacional de Planeación, se ha convertido en una de las ayudas más importantes para que los hogares colombianos enfrenten la crisis económica generada por el coronavirus, que inició en el mes de marzo. Esta entrega es mensual (160.000 por mes), sin ningún tipo de descuento y se comenzó a entregar desde abril a través de distintas modalidades digitales y bancarias.
# 

# Asignaciones por genero
# 
# Asignaciones por zona o región
# 
# Asignaciones por municipio
# 
# Asignaciones por categoría salarial
# 
# Asignaciones por sector económico
# 
# Asignaciones por rango de edad
# 

# In[12]:


get_ipython().run_line_magic('matplotlib', 'inline')
import pandas as pd
import numpy as np
from scipy import stats
import json
import plotly.express as px
import matplotlib.pyplot as plt
from sklearn.cluster import KMeans 
from sklearn.datasets.samples_generator import make_blobs 

import seaborn as sns
sns.set_style('darkgrid')
import statsmodels.api as sm
import statsmodels.formula.api as smf
from datetime import datetime as dt


import warnings
warnings.filterwarnings('ignore')


# In[2]:


df = pd.read_csv('IngresoSolidario_Nequi_Uso.csv', parse_dates=['fecha_transaccion'])
df.head()


# In[3]:


df.columns


# In[4]:


pd.options.display.max_columns = 100
df.head(3)


# In[5]:


df[['municipio','trans_particular_original','categoria_transaccion']].describe()


# In[6]:


df['categoria_transaccion'].describe()


# In[7]:


plt.figure(figsize=(12,12))
vars_to_plot = ['valor_transaccion']
for i, var in enumerate(vars_to_plot):
    plt.subplot(2,2,i+1)
    plt.hist(df[var],50)
    title_string = "Histogram of " + var
    plt.title(title_string)


# In[8]:


df1 = df.loc[(df['valor_transaccion'] < 400000 )]
df1  


# In[67]:


df2 = df[['valor_transaccion']]
df2  


# In[9]:


plt.figure(figsize=(20,20))
vars_to_plot = ['categoria_transaccion','tipo_canal','canal_desc']
for i, var in enumerate(vars_to_plot):
    plt.subplot(2,2,i+1)
    sns.boxplot(x = var, y='valor_transaccion', data = df1)
    title_string = "Boxplot of VT vs. " + var
    plt.ylabel("valor_transaccion")
    plt.title(title_string)


# In[13]:


X, y = make_blobs(n_samples=5000, centers=[[4,4], [-2, -1], [2, -3], [1, 1]], cluster_std=0.9)


# In[15]:


plt.scatter(X[:, 0], X[:, 1], marker='.')


# In[68]:


from sklearn.preprocessing import StandardScaler
X = df2.values[1:]
X


# In[69]:


k_means = KMeans(init = "k-means++", n_clusters = 4, n_init = 12)


# In[70]:


k_means.fit(X)


# In[71]:


k_means_labels = k_means.labels_
k_means_labels


# In[72]:


k_means_cluster_centers = k_means.cluster_centers_
k_means_cluster_centersk_means_cluster_centers = k_means.cluster_centers_
k_means_cluster_centers


# In[60]:


fig = plt.figure(figsize=(6, 4))

# Colors uses a color map, which will produce an array of colors based on
# the number of labels there are. We use set(k_means_labels) to get the
# unique labels.
colors = plt.cm.Spectral(np.linspace(0, 1, len(set(k_means_labels))))

ax = fig.add_subplot(1, 1, 1)

# For loop that plots the data points and centroids.
# k will range from 0-3, which will match the possible clusters that each
# data point is in.
for k, col in zip(range(len([[4,4], [-2, -1], [2, -3], [1, 1]])), colors):

    # Create a list of all data points, where the data poitns that are 
    # in the cluster (ex. cluster 0) are labeled as true, else they are
    # labeled as false.
    my_members = (k_means_labels == k)
    
    # Define the centroid, or cluster center.
    cluster_center = k_means_cluster_centers[k]
    
    # Plots the datapoints with color col.
    ax.plot(X[my_members, 0], X[my_members, 1], 'w', markerfacecolor=col, marker='.')
    
    # Plots the centroids with specified color, but with a darker outline
    ax.plot(cluster_center[0], cluster_center[1], 'o', markerfacecolor=col,  markeredgecolor='k', markersize=6)


ax.set_title('KMeans')
ax.set_xticks(())
ax.set_yticks(())
plt.show()


# In[33]:


from yellowbrick.cluster import KElbowVisualizer


# In[73]:


# Instantiate the clustering model and visualizer
model = KMeans()
visualizer = KElbowVisualizer(model, k=(2,10))

visualizer.fit(X)        # Fit the data to the visualizer
visualizer.show()        # Finalize and render the figure


# In[74]:


# Instantiate the clustering model and visualizer
model = KMeans()
visualizer = KElbowVisualizer(model, k=(2,10))

visualizer.fit(X)        # Fit the data to the visualizer
visualizer.show()        # Finalize and render the figure


# In[46]:


from yellowbrick.cluster import SilhouetteVisualizer


# In[76]:


model = KMeans(5, random_state=42)
visualizer = SilhouetteVisualizer(model, colors='yellowbrick')

visualizer.fit(X)        # Fit the data to the visualizer
visualizer.show()        # Finalize and render the figure


# In[77]:


from yellowbrick.cluster import InterclusterDistance


# In[80]:


# Instantiate the clustering model and visualizer
model = KMeans(6)
visualizer = InterclusterDistance(model)

visualizer.fit(X)        # Fit the data to the visualizer
visualizer.show()        # Finalize and render the figure


# In[81]:


import pandas as pd
cust_df = pd.read_csv('IngresoSolidario_Nequi_Uso.csv')
cust_df.head()


# In[82]:


df = cust_df.drop('_id', axis=1)
df.head()


# In[98]:


from sklearn.preprocessing import StandardScaler
X = df.values[:,1:]
X


# In[92]:


X = np.nan_to_num(X)
Clus_dataSet = StandardScaler().fit_transform(X)
Clus_dataSetX = np.nan_to_num(X)
Clus_dataSet = StandardScaler().fit_transform(X)
Clus_dataSet


# In[94]:


visualizer = KElbowVisualizer(model, k=(2,12), metric='calinski_harabasz', timings=False)

visualizer.fit(X)        # Fit the data to the visualizer
visualizer.show()        # Finalize and render the figurevisualizer = KElbowVisualizer(model, k=(2,12), metric='calinski_harabasz', timings=False)


# In[96]:


df["Clus_km"] = labels
df.head(5)


# In[97]:


clusterNum = 4
k_means = KMeans(init = "k-means++", n_clusters = clusterNum, n_init = 12)
k_means.fit(X)
labels = k_means.labels_
print(labels)


# In[102]:


area = np.pi * ( X[:, 1])**2  
plt.scatter(X[:, 0], X[:, 3], s=area, c=labels.astype(np.float), alpha=0.5)
plt.xlabel('valor_transaccion', fontsize=18)
plt.ylabel('watermark_date', fontsize=16)
plt.show()


# In[95]:


clusterNum = 4
k_means = KMeans(init = "k-means++", n_clusters = clusterNum, n_init = 12)
k_means.fit(X)
labels = k_means.labels_
print(labels)


# In[72]:


#df['tipo_identificacion_cliente'].unique() 
df[df['tipo_identificacion_cliente'].str.contains('CC')].groupby(['numero_identificacion_cliente']).count().sort_values(ascending=False)



# In[61]:


Dataframe = pd.DataFrame(
    columns=["numero_identificacion_cliente", "fecha_transaccion", "valor_transaccion", "municipio", "concepto_desc", "canal_desc", "ciudad_canal", "categoria_transaccion"],
    data = (df)
)
Dataframe



# In[27]:


Dataframe.isnull()


# In[63]:



print(Dataframe)groupby('numero_identificacion_cliente').count())


# In[60]:


Dataframe [‘categoria_transaccion’].fillna(‘NoInfoCanal’,inplace = True)
Dataframe


# In[39]:


sns.distplot(Dataframe['valor_transaccion'],fit=stats.norm, kde=False)
sns.set(color_codes=True)
plt.xticks(rotation=90)
plt.title("Histogram of Valor Uso")


# In[41]:


stats.probplot(x=Dataframe['valor_transaccion'], dist = "norm", plot = plt)
plt.title("QQ Plot for Prices")
plt.show()


# In[56]:


px.scatter(df, x='valor_transaccion', y='fecha_transaccion', color='canal_desc')
Dataframe


# In[ ]:




