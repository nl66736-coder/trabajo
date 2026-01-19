import re
import pytest
from bs4 import BeautifulSoup
from Comentarios import app

@pytest.fixture
def client():
    with app.test_client() as client:
        yield client

def test_existe_seccion_contacto(client):
    resp = client.get("/")
    assert resp.status_code == 200

    soup = BeautifulSoup(resp.data, "html.parser")
    assert soup.select_one("section#contacto") is not None, "No existe la sección 'contacto'"

def test_datos_contacto(client):
    resp = client.get("/")
    soup = BeautifulSoup(resp.data, "html.parser")
    contacto = soup.select_one("section#contacto")
    assert contacto is not None, "No existe la sección 'contacto'"
    
    # Título
    h1 = contacto.find("h1")
    assert h1 is not None and h1.text.strip() == "Contacto", "La sección contacto debe tener título"

    # Texto plano de la sección
    texto = contacto.get_text(" ", strip=True)

    texto = contacto.get_text(" ", strip=True)

    # Telefono
    assert re.search(r"tel[eé]fono\s*[:\-]?\s*\d+", texto, re.IGNORECASE), "Debe haber 'Teléfono' y que sea numérico"
    # Email
    assert re.search(r"email\s*[:\-]?\s*[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", texto, re.IGNORECASE), "Debe haber 'Email' y un correo válido"
    # Dirección
    assert re.search(r"direcci[oó]n\s*[:\-]?\s*\S.+", texto, re.IGNORECASE), "Debe haber 'Dirección' y la dirección"
    # Horario
    assert re.search(r"horario\s*[:\-]?.*\d{1,2}:\d{2}.*\d{1,2}:\d{2}", texto, re.IGNORECASE), "Debe haber 'Horario' con horas"