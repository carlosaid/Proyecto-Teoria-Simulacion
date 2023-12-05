import numpy as np

def generar_producto(nombre, tasa_demanda_media, tiempo_vida_util, costo_almacenamiento):
    return {
        'nombre': nombre,
        'tasa_demanda_media': tasa_demanda_media,
        'tiempo_vida_util': tiempo_vida_util,
        'costo_almacenamiento': costo_almacenamiento,
    }

def ejecutar_simulacion(tiempo_simulacion, productos):
    inventario = {producto['nombre']: [] for producto in productos}
    perdidas = {producto['nombre']: 0 for producto in productos}
    total_costos = 0

    for tiempo in range(tiempo_simulacion):
        for producto in productos:
            # Cambia la semilla en cada iteración para obtener números aleatorios diferentes
            np.random.seed(tiempo)

            # Simulación de la demanda (puedes usar una distribución específica)
            demanda = np.random.poisson(producto['tasa_demanda_media'])

            # Verifica si hay suficiente inventario para satisfacer la demanda
            while sum(inventario[producto['nombre']]) < demanda and inventario[producto['nombre']]:
                perdidas[producto['nombre']] += 1  # Contabiliza una unidad vencida como pérdida
                inventario[producto['nombre']].pop(0)  # Elimina la unidad vencida

            # Resta la demanda del inventario disponible
            for i in range(min(demanda, len(inventario[producto['nombre']]))):
                inventario[producto['nombre']][i] -= 1

            # Añade nuevos productos no vencidos al inventario
            inventario[producto['nombre']].extend([producto['tiempo_vida_util'] if np.random.rand() > 0.1 else 0 for _ in range(100)])

            # Actualiza el costo de almacenamiento
            total_costos += len(inventario[producto['nombre']]) * producto['costo_almacenamiento']

            # Reabastecimiento si el inventario está por debajo de cierto umbral (puedes ajustar esto)
            if len(inventario[producto['nombre']]) < 10:
                inventario[producto['nombre']].extend([producto['tiempo_vida_util'] if np.random.rand() > 0.1 else 0 for _ in range(100)])  # Añade nuevos productos al inventario

    return perdidas, total_costos

# Parámetros de la simulación para múltiples productos
productos_definidos = [
    generar_producto('producto_A', 10, 20, 1),
    generar_producto('producto_B', 20, 30, 2),
    # Puedes agregar más productos según sea necesario
]

# Ejecutar la simulación
tiempo_simulacion = 365
perdidas, total_costos = ejecutar_simulacion(tiempo_simulacion, productos_definidos)

# Imprimir resultados
for producto_nombre, cantidad_perdida in perdidas.items():
    print(f"Unidades perdidas para {producto_nombre}: {cantidad_perdida}")
print(f"Costo total: {total_costos}")
