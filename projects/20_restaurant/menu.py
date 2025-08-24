# py
from enum import Enum
# flet
# third
# owm

class MenuTypes(Enum):
    ENTRADA = "Entrada"
    PLATO_PRINCIPAL = "Plato Principal"
    POSTRE = "Postre"
    BEBIDA = "Bebida"

class ItemMenu:
    def __init__(self, name, price, quantity=1):
        self.name = name
        self.price = price
        self.quantity = quantity
    
    def calcular_subtotal(self):
        return self.price * self.quantity

class Entrada(ItemMenu):
    def __init__(self, name, price, quantity=1):
        super().__init__(name, price, quantity)
        self.type = MenuTypes.ENTRADA

class PlatoPrincipal(ItemMenu):
    def __init__(self, name, price, quantity=1):
        super().__init__(name, price, quantity)
        self.type = MenuTypes.PLATO_PRINCIPAL

class Postre(ItemMenu):
    def __init__(self, name, price, quantity=1):
        super().__init__(name, price, quantity)
        self.type = MenuTypes.POSTRE

class Bebida(ItemMenu):
    def __init__(self, name, price, quantity=1):
        super().__init__(name, price, quantity)
        self.type = MenuTypes.BEBIDA

class Menu:
    def __init__(self):
        self.entradas = []
        self.platos_principales = []
        self.postres = []
        self.bebidas = []
    
    def add_entrada(self, name, price, quantity=1):
        entrada = Entrada(name, price, quantity)
        self.entradas.append(entrada)
        return entrada
    
    def add_plato_principal(self, name, price, quantity=1):
        plato_principal = PlatoPrincipal(name, price, quantity)
        self.platos_principales.append(plato_principal)
        return plato_principal
    
    def add_postre(self, name, price, quantity=1):
        postre = Postre(name, price, quantity)
        self.postres.append(postre)
        return postre
    
    def add_bebida(self, name, price, quantity=1):
        bebida = Bebida(name, price, quantity)
        self.bebidas.append(bebida)
        return bebida
    
    def delete_item(self, type: MenuTypes, name):
        if type == MenuTypes.ENTRADA:
            items = self.entradas
        elif type == MenuTypes.PLATO_PRINCIPAL:
            items = self.platos_principales
        elif type == MenuTypes.POSTRE:
            items = self.postres
        elif type == MenuTypes.BEBIDA:
            items = self.bebidas
        else:
            return False
        
        for item in items[:]:
            if item.name == name:
                items.remove(item)
                return True
        return False
    
    def delete_entrada(self, name):
        return self.delete_item(MenuTypes.ENTRADA, name)
    
    def delete_plato_principal(self, name):
        return self.delete_item(MenuTypes.PLATO_PRINCIPAL, name)
    
    def delete_postre(self, name):
        return self.delete_item(MenuTypes.POSTRE, name)
    
    def delete_bebida(self, name):
        return self.delete_item(MenuTypes.BEBIDA, name)
    
    def get_item(self, type: MenuTypes, name):
        if type == MenuTypes.ENTRADA:
            items = self.entradas
        elif type == MenuTypes.PLATO_PRINCIPAL:
            items = self.platos_principales
        elif type == MenuTypes.POSTRE:
            items = self.postres
        elif type == MenuTypes.BEBIDA:
            items = self.bebidas
        else:
            return None
        
        for item in items:
            if item.name == name:
                return item
        return None