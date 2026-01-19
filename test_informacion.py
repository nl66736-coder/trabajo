#Realizado por:
#Marina Martinez Andaluz
#Laura Gómez Patino
#24/12/2025
import pytest
from bs4 import BeautifulSoup
from Comentarios import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_existe_seccion_informacion(client):
    resp = client.get("/")
    assert resp.status_code == 200

    soup = BeautifulSoup(resp.data, "html.parser")
    assert soup.select_one("section#informacion") is not None, "No existe la sección 'informacion'"

def test_datos_informacion(client):
    resp = client.get("/")
    assert resp.status_code == 200
    soup = BeautifulSoup(resp.data, "html.parser")
    info = soup.select_one("section#informacion")
    assert info is not None, "No existe la sección 'informacion'"

    # Nombre
    h1 = info.find("h1")
    assert h1 and h1.text.strip(), "Falta el nombre de la tienda"

    # Logo
    img = info.find("img")
    assert img is not None, "Falta el log de la tienda"
    assert img.get("src"), "El logo debe tener atributo src"
    assert img.get("alt"), "El logo debe tener atributo alt"

    # Descripción 
    p = info.find("p")
    assert p is not None and p.text.strip(), "Falta la descripción de la tienda"
