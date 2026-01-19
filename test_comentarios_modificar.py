# test_comentarios_crud_independiente.py
import pytest
from bs4 import BeautifulSoup
from app import app, pagina  # Importa tu Flask app y la página principal

@pytest.fixture
def client():
    app.config['TESTING'] = True
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
    autor_h3 = soup.find("h3", string="Usuario Test")
    assert autor_h3 is not None, "El comentario no aparece en el HTML tras crearlo"

    div_comentario = autor_h3.find_parent("div")
    texto_limpio = div_comentario.text.replace(" ", "").replace("\n", "")
    assert "★★★★☆" in texto_limpio
