class CatalogoProductos:
    def __init__(self, archivo="catalogo.json"):
        self.archivo = archivo
        self.productos = []
        self.cargar()

    def agregar_producto(self, nombre, descripcion, precio, empaquetado, imagen):
        producto = {
            "nombre": nombre,
            "descripcion": descripcion,
            "precio": precio,
            "empaquetado": empaquetado,
            "imagen": imagen,
        }
        self.productos.append(producto)
        self.guardar()

    def guardar(self):
        import json
        with open(self.archivo, "w", encoding="utf-8") as f:
            json.dump(self.productos, f, ensure_ascii=False, indent=4)

    def cargar(self):
        import os, json
        if os.path.exists(self.archivo):
            with open(self.archivo, "r", encoding="utf-8") as f:
                self.productos = json.load(f)

    def render(self):
        html = "<section id='catalogo'><h1>Catálogo</h1>"
        for p in self.productos:
            html += f"<div><h3>{p['nombre']}</h3>"
            html += f"<img src='{p['imagen']}' alt='{p['nombre']}' style='max-width:200px;'>"
            html += f"<p>{p['descripcion']}</p><p>Precio: {p['precio']} €</p>"
            html += f"<p>Empaquetado: {p['empaquetado']}</p></div>"
        html += "</section>"
        return html
