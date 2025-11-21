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
    contenido = RenderHTML.render_apartado_sesion(session.get('usuario'))
    contenido += pagina.seccion_comentarios.render()
    if 'usuario' in session:
        contenido += RenderHTML.render_formulario_nuevo_comentario()
    else:
        contenido += "<p style='color:gray;'>Inicia sesión para añadir comentarios.</p>"
    
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

# ---------- AÑADIR CARRITO ----------
@app.route("/añadir_carrito/<int:indice>", methods=["POST"])
def añadir_carrito(indice):
    # Obtenemos el producto del catálogo por índice
    producto = pagina.seccion_catalogo.catalogo.productos[indice]
    cantidad = int(request.form.get("cantidad", 1))  #recogemos la cantidad del formulario
    # Lo añadimos al carrito
    pagina.carrito.añadir_producto(producto)
    # Renderizamos la página con el carrito actualizado
    contenido = pagina.carrito.render()
    html = pagina.render_layout(contenido)
    return render_template_string(html)

# ---------- ELIMINAR CARRITO/PRODUCTO ----------
@app.route("/eliminar_carrito/<int:indice>", methods=["POST"])
def eliminar_carrito(indice):
    # Eliminamos el producto del carrito según el índice recibido en la URL
    pagina.carrito.eliminar_producto(indice)
    # Volvemos a renderizar el carrito actualizado
    contenido = pagina.carrito.render()
    # Integramos el carrito dentro del layout
    html = pagina.render_layout(contenido)
    # Devolvemos el HTML actualizado al navegador
    return render_template_string(html)

# ---------- VER CARRITO ----------
@app.route("/carrito")
def ver_carrito():
    # Renderizamos el contenido del carrito usando el método render()
    contenido = pagina.carrito.render()
    # Lo integramos dentro del layout general de la página
    html = pagina.render_layout(contenido)
    # Devolvemos el HTML generado al navegador
    return render_template_string(html)

# ---------- VACIAR CARRITO ----------
@app.route("/vaciar_carrito", methods=["POST"])
def vaciar_carrito():
    pagina.carrito.vaciar()
    contenido = pagina.carrito.render()
    html = pagina.render_layout(contenido)
    return render_template_string(html)



# ---------- ACCIONES SOBRE COMENTARIOS ----------

@app.route('/comentar', methods=['POST'])
def comentar():
    autor = session['usuario']
    texto = request.form['texto']
    valoracion = int(request.form['valoracion'])

    pagina.seccion_comentarios.agregar_comentario(autor, texto, valoracion)
    return redirect('/comentarios')

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

@app.route('/logout')
def logout():
    session.pop('usuario', None)  # elimina la clave de sesión si existe
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
