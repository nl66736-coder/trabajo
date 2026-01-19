from pagina_principal import PaginaPrincipal
p = PaginaPrincipal(api_key_news='test')
p.construir()
body = p.seccion_catalogo.render()
html = "<!DOCTYPE html>\n<html><head><meta charset='utf-8'><meta name='viewport' content='width=device-width,initial-scale=1.0'><link rel='stylesheet' href='/static/style.css'></head><body>"+body+"</body></html>"
with open('salida_catalogo_simple.html','w',encoding='utf-8') as f:
    f.write(html)
print('WROTE salida_catalogo_simple.html')
print('HAS_CSS', 'style.css' in html)
print('HAS_PRODUCTO_ITEM', 'producto-item' in html)
