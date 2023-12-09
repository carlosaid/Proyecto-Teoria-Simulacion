import numpy as np
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
from cargaArchivoCSV import dic_lista_productos
from collections import deque
import time

#obtener datos del CSV
productos = dic_lista_productos()

# Imprimir el estado actual de las colas
colas_reabastecimiento = {producto['nombre']: deque([producto.copy()]) for producto in productos}
#print(colas_reabastecimiento)

# Imprimir inventario inicial
print("Inventario inicial por producto:")
inventario_strings = []
for producto in productos:
    inventario_strings = [f"{producto['nombre']}: {producto['inventario']} unidades" for producto in productos]
print(", ".join(inventario_strings))

# Solicitar entrada del usuario para tasa_reabastecimiento y meses_simulacion
tasa_reabastecimiento = int(input("Ingrese la tasa de reabastecimiento: "))
meses_simulacion = int(input("Ingrese la cantidad de meses para simular: "))

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

        for producto_nombre, cola_producto in colas_reabastecimiento.items():
            # Obtener el primer elemento de la cola (si existe)
            if cola_producto:
                producto = cola_producto[0]
                fecha_vencimiento = datetime.strptime(producto['fecha_vencimiento'], '%Y-%m-%d')

                fecha_vecimiento = datetime.strptime(producto['fecha_vencimiento'], '%Y-%m-%d')
                if fecha_vecimiento <= fecha_actual:
                    print(f"Mes {mes}, Producto {producto['nombre']}: Producto vencido, inventario: {producto['inventario']}, se ha perdido, Fecha actual: {fecha_actual.strftime('%Y-%m-%d')}")
                    if(producto['estado_producto'] == 0):
                        perdida_mes += producto['inventario'] * producto['precio_producto']  # Calcular la pérdida por el inventario restante
                        productos_vencidos_mes[producto['nombre']] = producto['inventario']  # Registrar la # Obtener la cantidad de productos que quedaron sin venderse antes de eliminar el elemento
                        # Obtener la cantidad de productos que quedaron sin venderse antes de eliminar el elemento
                        inventario_restante = producto['inventario']
                        print(f"El producto {producto['nombre']} ha vencido. Cantidad no vendida: {inventario_restante} unidades.")

                        # Eliminar el producto vencido de la cola
                        producto_vencido = cola_producto.popleft()
                        print(f"El producto {producto_vencido['nombre']} ha sido eliminado de la cola.")
                        
                        # Hacer un nuevo pedido para el producto vencido
                        nuevo_producto = producto.copy()
                        nuevo_producto['inventario'] += tasa_reabastecimiento
                        nuevo_producto['fecha_vencimiento'] = (fecha_actual + timedelta(days=np.random.randint(150, 300))).strftime('%Y-%m-%d')
                        nuevo_producto['estado_producto'] = 0  # Actualizar el estado del nuevo producto a no vencido
                        cola_producto.append(nuevo_producto)
                        print(f"Se ha realizado un nuevo pedido para el producto {nuevo_producto['nombre']}.")

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
                    nuevo_producto = producto.copy()
                    nuevo_producto['fecha_vencimiento'] = (fecha_actual + timedelta(days=np.random.randint(150, 300))).strftime('%Y-%m-%d')
                    cola_producto.append(nuevo_producto)
                    print(f"Mes {mes}, Producto {producto['nombre']}: Se ha hecho un nuevo pedido. Inventario actualizado a {producto['inventario']} unidades.")
                    

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
        
        time.sleep(1)

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
    
simular_productos_perecederos(productos, tasa_reabastecimiento, meses_simulacion)