import json
import os
from catalogo import CatalogoProductos
from menu import MenuNavegacion
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
        html = '<section id="informacion">\n'

        if self.nombre:
            html += f"<h1>{self.nombre}</h1>\n"

        if self.imagen:
            html += f'<img src="{self.imagen}" alt="Imagen de la tienda">\n'

        if self.descripcion:
            html += f"<p>{self.descripcion}</p>\n"
       
        html += "\n</section>\n"
        return html

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
        html = '<section id="contacto">\n'
        
        if self.titulo:
            html += f"  <h1>{self.titulo}</h1>\n"
        
        if self.telefono:
            html += f"  <p><strong>Teléfono:</strong> {self.telefono}</p>\n"
        
        if self.email:
            html += f"  <p><strong>Email:</strong> {self.email}</p>\n"
        
        if self.direccion:
            html += f"  <p><strong>Dirección:</strong> {self.direccion}</p>\n"
        
        if self.horario:
            html += f"  <p><strong>Horario:</strong> {self.horario}</p>\n"
        
        html += "</section>\n"
        return html

from menu import MenuNavegacion

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
        html = '<section id="informacion">\n'

        if self.nombre:
            html += f"<h1>{self.nombre}</h1>\n"

        if self.imagen:
            html += f'<img src="{self.imagen}" alt="Imagen de la tienda">\n'

        if self.descripcion:
            html += f"<p>{self.descripcion}</p>\n"
       
        html += "\n</section>\n"
        return html

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
        html = '<section id="contacto">\n'
        
        if self.titulo:
            html += f"  <h1>{self.titulo}</h1>\n"
        
        if self.telefono:
            html += f"  <p><strong>Teléfono:</strong> {self.telefono}</p>\n"
        
        if self.email:
            html += f"  <p><strong>Email:</strong> {self.email}</p>\n"
        
        if self.direccion:
            html += f"  <p><strong>Dirección:</strong> {self.direccion}</p>\n"
        
        if self.horario:
            html += f"  <p><strong>Horario:</strong> {self.horario}</p>\n"
        
        html += "</section>\n"
        return html

class SeccionComentarios:
    def __init__(self, archivo="comentarios.json"):
        # Aseguramos que el archivo esté en la misma carpeta que este script
        self.archivo = os.path.join(os.path.dirname(__file__), archivo)
        self.titulo = None
        self.comentarios = []
        self.cargar_comentarios()

    def establecer_titulo(self, titulo):
        self.titulo = titulo
    
    def agregar_comentario(self, autor, texto, valoracion):
        valoracion = max(1, min(5, valoracion))
        self.comentarios.append((autor, texto, valoracion))
        self.guardar_comentarios()
    
    def eliminar_comentario(self, comentario_id):
        if 0 <= comentario_id < len(self.comentarios):
            self.comentarios.pop(comentario_id)
            self.guardar_comentarios()

    def guardar_comentarios(self):
        """Guarda los comentarios en un archivo JSON."""
        data = [{"autor": a, "texto": t, "valoracion": v} for a, t, v in self.comentarios]
        try:
            with open(self.archivo, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print("❌ Error guardando comentarios:", e)

    def cargar_comentarios(self):
        """Carga los comentarios si el archivo existe, o crea uno vacío."""
        if not os.path.exists(self.archivo):
            with open(self.archivo, "w", encoding="utf-8") as f:
                json.dump([], f)
        try:
            with open(self.archivo, "r", encoding="utf-8") as f:
                data = json.load(f)
                self.comentarios = [(d["autor"], d["texto"], d["valoracion"]) for d in data]
        except Exception as e:
            print("❌ Error cargando comentarios:", e)
            self.comentarios = []
    
    def render(self):
        html = '<section id="comentarios">\n'
        
        if self.titulo:
            html += f"  <h1>{self.titulo}</h1>\n"
        
        if self.comentarios:
            for i, (autor, texto, valoracion) in enumerate(self.comentarios):
                estrellas = "★" * valoracion + "☆" * (5 - valoracion)
                html += f"  <div>\n"
                html += f"    <h3>{autor}</h3>\n"
                html += f"    <p>{texto}</p>\n"
                html += f"    <p>Valoración: {estrellas}</p>\n"
                html += f"""    <form action="/eliminar/{i}" method="post" style="margin-top:10px;">
                                <button type="submit">Eliminar</button>
                              </form>\n"""
                html += f"  </div>\n"
        else:
            html += "<p>No hay comentarios aún. ¡Sé el primero en dejar uno!</p>\n"
        
        html += "</section>\n"
        return html

class PaginaPrincipal:
    def __init__(self):
        self.menu = MenuNavegacion.crear_menu_estandar()
        self.seccion_info = SeccionInformacion()
        self.seccion_comentarios = SeccionComentarios()
        self.seccion_contacto = SeccionContacto()
    
    def construir(self):
        # información
        self.seccion_info.establecer_nombre("Chamba Store")
        self.seccion_info.establecer_imagen("dragon.png")
        self.seccion_info.establecer_descripcion("""En nuestra tienda online encontrarás mucho más que tecnología, encontrarás innovación, calidad y confianza.
                                                   Seleccionamos cuidadosamente los mejores productos electrónicos del mercado -desde smartphones y ordenadores hasta accesorios inteligentes- para ofrecerte una experiencia de compra fácil, segura y con garantía total.
                                                   Porque creemos que la tecnología debe mejorar tu vida, no complicarla.""")
        
        # contacto
        self.seccion_contacto.establecer_titulo("Contacto")
        self.seccion_contacto.establecer_telefono("988 87 54 20")
        self.seccion_contacto.establecer_email("atencionalcliente@chambastore.com")
        self.seccion_contacto.establecer_direccion("Rúa de La Habana, 88, Ourense, Galicia")
        self.seccion_contacto.establecer_horario("Lunes a Viernes: 8:30 - 21:00")

        # comentarios
        self.seccion_comentarios.establecer_titulo("Comentarios de clientes")

        # 🔽 Solo añadir los comentarios iniciales si el JSON está vacío
        if not self.seccion_comentarios.comentarios:
            self.seccion_comentarios.agregar_comentario(
                "Leonardo Dicaprio",
                "Sublime !! Tanto la rapidez de entrega como el servicio post-venta son inmejorables, ya soy cliente desde 2011 que hice mi primer pedido y llevaré ya alrededor de 100 y la verdad que para mí siempre es la primera opción para comprar.",
                5
            )
            self.seccion_comentarios.agregar_comentario(
                "Antonio Recio",
                "Desde que compré este portátil (Chambatron), mis FPS son más estables que mi vida amorosa.",
                4
            )
            self.seccion_comentarios.agregar_comentario(
                "Miky Olveira",
                "Los auriculares FullChamba Audio eran justo lo que estaba buscando, cancelan tanto el ruido que no escuché a mi madre llamarme para cenar. Pasé 8 horas sin comer, pero feliz.",
                5
            )
            self.seccion_comentarios.agregar_comentario(
                "Bad Bunny",
                "Desde que uso el ratón ChambaMouse, mi puntería mejoró tanto que mis enemigos me reportan por hacks.",
                5
            )
            self.seccion_comentarios.agregar_comentario(
                "Miky Olveira",
                "En la televisión ChambaVision™ 4K SmartTV, los colores son tan vivos que mi gato intenta cazar a los peces del documental. Le doy 5 estrellas, a mi gato solo 2.",
                5
            )
            self.seccion_comentarios.agregar_comentario(
                "Lucas Garrido",
                "Le pedí a Mael uno de los trabajadores que me orientara para comprar un ordenador, pero la verdad es que su ayuda fue bastante pobre...",
                2
            )
    def render_html(self):
    
        html = "<!DOCTYPE html>\n<html>\n<head>\n"
        html += "  <meta charset='UTF-8'>\n"
        html += "  <title>Chamba_Store</title>\n"
        html += "</head>\n<body>\n"
        html += self.menu.render()
        html += self.seccion_info.render()
        html += self.seccion_contacto.render()
        html += self.seccion_comentarios.render()
        html += "</body>\n</html>"
        return html
    
    def guardar_html(self, nombre_archivo="tienda.html"):
        html_contenido = self.render_html()
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write(html_contenido)
        return nombre_archivo

if __name__ == "__main__":
    pagina = PaginaPrincipal()
    archivo_generado = pagina.guardar_html("chamba_store.html")
class PaginaPrincipal:
    def __init__(self):
        self.menu = MenuNavegacion.crear_menu_estandar()
        self.seccion_info = SeccionInformacion()
        self.seccion_comentarios = SeccionComentarios()
        self.seccion_contacto = SeccionContacto()
    
    def construir(self):
        # información
        self.seccion_info.establecer_nombre("Chamba Store")
        self.seccion_info.establecer_imagen("dragon.png")
        self.seccion_info.establecer_descripcion("""En nuestra tienda online encontrarás mucho más que tecnología, encontrarás innovación, calidad y confianza.
                                                   Seleccionamos cuidadosamente los mejores productos electrónicos del mercado -desde smartphones y ordenadores hasta accesorios inteligentes- para ofrecerte una experiencia de compra fácil, segura y con garantía total.
                                                   Porque creemos que la tecnología debe mejorar tu vida, no complicarla.""")
        
        # contacto
        self.seccion_contacto.establecer_titulo("Contacto")
        self.seccion_contacto.establecer_telefono("988 87 54 20")
        self.seccion_contacto.establecer_email("atencionalcliente@chambastore.com")
        self.seccion_contacto.establecer_direccion("Rúa de La Habana, 88, Ourense, Galicia")
        self.seccion_contacto.establecer_horario("Lunes a Viernes: 8:30 - 21:00")

        # comentarios
        self.seccion_comentarios.establecer_titulo("Comentarios de clientes")
        self.seccion_comentarios.agregar_comentario(
            "Leonardo Dicaprio",
            "Sublime !! Tanto la rapidez de entrega como el servicio post-venta son inmejorables, ya soy cliente desde 2011 que hice mi primer pedido y llevare ya alrededor de 100 y la verdad que para mi siempre es la 1º opcion para comprar.",
            5
        )
        self.seccion_comentarios.agregar_comentario(
            "Antonio Recio",
            "Desde que compré este portátil(Chambatron), mis FPS son más estables que mi vida amorosa.",
            4
        )
        self.seccion_comentarios.agregar_comentario(
            "Miky Olveira",
            "Los auriculares FullChamba Audio, eran justo lo que estaba buscando, cancelan tanto el ruido que no escuché a mi madre llamarme para cenar. Pasé 8 horas sin comer, pero feliz.",
            5
        )
        self.seccion_comentarios.agregar_comentario(
            "Bad Bunny",
            "Desde que uso el ratón ChambaMouse, mi puntería mejoró tanto que mis enemigos me reportan por hacks.",
            5
        )
        self.seccion_comentarios.agregar_comentario(
            "Miky Olveira",
            "En la televisión ChambaVision™ 4K SmartTV, es tal como el anuncio, los colores son tan vivos que mi gato intenta cazar a los peces del documental. Le doy 5 estrellas, a mi gato solo 2.",
            5
        )
        self.seccion_comentarios.agregar_comentario(
            "Lucas Garrido",
            "Le pedí a Mael uno de los trabajadores, que me orientara para comprar un ordenador, ya que no entiendo mucho del tema, pero la verdad es que su ayuda fue bastante pobre. Me recomendó un modelo diciendo que era ‘de lo mejor’, y resultó ser justo lo contrario: lento, con poca memoria y encima más caro que otras opciones que encontré después. Cuando le comenté el problema, solo me dijo que ‘seguro yo lo estaba usando mal’. Me pareció poco profesional y nada empático. No volvería a pedirle consejo.",
            2
        )

    def render_html(self):
    
        html = "<!DOCTYPE html>\n<html>\n<head>\n"
        html += "  <meta charset='UTF-8'>\n"
        html += "  <title>Chamba_Store</title>\n"
        html += "</head>\n<body>\n"
        html += self.menu.render()
        html += self.seccion_info.render()
        html += self.seccion_contacto.render()
        html += self.seccion_comentarios.render()
        html += "</body>\n</html>"
        return html
    
    def guardar_html(self, nombre_archivo="tienda.html"):
        html_contenido = self.render_html()
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write(html_contenido)
        return nombre_archivo

if __name__ == "__main__":
    pagina = PaginaPrincipal()
    archivo_generado = pagina.guardar_html("chamba_store.html")