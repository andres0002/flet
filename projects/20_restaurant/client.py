# py
# flet
# third
# owm

class Client:
    _next_id = 1 # Variable de class para mantener el siguiente id.
    
    def __init__(self, group_size):
        self.id = f"C{Client._next_id:03d}" # format: C001, C002, etc.
        Client._next_id += 1
        self.group_size = group_size
        self.current_order = None
    
    def order_assign(self, order):
        self.current_order = order
    
    def get_current_total(self):
        return self.current_order.calcular_total() if self.current_order else 0
    
    def cleam_order(self):
        self.current_order = None
    
    @classmethod
    def reset_counter(cls):
        cls._next_id = 1