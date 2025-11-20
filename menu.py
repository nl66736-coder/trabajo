class MenuNavegacion:
    def __init__(self):
        self.items = []

    def agregar_item(self, nombre, url):
        self.items.append((nombre, url))

    def render(self):
        html = "<nav><ul>\n"
        for nombre, url in self.items:
            html += f'  <li><a href="{url}">{nombre}</a></li>\n'
        html += "</ul></nav>\n"
        return html
    
    @staticmethod
    def crear_menu_estandar():
        menu = MenuNavegacion()
        menu.agregar_item("Inicio", "/inicio")
        menu.agregar_item("Contacto", "/contacto")
        menu.agregar_item("Historia y Evolución", "/historia")
        menu.agregar_item("Comentarios", "/comentarios")
        menu.agregar_item("Tendencias", "/tendencias")
        return menu
    
    #prueba
    


