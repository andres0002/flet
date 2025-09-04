# py
# flet
# third
# own

class Player:
    def __init__(self, name):
        self.name = name
        self.inventory = []
        self.current_place = None
    
    def collect_object(self, name_object):
        object = self.current_place.remove_object(name_object)
        if object:
            self.inventory.append(object)
            return f"Has collect: {name_object}."
        return f"No hay ningún '{name_object}' here."
    
    def show_inventory(self):
        if not self.inventory:
            return "Inventory is empty."
        items = [obj.name for obj in self.inventory]
        return f"Inventory: {", ".join(items)}."
    
    def move(self, address):
        if address in self.current_place.connections:
            self.current_place = self.current_place.connections[address]
            return f"Te has move to: {self.current_place.name}."
        return "No puedes ir en esa address."