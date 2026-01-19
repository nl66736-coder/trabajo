class Carrito:
    def __init__(self, catalogo):
        # Lista que guarda los productos añadidos al carrito
        # Cada producto será un diccionario con 'producto' y 'cantidad'
        self.catalogo = catalogo
        self.productos = []

    def añadir_producto(self, producto, cantidad=1):
        nombre = producto["nombre"]
        catalogo = self.catalogo

        # 1. Comprobar stock disponible
        stock_disponible = catalogo.obtener_stock(nombre)
        if stock_disponible < cantidad:
            print("No queda stock suficiente de este producto.")
            return False

        # 2. Si el producto ya está en el carrito, aumentar cantidad
        for p in self.productos:
            if p["producto"]["nombre"] == nombre:
                p["cantidad"] += cantidad
                catalogo.reducir_stock(nombre, cantidad)
                return True

        # 3. Si no está en el carrito, añadirlo
        self.productos.append({"producto": producto, "cantidad": cantidad})

        # 4. Reducir stock en el catálogo
        catalogo.reducir_stock(nombre, cantidad)

        return True


    def eliminar_producto(self, indice):
        # Elimina el producto en la posición indicada si el índice es válido
        if 0 <= indice < len(self.productos):
            del self.productos[indice]

    def vaciar(self):
        # Vacía completamente el carrito
        self.productos = []

    def calcular_total(self):
        # Calcula el precio total sumando precio * cantidad de cada producto
        return sum(float(p["producto"]["precio"]) * p["cantidad"] for p in self.productos)

    def render(self):
        # Genera el HTML para mostrar el carrito en la página web
        html = "<section id='carrito'><h1>Carrito de Compras</h1>"

        if not self.productos:
            html += "<p class='carrito-vacio'>Tu carrito está vacío.</p>"
        else:
            for i, p in enumerate(self.productos):
                producto = p["producto"]
                cantidad = p["cantidad"]
                subtotal = float(producto['precio']) * cantidad
                html += f"""
                <div class="producto-carrito">
                    <div class="producto-info">
                        <h3>{producto['nombre']}</h3>
                        <p>{producto['descripcion']}</p>
                        <p><strong>Precio unitario:</strong> {producto['precio']} €</p>
                        <p><strong>Cantidad:</strong> {cantidad}</p>
                        <form action='/eliminar_carrito/{i}' method='post' style='display:inline;'>
                            <button type='submit' class='btn-eliminar'>Eliminar</button>
                        </form>
                    </div>
                    <div class="producto-precio">{subtotal:.2f} €</div>
                </div>
                """
            # Mostrar el total acumulado
            total = self.calcular_total()
            html += f"""
            <div class="total-section">
                <h2>Total: {total:.2f} €</h2>
            </div>
            
            <div style='text-align: center; margin-top: 2rem;'>
                <form action='/finalizar_compra' method='post' style='display: inline;'>
                    <button type='submit' class='btn-comprar'>Finalizar Compra</button>
                </form>
                <form action='/vaciar_carrito' method='post' style='display: inline;'>
                    <button type='submit' class='btn-vaciar'>Vaciar carrito</button>
                </form>
            </div>
            """

        html += "</section>"
        return html

            
