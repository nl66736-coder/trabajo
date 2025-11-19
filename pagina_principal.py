from menu import MenuNavegacion
from render_html import RenderHTML
from datetime import datetime
import json
import os

class SeccionInformacion:
    def __init__(self):
        self.nombre = None
        self.descripcion = None
        self.imagen = None
    
    def establecer_nombre(self, nombre):
        self.nombre = nombre
    
    def establecer_descripcion(self, descripcion):
        self.descripcion = descripcion
    
    def establecer_imagen(self, url):
        self.imagen = url
    
    def render(self):
        return RenderHTML.render_seccion_informacion(self.nombre, self.imagen, self.descripcion)


class SeccionContacto:
    """Sección de información de contacto"""
    def __init__(self):
        self.titulo = None
        self.telefono = None
        self.email = None
        self.direccion = None
        self.horario = None
    
    def establecer_titulo(self, titulo):
        self.titulo = titulo
    
    def establecer_telefono(self, telefono):
        self.telefono = telefono
    
    def establecer_email(self, email):
        self.email = email
    
    def establecer_direccion(self, direccion):
        self.direccion = direccion
    
    def establecer_horario(self, horario):
        self.horario = horario
    
    def render(self):
        return RenderHTML.render_seccion_contacto(
            self.titulo, self.telefono, self.email, self.direccion, self.horario
        )


class SeccionComentarios:
    def __init__(self, archivo="comentarios.json"):
        self.titulo = None
        self.comentarios = []
        self.archivo = archivo
        self.cargar_comentarios()
    
    def establecer_titulo(self, titulo):
        self.titulo = titulo
    
    def agregar_comentario(self, autor, texto, valoracion):
        valoracion = max(1, min(5, valoracion))
        fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
        self.comentarios.append((autor, texto, valoracion, fecha))
        self.guardar_comentarios()

    def eliminar_comentario(self, comentario_id):
        """Elimina un comentario por su índice y guarda los cambios."""
        if 0 <= comentario_id < len(self.comentarios):
            self.comentarios.pop(comentario_id)
            self.guardar_comentarios()

    def editar_comentario(self, comentario_id, nuevo_texto, nueva_valoracion):
        """Edita un comentario por su índice y guarda cambios"""
        if 0 <= comentario_id < len(self.comentarios):
            autor, _, _, fecha_original = self.comentarios[comentario_id]
            fecha = datetime.now().strftime("%d/%m/%Y %H:%M")
            self.comentarios[comentario_id] = (autor, nuevo_texto, max(1, min(5, nueva_valoracion)), fecha)
            self.guardar_comentarios()

    def guardar_comentarios(self):
        data = [
            {"autor": a, "texto": t, "valoracion": v, "fecha": f}
            for a, t, v, f in self.comentarios
        ]
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
    
    def cargar_comentarios(self):
        if os.path.exists(self.archivo):
            try:
                with open(self.archivo, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    self.comentarios = [
                        (d["autor"], d["texto"], d["valoracion"], d["fecha"])
                        for d in data
                    ]
            except json.JSONDecodeError:
                self.comentarios = []
        else:
            self.comentarios = []
    
    def render(self):
        return RenderHTML.render_seccion_comentarios(self.titulo, self.comentarios)


class PaginaPrincipal:
    def __init__(self):
        self.menu = MenuNavegacion.crear_menu_estandar()
        self.seccion_info = SeccionInformacion()
        self.seccion_comentarios = SeccionComentarios()
        self.seccion_contacto = SeccionContacto()
    
    def construir(self):
        # Información
        self.seccion_info.establecer_nombre("Chamba Store")
        self.seccion_info.establecer_imagen("/static/dragon (1).png")
        self.seccion_info.establecer_descripcion("""En nuestra tienda online encontrarás mucho más que tecnología, encontrarás innovación, calidad y confianza.
                                                   Seleccionamos cuidadosamente los mejores productos electrónicos del mercado -desde smartphones y ordenadores hasta accesorios inteligentes- para ofrecerte una experiencia de compra fácil, segura y con garantía total.
                                                   Porque creemos que la tecnología debe mejorar tu vida, no complicarla.""")
        
        # Contacto
        self.seccion_contacto.establecer_titulo("Contacto")
        self.seccion_contacto.establecer_telefono("988 87 54 20")
        self.seccion_contacto.establecer_email("atencionalcliente@chambastore.com")
        self.seccion_contacto.establecer_direccion("Rúa de La Habana, 88, Ourense, Galicia")
        self.seccion_contacto.establecer_horario("Lunes a Viernes: 8:30 - 21:00")

        # Comentarios
        self.seccion_comentarios.establecer_titulo("Comentarios de clientes")

        if not self.seccion_comentarios.comentarios:
            ejemplos = [
                ("Leonardo Dicaprio", "Sublime !! Tanto la rapidez de entrega como el servicio post-venta son inmejorables.", 5),
                ("Antonio Recio", "Desde que compré este portátil (Chambatron), mis FPS son más estables que mi vida amorosa.", 4),
                ("Miky Olveira", "Los auriculares FullChamba Audio cancelan tanto el ruido que no escuché a mi madre llamarme para cenar.", 5),
                ("Bad Bunny", "Desde que uso el ratón ChambaMouse, mi puntería mejoró tanto que mis enemigos me reportan por hacks.", 5),
                ("Miky Olveira", "La televisión ChambaVision™ 4K SmartTV tiene colores tan vivos que mi gato intenta cazar los peces.", 5),
                ("Lucas Garrido", "Le pedí a Mael ayuda para comprar un ordenador, pero la experiencia fue muy pobre. No volvería a pedirle consejo.", 2)
            ]
            for autor, texto, valoracion in ejemplos:
                self.seccion_comentarios.agregar_comentario(autor, texto, valoracion)

    def render_html(self):
        menu_html = self.menu.render()
        info_html = self.seccion_info.render()
        contacto_html = self.seccion_contacto.render()
        comentarios_html = self.seccion_comentarios.render()
        
        return RenderHTML.render_pagina_completa(
            menu_html, info_html, contacto_html, comentarios_html
        )
    
    def guardar_html(self, nombre_archivo="tienda.html"):
        html_contenido = self.render_html()
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write(html_contenido)
        return nombre_archivo


if __name__ == "__main__":
    pagina = PaginaPrincipal()
    pagina.construir()
    archivo_generado = pagina.guardar_html("chamba_store.html")
    print(f"✅ Archivo generado: {archivo_generado}")
#prueba