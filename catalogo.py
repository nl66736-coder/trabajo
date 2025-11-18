# catalogo.py
import json, os
from datetime import datetime

class CatalogoProductos:
    def __init__(self, archivo="catalogo.json"):
        self.archivo = archivo
        self.productos = []
        self.cargar()

    def agregar_producto(self, nombre, descripcion, precio, empaquetado):
        producto = {
            "nombre": nombre,
            "descripcion": descripcion,
            "precio": precio,
            "empaquetado": empaquetado,
            "fecha_agregado": datetime.now().strftime("%d/%m/%Y %H:%M")
        }
        self.productos.append(producto)
        self.guardar()

    def actualizar_catalogo(self, nuevos_productos):
        """Renueva el catálogo cada X meses"""
        self.productos = nuevos_productos
        self.guardar()

    def guardar(self):
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(self.productos, f, ensure_ascii=False, indent=4)

    def cargar(self):
        if os.path.exists(self.archivo):
            with open(self.archivo, "r", encoding="utf-8") as f:
                self.productos = json.load(f)

    def render(self):
        html = '<section id="catalogo"><h1>Catálogo de Productos</h1>'
        for p in self.productos:
            html += f"<div><h3>{p['nombre']}</h3><p>{p['descripcion']}</p>"
            html += f"<p>Precio: {p['precio']} €</p>"
            html += f"<p>Empaquetado: {p['empaquetado']}</p></div>"
        html += "</section>"
        return html
print("probando")
