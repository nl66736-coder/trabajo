import pytest
from bs4 import BeautifulSoup
from app import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_existe_menu_navegacion(client):
    resp = client.get("/")
    assert resp.status_code == 200

    soup = BeautifulSoup(resp.data, "html.parser")
    nav = soup.select_one("nav")
    
    assert nav is not None, "No existe el menú de navegación con id='menu'"

def test_enlaces_menu_navegacion(client):
    resp = client.get("/")
    assert resp.status_code == 200

    soup = BeautifulSoup(resp.data, "html.parser")
    nav = soup.select_one("nav")
    assert nav is not None, "No existe el menú de navegación con id='menu'"

    links = {a.text.strip().lower(): a.get("href") for a in nav.find_all("a")}

    assert "inicio" in links, "El menú debe incluir enlace a 'Inicio'"
    assert "contacto" in links, "El menú debe incluir enlace a 'Contacto'"
    assert "comentarios" in links, "El menú debe incluir enlace a 'Comentarios'"

    assert links["inicio"] == "#inicio", "El enlace 'Inicio' debe apuntar a #inicio"
    assert links["contacto"] == "#contacto", "El enlace 'Contacto' debe apuntar a #contacto"
    assert links["comentarios"] == "#comentarios", "El enlace 'Comentarios' debe apuntar a #comentarios"
