import pytest
from pagina_principal import SeccionTendencias

# ---------------------------
#  TEST: Sin API Key
# ---------------------------
def test_sin_api_key_no_tendencias():
    st = SeccionTendencias(api_key=None)
    st.actualizar_tendencias()

    assert st.tendencias == [], "Si no hay API key debe dejar tendencias vacías"


# ---------------------------
#  TEST: API OK → devuelve 5 artículos
# ---------------------------
def test_actualizar_tendencias_api_ok(monkeypatch):

    respuesta_fake = {
        "articles": [
            {"title": "Noticia 1", "description": "Desc 1", "url": "http://1"},
            {"title": "Noticia 2", "description": "Desc 2", "url": "http://2"},
            {"title": "Noticia 3", "description": "Desc 3", "url": "http://3"},
            {"title": "Noticia 4", "description": "Desc 4", "url": "http://4"},
            {"title": "Noticia 5", "description": "Desc 5", "url": "http://5"},
        ]
    }

    class MockResponse:
        def json(self):
            return respuesta_fake

    def mock_get(url):
        return MockResponse()

    # IMPORTANTE → apuntar al módulo correcto
    monkeypatch.setattr("pagina_principal.requests.get", mock_get)

    st = SeccionTendencias(api_key="abc123")
    st.actualizar_tendencias()

    assert len(st.tendencias) == 5
    assert st.tendencias[0]["titulo"] == "Noticia 1"


# ---------------------------
#  TEST: API devuelve JSON sin "articles"
# ---------------------------
def test_api_sin_articles(monkeypatch):

    class MockResponse:
        def json(self):
            return {}  # sin "articles"

    def mock_get(url):
        return MockResponse()

    monkeypatch.setattr("pagina_principal.requests.get", mock_get)

    st = SeccionTendencias(api_key="abc123")
    st.actualizar_tendencias()

    assert st.tendencias == [], "Si no hay 'articles', tendencias debe quedar vacío"


# ---------------------------
#  TEST: Error en la API
# ---------------------------
def test_api_error(monkeypatch):

    def mock_get(url):
        raise Exception("Error simulado")

    monkeypatch.setattr("pagina_principal.requests.get", mock_get)

    st = SeccionTendencias(api_key="abc123")
    st.actualizar_tendencias()

    assert st.tendencias == [], "Si hay un error, tendencias debe quedar vacío"


# ---------------------------
#  TEST: Render SIN tendencias
# ---------------------------
def test_render_sin_tendencias():
    st = SeccionTendencias(api_key=None)
    st.tendencias = []  # forzamos vacío

    html = st.render()
    assert "No hay tendencias relevantes disponibles" in html


# ---------------------------
#  TEST: Render CON tendencias
# ---------------------------
def test_render_con_tendencias():
    st = SeccionTendencias(api_key="abc")
    st.tendencias = [
        {"titulo": "A", "descripcion": "B", "url": "http://x"}
    ]

    html = st.render()

    assert "<h3>A</h3>" in html
    assert "<p>B</p>" in html
    assert 'href="http://x"' in html
