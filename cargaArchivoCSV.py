import csv
import datetime
#Definicion del objeto
class producto:
    def __init__(self,id ,nombre ,precio ,fechaVencimiento,stock):
        self._id = id
        self._nombre = nombre
        self._precio = precio
        self._fechaVencimiento = fechaVencimiento
        self._stock = stock

    @property
    def id(self):
        return self.id

    @property
    def nombre(self):
        return self._nombre

    @property
    def precio(self):
        return self._precio

    @property
    def fechaVencimiento(self):
        return self._fechaVencimiento

    @property
    def stock(self):
        return self._stock

    @fechaVencimiento.setter
    def fechaVencimiento(self, value):
        self._fechaVencimiento = value

    @stock.setter
    def stock(self, value):
        self._stock = value

    #Imprime un objeto de tipo producto
    def mostrarDetalle(self):
        print(f"Imprimiento un objeto por medio de un metodo\n"
              f"ID:{self._id}\n"
              f"Nombre:{self._nombre}\n"
              f"precio:{self._precio}\n"
              f"fechaVencimiento:{self._fechaVencimiento}\n"
              f"stock:{self._stock}\n")
    #cambia la fecha de String a un datetime
    def formatoFecha(self):
        objetoFecha = datetime.datetime.strptime(self._fechaVencimiento, "%m/%d/%y")
        self.fechaVencimiento = objetoFecha


#Carga del archivo
listaProductos = []
with open('productosSimulacion.csv', 'r', newline='') as archivo:
    lectura = csv.reader(archivo, delimiter=',')
    next(lectura)
    for linea in lectura:
        
        listaProductos.append(linea)

#producto1 = producto(1,'platanos',20,'1/12/2023',10)
productos = []
#producto.mostrarDetalle(producto1)
#Tratamiento de datos y creacion de objetos
for datos in listaProductos:
    
    subList = str(datos)
    caracteresProhibidos = " [']"
    textFormateado = subList.translate(str.maketrans('','',caracteresProhibidos))
    atributos = textFormateado.strip().split(",")
    productos.append(producto(*textFormateado.split(",")))
    #productos.append(producto(atributos[0],atributos[1],atributos[2],atributos[3],atributos[4]))
    #print(len(textFormateado))
    #print(str(datos))
    #for i in subList:
        #print(subList)
        #pass


#(len(productos))
def obter_lista_productos():
    return listaProductos

datos_lista = obter_lista_productos()

lista_de_diccionarios = []

for datos in datos_lista:
    nuevo_diccionario = {
        'id': int(datos[0]),
        'nombre': datos[1],
        'precio_producto': float(datos[2]),
        'fecha_vencimiento': datos[3],
        'inventario': int(datos[4]),
        'ganancias_acumuladas': 0,
        'perdida_acumulada': 0,
        'productos_vendidos': [],
        'tasa_reabastecimiento':20,
        'estado_producto': 0
    }
    lista_de_diccionarios.append(nuevo_diccionario)

def dic_lista_productos():
    return lista_de_diccionarios