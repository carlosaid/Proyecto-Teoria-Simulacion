# productos.py

import numpy as np

def generar_producto(nombre, tasa_demanda_media, tiempo_vida_util, costo_almacenamiento):
    return {
        'nombre': nombre,
        'tasa_demanda_media': tasa_demanda_media,
        'tiempo_vida_util': tiempo_vida_util,
        'costo_almacenamiento': costo_almacenamiento,
    }