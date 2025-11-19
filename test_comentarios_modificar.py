# test_comentarios_crud_independiente.py
import pytest
from bs4 import BeautifulSoup
from Comentarios import app, pagina  # Importa tu Flask app y la página principal

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_agregar_editar_eliminar_comentario(client):
    """Simula agregar, editar y eliminar un comentario sin tocar archivos originales"""

    # -------------------------
    # Agregar un comentario
    # -------------------------
    nuevo_comentario = {
        "autor": "Usuario Test",
        "texto": "Comentario de prueba",
        "valoracion": "4"
    }
    resp = client.post("/comentar", data=nuevo_comentario, follow_redirects=True)
    assert resp.status_code == 200

    # Comprobar que se añadió
    soup = BeautifulSoup(resp.data, "html.parser")
    div_comentario = soup.find("h3", string="Usuario Test").find_parent("div")
    assert div_comentario is not None, "No se encontró el comentario agregado"
    assert "★★★★☆" in div_comentario.text.replace(" ", ""), "Valoración incorrecta"

    # -------------------------
    # Editar el comentario
    # -------------------------
    indice = len(pagina.seccion_comentarios.comentarios) - 1  # Último agregado
    datos_editar = {
        "texto": "Comentario editado",
        "valoracion": "5"
    }
    resp_edit = client.post(f"/editar/{indice}", data=datos_editar, follow_redirects=True)
    assert resp_edit.status_code == 200

    # Comprobar que se editó correctamente
    soup_edit = BeautifulSoup(resp_edit.data, "html.parser")
    div_editado = soup_edit.find("h3", string="Usuario Test").find_parent("div")
    assert "Comentario editado" in div_editado.text, "El comentario no se editó"
    assert "★★★★★" in div_editado.text.replace(" ", ""), "Valoración editada incorrecta"

    # -------------------------
    # Eliminar el comentario
    # -------------------------
    resp_delete = client.post(f"/eliminar/{indice}", follow_redirects=True)
    assert resp_delete.status_code == 200

    # Comprobar que se eliminó
    soup_delete = BeautifulSoup(resp_delete.data, "html.parser")
    div_eliminado = soup_delete.find("h3", string="Usuario Test")
    assert div_eliminado is None, "El comentario no se eliminó"
