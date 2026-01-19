# Módulo: render_html.py
# Genera fragmentos HTML para mostrar noticias, tendencias y notificaciones.

from pydoc import html


class RenderHTML:
    """Clase responsable de generar todo el HTML de la aplicación"""
    print("✅ USANDO ESTE render_html.py")

    
    @staticmethod
    def render_seccion_informacion(nombre, imagen, descripcion):
        html = '<section id="informacion">\n'
        if nombre:
            html += f"<h1>{nombre}</h1>\n"
        if imagen:
            html += f'<img src="{imagen}" alt="Imagen de la tienda">\n'
        if descripcion:
            html += f"<p>{descripcion}</p>\n"
        html += "\n</section>\n"
        return html
    
    @staticmethod
    def render_seccion_historia_evolucion(titulo, historia, evolucion):
        html = f'<section id="historiaevolucion">\n'
        html += f'  <h1>{titulo}</h1>\n'

        if historia:
            html += f'  <h2>Historia</h2>\n'
            html += f'  <p>{historia}</p>\n'

        if evolucion:
            html += f'  <h2>Evolución</h2>\n'
            html += f'  <p>{evolucion}</p>\n'

        html += "</section>\n"
        return html

    @staticmethod
    def render_seccion_contacto(titulo, telefono, email, direccion, horario):
        html = '<section id="contacto">\n'
        if titulo:
            html += f"  <h1>{titulo}</h1>\n"
        if telefono:
            html += f"  <p><strong>Teléfono:</strong> {telefono}</p>\n"
        if email:
            html += f"  <p><strong>Email:</strong> {email}</p>\n"
        if direccion:
            html += f"  <p><strong>Dirección:</strong> {direccion}</p>\n"
        if horario:
            html += f"  <p><strong>Horario:</strong> {horario}</p>\n"
        html += "</section>\n"
        return html
    
    @staticmethod
    def render_seccion_comentarios(titulo, comentarios):
        html = """
        <section id="comentarios" style="margin:20px;">
        """

        if titulo:
            html += f"<h1>{titulo}</h1>"

        # Botón para abrir el modal
        html += """
            <button onclick="document.getElementById('modal-comentarios').style.display='block'"
                    style="padding:10px 20px; margin:10px 0; cursor:pointer;">
                Ver comentarios
            </button>
        """

        # Modal flotante
        html += """
        <div id="modal-comentarios" 
            style="display:none; position:fixed; top:0; left:0; width:100%; height:100%;
                    background:rgba(0,0,0,0.5); justify-content:center; align-items:center;">
            
            <div style="background:white; padding:20px; width:80%; max-width:600px; 
                        border-radius:10px; max-height:80%; overflow-y:auto; position:relative;">

                <!-- Botón cerrar -->
                <span onclick="document.getElementById('modal-comentarios').style.display='none'"
                    style="position:absolute; top:10px; right:15px; cursor:pointer; font-size:22px;">
                    &times;
                </span>

                <h2>Comentarios de usuarios</h2>
        """

        # Contenido del modal
        if comentarios:
            for autor, texto, valoracion, fecha in comentarios:
                estrellas = "★" * valoracion + "☆" * (5 - valoracion)
                html += f"""
                    <div style='border:1px solid #ccc; margin:10px 0; padding:10px; border-radius:8px;'>
                        <h3>{autor}</h3>
                        <small style='color:gray;'>Publicado el {fecha}</small><br>
                        <p>{texto}</p>
                        <p>Valoración: {estrellas}</p>
                    </div>
                """
        else:
            html += """
                <div style="border:1px dashed #ccc; margin:10px 0; padding:10px; border-radius:8px;">
                    <p>No hay comentarios aún. ¡Sé el primero!</p>
                </div>
            """

        # Cerrar modal + cierre de bloques
        html += """
            </div>
        </div> <!-- FINAL DEL MODAL -->
        </section>
        """

        return html

    
    @staticmethod
    def render_formulario_nuevo_comentario():
        return """
        <section id="nuevo-comentario" style="margin:20px;">
            <h2>Deja tu comentario</h2>
            <form action="/comentar" method="post">
                <textarea name="texto" placeholder="Escribe tu comentario..." required></textarea><br><br>
                <label>Valoración (1-5):</label>
                <input type="number" name="valoracion" min="1" max="5" required><br><br>
                <button type="submit">Enviar</button>
            </form>
        </section>
        """
    
    @staticmethod
    def render_pagina_completa(menu_html, info_html, historia_evolucion, contacto_html, comentarios_html, tendencias , info_social_html):
        html = "<!DOCTYPE html>\n<html>\n<head>\n"
        html += "  <meta charset='UTF-8'>\n"
        html += "  <title>Chamba_Store</title>\n"
        html += "</head>\n<body>\n"
        html += menu_html
        html += info_html
        html += historia_evolucion 
        html += contacto_html
        html += comentarios_html
        html += tendencias
        html += info_social_html

        html += "</body>\n</html>"
        return html

    
    @staticmethod
    def render_seccion_catalogo(productos):
        html = '<section id="catalogo">\n'
        html += "<h1>Catálogo de productos</h1>\n"

        if productos:
            for i, p in enumerate(productos):
                comentarios = p.get("comentarios", [])

                html += f"""
                <div style="
                    border:1px solid #ccc;
                    margin:10px;
                    padding:10px;
                    border-radius:8px;
                    display:flex;
                    gap:20px;
                ">
                    <!-- IZQUIERDA: PRODUCTO -->
                    <div style="flex:1; min-width:280px;">
                        <h3>{p['nombre']}</h3>
                        <p>{p['descripcion']}</p>
                        <p><strong>Precio:</strong> {p['precio']} €</p>
                        <p><strong>Empaquetado:</strong> {p['empaquetado']}</p>
                """

                stock = p.get("stock", 0)
                if stock > 0:
                    html += f"<p><strong>Stock disponible:</strong> {stock}</p>"
                else:
                    html += "<p><strong>Stock disponible:</strong> <span style='color:red; font-weight:bold;'>AGOTADO</span></p>"

                html += f"""
                        <img src="{p['imagen']}" alt="{p['nombre']}" style="max-width:200px;"><br><br>

                        <!-- Formulario carrito -->
                """

                # Si no hay stock, desactivamos el botón (queda muy “profe”)
                if stock > 0:
                    html += f"""
                        <form action="/añadir_carrito/{i}" method="post">
                            <label>Cantidad:</label>
                            <input type="number" name="cantidad" value="1" min="1" max="{stock}">
                            <button type="submit">Añadir al carrito</button>
                        </form>
                    """
                else:
                    html += """
                        <p style="color:#888;">No disponible (sin stock).</p>
                    """

                html += """
                    </div>

                    <!-- DERECHA: COMENTARIOS -->
                    <div style="flex:1; border-left:1px dashed #bbb; padding-left:15px;">
                        <h4>Reseñas</h4>
                """

                if comentarios:
                    for c in comentarios[-5:]:
                        autor = c.get("autor", "Anónimo")
                        texto = c.get("texto", "")
                        fecha = c.get("fecha", "")
                        html += f"""
                        <div style="border:1px solid #eee; padding:8px; margin-bottom:8px; border-radius:6px;">
                            <p style="margin:0;"><strong>{autor}</strong> <span style="color:#777; font-size:12px;">{fecha}</span></p>
                            <p style="margin:6px 0 0 0;">{texto}</p>
                        </div>
                        """
                else:
                    html += "<p style='color:gray;'>Sin reseñas todavía.</p>"

                html += f"""
                <form action="/comentar_producto/{i}" method="post" style="margin-top:12px;">
                    <input type="text" name="autor" placeholder="Tu nombre (opcional)"
                        style="width:100%; padding:6px; margin-bottom:6px;">
                    <textarea name="texto" placeholder="Escribe tu reseña..." required
                        style="width:100%; height:70px; padding:6px;"></textarea>
                    <button type="submit" style="margin-top:6px;">Añadir comentario</button>
                </form>
                """

                html += """
                    </div>
                </div>
                """
        else:
            html += "<p>No hay productos en el catálogo aún.</p>\n"

        html += "</section>\n"
        return html
    
    @staticmethod
    def render_login():
        return """
        <section style="margin:20px;">
            <h2>Iniciar sesión</h2>
            <form method="POST" action="/login">
                Usuario: <input type="text" name="usuario" required><br><br>
                Contraseña: <input type="password" name="contrasenha" required><br><br>
                <button type="submit">Iniciar sesión</button>
            </form>
            <br>
            <a href="/registro"><button>Registrarse</button></a>
            <a href="/inicio"><button>Volver al inicio</button></a>
        </section>
        """
       
    @staticmethod
    def render_registro():
        return """
        <section style="margin:20px;">
            <h2>Registro de usuario</h2>
            <form method="POST" action="/registro">
                Usuario: <input type="text" name="usuario" required><br><br>
                Contraseña: <input type="password" name="contrasena" required><br><br>

                <label>
                    <input type="checkbox" name="recibir_notificaciones" checked>
                    Quiero recibir notificaciones y recomendaciones
                </label><br><br>

                <button type="submit">Registrarse</button>
            </form>
        </section>
        """


    @staticmethod
    def render_boton_registro():
        return """
        <form action="/registro" method="GET">
             <button type="submit">Registrarse</button>
        </form>
        """
    
    @staticmethod
    def render_boton_login():
        return """
        <form action="/login" method="GET">
             <button type="submit">Iniciar Sesion</button>
        </form>
        """
    
    @staticmethod
    def render_apartado_sesion(usuario=None):
        if usuario:
            return f"""
            <div style="border:1px solid #ccc; padding:10px; margin:10px;">
                <p>Sesión iniciada como <b>{usuario}</b></p>
                <a href="/logout"><button>Cerrar sesión</button></a>
            </div>
            """
        else:
            return RenderHTML.render_boton_login()
    
    @staticmethod
    def render_seccion_notificaciones(titulo, lista):
        html = '<section id="notificaciones">\n'
        html += f'<h1>{titulo}</h1>\n'
        
        if lista:
            nuevos_productos = sum(1 for n in lista if n.get("tipo") == "nuevo_producto")
            recomendaciones = sum(1 for n in lista if n.get("tipo") == "recomendacion")
            
            html += '<div>\n'
            html += f'<p style="margin:5px 0;"><strong>Resumen:</strong></p>\n'
            html += f'<p style="margin:5px 0;">{nuevos_productos} nuevos productos</p>\n'
            html += f'<p style="margin:5px 0;">{recomendaciones} recomendaciones personalizadas</p>\n'
            html += '</div>\n'
            for i, n in enumerate(lista):
                tipo = n.get("tipo", "info")
                html += f'''
                <div>
                    <p style="margin:0 0 8px 0;">
                        <span style="font-size:24px; margin-right:8px;"></span>
                        <a href="{n["link"]}">{n["texto"]}</a>
                    </p>
                    <small style="color:#666;"> {n["fecha"]}</small>
                </div>
                '''
                html += '</div>\n'
                
            html += '''
            <form action="/limpiar_notificaciones" method="post" style="margin-top:20px;">
                <button type="submit">Limpiar todas las notificaciones</button>
            </form>
            '''
        else:
            html += '''
            <div>
                <p style="color:#666; font-size:16px;">No tienes notificaciones por ahora.</p>
                <p style="color:#999; font-size:14px;">Te avisaremos cuando haya nuevos productos o recomendaciones para ti.</p>
            </div>
            '''
        html += "</section>\n"
        return html
                
