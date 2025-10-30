from flask import Flask, render_template_string, request, redirect
from pagina_principal import PaginaPrincipal

app = Flask(__name__)
pagina = PaginaPrincipal()
pagina.construir()

@app.route('/')
def index():
    html = pagina.render_html()
    html = html.replace("</body>", """
        <section id="nuevo-comentario" style="margin:20px;">
            <h2>Deja tu comentario</h2>
            <form action="/comentar" method="post">
                <input type="text" name="autor" placeholder="Tu nombre" required><br><br>
                <textarea name="texto" placeholder="Escribe tu comentario..." required></textarea><br><br>
                <label>Valoración (1-5):</label>
                <input type="number" name="valoracion" min="1" max="5" required><br><br>
                <button type="submit">Enviar</button>
            </form>
        </section>
    </body>""")
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


if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
