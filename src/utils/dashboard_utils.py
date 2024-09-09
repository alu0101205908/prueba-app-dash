import plotly.graph_objs as go
import plotly.express as px
import altair as alt
from utils.pre_procesado import *


columnChartTin = alt.Chart(dfProdAgg).mark_bar().encode(
    x=alt.X('year:O', title='Año'),
    y=alt.Y('sum(Tinto):Q', title='Producción (litros)'),
    color=alt.Color('comarca_nombre:N', title='Comarcas', scale=alt.Scale(domain=comarcas, range=colores)),
    tooltip=['year', 'comarca_nombre', 'sum(Tinto)']
).properties(
    width=250,
    height=300,
    title='Producción total vino tinto'
)

columnChartBlan = alt.Chart(dfProdAgg).mark_bar().encode(
    x=alt.X('year:O', title='Año'),
    y=alt.Y('sum(Blanco):Q', title='Producción (litros)'),
    color=alt.Color('comarca_nombre:N', title='Comarcas', scale=alt.Scale(domain=comarcas, range=colores)),
    tooltip=['year', 'comarca_nombre', 'sum(Blanco)']
).properties(
    width=250,
    height=300,
    title='Producción total vino blanco'
)

heatmap = alt.Chart(df_avisos_est).mark_rect().encode(
    x=alt.X('estacion:O', title='Estación'),
    y=alt.Y('comarca_nombre:O', title='Comarca'),
    color=alt.Color(
        'tramo:O',
        title='Tramo de Avisos',
        scale=alt.Scale(domain=list(colores_tramos.keys()), range=list(colores_tramos.values()))
    ),
    tooltip=['comarca_nombre', 'estacion', 'total_avisos']
).properties(
    width=500,
    height=500,
    title='Número de avisos de Plaga/Enfermedad por comarca y estación del año'
) + alt.Chart(df_avisos_est).mark_text(baseline='middle', fontSize=12, fontWeight='bold', color='white').encode(
    x=alt.X('estacion:O'),
    y=alt.Y('comarca_nombre:O'),
    text=alt.Text('total_avisos:Q')
)

areaChart = alt.Chart(dfAvisosAgg).mark_area(opacity=0.5).encode(
    x=alt.X('year:O', title='Año', scale=alt.Scale(domain=[2013, 2014, 2015, 2016])),
    y=alt.Y('sum(Total_Avisos):Q', title='Número de Avisos'),
    color=alt.Color('plaga_enfermedad:N', title='Plaga/Enfermedad', scale=alt.Scale(domain=['BOTRYTIS', 'OIDIO', 'MILDIU'], range=['rgb(160, 147, 125)', 'rgb(182, 199, 170)', 'rgb(231, 212, 181)'])),
    tooltip=['year', 'plaga_enfermedad', 'sum(Total_Avisos)']
).properties(
    width=500,
    height=500,
    title='Total de Avisos por Año y Plaga/Enfermedad'
)

def meteo_prod(sensor_alias, selected_comarca):
    dfFiltered = dfMeteoProd[(dfMeteoProd['sensor_alias'] == sensor_alias) & (dfMeteoProd['comarca_nombre'] == selected_comarca)]

    leyendaSensor = {
        "RAD": ["Radiación solar (W/m²)", "Radiación solar"],
        "TEMP": ["Temperatura (ºC)", "Tempertatura"],
        "HUM": ["Húmedad relativa (%)", "Húmedad"],
    }

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=dfFiltered['year'],
        y=dfFiltered['valor'],
        mode='lines+markers',
        name=f'{sensor_alias} - {selected_comarca}',
        line=dict(color='rgba(160, 147, 125, 1)'),
        yaxis='y1'
    ))

    fig.add_trace(go.Bar(
        x=dfFiltered['year'],
        y=dfFiltered['Total'],
        name=f'Comarca - {selected_comarca}',
        marker=dict(color='rgba(182, 199, 170, 0.3)'),
        yaxis='y2'
    ))

    fig.update_layout(
        title=f'{leyendaSensor[sensor_alias][1]} y producción total en {selected_comarca}',
        title_x=0.5,
        xaxis_title='Año',
        yaxis2=dict(
            title='Producción (litros)',
            overlaying='y',
            side='right',
            showgrid=False
        ),
        yaxis=dict(
            title=leyendaSensor[sensor_alias][0],
            showgrid=True,
            side='left',
            layer="below traces"
        ),
        legend=dict(
            x=0,
            y=1.1,
            bgcolor='rgba(255, 255, 255, 0)',
            bordercolor='rgba(255, 255, 255, 0)'
        )
    )

    return fig

mapaChart = px.choropleth_mapbox(
    gdfComarcas,
    geojson=gdfComarcas.geometry,
    locations=gdfComarcas.index,
    color=gdfComarcas['agrupacion'],
    color_discrete_map=colores_personalizados,
    mapbox_style="carto-positron",
    center={"lat": gdfComarcas.geometry.centroid.y.mean(), "lon": gdfComarcas.geometry.centroid.x.mean()},
    zoom=8,
    labels={'agrupacion': 'Comarca - zona'}
).update_layout(showlegend=False)