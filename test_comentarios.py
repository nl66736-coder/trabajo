# test_comentarios.py
import re
import pytest
from bs4 import BeautifulSoup
from Comentarios import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_comentarios_listan_nombre_texto_valoracion_y_fecha(client):
    """Comprueba que los comentarios muestran nombre, texto, valoración y fecha/hora"""
    resp = client.get("/")
    assert resp.status_code == 200
    soup = BeautifulSoup(resp.data, "html.parser")
    comentarios = soup.select("#comentarios div")
    assert comentarios, "No hay comentarios listados"

    patron_fecha = re.compile(r"\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}")
    for c in comentarios:
        assert c.find("h3"), "Falta el nombre del autor"
        assert c.find("p"), "Falta el texto del comentario"
        val = c.find_all("p")[-1].text
        assert "Valoración:" in val and ("★" in val or "☆" in val), "Valoración incorrecta"
        fecha = c.find("small")
        assert fecha and "Publicado el" in fecha.text and patron_fecha.search(fecha.text), "Fecha no válida"

def test_agregar_comentario_muestra_fecha_y_valoracion(client):
    """Comprueba que al enviar un comentario nuevo aparece con fecha y valoración"""
    data = {"autor": "Test User", "texto": "Comentario de prueba", "valoracion": "4"}
    resp = client.post("/comentar", data=data, follow_redirects=True)
    soup = BeautifulSoup(resp.data, "html.parser")
    nuevo = soup.find("h3", string="Test User").find_parent("div")
    assert nuevo, "No se encontró el comentario añadido"
    assert "★★★★☆" in nuevo.text.replace(" ", ""), "La valoración no coincide con 4 estrellas"
    assert re.search(r"\d{2}/\d{2}/\d{4}\s\d{2}:\d{2}", nuevo.text), "No se muestra la fecha/hora"