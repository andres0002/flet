# py
# flet
# third
# owm
from menu import Menu, MenuTypes
from order import Order

class Restaurant:
    def __init__(self):
        self.mesas = []
        self.clients = []
        self.pedidos_activos = []
        self.menu = Menu()
        self._inicializar_menu()
    
    def _inicializar_menu(self):
        # Add entradas
        self.menu.add_entrada("Ensalada César", 8.50)
        self.menu.add_entrada("Sopa del día", 6.00)
        # Add platos principales
        self.menu.add_plato_principal("Filete Mignon", 25.99)
        self.menu.add_plato_principal("Salmón a la parrilla", 22.50)
        # Add postres
        self.menu.add_postre("Tiramisú", 6.99)
        self.menu.add_postre("Flan casero", 5.50)
        # Add bebidas
        self.menu.add_bebida("Vino Tinto", 12.00)
        self.menu.add_bebida("Agua mineral", 2.50)
    
    def add_table(self, table):
        self.mesas.append(table)
        return f"Mesa {table.number} (capacidad: {table.size} agregada exitosamente.)"
    
    def search_table(self, table_number):
        for table in self.mesas:
            if table.number == table_number:
                return table
        return None
    
    def assign_client_to_table(self, client, table_number):
        table = self.search_table(table_number)
        if not table:
            return "Mesa no encontrada"
        if table.busy:
            return "Mesa no disponible"
        if client.group_size > table.size:
            return f"Grupo demasiado grande para la mesa (capacidad máxima: {table.size})."
        if table.assign_client(client):
            self.clients.append(client)
            return f"Cliente {client.id} asignado a mesa {table_number}."
        return "No se pudo asignar el client a la mesa."
    
    def create_order(self, table_number):
        table = self.search_table(table_number)
        if table and table.busy:
            order = Order(table)
            self.pedidos_activos.append(order)
            table.current_order = order
            table.client.order_assign(order)
            return order
        return None
    
    def liberar_mesa(self, table_number):
        table = self.search_table(table_number)
        if table:
            client = table.client
            if client:
                client.cleam_order()
                if client in self.clients:
                    self.clients.remove(client)
                if table.current_order in self.pedidos_activos:
                    self.pedidos_activos.remove(table.current_order)
            table.liberar()
            return f"Mesa {table_number} liberada."
        return "Mesa no encontrada."
    
    def get_item_menu(self, type: MenuTypes, name):
        return self.menu.get_item(type, name)