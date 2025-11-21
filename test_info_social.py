import pytest
from pagina_principal import SeccionInfoSocial


def test_inicializacion_vacia():
    info = SeccionInfoSocial()

    assert info.razon_social is None
    assert info.forma_juridica is None
    assert info.cif_nif is None
    assert info.domicilio_social is None
    assert info.capital_social is None
    assert info.numero_registro is None


def test_establecer_datos():
    info = SeccionInfoSocial()

    info.establecer_razon_social("ChambaTech S.L.")
    info.establecer_forma_juridica("S.L.")
    info.establecer_cif_nif("B12345678")
    info.establecer_domicilio_social("C/ Ejemplo 123, Madrid")
    info.establecer_capital_social("20.000€")
    info.establecer_numero_registro("Tomo 123, Folio 456")

    assert info.razon_social == "ChambaTech S.L."
    assert info.forma_juridica == "S.L."
    assert info.cif_nif == "B12345678"
    assert info.domicilio_social == "C/ Ejemplo 123, Madrid"
    assert info.capital_social == "20.000€"
    assert info.numero_registro == "Tomo 123, Folio 456"


def test_render_con_todo():
    info = SeccionInfoSocial()

    info.establecer_razon_social("ChambaTech S.L.")
    info.establecer_forma_juridica("S.L.")
    info.establecer_cif_nif("B12345678")
    info.establecer_domicilio_social("C/ Ejemplo 123, Madrid")
    info.establecer_capital_social("20.000€")
    info.establecer_numero_registro("Tomo 123, Folio 456")

    html = info.render()

    assert "<strong>Razón social:</strong> ChambaTech S.L." in html
    assert "<strong>Forma jurídica:</strong> S.L." in html
    assert "<strong>CIF/NIF:</strong> B12345678" in html
    assert "<strong>Domicilio social:</strong> C/ Ejemplo 123, Madrid" in html
    assert "<strong>Capital social:</strong> 20.000€" in html
    assert "<strong>Número de registro:</strong> Tomo 123, Folio 456" in html


def test_render_vacio():
    info = SeccionInfoSocial()

    html = info.render()

    # Debe contener la estructura básica
    assert "<section id='info-social'>" in html
    assert "<h2>Información social de la empresa</h2>" in html
    assert "<ul>" in html

    # No debe tener ningún <li> porque no hay datos
    assert "<li>" not in html
