from flask import Flask, render_template_string, request, redirect
from pagina_principal import PaginaPrincipal
from render_html import RenderHTML

app = Flask(__name__)
pagina = PaginaPrincipal(api_key_news="5a7f6908927b43c3fd3f2d9f4a03d271")
pagina.construir()

# ---------- RUTA RAÍZ: REDIRIGE A /inicio ----------
@app.route('/')
def raiz():
    return redirect('/inicio')


# ---------- INICIO ----------
@app.route('/inicio')
def inicio():
    # Mostramos la sección de información (Chamba Store, imagen, texto...)
    contenido = pagina.seccion_info.render()
    html = pagina.render_layout(contenido)
    return render_template_string(html)


# ---------- CONTACTO ----------
@app.route('/contacto')
def contacto():
    contenido = pagina.seccion_contacto.render()
    html = pagina.render_layout(contenido)
    return render_template_string(html)


# ---------- COMENTARIOS ----------
@app.route('/comentarios')
def comentarios():
    # Comentarios + formulario de nuevo comentario
    contenido = pagina.seccion_comentarios.render()
    contenido += RenderHTML.render_formulario_nuevo_comentario()
    html = pagina.render_layout(contenido)
    return render_template_string(html)


# ---------- HISTORIA ----------
@app.route('/historia')
def historia():
    # Usamos directamente la sección de historia y evolución que has construido
    contenido = pagina.seccion_hist_evo.render()
    html = pagina.render_layout(contenido)
    return render_template_string(html)

# ---------- TENDENCIAS ----------
@app.route('/tendencias')
def tendencias():
    contenido = pagina.seccion_tendencias.render()
    html = pagina.render_layout(contenido)
    return render_template_string(html)

# ---------- ACCIONES SOBRE COMENTARIOS ----------

@app.route('/comentar', methods=['POST'])
def comentar():
    autor = request.form['autor']
    texto = request.form['texto']
    valoracion = int(request.form['valoracion'])
    pagina.seccion_comentarios.agregar_comentario(autor, texto, valoracion)
    return redirect('/')

@app.route('/eliminar/<int:comentario_id>', methods=['POST'])
def eliminar(comentario_id):
    pagina.seccion_comentarios.eliminar_comentario(comentario_id)
    return redirect('/')

@app.route('/editar/<int:comentario_id>', methods=['POST'])
def editar(comentario_id):
    nuevo_texto = request.form['texto']
    nueva_valoracion = int(request.form['valoracion'])
    pagina.seccion_comentarios.editar_comentario(comentario_id, nuevo_texto, nueva_valoracion)
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)