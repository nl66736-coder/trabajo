import json
import os
from catalogo import CatalogoProductos
from menu import MenuNavegacion

# ============================================================
# SECCION DE CONTACTO
# ============================================================
class SeccionContacto:
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
            html += f"<h1>{self.titulo}</h1>\n"
        
        if self.telefono:
            html += f"<p><strong>Teléfono:</strong> {self.telefono}</p>\n"
        
        if self.email:
            html += f"<p><strong>Email:</strong> {self.email}</p>\n"
        
        if self.direccion:
            html += f"<p><strong>Dirección:</strong> {self.direccion}</p>\n"
        
        if self.horario:
            html += f"<p><strong>Horario:</strong> {self.horario}</p>\n"
        
        html += "</section>\n"
        return html


# ============================================================
# SECCION DE INFORMACION
# ============================================================
class SeccionInformacion:
    def __init__(self):
        self.nombre = None
        self.descripcion = None
        self.historia = None
        self.evolucion = None
        self.imagen = None
    
    def establecer_nombre(self, nombre):
        self.nombre = nombre
    
    def establecer_descripcion(self, descripcion):
        self.descripcion = descripcion
    
    def establecer_historia(self, texto):
        self.historia = texto

    def establecer_evolucion(self, texto):
        self.evolucion = texto
    
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

        if self.historia:
            html += "<h2>Historia</h2>\n"
            html += f"<p>{self.historia}</p>\n"

        if self.evolucion:
            html += "<h2>Evolución</h2>\n"
            html += f"<p>{self.evolucion}</p>\n"
       
        html += "</section>\n"
        return html


# ============================================================
# SECCION DE COMENTARIOS
# ============================================================
class SeccionComentarios:
    def __init__(self, archivo="comentarios.json"):
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
        data = [{"autor": a, "texto": t, "valoracion": v} for a, t, v in self.comentarios]
        try:
            with open(self.archivo, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print("❌ Error guardando comentarios:", e)

    def cargar_comentarios(self):
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
            html += f"<h1>{self.titulo}</h1>\n"
        
        if self.comentarios:
            for i, (autor, texto, valoracion) in enumerate(self.comentarios):
                estrellas = "★" * valoracion + "☆" * (5 - valoracion)
                html += "<div>\n"
                html += f"<h3>{autor}</h3>\n"
                html += f"<p>{texto}</p>\n"
                html += f"<p>Valoración: {estrellas}</p>\n"
                html += "</div>\n"
        else:
            html += "<p>No hay comentarios aún. ¡Sé el primero en dejar uno!</p>\n"
        
        html += "</section>\n"
        return html


# ============================================================
# PAGINA PRINCIPAL
# ============================================================
class PaginaPrincipal:
    def __init__(self):
        self.menu = MenuNavegacion.crear_menu_estandar()
        self.seccion_info = SeccionInformacion()
        self.seccion_comentarios = SeccionComentarios()
        self.seccion_contacto = SeccionContacto()
    
    def construir(self):
        # INFORMACIÓN
        self.seccion_info.establecer_nombre("Chamba Store")
        self.seccion_info.establecer_imagen("dragon.png")
        self.seccion_info.establecer_descripcion("""
        En nuestra tienda online encontrarás mucho más que tecnología: 
        encontrarás innovación, calidad y confianza. Seleccionamos cuidadosamente 
        los mejores productos electrónicos del mercado para ofrecerte una 
        experiencia de compra fácil, segura y con garantía total.
        """)

        self.seccion_info.establecer_historia("""
        Chamba Store nació en 2010 como una pequeña tienda local dedicada a la 
        venta de componentes informáticos. Con el tiempo, el trato al cliente 
        y la calidad del servicio la convirtieron en un referente tecnológico 
        en Galicia.
        """)

        self.seccion_info.establecer_evolucion("""
        En 2015 dimos el salto al comercio online, ampliando el catálogo con 
        productos electrónicos de última generación. Hoy combinamos innovación 
        con un trato cercano para ofrecer soluciones tecnológicas a todo tipo 
        de usuarios.
        """)

        # CONTACTO
        self.seccion_contacto.establecer_titulo("Contacto")
        self.seccion_contacto.establecer_telefono("988 87 54 20")
        self.seccion_contacto.establecer_email("atencionalcliente@chambastore.com")
        self.seccion_contacto.establecer_direccion("Rúa de La Habana, 88, Ourense, Galicia")
        self.seccion_contacto.establecer_horario("Lunes a Viernes: 8:30 - 21:00")

        # COMENTARIOS
        self.seccion_comentarios.establecer_titulo("Comentarios de clientes")

        # Solo si el JSON está vacío
        if not self.seccion_comentarios.comentarios:
            self.seccion_comentarios.agregar_comentario(
                "Leonardo Dicaprio",
                "Sublime !! Tanto la rapidez de entrega como el servicio post-venta son inmejorables.",
                5
            )

    def render_html(self):
        html = "<!DOCTYPE html>\n<html>\n<head>\n"
        html += "<meta charset='UTF-8'>\n"
        html += "<title>Chamba Store</title>\n"
        html += "</head>\n<body>\n"
        html += self.menu.render()
        html += self.seccion_info.render()
        html += self.seccion_contacto.render()
        html += self.seccion_comentarios.render()
        html += "</body>\n</html>"
        return html
    
    def guardar_html(self, nombre_archivo="chamba_store.html"):
        html_contenido = self.render_html()
        with open(nombre_archivo, 'w', encoding='utf-8') as archivo:
            archivo.write(html_contenido)
        return nombre_archivo


# ============================================================
# EJECUCIÓN PRINCIPAL
# ============================================================
if __name__ == "__main__":
    pagina = PaginaPrincipal()
    pagina.construir()
    pagina.guardar_html("chamba_store.html")
    print("✔ Página generada correctamente")
