# test_catalogo.py
import pytest
import os
from catalogo import CatalogoProductos
from render_html import RenderHTML

def test_agregar_producto(tmp_path):
    """
    Verifica que se puede agregar un producto y que se guarda correctamente en JSON,
    incluyendo el nuevo campo 'comentarios'.
    """
    archivo_test = tmp_path / "catalogo_test.json"
    catalogo = CatalogoProductos(str(archivo_test))

    catalogo.agregar_producto(
        "ChambaMouse",
        "Ratón ergonómico con sensor óptico",
        29.99,
        "Caja reciclable",
        "/static/chambamouse.png"
    )

    assert len(catalogo.productos) == 1
    assert catalogo.productos[0]["nombre"] == "ChambaMouse"
    assert catalogo.productos[0]["imagen"] == "/static/chambamouse.png"

    # ✅ Nuevo: comentarios inicializados
    assert "comentarios" in catalogo.productos[0]
    assert isinstance(catalogo.productos[0]["comentarios"], list)
    assert catalogo.productos[0]["comentarios"] == []

    assert archivo_test.exists()


def test_agregar_comentario_y_guardar_en_json(tmp_path):
    """
    Verifica que se puede añadir un comentario a un producto y que se persiste en JSON.
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

    ok = catalogo.agregar_comentario_por_indice(
        0,
        "Mael",
        "Se ve increíble, muy buena calidad."
    )
    assert ok is True

    # ✅ En memoria
    assert len(catalogo.productos[0]["comentarios"]) == 1
    comentario = catalogo.productos[0]["comentarios"][0]
    assert comentario["autor"] == "Mael"
    assert "muy buena calidad" in comentario["texto"]
    assert "fecha" in comentario  # la fecha la genera el método

    # ✅ Persistencia: recargar desde el JSON y comprobar que sigue
    catalogo2 = CatalogoProductos(str(archivo_test))
    assert len(catalogo2.productos) == 1
    assert len(catalogo2.productos[0]["comentarios"]) == 1
    assert catalogo2.productos[0]["comentarios"][0]["autor"] == "Mael"


def test_render_html_incluye_comentarios(tmp_path):
    """
    Verifica que el HTML generado contiene los datos del producto y el texto de reseñas.
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

    catalogo.agregar_comentario_por_indice(
        0,
        "Usuario1",
        "Me encanta cómo se ve el 4K."
    )

    # ✅ Render real (el que se usa en la web)
    html = RenderHTML.render_seccion_catalogo(catalogo.productos)

    assert "ChambaVision 4K" in html
    assert "Televisión inteligente" in html
    assert "499.99" in html
    assert "/static/chambavision.png" in html

    # ✅ El comentario debe aparecer en el HTML
    assert "Usuario1" in html
    assert "Me encanta cómo se ve el 4K." in html