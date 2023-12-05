from productos import generar_producto
from simulacion import ejecutar_simulacion

# Definición de productos
productos_definidos = [
    generar_producto('producto_A', 20, 7, 0.5),
    generar_producto('producto_B', 15, 5, 0.7),
    # Puedes agregar más productos según sea necesario
]

# Ejecutar la simulación
tiempo_simulacion = 365
perdidas, total_costos = ejecutar_simulacion(tiempo_simulacion, productos_definidos)

# Imprimir resultados
for producto_nombre, cantidad_perdida in perdidas.items():
    print(f"Unidades perdidas para {producto_nombre}: {cantidad_perdida}")
print(f"Costo total: {total_costos}")