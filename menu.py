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
        menu.agregar_item("Catálogo", "/catalogo")
        menu.agregar_item("Carrito", "/carrito")
<<<<<<< HEAD
        menu.agregar_item("Comentarios", "/comentarios")
        menu.agregar_item("Contacto", "/contacto")
        menu.agregar_item("Historia", "/historia")
        menu.agregar_item("Tendencias", "/tendencias")
=======
        menu.agregar_item("Notificaciones", "/notificaciones")
        menu.agregar_item("Mi Perfil", "/perfil") 
>>>>>>> afd8f92a7686afd7e48c188dfc06ab2cc985a90f
        menu.agregar_item("Info Social", "/info-social")
        return menu
    

    


