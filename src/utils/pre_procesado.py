import pandas as pd
import numpy as np
import geopandas as gpd
from shapely.geometry import Point
from utils.dashboard_utilites import *


# Datos de producción
dfProd =  pd.read_csv("../data/produccion-vitivinicola-por-consejo-regulador.csv", sep=",")

dfProd.rename(columns={'denominacion': 'comarca_nombre', 'periodo': 'year'}, inplace=True)
years = dfProd['year'].unique()
dfProd['comarca_nombre'] = dfProd['comarca_nombre'].str.upper()
dfProd['comarca_nombre'] = dfProd['comarca_nombre'].replace({'VALLE DE GÜIMAR': 'VALLE DE GÜÍMAR'})
dfProd = dfProd.loc[~dfProd['comarca_nombre'].isin(["TOTAL"])]
comarcas = dfProd['comarca_nombre'].unique()
colores = []
for comarca in comarcas:
    base_color = COLOR_DICT.get(comarca, 'rgb(0, 0, 0)')
    colores.append(f'rgba{base_color[3:-1]}, 1.0)')


dfProdAgg = dfProd.groupby(['year', 'comarca_nombre']).agg({'Blanco': 'sum', 'Tinto': 'sum'}).reset_index()


# Datos de avisos fitosanitarios
df_avisos_bo = pd.read_csv("../data/avisos/avisos-fitosanitarios-del-cultivo-de-vina-de-riesgo-de-botrytis.csv")
df_avisos_mi = pd.read_csv("../data/avisos/avisos-fitosanitarios-del-cultivo-de-vina-de-riesgo-de-mildiu.csv")
df_avisos_oi = pd.read_csv("../data/avisos/avisos-fitosanitarios-del-cultivo-de-vina-de-riesgo-de-oidio.csv")

df_avisos = pd.concat([df_avisos_bo, df_avisos_mi, df_avisos_oi])
df_avisos.drop(columns=["cultivo", "comarca_zona_id"], inplace=True)
df_avisos['comarca_nombre'] = df_avisos['comarca_nombre'].replace({'ISORA': 'YCODEN-DAUTE-ISORA', 'YCODEN-DAUTE': 'YCODEN-DAUTE-ISORA'})
df_avisos['fecha_aviso'] = pd.to_datetime(df_avisos['fecha_aviso'])
df_avisos['year'] = df_avisos['fecha_aviso'].dt.year
df_avisos['estacion'] = df_avisos['fecha_aviso'].apply(obtener_estacion)
df_avisos_est = df_avisos.groupby(['comarca_nombre', 'estacion']).size().reset_index(name='total_avisos')
df_avisos_est['tramo'] = df_avisos_est['total_avisos'].apply(definir_tramo)
df_avisos['mes'] = df_avisos['fecha_aviso'].dt.month
df_avisos['mes_nombre'] = df_avisos['mes'].map(MESES)

periodos = df_avisos['year'].unique()
periodos_total = np.intersect1d(years, periodos)
periodos_total.sort()
dfProdAgg = dfProdAgg.loc[dfProdAgg["year"].isin(periodos_total)]
dfAvisosAgg = df_avisos.loc[df_avisos["year"].isin(periodos_total)].groupby(['year', 'plaga_enfermedad']).size().reset_index(name='Total_Avisos')


# Datos georeferenciados comarcas
gdfComarcas = gpd.read_file('../data/comarcas-de-cultivos-de-la-vina.geojson')
gdfComarcas.set_crs(epsg=4326, inplace=True)
gdfComarcas['agrupacion'] = gdfComarcas['comarca_nombre'] + "-" + gdfComarcas['zona']


# Datos estaciones meteorologicas
dfEstaciones = pd.read_csv("../data/estaciones.csv", sep=";")
geometry = [Point(xy) for xy in zip(dfEstaciones['longitude'], dfEstaciones['latitude'])]
gdfEstaciones= gpd.GeoDataFrame(dfEstaciones, geometry=geometry)
gdfEstaciones.set_crs(epsg=4326, inplace=True)


gdfComEst = gpd.sjoin(gdfEstaciones, gdfComarcas, how="left")
dfComEst = pd.DataFrame(gdfComEst.drop(columns=['name', 'municipality_name', 'latitude', 'longitude', 'x_cords', 'y_cords', 'altitude', 'geometry', 'index_right', 'zona']))
dfComEst['comarca_nombre'] = dfComEst['comarca_nombre'].replace({'ISORA': 'YCODEN-DAUTE-ISORA', 'YCODEN-DAUTE': 'YCODEN-DAUTE-ISORA'})

# Datos sensores estaciones meteorologicas
dfSensores = pd.read_csv("../data/sensores.csv", sep=";")
dfSensores.drop(columns=['unit'], inplace=True)
dfComEstSens = dfComEst.merge(dfSensores, on=['id_weatherstation'])
print(dfComEstSens)

# Datos meteorologicos
dfMeteo = pd.read_csv("../data/meteo.csv", sep=";")
dfMeteo['observation_date'] = pd.to_datetime(dfMeteo['observation_date'])
dfMeteo['year'] = dfMeteo['observation_date'].dt.year
dfMeteo = dfMeteo.dropna(subset=['mean', 'min', 'max'], how='all')

dfMeteoGrouped = dfMeteo.groupby(['id_weatherstation', 'id_weatherstationsensor', 'year']).agg({
    'mean': 'mean',
    'min': 'mean',
    'max': 'mean'
}).reset_index()

dfMeteoGrouped['valor'] = dfMeteoGrouped['mean'].combine_first(dfMeteoGrouped['min']).combine_first(dfMeteoGrouped['max'])


dfMetComEstSens = dfMeteoGrouped.merge(dfComEstSens, on=['id_weatherstationsensor'])
dfResult = dfMetComEstSens.filter(items=['year', 'valor', 'comarca_nombre', 'sensor_alias'])
dfResult = dfResult.groupby(['year', 'comarca_nombre', 'sensor_alias']).agg({'valor': 'mean'}).reset_index()
dfMeteoProd = dfResult.merge(dfProd, on=["year", "comarca_nombre"])