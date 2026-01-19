# app.py
# Punto de entrada de la aplicación.
# Muestra el menú principal y delega las acciones en los módulos correspondientes.

from flask import Flask, render_template_string, request, redirect, session
from pagina_principal import PaginaPrincipal
from render_html import RenderHTML
import json 
from datetime import datetime
import os

def cargar_usuarios():
    with open("usuarios.json", "r") as f:
        return json.load(f)

def guardar_usuarios(usuarios):
    with open('usuarios.json', 'w') as archivo:
        json.dump(usuarios, archivo)

def cargar_historial():
    with open("historial.json", "r", encoding="utf-8") as f:
        return json.load(f)
    
def guardar_historial(historial):
    with open('historial.json', 'w', encoding="utf-8") as archivo:
        json.dump(historial, archivo, indent=4, ensure_ascii=False)

app = Flask(__name__, static_folder='static', static_url_path='/static')
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
    contenido = pagina.seccion_info.render()
    # Añadir comentarios también en inicio
    contenido += pagina.seccion_comentarios.render()
    contenido += pagina.seccion_contacto.render()
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

@app.route("/comentar_producto/<int:i>", methods=["POST"])
def comentar_producto(i):
    autor = request.form.get("autor", "Anónimo")
    texto = request.form.get("texto", "")

    # OJO: usamos el MISMO catálogo que está dentro de la sección catálogo
    pagina.seccion_catalogo.catalogo.agregar_comentario_por_indice(i, autor, texto)

    return redirect("/catalogo")

# ---------- AÑADIR CARRITO ----------
@app.route("/añadir_carrito/<int:indice>", methods=["POST"])
def añadir_carrito(indice):
    # Cargar catálogo actualizado 
    pagina.seccion_catalogo.catalogo.cargar()
    # Obtenemos el producto del catálogo por índice
    producto = pagina.seccion_catalogo.catalogo.productos[indice]
    cantidad = int(request.form.get("cantidad", 1))  #recogemos la cantidad del formulario
    # Lo añadimos al carrito
    pagina.carrito.añadir_producto(producto, cantidad)

    usuario = session.get('usuario')
    if usuario:
        # Registrar en historial de compras
        historial = cargar_historial()
        if usuario in historial:
            # Buscar si ya existe una compra pendiente
            compra_pendiente = None
            for compra in historial[usuario]["compras"]:
                if compra.get("estado") == "carrito":
                    compra_pendiente = compra
                    break

            if not compra_pendiente:
                compra_pendiente = {
                    "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                    "estado": "carrito",
                    "productos": []
                }
                historial[usuario]["compras"].append(compra_pendiente)
            
            # Añadir producto a la compra pendiente
            compra_pendiente["productos"].append({
                "nombre": producto["nombre"],
                "precio": producto["precio"],
                "cantidad": cantidad
            })
            
            guardar_historial(historial)
        
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
    usuario = session.get('usuario')
    if usuario:
        pagina.seccion_notificaciones.agregar_notificacion(
            usuario,
            'Has vaciado tu carrito de compras',
            '/carrito'
        )
    contenido = pagina.carrito.render()
    html = pagina.render_layout(contenido)
    return render_template_string(html)

# REALIZAR COMPRA
@app.route("/finalizar_compra", methods=["POST"])
def finalizar_compra():
    usuario = session.get('usuario')
    if not usuario:
        return redirect('/login')
    
    if len(pagina.carrito.productos) == 0:
        return redirect('/carrito')
    
    # Actualizar historial con compra finalizada
    historial = cargar_historial()
    if usuario in historial:
        # Cambiar estado de "carrito" a "finalizada"
        for compra in historial[usuario]["compras"]:
            if compra.get("estado") == "carrito":
                compra["estado"] = "finalizada"
                compra["fecha_compra"] = datetime.now().strftime("%d/%m/%Y %H:%M")
        
        guardar_historial(historial)
        
        # Vaciar carrito
        pagina.carrito.vaciar()
        
        # Generar nueva recomendación basada en la compra
        pagina.seccion_notificaciones.generar_notificaciones_recomendaciones(
            usuario,
            pagina.seccion_catalogo.catalogo.productos
        )
        
        # Notificación de compra exitosa
        pagina.seccion_notificaciones.agregar_notificacion(
            usuario,
            "¡Compra realizada con éxito! Gracias por tu confianza",
            "/notificaciones",
            tipo="info"
        )
    
    return redirect('/notificaciones')

# ---------- ACCIONES SOBRE COMENTARIOS ----------

@app.route('/comentar', methods=['POST'])
def comentar():
    autor = session.get('usuario') or request.form.get("autor", "Anónimo")
    texto = request.form['texto']
    valoracion = int(request.form['valoracion'])

    pagina.seccion_comentarios.agregar_comentario(autor, texto, valoracion)
    pagina.seccion_notificaciones.agregar_notificacion(autor, 'Tu comentario ha sido publicado correctamente','/comentarios')
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
            session["mensaje"] = f"👋 Bienvenido, {usuario}. Has iniciado sesión correctamente."
            return redirect('/inicio')

        
        elif usuario not in usuarios:
            html = RenderHTML.render_pagina_login_completa()
            html = html.replace("</body>", f"<p style='color:red; margin: 2rem;'>El usuario no existe.</p>\n</body>")
            return render_template_string(html)
        else:
            html = RenderHTML.render_pagina_login_completa()
            html = html.replace("</body>", f"<p style='color:red; margin: 2rem;'>Credenciales incorrectas. Intenta de nuevo.</p>\n</body>")
            return render_template_string(html)
    else:
        return render_template_string(RenderHTML.render_pagina_login_completa())

# ---------- registro ----------
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        usuario = request.form["usuario"]
        contrasena = request.form["contrasena"]

        recibir_notificaciones = "recibir_notificaciones" in request.form

        # Cargar usuarios
        usuarios = cargar_usuarios()

        # Evitar duplicados
        if usuario in usuarios:
            html = RenderHTML.render_pagina_registro_completa()
            html = html.replace("</body>", f"<p style='color:red; margin: 2rem;'>El usuario ya existe.</p>\n</body>")
            return render_template_string(html)

        # Guardar usuario y contraseña
        usuarios[usuario] = contrasena
        guardar_usuarios(usuarios)

        # Cargar historial
        historial = cargar_historial()

        historial[usuario] = {
            "compras": [],
            "notificaciones": [],
            "preferencias": {
                "recibir_notificaciones": recibir_notificaciones
            }
        }

        # Notificación de bienvenida SOLO si acepta
        if recibir_notificaciones:
            historial[usuario]["notificaciones"].append({
                "texto": "¡Bienvenido a Chamba Store! Gracias por registrarte.",
                "link": "/catalogo",
                "fecha": datetime.now().strftime("%d/%m/%Y %H:%M"),
                "tipo": "info"
            })

        guardar_historial(historial)

        session["mensaje"] = "✅ Registro completado correctamente. Ya puedes iniciar sesión."
        return redirect("/login")

    return render_template_string(RenderHTML.render_pagina_registro_completa())



@app.route('/logout')
def logout():
    session.pop('usuario', None)  # elimina la clave de sesión si existe
    return redirect('/')

@app.route('/notificaciones')
def notificaciones():
    usuario = session.get('usuario')
    if usuario:
        contenido = RenderHTML.render_apartado_sesion(usuario)
        analisis = pagina.seccion_notificaciones.analizar_historial_compras(usuario)
        analisis_comentarios = pagina.seccion_notificaciones.analizar_comentarios_usuario(usuario, pagina.seccion_comentarios.comentarios)
        contenido += f'''
        <div>
            <h2>Tu Perfil de Compras</h2>
            <p><strong>Total de compras:</strong> {analisis["total_compras"]}</p>
            <p><strong>Gasto total:</strong> {analisis["gasto_total"]:.2f}€</p>
            <p><strong>Categorías favoritas:</strong> {", ".join(analisis["categorias_preferidas"]) if analisis["categorias_preferidas"] else "Aún no tienes favoritas"}</p>
            <p><strong>Comentarios realizados:</strong> {analisis_comentarios["total_comentarios"]}</p>
            <p><strong>Valoración promedio:</strong> {analisis_comentarios["valoracion_promedio"]:.1f}/5</p>
            <p><strong>Productos mencionados:</strong> {", ".join(analisis_comentarios["productos_mencionados"]) if analisis_comentarios["productos_mencionados"] else "Ninguno detectado"}</p>
            <form action="/generar_recomendaciones" method="post" style="margin-top:15px;">
                <button type="submit">
                    Generar nuevas recomendaciones
                </button>
            </form>
        </div>
        '''
        contenido += pagina.seccion_notificaciones.render(usuario)
    else:
        contenido = RenderHTML.render_apartado_sesion(None)
        contenido += "<p style='color:gray;'>Inicia sesión para recibir y ver tus notificaciones.</p>"   

    html = pagina.render_layout(contenido)
    return render_template_string(html)

@app.route('/limpiar_notificaciones', methods=['POST'])
def limpiar_notificaciones():
    usuario = session.get('usuario')
    if usuario:
        pagina.seccion_notificaciones.limpiar_notificaciones(usuario)
    return redirect('/notificaciones')

@app.route('/generar_recomendaciones', methods=['POST'])
def generar_recomendaciones():
    usuario = session.get('usuario')
    if usuario:
        pagina.seccion_notificaciones.generar_notificaciones_recomendaciones(usuario, pagina.seccion_catalogo.catalogo.productos)
    return redirect('/notificaciones')

<<<<<<< HEAD
# Nota: Flask sirve automáticamente /static/ gracias a:
# Flask(__name__, static_folder='static', static_url_path='/static')
=======
# ---------- PERFIL ----------
from perfil import ver_perfil, editar_perfil, actualizar_perfil

@app.route('/perfil')
def perfil():
    return ver_perfil()

@app.route('/editar-perfil', methods=['GET'])
def editar_perfil_route():
    return editar_perfil()

@app.route('/actualizar-perfil', methods=['POST'])
def actualizar_perfil_route():
    return actualizar_perfil()
>>>>>>> afd8f92a7686afd7e48c188dfc06ab2cc985a90f

if __name__ == '__main__':
    app.run(debug=True, use_reloader=False)
