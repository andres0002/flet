# py
from enum import Enum
# flet
# third
# own

class TableStates:
    LIBRE = "LIBRE"
    OCUPADA = "OCUPADA"


class Table:
    def __init__(self, number, size):
        self.number = number
        self.size = size
        self.busy = False
        self.client = None
        self.current_order = None
    
    def assign_client(self, client):
        if client.group_size <= self.size:
            self.client = client
            self.busy = True
            return True
        return False
    
    def liberar(self):
        self.client = None
        self.busy = False
        self.current_order = None
    
    def is_order_active(self):
        return self.current_order is not None