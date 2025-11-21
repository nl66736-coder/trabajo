class Carrito:
    def __init__(self):
        # Lista que guarda los productos añadidos al carrito
        self.productos = []

    def añadir_producto(self, producto):
        # Añade un producto (diccionario) al carrito
        self.productos.append(producto)

    def eliminar_producto(self, indice):
        # Elimina el producto en la posición indicada si el índice es válido
        if 0 <= indice < len(self.productos):
            del self.productos[indice]

    def vaciar(self):
        # Vacía completamente el carrito
        self.productos = []

    def calcular_total(self):
        # Calcula el precio total sumando el campo 'precio' de cada producto
        return sum(float(p["precio"]) for p in self.productos)

    def render(self):
        # Genera el HTML para mostrar el carrito en la página web
        html = "<section id='carrito'><h1>Carrito de Compras</h1>"

        if not self.productos:
            # Si no hay productos, mostramos un mensaje
            html += "<p>Tu carrito está vacío.</p>"
        else:
            # Si hay productos, los mostramos uno por uno
            for i, p in enumerate(self.productos):
                html += f"""
                <div style='border:1px solid #ccc; margin:10px; padding:10px;'>
                    <h3>{p['nombre']}</h3>
                    <p>{p['descripcion']}</p>
                    <p><strong>Precio:</strong> {p['precio']} €</p>
                    <form action='/eliminar_carrito/{i}' method='post'>
                        <button type='submit'>Eliminar</button>
                    </form>
                </div>
                """
            