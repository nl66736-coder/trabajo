# analisis.py
class AnalisisCliente:
    def __init__(self):
        self.compras = []
        self.comentarios = []

    def registrar_compra(self, producto):
        self.compras.append(producto)

    def registrar_comentario(self, comentario):
        self.comentarios.append(comentario)

    def resumen(self):
        return {
            "total_compras": len(self.compras),
            "total_comentarios": len(self.comentarios),
            "producto_mas_comprado": max(set(self.compras), key=self.compras.count) if self.compras else None
        }
