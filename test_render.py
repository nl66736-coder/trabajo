from pagina_principal import PaginaPrincipal
p = PaginaPrincipal(api_key_news='test')
try:
    p.construir()
except Exception as e:
    print('construir error', e)
html = p.render_html()
print('HAS_CSS', 'style.css' in html)
print('HAS_PRODUCTO_ITEM', 'producto-item' in html)
print('HAS_PRODUCTO_CARRITO', 'producto-carrito' in html)
start = html.find('<head>')
end = html.find('</head>')
print('\nHEAD:\n', html[start:end+7])
idx = html.find('producto-item')
if idx!=-1:
    s = html[max(0, idx-200):idx+200]
    print('\nSAMPLE PRODUCTO ITEM:\n', s)
else:
    print('\nNo producto-item found')
