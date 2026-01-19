from pagina_principal import PaginaPrincipal
p = PaginaPrincipal(api_key_news='test')
p.construir()
html = p.render_layout(p.seccion_catalogo.render())
with open('salida_catalogo.html','w',encoding='utf-8') as f:
    f.write(html)
print('WROTE salida_catalogo.html')
print('HAS_CSS', 'style.css' in html)
print('HAS_PRODUCTO_ITEM', 'producto-item' in html)
