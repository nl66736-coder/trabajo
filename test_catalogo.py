# test_catalogo.py
import pytest
import os
from catalogo import CatalogoProductos

def test_agregar_producto(tmp_path):
    """
    Verifica que se puede agregar un producto y que se guarda correctamente en JSON.
    """
    # Usamos un archivo temporal para no tocar el catálogo real
    archivo_test = tmp_path / "catalogo_test.json"
    catalogo = CatalogoProductos(str(archivo_test))

    # Agregamos un producto de prueba
    catalogo.agregar_producto(
        "ChambaMouse",
        "Ratón ergonómico con sensor óptico",
        29.99,
        "Caja reciclable",
        "/static/chambamouse.png"
    )

    # Comprobamos que el producto se añadió en memoria
    assert len(catalogo.productos) == 1
    assert catalogo.productos[0]["nombre"] == "ChambaMouse"
    assert catalogo.productos[0]["imagen"] == "/static/chambamouse.png"

    # Comprobamos que el archivo JSON se creó
    assert archivo_test.exists()

def test_render_html(tmp_path):
    """
    Verifica que el HTML generado contiene los datos del producto.
    """
    archivo_test = tmp_path / "catalogo_test.json"
    catalogo = CatalogoProductos(str(archivo_test))

    catalogo.agregar_producto(
        "ChambaVision 4K",
        "Televisión inteligente con colores vivos",
        499.99,
        "Caja premium",
        "/static/chambavision.png"
    )

    html = catalogo.render()

    # Comprobamos que el HTML contiene los datos del producto
    assert "ChambaVision 4K" in html
    assert "Televisión inteligente" in html
    assert "499.99" in html
    assert "/static/chambavision.png" in html
