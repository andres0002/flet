# py
from enum import Enum
# flet
# third
# owm
from menu import MenuTypes

class OrderStates:
    PENDIENTE = "Pendiente"
    LISTO = "Listo"
    ENTREGADO = "Entregado"
    EN_PREPARACION = "En Preparación"

from menu import ItemMenu

class Order:
    def __init__(self, mesa):
        self.mesa = mesa
        self.items = {
            "entradas": [],
            "platos_principales": [],
            "postres": [],
            "bebidas": []
        }
        self.state = OrderStates.PENDIENTE
    
    def add_item(self, item):
        if isinstance(item, ItemMenu):
            if item.type == MenuTypes.ENTRADA:
                self.items["entradas"].append(item)
            if item.type == MenuTypes.PLATO_PRINCIPAL:
                self.items["platos_principales"].append(item)
            if item.type == MenuTypes.POSTRE:
                self.items["postres"].append(item)
            if item.type == MenuTypes.BEBIDA:
                self.items["bebidas"].append(item)
    
    def calcular_total(self):
        total = 0
        for values in self.items.values():
            for value in values:
                total += value.calcular_subtotal()
        return round(total, 2)
    
    def change_state(self, new_state: OrderStates):
        if new_state in [OrderStates.ENTREGADO, OrderStates.PENDIENTE, OrderStates.EN_PREPARACION, OrderStates.LISTO]:
            self.state = new_state
            return True
        return False
    
    def get_summary(self):
        summary = []
        for key, values in self.items.items():
            if values:
                summary.append(f"{"\n" if summary else ""}{key.replace("_", "").title()}:")
                for value in values:
                    summary.append(f"- {value.name} x {value.quantity}: ${value.calcular_subtotal():.2f}.")
        summary.append(f"{"\n" if summary else ""}Total: ${self.calcular_total():.2f}.")
        return "\n".join(summary)