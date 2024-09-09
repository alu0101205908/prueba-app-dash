import pandas as pd


CARD_STYLE = {
    
    "margin-right": "10px",
    "background-color": "#FFFFFF",
    "color": "#343a40",
    "border": "1px solid #ced4da",
    "box-shadow": "0 4px 8px rgba(0,0,0,0.1)",
    "border-radius": "0.375rem",
    "padding": "1rem",
    "font-weight": "bold",
    "display": "flex"
}

TEXT_STYLE = {
    "font-family": "Helvetica Neue, Arial, sans-serif",
    "text-align": "center",
    "padding": "1rem",
    "font-size": "1rem"
}

COLOR_DICT = {
    'YCODEN-DAUTE-ISORA': 'rgb(160, 147, 125)',
    'ABONA': 'rgb(182, 199, 170)',
    'VALLE DE GÜÍMAR': 'rgb(246, 230, 203)',
    'VALLE DE LA OROTAVA': 'rgb(231, 212, 181)',
    'TACORONTE-ACENTEJO': 'rgb(216, 239, 211)'
}


COLOR_DICT_II_BASE = {
    'YCODEN-DAUTE': 'rgb(246, 230, 203)',
    'ISORA': 'rgb(246, 230, 203)',
    'ABONA': 'rgb(182, 199, 170)',
    'VALLE DE GÜÍMAR': 'rgb(191, 163, 118)',
    'VALLE DE LA OROTAVA': 'rgb(160, 147, 125)',
    'TACORONTE-ACENTEJO': 'rgb(216, 239, 211)'
}

OPACIDAD = {
    'Zona alta': 1.0,
    'Zona media': 0.6,
    'Zona baja': 0.3
}

MESES = {
    1: 'Enero', 2: 'Febrero', 3: 'Marzo', 4: 'Abril', 5: 'Mayo', 6: 'Junio',
    7: 'Julio', 8: 'Agosto', 9: 'Septiembre', 10: 'Octubre', 11: 'Noviembre', 12: 'Diciembre'
}

colores_personalizados = {
    f"{key}-{op_key}": color.replace('rgb', 'rgba').replace(')', f', {opacidad})')
    for key, color in COLOR_DICT_II_BASE.items()
    for op_key, opacidad in OPACIDAD.items()
}

def obtener_estacion(fecha):

    year = str(fecha.year)

    if (fecha >= pd.Timestamp(f'{year}-12-21')) or (fecha < pd.Timestamp(f'{year}-03-21')):
        return 'Invierno'
    elif (fecha >= pd.Timestamp(f'{year}-03-21')) and (fecha < pd.Timestamp(f'{year}-06-21')):
        return 'Primavera'
    elif (fecha >= pd.Timestamp(f'{year}-06-21')) and (fecha < pd.Timestamp(f'{year}-09-21')):
        return 'Verano'
    elif (fecha >= pd.Timestamp(f'{year}-09-21')) and (fecha < pd.Timestamp(f'{year}-12-21')):
        return 'Otoño'
    
def definir_tramo(total_avisos):
    if total_avisos < 100:
        return '9 - 99'
    elif 100 <= total_avisos < 500:
        return '100 - 499'
    elif 500 <= total_avisos < 1000:
        return '500 - 999'
    elif 1000 <= total_avisos < 1500:
        return '1000 - 1499'
    else:
        return '1500+'

colores_tramos = {
    '9 - 99': 'rgb(192, 216, 186)',
    '100 - 499': 'rgb(246, 230, 203)',
    '500 - 999': 'rgb(182, 199, 170)',
    '1000 - 1499': 'rgb(231, 212, 181)',
    '1500+': 'rgb(160, 147, 125)'
}