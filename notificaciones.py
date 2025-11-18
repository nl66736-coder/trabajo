# notificaciones.py
class Notificaciones:
    def __init__(self):
        self.avisos = []
        self.recomendaciones = []

    def nuevo_producto(self, producto):
        self.avisos.append(f"Nuevo producto disponible: {producto['nombre']}")

    def recomendar(self, historial_compras):
        # Ejemplo simple: recomendar el último producto comprado
        if historial_compras:
            ultimo = historial_compras[-1]
            self.recomendaciones.append(f"Basado en tu compra de {ultimo}, te recomendamos otros similares.")
    
    def render(self):
        html = "<section id='notificaciones'><h1>Notificaciones</h1>"
        for aviso in self.avisos:
            html += f"<p>{aviso}</p>"
        for rec in self.recomendaciones:
            html += f"<p>{rec}</p>"
        html += "</section>"
        return html
