class RenderHTML:
    """Clase responsable de generar todo el HTML de la aplicación"""
    
    @staticmethod
    def render_menu(items):
        html = "<nav><ul>\n"
        for nombre, url in items:
            html += f'  <li><a href="{url}">{nombre}</a></li>\n'
        html += "</ul></nav>\n"
        return html
    
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
        html = '<section id="comentarios">\n'
        if titulo:
            html += f"  <h1>{titulo}</h1>\n"

        if comentarios:
            for i, (autor, texto, valoracion, fecha) in enumerate(comentarios):
                estrellas = "★" * valoracion + "☆" * (5 - valoracion)
                html += f"  <div style='border:1px solid #ccc; margin:10px; padding:10px; border-radius:8px;'>\n"
                html += f"    <h3>{autor}</h3>\n"
                html += f"    <small style='color:gray;'>Publicado el {fecha}</small><br>\n"
                html += f"    <p>{texto}</p>\n"
                html += f"    <p>Valoración: {estrellas}</p>\n"

                html += f"    <form action='/eliminar/{i}' method='post' style='display:inline;'>\n"
                html += f"        <button type='submit' style='background-color:#d9534f; color:white; border:none; padding:5px 10px; border-radius:5px; cursor:pointer;'>Eliminar</button>\n"
                html += f"    </form>\n"

                html += f"""
                <form action='/editar/{i}' method='post' style='margin-top:5px;'>
                    <input type='text' name='texto' value="{texto}" required style='width:70%; padding:3px;'>
                    <input type='number' name='valoracion' min='1' max='5' value="{valoracion}" required style='width:50px;'>
                    <button type='submit' style='background-color:#0275d8; color:white; border:none; padding:5px 10px; border-radius:5px; cursor:pointer;'>Editar</button>
                </form>
                """
                html += f"  </div>\n"
        else:
            html += "<p>No hay comentarios aún. ¡Sé el primero en dejar uno!</p>\n"

        html += "</section>\n"
        return html
    
    @staticmethod
    def render_formulario_nuevo_comentario():
        return """
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
        """
    
    @staticmethod
    def render_pagina_completa(menu_html, info_html, historia_evolucion, contacto_html, comentarios_html, tendencias):
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

        html += "</body>\n</html>"
        return html
    
    @staticmethod
    def render_seccion_catalogo(productos):
        html = '<section id="catalogo">\n'
        html += "<h1>Catálogo de productos</h1>\n"

        # Formulario para añadir productos
        html += """
        <form action="/agregar_producto" method="post" style="margin-bottom:20px;">
            <input type="text" name="nombre" placeholder="Nombre" required>
            <input type="text" name="descripcion" placeholder="Descripción" required>
            <input type="number" step="0.01" name="precio" placeholder="Precio" required>
            <input type="text" name="empaquetado" placeholder="Empaquetado">
            <input type="text" name="imagen" placeholder="URL de la imagen">
            <button type="submit">Añadir producto</button>
        </form>
        """

        # Mostrar productos existentes
        if productos:
            for p in productos:
                html += f"""
                <div style='border:1px solid #ccc; margin:10px; padding:10px; border-radius:8px;'>
                    <h3>{p['nombre']}</h3>
                    <p>{p['descripcion']}</p>
                    <p><strong>Precio:</strong> {p['precio']} €</p>
                    <p><strong>Empaquetado:</strong> {p['empaquetado']}</p>
                    <img src="{p['imagen']}" alt="{p['nombre']}" style="max-width:200px;">
                </div>
                """
        else:
            html += "<p>No hay productos en el catálogo aún.</p>\n"

        html += "</section>\n"
        return html
    
    @staticmethod
    def render_login():
        return """
        <form method="POST" action="/login">
            Usuario: <input type="text" name="usuario"><br>
            Contraseña: <input type="password" name="contrasenha"><br>
            <button type="submit">Iniciar sesión</button>
        </form>
        """
       
    @staticmethod
    def render_registro():
        return """
        <form method="POST" action="/registro">
            Nuevo usuario: <input type="text" name="usuario"><br>
            Nueva contraseña: <input type="password" name="contrasena"><br>
            <button type="submit">Registrarse</button>
        </form>
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