import numpy as np

def ejecutar_simulacion(tiempo_simulacion, productos):
    inventario = {producto['nombre']: [] for producto in productos}
    perdidas = {producto['nombre']: 0 for producto in productos}
    total_costos = 0

    for tiempo in range(tiempo_simulacion):
        for producto in productos:
            # Cambia la semilla en cada iteración para obtener números aleatorios diferentes
            np.random(tiempo)

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