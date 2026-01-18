# Módulo: catalogo.py
# Gestiona la carga y consulta del catálogo de productos.

import json
import os
from datetime import datetime

class CatalogoProductos:
    def __init__(self, archivo="catalogo.json"):
        # Nombre del archivo donde se guardará el catálogo
        self.archivo = archivo
        # Lista en memoria que contendrá todos los productos
        self.productos = []
        # Al iniciar la clase, intentamos cargar productos desde el archivo si existe
        self.cargar()

    def agregar_producto(self, nombre, descripcion, precio, empaquetado, imagen):
        # Creamos un diccionario con todos los datos del producto
        producto = {
            "nombre": nombre,               # Nombre del producto
            "descripcion": descripcion,     # Descripción detallada
            "precio": precio,               # Precio en euros
            "empaquetado": empaquetado,     # Tipo de empaquetado
            "imagen": imagen,               # Ruta o URL de la imagen
            "fecha_agregado": datetime.now().strftime("%d/%m/%Y %H:%M")  # Fecha y hora actual
        }
        # Añadimos el producto a la lista en memoria
        self.productos.append(producto)
        # Guardamos la lista actualizada en el archivo JSON
        self.guardar()
    
    def guardar(self):
        # Abre el archivo en modo escritura y guarda la lista de productos en formato JSON
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(self.productos, f, ensure_ascii=False, indent=4)

    def cargar(self):
        # Si el archivo existe, lo abrimos y cargamos los productos en memoria
        if os.path.exists(self.archivo):
            with open(self.archivo, "r", encoding="utf-8") as f:
                self.productos = json.load(f)
    def obtener_stock(self, nombre):
        #Devuelve el stock disponible de un producto.
        for producto in self.productos:
            if producto["nombre"] == nombre:
                return producto.get("stock", 0)
        return 0
    def reducir_stock(self, nombre, cantidad):
        #Reduce el stock del producto tras una compra.
        for producto in self.productos:
            if producto["nombre"] == nombre:
                producto["stock"] = max(0, producto.get("stock", 0) - cantidad)
                self.guardar()  # Guardamos el cambio en el JSON
                return True
        return False

    def render(self):
        # Genera el HTML para mostrar el catálogo en la página web
        html = "<section id='catalogo'><h1>Catálogo de Productos</h1>"
        # Recorremos cada producto en la lista
        for p in self.productos:
            html += "<div style='border:1px solid #ccc; margin:10px; padding:10px;'>"
            html += f"<h3>{p['nombre']}</h3>"  # Nombre del producto
            # Si el producto tiene imagen, la mostramos
            if p.get("imagen"):
                html += f"<img src='{p['imagen']}' alt='Imagen de {p['nombre']}' style='max-width:200px;'><br>"
            html += f"<p>{p['descripcion']}</p>"       # Descripción
            html += f"<p>Precio: {p['precio']} €</p>" # Precio
            html += f"<p>Empaquetado: {p['empaquetado']}</p>" # Tipo de empaquetado
            html += "</div>"
        html += "</section>"
        # Devolvemos el HTML completo para integrarlo en la página principal
        return html
