import pytest
from carrito import Carrito

#   CATÁLOGO MOCK PARA TESTS

class CatalogoMock:
    def __init__(self):
        self.productos = []
        self.stock = {}

    def agregar_producto(self, producto, stock):
        self.productos.append(producto)
        self.stock[producto["nombre"]] = stock

    def obtener_stock(self, nombre):
        return self.stock.get(nombre, 0)

    def reducir_stock(self, nombre, cantidad):
        self.stock[nombre] -= cantidad


#   PRODUCTOS DE PRUEBA

producto1 = {
    "nombre": "ChambaPhone X",
    "descripcion": "Smartphone con cámara de 108MP",
    "precio": 999.99,
    "empaquetado": "Caja ecológica",
    "imagen": "chambaphone.png"
}

producto2 = {
    "nombre": "ChambaLaptop Pro",
    "descripcion": "Portátil ultraligero con pantalla Retina",
    "precio": 1299.99,
    "empaquetado": "Estuche protector",
    "imagen": "chambalaptop.png"
}


#   FUNCIÓN AUXILIAR

def crear_carrito_con_catalogo():
    catalogo = CatalogoMock()
    catalogo.agregar_producto(producto1, stock=10)
    catalogo.agregar_producto(producto2, stock=10)
    return Carrito(catalogo), catalogo


#   TESTS DEL CARRITO

def test_añadir_producto():
    carrito, _ = crear_carrito_con_catalogo()
    carrito.añadir_producto(producto1)
    assert len(carrito.productos) == 1
    assert carrito.productos[0]["producto"]["nombre"] == "ChambaPhone X"


def test_eliminar_producto():
    carrito, _ = crear_carrito_con_catalogo()
    carrito.añadir_producto(producto1)
    carrito.añadir_producto(producto2)
    carrito.eliminar_producto(0)
    assert len(carrito.productos) == 1
    assert carrito.productos[0]["producto"]["nombre"] == "ChambaLaptop Pro"


def test_calcular_total():
    carrito, _ = crear_carrito_con_catalogo()
    carrito.añadir_producto(producto1)
    carrito.añadir_producto(producto2)
    total = carrito.calcular_total()
    assert total == pytest.approx(2299.98, 0.01)


def test_vaciar_carrito():
    carrito, _ = crear_carrito_con_catalogo()
    carrito.añadir_producto(producto1)
    carrito.añadir_producto(producto2)
    carrito.vaciar()
    assert len(carrito.productos) == 0


#   TESTS DEL STOCK

def test_no_añadir_sin_stock():
    catalogo = CatalogoMock()
    catalogo.agregar_producto(producto1, stock=0)
    carrito = Carrito(catalogo)

    resultado = carrito.añadir_producto(producto1, 1)

    assert resultado is False
    assert len(carrito.productos) == 0


def test_no_añadir_si_cantidad_supera_stock():
    catalogo = CatalogoMock()
    catalogo.agregar_producto(producto1, stock=2)
    carrito = Carrito(catalogo)

    resultado = carrito.añadir_producto(producto1, 5)

    assert resultado is False
    assert len(carrito.productos) == 0


def test_reducir_stock_al_añadir():
    catalogo = CatalogoMock()
    catalogo.agregar_producto(producto1, stock=5)
    carrito = Carrito(catalogo)

    carrito.añadir_producto(producto1, 2)

    assert catalogo.obtener_stock("ChambaPhone X") == 3
