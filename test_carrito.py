import pytest
from carrito import Carrito

# Creamos un producto de prueba como diccionario
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

def test_añadir_producto():
    carrito = Carrito()
    carrito.añadir_producto(producto1)
    assert len(carrito.productos) == 1
    assert carrito.productos[0]["nombre"] == "ChambaPhone X"

def test_eliminar_producto():
    carrito = Carrito()
    carrito.añadir_producto(producto1)
    carrito.añadir_producto(producto2)
    carrito.eliminar_producto(0)
    assert len(carrito.productos) == 1
    assert carrito.productos[0]["nombre"] == "ChambaLaptop Pro"

def test_calcular_total():
    carrito = Carrito()
    carrito.añadir_producto(producto1)
    carrito.añadir_producto(producto2)
    total = carrito.calcular_total()
    assert total == pytest.approx(2299.98, 0.01)

def test_vaciar_carrito():
    carrito = Carrito()
    carrito.añadir_producto(producto1)
    carrito.añadir_producto(producto2)
    carrito.vaciar()
    assert len(carrito.productos) == 0
