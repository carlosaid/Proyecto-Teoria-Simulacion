import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from cargaArchivoCSV import dic_lista_productos
from collections import deque

productos = dic_lista_productos()

# Imprimir inventario inicial
print("Inventario inicial por producto:")
inventario_strings = []
for producto in productos:
    inventario_strings = [f"{producto['nombre']}: {producto['inventario']} unidades" for producto in productos]
print(", ".join(inventario_strings))

def simular_productos_perecederos(productos, tasa_reabastecimiento, meses_simulacion):
    fecha_actual = datetime.now()
    ganancias_totales = 0
    perdida_acumulada = 0
    productos_vencidos_acumulados = {}  # Diccionario para acumular la cantidad de productos vencidos por tipo
    productos_vendidos_acumulados = {}  # Diccionario para acumular la cantidad de productos vendidos por tipo
    
    for mes in range(1, meses_simulacion + 1):
        # Obtener la fecha actual al principio de cada mes
        fecha_actual += timedelta(days=30)  # Asumiendo un mes de 30 días
        ganancias_mes = 0  # Inicializar ganancias_mes para el mes actual
        perdida_mes = 0
        productos_vencidos_mes = {}  # Diccionario para contar la cantidad de productos vencidos por tipo en el mes actual
        productos_vendidos_mes = {}  # Diccionario para contar la cantidad de productos vendidos por tipo en el mes actual
        id_producto_vencidos = {}

        for producto in productos:
            fecha_vecimiento = datetime.strptime(producto['fecha_vencimiento'], '%Y-%m-%d')
            if fecha_vecimiento <= fecha_actual:
                print(f"Mes {mes}, Producto {producto['nombre']}: Producto vencido, inventario: {producto['inventario']}, se ha perdido, Fecha actual: {fecha_actual.strftime('%Y-%m-%d')}")
                if(producto['estado_producto'] == 0):
                    perdida_mes += producto['inventario'] * producto['precio_producto']  # Calcular la pérdida por el inventario restante
                    productos_vencidos_mes[producto['nombre']] = producto['inventario']  # Registrar la cantidad de productos vencidos por tipo
                    # Calcular el reabastecimiento en función de la cantidad restante en el inventario vencido
                    reabastecimiento = min(tasa_reabastecimiento, producto['inventario'])
                    producto['inventario'] = 0
                    # Hacer un nuevo pedido para el producto vencido
                    dias_reabastecimiento = np.random.randint(150, 180)
                    producto['inventario'] += tasa_reabastecimiento
                    producto['fecha_vencimiento'] = (fecha_actual + timedelta(days=dias_reabastecimiento)).strftime('%Y-%m-%d')
                    producto['estado_producto'] = 1
                    continue  # Saltar el procesamiento del producto vencido

            # Simular ventas y ajustar inventario
            if(producto['estado_producto'] == 0):
                # Generar demanda aleatoria solo si el producto no ha vencido
                demanda = np.random.poisson(lam=20)  # Ajusta la tasa de demanda según tus necesidades
                ventas = min(demanda, producto['inventario'])
                producto['inventario'] -= ventas

                # Calcular ganancias y registrar productos vendidos
                ganancias_mes += ventas * producto['precio_producto']
                producto['ganancias_acumuladas'] += ventas * producto['precio_producto']
                productos_vendidos_mes[producto['nombre']] = ventas  # Registrar la cantidad de productos vendidos por tipo en este mes

            # Reabastecer el inventario si es necesario
            if producto['inventario'] <= tasa_reabastecimiento:
                # Calcular el reabastecimiento en función de la tasa_reabastecimiento
                reabastecimiento = tasa_reabastecimiento
                producto['inventario'] += reabastecimiento
                # Hacer un nuevo pedido para el producto reabastecido
                producto['fecha_vencimiento'] = (fecha_actual + timedelta(days=np.random.randint(150, 300))).strftime('%Y-%m-%d')

            print(f"Mes {mes}, Producto {producto['nombre']}: Demand: {demanda}, Ventas: {ventas}, Inventario: {producto['inventario']}, Ganancias: {producto['ganancias_acumuladas']}, Fecha de vencimiento: {fecha_vecimiento}, Fecha actual: {fecha_actual.strftime('%Y-%m-%d')}")

        # Imprimir la pérdida total del mes
        print(f"Pérdida total del mes {mes}: {perdida_mes}")
        # Imprimir las ganancias totales del mes
        print(f"Ganancias totales del mes {mes}: {ganancias_mes}")

        # Acumular las ganancias, pérdidas y productos vencidos al final de cada mes
        ganancias_totales += ganancias_mes
        perdida_acumulada += perdida_mes

        # Actualizar los diccionarios de productos vendidos y vencidos acumulados
        for nombre, cantidad in productos_vencidos_mes.items():
            if nombre in productos_vencidos_acumulados:
                productos_vencidos_acumulados[nombre] += cantidad
            else:
                productos_vencidos_acumulados[nombre] = cantidad

        for nombre, cantidad in productos_vendidos_mes.items():
            if nombre in productos_vendidos_acumulados:
                productos_vendidos_acumulados[nombre] += cantidad
            else:
                productos_vendidos_acumulados[nombre] = cantidad

    # Imprimir la pérdida acumulada al final de la simulación
    print(f"Pérdida acumulada al final de la simulación: {perdida_acumulada}")
    # Imprimir la cantidad total de productos vencidos por tipo al final de la simulación
    print("Productos vencidos totales por tipo al final de la simulación:")
    for nombre, cantidad in productos_vencidos_acumulados.items():
        print(f"{nombre}: {cantidad}")
    # Imprimir la cantidad total de productos vendidos por tipo al final de la simulación
    print("Productos vendidos totales por tipo al final de la simulación:")
    for nombre, cantidad in productos_vendidos_acumulados.items():
        print(f"{nombre}: {cantidad}")
        
    print("\nInventario final por producto:")
    inventario_strings = [f"{producto['nombre']}: {producto['inventario']} unidades" for producto in productos]
    print(", ".join(inventario_strings))
    
    # Generar gráficos al final de la simulación
    etiquetas_resumen = ["Ganancias", "Pérdida"]
    valores_resumen = [ganancias_totales, perdida_acumulada]

    # Filtrar solo los productos vencidos para la gráfica correspondiente
    etiquetas_productos_vencidos = [nombre for nombre, cantidad in productos_vencidos_acumulados.items()]
    valores_productos_vencidos = [cantidad for nombre, cantidad in productos_vencidos_acumulados.items()]

    plt.figure(figsize=(15, 5))

    # Gráfico de resumen
    plt.subplot(1, 3, 1)
    plt.bar(etiquetas_resumen, valores_resumen, color=['green', 'red'])
    plt.title("Resumen de la Simulación")
    plt.xlabel("Categoría")
    plt.ylabel("Cantidad")

    # Gráfico de productos vendidos
    plt.subplot(1, 3, 2)
    plt.bar(productos_vendidos_acumulados.keys(), productos_vendidos_acumulados.values(), color='blue', alpha=0.7)
    plt.title("Productos Vendidos Totales")
    plt.xlabel("Producto")
    plt.ylabel("Cantidad")

    # Gráfico de productos vencidos
    plt.subplot(1, 3, 3)
    plt.bar(etiquetas_productos_vencidos, valores_productos_vencidos, color='gray', alpha=0.7)
    plt.title("Productos Vencidos Totales")
    plt.xlabel("Producto")
    plt.ylabel("Cantidad")

    plt.tight_layout()
    plt.show()

# Simular la gestión de productos perecederos
simular_productos_perecederos(productos, tasa_reabastecimiento=20, meses_simulacion=6)