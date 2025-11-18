# corporativa.py
class SeccionCorporativa:
    def __init__(self):
        self.historia = ""
        self.tendencias = []
        self.contacto_social = {}

    def establecer_historia(self, texto):
        self.historia = texto

    def agregar_tendencia(self, tendencia):
        self.tendencias.append(tendencia)

    def establecer_contacto_social(self, redes):
        """redes es un diccionario con claves: facebook, instagram, twitter, email"""
        self.contacto_social = redes

    def render(self):
        html = "<section id='corporativa'><h1>Información Corporativa</h1>"
        if self.historia:
            html += f"<h2>Historia</h2><p>{self.historia}</p>"
        if self.tendencias:
            html += "<h2>Tendencias Globales</h2><ul>"
            for t in self.tendencias:
                html += f"<li>{t}</li>"
            html += "</ul>"
        if self.contacto_social:
            html += "<h2>Redes Sociales</h2><ul>"
            for red, enlace in self.contacto_social.items():
                html += f"<li>{red}: <a href='{enlace}'>{enlace}</a></li>"
            html += "</ul>"
        html += "</section>"
        return html
