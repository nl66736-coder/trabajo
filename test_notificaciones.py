import pytest
import json
import os
from datetime import datetime
from pagina_principal import SeccionNotificaciones


# -------------------------------------------------------
# FIXTURES
# -------------------------------------------------------

@pytest.fixture
def archivo_tmp(tmp_path):
    return tmp_path / "historial.json"

@pytest.fixture
def seccion(archivo_tmp):
    return SeccionNotificaciones(archivo=str(archivo_tmp))


# -------------------------------------------------------
# TEST cargar / guardar historial
# -------------------------------------------------------

def test_guardar_y_cargar_historial(seccion, archivo_tmp):
    data = {"user1": {"notificaciones": []}}
    seccion.guardar_historial(data)

    assert os.path.exists(archivo_tmp)
    
    cargado = seccion.cargar_historial()
    assert cargado == data


def test_cargar_historial_inexistente(seccion):
    assert seccion.cargar_historial() == {}


# -------------------------------------------------------
# TEST agregar / obtener / limpiar notificaciones
# -------------------------------------------------------

def test_agregar_notificacion(seccion):
    # Inicializa el usuario en el historial
    historial = {"laura": {"notificaciones": [], "preferencias": {"recibir_notificaciones": True}}}
    seccion.guardar_historial(historial)

    # Ahora sí se puede agregar la notificación
    seccion.agregar_notificacion("laura", "Hola")

    notificaciones = seccion.obtener_notificaciones("laura")
    assert len(notificaciones) == 1
    assert notificaciones[0]["texto"] == "Hola"


def test_limpiar_notificaciones(seccion):
    seccion.agregar_notificacion("laura", "Hola")
    seccion.limpiar_notificaciones("laura")

    assert seccion.obtener_notificaciones("laura") == []


# -------------------------------------------------------
# TEST detectar categoría
# -------------------------------------------------------

@pytest.mark.parametrize(
    "nombre,categoria",
    [
        ("iPhone 14", "Smartphones"),
        ("Laptop HP", "Portátiles"),
        ("Galaxy Watch", "Smartwatches"),
        ("Auriculares Sony", "Audio"),
        ("Tablet Lenovo", "Tablets"),
        ("Cargador USB", "General")
    ]
)
def test_detectar_categoria_producto(seccion, nombre, categoria):
    assert seccion.detectar_categoria_producto(nombre) == categoria


# -------------------------------------------------------
# TEST analizar historial de compras
# -------------------------------------------------------

def test_analizar_historial_compras(seccion):
    historial = {
        "laura": {
            "compras": [
                {
                    "estado": "finalizada",
                    "productos": [
                        {"nombre": "iPhone 14", "precio": 999, "cantidad": 1},
                        {"nombre": "Auriculares Sony", "precio": 50, "cantidad": 2}
                    ]
                }
            ]
        }
    }

    seccion.guardar_historial(historial)
    analisis = seccion.analizar_historial_compras("laura")

    assert analisis["total_compras"] == 1
    assert "iPhone 14" in analisis["productos_comprados_nombres"]
    assert "Auriculares Sony" in analisis["productos_comprados_nombres"]
    assert "Smartphones" in analisis["categorias_preferidas"]
    assert analisis["gasto_total"] == 999 + (50 * 2)


def test_analizar_compras_usuario_sin_compras(seccion):
    seccion.guardar_historial({"laura": {"compras": []}})
    analisis = seccion.analizar_historial_compras("laura")

    assert analisis["total_compras"] == 0
    assert analisis["gasto_total"] == 0


# -------------------------------------------------------
# TEST generar recomendaciones
# -------------------------------------------------------

def test_recomendaciones_usuario_nuevo(seccion):
    catalogo = [
        {"nombre": "iPhone 14"},
        {"nombre": "Laptop HP"},
        {"nombre": "Galaxy Watch"},
        {"nombre": "Cargador USB"}
    ]

    seccion.guardar_historial({"pepe": {"compras": []}})
    rec = seccion.generar_recomendaciones("pepe", catalogo)

    assert len(rec) == 3
    assert rec == catalogo[:3]


def test_recomendaciones_por_categoria(seccion):
    historial = {
        "laura": {
            "compras": [
                {
                    "estado": "finalizada",
                    "productos": [
                        {"nombre": "Laptop HP", "precio": 900, "cantidad": 1}
                    ]
                }
            ]
        }
    }

    seccion.guardar_historial(historial)

    catalogo = [
        {"nombre": "Laptop Lenovo"},
        {"nombre": "iPhone 14"},
        {"nombre": "Galaxy Watch"},
        {"nombre": "Auriculares Sony"}
    ]

    rec = seccion.generar_recomendaciones("laura", catalogo)

    assert rec[0]["nombre"] == "Laptop Lenovo"


# -------------------------------------------------------
# TEST notificar_nuevo_producto
# -------------------------------------------------------

def notificar_nuevo_producto(self, producto, usuarios_registrados):
    historial = self.cargar_historial()

    # SIEMPRE existe
    usuarios_relevantes = []

    for usuario in usuarios_registrados:
        if usuario in historial:
            usuarios_relevantes.append(usuario)

    for usuario in usuarios_relevantes:
        texto = f"Nuevo producto disponible: {producto['nombre']}"
        self.agregar_notificacion(usuario, texto)



# -------------------------------------------------------
# TEST generar_notificaciones_recomendaciones
# -------------------------------------------------------
def generar_notificaciones_recomendaciones(self, usuario, catalogo_productos):
    recomendaciones = self.generar_recomendaciones(usuario, catalogo_productos)

    for producto in recomendaciones:
        texto = f"Recomendación para ti: {producto['nombre']}"
        self.agregar_notificacion(usuario, texto)




# -------------------------------------------------------
# TEST analizar comentarios
# -------------------------------------------------------

def test_analizar_comentarios_usuario(seccion):
    comentarios = [
        ("laura", "Excelente móvil, muy rápido", 5, "01/01/2025"),
        ("pepe", "Buen sonido", 4, "01/01/2025"),
        ("laura", "La batería del teléfono dura mucho", 4, "02/01/2025")
    ]

    res = seccion.analizar_comentarios_usuario("laura", comentarios)

    assert res["total_comentarios"] == 2
    assert res["valoracion_promedio"] == 4.5
    assert "Movil" in res["productos_mencionados"]

# -------------------------------------------------------
# TEST notificaciones solo si activadas
# -------------------------------------------------------

def test_notificaciones_solo_si_activadas(seccion):
    historial = {
        "marta": {
            "compras": [],
            "notificaciones": [],
            "preferencias": {"recibir_notificaciones": False}  # usuario que no quiere notificaciones
        }
    }
    seccion.guardar_historial(historial)

    seccion.agregar_notificacion("marta", "Mensaje importante")
    notificaciones = seccion.obtener_notificaciones("marta")
    
    # Como usuario no quiere notificaciones, debería estar vacío
    assert notificaciones == []

# -------------------------------------------------------
# TEST notificación de bienvenida al registrarse
# -------------------------------------------------------


def test_notificacion_bienvenida(seccion):
    historial = {
        "ana": {
            "compras": [],
            "notificaciones": [],
            "preferencias": {"recibir_notificaciones": True}
        }
    }
    seccion.guardar_historial(historial)

    # Simula registro
    seccion.agregar_notificacion("ana", "¡Bienvenido a Chamba Store! Gracias por registrarte.")

    notifs = seccion.obtener_notificaciones("ana")
    assert len(notifs) == 1
    assert "Bienvenido" in notifs[0]["texto"]
