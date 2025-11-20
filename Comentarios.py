from flask import Flask, render_template_string, request, redirect, session
from pagina_principal import PaginaPrincipal
from render_html import RenderHTML
import json 

def cargar_usuarios():
    with open("usuarios.json", "r") as f:
        return json.load(f)

def guardar_usuarios(usuarios):
    with open('usuarios.json', 'w') as archivo:
        json.dump(usuarios, archivo)

app = Flask(__name__)
app.secret_key = 'ab23252894yrhugioghskjdhg0uewri'
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

# ---------- CATALOGO ----------
@app.route('/catalogo')
def catalogo():
    contenido = pagina.seccion_catalogo.render()
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

@app.route('/info-social')
def info_social():
    contenido = pagina.seccion_info_social.render()
    html = pagina.render_layout(contenido)
    return render_template_string(html)

# ---------- Login ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasenha = request.form['contrasenha']
        usuarios = cargar_usuarios()

        if usuario in usuarios and usuarios[usuario] == contrasenha:
            session['usuario'] = usuario
            return redirect('/')
        
        elif usuario not in usuarios:
            return RenderHTML.render_login() + "<p style='color:red;'>El usuario no existe.</p>" + RenderHTML.render_boton_registro()
        else:
            return RenderHTML.render_login() + "<p style='color:red;'>Credenciales incorrectas. Intenta de nuevo.</p>"
    else:
        return RenderHTML.render_login()

# ---------- registro ----------
@app.route('/registro', methods=['GET', 'POST'])
def registro():
    if request.method == 'POST':
        usuario = request.form['usuario']
        contrasena = request.form['contrasena']
        usuarios = cargar_usuarios()

        if usuario in usuarios:
            return RenderHTML.render_registro() + "<p style='color:red;'>El usuario ya existe. Intenta con otro nombre o inicie sesión.</p>" + RenderHTML.render_boton_login()
        
        else:
            usuarios[usuario] = contrasena
            guardar_usuarios(usuarios)
            return RenderHTML.render_registro() + "<p style='color:red;'>El usuario se ha registrado corectamente. Puede iniciar sesión</p>" +  RenderHTML.render_boton_login()
    else:
        return RenderHTML.render_registro()

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)