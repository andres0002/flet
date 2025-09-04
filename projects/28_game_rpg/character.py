# py
# flet
# third
# own

class Character:
    def __init__(self, name, dialogue):
        self.name = name
        self.dialogue = dialogue
    
    def talk(self):
        return f"{self.name}: {self.dialogue}."