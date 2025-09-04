# py
# flet
# third
# own

class Place:
    def __init__(self, name, description):
        self.name = name
        self.description = description
        self.objects = []
        self.characters = []
        self.connections = {}
    
    def add_object(self, object):
        self.objects.append(object)
    
    def remove_object(self, name_object):
        for object in self.objects:
            if object.name.lower() == name_object.lower():
                self.objects.remove(object)
                return object
        return None
    
    def add_character(self, character):
        self.characters.append(character)
    
    def connect(self, address, place):
        self.connections[address] = place