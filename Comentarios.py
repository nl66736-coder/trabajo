from flask import Flask, render_template_string, request, redirect
from pagina_principal import PaginaPrincipal
from render_html import RenderHTML

app = Flask(__name__)
pagina = PaginaPrincipal()
pagina.construir()

@app.route('/')
def index():
    html = pagina.render_html()
    formulario = RenderHTML.render_formulario_nuevo_comentario()
    html = html.replace("</body>", formulario + "</body>")
    return render_template_string(html)

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