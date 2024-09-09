import dash_bootstrap_components as dbc
from dash import Dash, dcc, html, Input, Output
import dash_vega_components as dvc
from utils.dashboard_utils import *

alt.data_transformers.disable_max_rows()
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])
server = app.server

app.layout = dbc.Container(fluid=True,
    children=[
    dbc.Row([
        dbc.Col(html.H1("Producción vitinicola y avisos fitosanitarios"), className="text-center mb-4")
    ]),

    dbc.Row([
        dbc.Col([
            dvc.Vega(
                id="columnChartTin",
                opt={"renderer": "svg", "actions": False},
                spec=columnChartTin.to_dict(),
                style={'width': '100%', 'height': '100%'}
            ),
        ], width=4),
        dbc.Col([
            dcc.Graph(
                id='mapa',
                figure=mapaChart
            )
        ], width=4),
        dbc.Col([
            dvc.Vega(
                id="columnChartBlan",
                opt={"renderer": "svg", "actions": False},
                spec=columnChartBlan.to_dict(),
                style={'width': '100%', 'height': '100%'}
            )
        ], width=4)
    ])
])

if __name__ == "__main__":
    app.run_server(debug=True)