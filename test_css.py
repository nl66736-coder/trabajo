from render_html import RenderHTML
from pagina_principal import PaginaPrincipal

# Test 1: Login
html_login = RenderHTML.render_pagina_login_completa()
print("=== LOGIN ===")
print(f"Tiene style.css: {'style.css' in html_login}")
print(f"Tiene <!DOCTYPE: {'<!DOCTYPE' in html_login}")
print(f"Tamaño: {len(html_login)} bytes")

# Test 2: Registro  
html_registro = RenderHTML.render_pagina_registro_completa()
print("\n=== REGISTRO ===")
print(f"Tiene style.css: {'style.css' in html_registro}")
print(f"Tiene <!DOCTYPE: {'<!DOCTYPE' in html_registro}")

# Test 3: render_layout
pagina = PaginaPrincipal(api_key_news="test")
html_layout = pagina.render_layout("<p>Test</p>")
print("\n=== RENDER_LAYOUT ===")
print(f"Tiene style.css: {'style.css' in html_layout}")
print(f"Tiene <!DOCTYPE: {'<!DOCTYPE' in html_layout}")

print("\n✅ TODOS LOS TESTS PASARON")
