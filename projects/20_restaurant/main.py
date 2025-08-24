# py
# flet
import flet as ft # type: ignore
# third
# own
from client import Client
from table import Table, TableStates
from restaurant import Restaurant
from menu import MenuTypes
from order import OrderStates

class RestaurantGUI:
    def __init__(self):
        self.restaurant = Restaurant()
        capacidades = [2, 3, 4, 5, 6, 7]
        for i in range(1, 7):
            self.restaurant.add_table(Table(i, capacidades[i - 1]))
    
    # methods views.
    def create_view_mesera(self):
        self.grid_container = ft.Container(
            content=self.create_grid_mesas(),
            width=600,
            expand=1
        )
        
        return ft.Row(
            controls=[
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Text(
                                "Mesas del Restaurant",
                                size=20,
                                weight="bold"
                            ),
                            self.grid_container
                        ],
                        expand=1,
                        scroll=ft.ScrollMode.ALWAYS
                    ),
                    padding=20
                ),
                self.vertical_divider,
                ft.Container(
                    content=self.create_panel_gestion(),
                    width=400,
                    expand=1,
                    padding=20
                )
            ],
            expand=1,
            alignment=ft.alignment.center,
            scroll=ft.ScrollMode.AUTO
        )
    
    def create_view_cocina(self):
        self.list_orders_cocina = ft.ListView(
            expand=1,
            spacing=10,
            padding=20,
            auto_scroll=True
        )
        
        def change_state_order(event, order, new_state: OrderStates):
            order.change_state(new_state)
            self.update_view_cocina()
            self.update_ui(event.page)
            event.page.update()
        
        def create_item_order(order):
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            f"Mesa {order.mesa.number}",
                            size=20,
                            weight="bold"
                        ),
                        ft.Text(
                            order.get_summary()
                        ),
                        ft.Row(
                            controls=[
                                ft.ElevatedButton(
                                    text=OrderStates.EN_PREPARACION,
                                    on_click=lambda event, p_order=order: change_state_order(event, p_order, OrderStates.EN_PREPARACION),
                                    disabled=order.state != OrderStates.PENDIENTE,
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.Colors.ORANGE_700,
                                        color=ft.Colors.WHITE
                                    )
                                ),
                                ft.ElevatedButton(
                                    text=OrderStates.LISTO,
                                    on_click=lambda event, p_order=order: change_state_order(event, p_order, OrderStates.LISTO),
                                    disabled=order.state != OrderStates.EN_PREPARACION,
                                    style=ft.ButtonStyle(
                                        bgcolor=ft.Colors.GREEN_700,
                                        color=ft.Colors.WHITE
                                    )
                                ),
                                ft.Text(
                                    f"Estado: {order.state}",
                                    color=ft.Colors.BLUE_200
                                )
                            ]
                        )
                    ]
                ),
                bgcolor=ft.Colors.BLUE_GREY_900,
                padding=10,
                border_radius=8
            )
        
        def update_view_cocina():
            self.list_orders_cocina.controls.clear()
            for order in self.restaurant.pedidos_activos:
                if order.state in [OrderStates.PENDIENTE, OrderStates.EN_PREPARACION]:
                    self.list_orders_cocina.controls.append(create_item_order(order))
        
        self.update_view_cocina = update_view_cocina
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Pedidos Pendientes",
                        size=24,
                        weight="bold"
                    ),
                    self.list_orders_cocina
                ],
            ),
            expand=1,
            padding=20
        )
    
    def create_view_box(self):
        self.list_box = ft.ListView(
            expand=1,
            spacing=10,
            padding=20,
            auto_scroll=True
        )
        
        def procesar_pago(event, table):
            if table.current_order:
                self.restaurant.liberar_mesa(table.number)
                self.update_ui(event.page)
        
        def create_item_acount(table):
            if not table.current_order:
                return None
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            f"Mesa {table.number}",
                            size=20,
                            weight="bold"
                        ),
                        ft.Text(
                            f"Cliente: {table.client.id}"
                        ),
                        ft.Text(
                            table.current_order.get_summary()
                        ),
                        ft.ElevatedButton(
                            "Procesar Pago",
                            on_click=lambda event, p_table=table: procesar_pago(event, p_table),
                            style=ft.ButtonStyle(
                                bgcolor=ft.Colors.GREEN_700,
                                color=ft.Colors.WHITE
                            )
                        )
                    ]
                ),
                bgcolor=ft.Colors.BLUE_GREY_900,
                padding=10,
                border_radius=8
            )
        
        def update_view_box():
            self.list_box.controls.clear()
            for table in self.restaurant.mesas:
                if table.busy and table.current_order:
                    item = create_item_acount(table)
                    if item:
                        self.list_box.controls.append(item)
        
        self.update_view_box = update_view_box
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Cuentas Activas",
                        size=24,
                        weight="bold"
                    ),
                    self.list_box
                ]
            ),
            expand=1,
            padding=20
        )
    
    def create_view_admin(self):
        # new items
        self.type_item_admin = ft.Dropdown(
            label="Tipo de Item",
            options=[
                ft.DropdownOption(
                    key=MenuTypes.ENTRADA.value,
                    content=ft.Text(
                        MenuTypes.ENTRADA.value
                    )
                ),
                ft.DropdownOption(
                    key=MenuTypes.PLATO_PRINCIPAL.value,
                    content=ft.Text(
                        MenuTypes.PLATO_PRINCIPAL.value
                    )
                ),
                ft.DropdownOption(
                    key=MenuTypes.POSTRE.value,
                    content=ft.Text(
                        MenuTypes.POSTRE.value
                    )
                ),
                ft.DropdownOption(
                    key=MenuTypes.BEBIDA.value,
                    content=ft.Text(
                        MenuTypes.BEBIDA.value
                    )
                )
            ],
            width=300
        )
        
        self.name_item = ft.TextField(
            label="Name",
            width=300
        )
        
        self.price_item = ft.TextField(
            label="Price",
            width=300,
            input_filter=ft.NumbersOnlyInputFilter()
        )
        
        # delete items
        self.type_item_delete = ft.Dropdown(
            label="Tipo de Item",
            options=[
                ft.DropdownOption(
                    key=MenuTypes.ENTRADA.value,
                    content=ft.Text(
                        MenuTypes.ENTRADA.value
                    )
                ),
                ft.DropdownOption(
                    key=MenuTypes.PLATO_PRINCIPAL.value,
                    content=ft.Text(
                        MenuTypes.PLATO_PRINCIPAL.value
                    )
                ),
                ft.DropdownOption(
                    key=MenuTypes.POSTRE.value,
                    content=ft.Text(
                        MenuTypes.POSTRE.value
                    )
                ),
                ft.DropdownOption(
                    key=MenuTypes.BEBIDA.value,
                    content=ft.Text(
                        MenuTypes.BEBIDA.value
                    )
                )
            ],
            width=300,
            on_change=self.update_item_delete
        )
        
        self.item_delete = ft.Dropdown(
            label="Seleccionar Item a Eliminar",
            width=300
        )
        
        def add_item(event):
            type = self.type_item_admin.value
            name = self.name_item.value
            
            try:
                price = float(self.price_item.value)
                if type and name and price > 0:
                    type = MenuTypes(type)
                    if type == MenuTypes.ENTRADA:
                        self.restaurant.menu.add_entrada(name, price)
                    elif type == MenuTypes.PLATO_PRINCIPAL:
                        self.restaurant.menu.add_plato_principal(name, price)
                    elif type == MenuTypes.POSTRE:
                        self.restaurant.menu.add_postre(name, price)
                    elif type == MenuTypes.BEBIDA:
                        self.restaurant.menu.add_bebida(name, price)
                    
                    # cleam fields
                    self.name_item.value = ""
                    self.price_item.value = ""
                    # update dropdowns
                    self.update_item_menu(None)
                    self.update_item_delete(None)
                    event.page.update()
            except Exception as _:
                print("Error")
        
        def delete_item(event):
            type = self.type_item_delete.value
            name = self.item_delete.value
            if type and name:
                self.restaurant.menu.delete_item(MenuTypes(type), name)
                # update dropdowns
                self.update_item_menu(None)
                self.update_item_delete(None)
                event.page.update()

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(
                        "Agregar Item al Menu",
                        size=20,
                        weight="bold"
                    ),
                    self.type_item_admin,
                    self.name_item,
                    self.price_item,
                    ft.ElevatedButton(
                        text="Add Item",
                        on_click=add_item,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.GREEN_700,
                            color=ft.Colors.WHITE
                        )
                    ),
                    self.divider,
                    ft.Text(
                        "Eliminar Item del Menu",
                        size=20,
                        weight="bold"
                    ),
                    self.type_item_delete,
                    self.item_delete,
                    ft.ElevatedButton(
                        text="Elinimar Item",
                        on_click=delete_item,
                        style=ft.ButtonStyle(
                            bgcolor=ft.Colors.RED_700,
                            color=ft.Colors.WHITE
                        )
                    )
                ],
                expand=1,
                scroll=ft.ScrollMode.AUTO
            ),
            padding=20
        )
    
    # methods internos views.
    def update_item_delete(self, event):
        type = self.type_item_delete.value
        self.item_delete.options = []
        
        if type == None:
            type = self.type_item_admin.value
        
        type = MenuTypes(type)
        
        if type == MenuTypes.ENTRADA:
            items = self.restaurant.menu.entradas
        elif type == MenuTypes.PLATO_PRINCIPAL:
            items = self.restaurant.menu.platos_principales
        elif type == MenuTypes.POSTRE:
            items = self.restaurant.menu.postres
        elif type == MenuTypes.BEBIDA:
            items = self.restaurant.menu.bebidas
        else:
            items = []
        
        self.item_delete.options = [
            ft.DropdownOption(
                key=item.name,
                content=ft.Text(
                    item.name
                )
            ) for item in items
        ]
        
        if event and event.page:
            event.page.update()
    
    def create_grid_mesas(self):
        grid = ft.GridView(
            expand=1,
            runs_count=2,
            max_extent=200,
            child_aspect_ratio=1.0,
            spacing=10,
            run_spacing=10,
            padding=10
        )
        
        for mesa in self.restaurant.mesas:
            color = ft.Colors.GREEN_700 if not mesa.busy else ft.Colors.RED_700
            state = TableStates.LIBRE if not mesa.busy else TableStates.OCUPADA
            
            grid.controls.append(
                ft.Container(
                    content=ft.Column(
                        controls=[
                            ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.TABLE_RESTAURANT,
                                        color=ft.Colors.AMBER_400
                                    ),
                                    ft.Text(
                                        f"Mesa {mesa.number}",
                                        size=16,
                                        weight="bold"
                                    )
                                ],
                                alignment=ft.MainAxisAlignment.CENTER
                            ),
                            ft.Text(
                                f"Capacidad: {mesa.size} personas.",
                                size=14
                            ),
                            ft.Text(
                                state,
                                size=16,
                                weight="bold"
                            )
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=5
                    ),
                    bgcolor=color,
                    border_radius=8,
                    ink=True,
                    on_click=lambda event, num=mesa.number: self.select_mesa(event, num)
                )
            )
        return grid
    
    def update_ui(self, page):
        new_grid = self.create_grid_mesas()
        self.grid_container.content = new_grid
        
        if self.table_selected:
            if self.table_selected.busy and self.table_selected.current_order:
                self.summary_order.value = self.table_selected.current_order.get_summary()
            else:
                self.summary_order.value = "Empty"
            
            self.assign_btn.disabled = self.table_selected.busy
            self.add_item_btn.disabled = not self.table_selected.busy
            self.liberar_btn.disabled = not self.table_selected.busy
            
        self.update_view_cocina()
        self.update_view_box()
        
        page.update()
    
    def select_mesa(self, event, table_number):
        self.table_selected = self.restaurant.search_table(table_number)
        table = self.table_selected
        
        self.table_info.value = f"Mesa {table.number} - Capacidad: {table.size} personas."
        self.assign_btn.disabled = table.busy
        self.add_item_btn.disabled = not table.busy
        self.liberar_btn.disabled = not table.busy
        
        if table.busy and table.current_order:
            self.summary_order.value = table.current_order.get_summary()
        else:
            self.summary_order.value = "Empty"
        
        event.page.update()
        
        return None
    
    def assign_client(self, event):
        if not self.table_selected:
            return
        try:
            group_size = int(self.group_size_input.value)
            if group_size <= 0:
                return
            client = Client(group_size)
            result = self.restaurant.assign_client_to_table(client, self.table_selected.number)
            if "asignado" in result:
                self.restaurant.create_order(self.table_selected.number)
                self.group_size_input.value = ""
                self.update_ui(event.page)
        except Exception as _:
            pass
    
    def add_item_order(self, event):
        if not self.table_selected or not self.table_selected.current_order:
            return
        type = self.type_item_dropdown.value
        name = self.items_dropdown.value
        
        if type and name:
            item = self.restaurant.get_item_menu(MenuTypes(type), name)
            if item:
                self.table_selected.current_order.add_item(item)
                self.update_ui(event.page)
    
    def liberar_mesa(self, event):
        if self.table_selected:
            self.restaurant.liberar_mesa(self.table_selected.number)
            self.update_ui(event.page)
    
    def create_panel_gestion(self):
        self.table_selected = None
        self.table_info = ft.Text(
            "No se a seleccionado ninguna mesa.",
            size=16,
            weight="bold"
        )
        
        self.group_size_input = ft.TextField(
            label="Tamaño del grupo",
            input_filter=ft.NumbersOnlyInputFilter(),
            prefix_icon=ft.Icons.PEOPLE
        )
        self.type_item_dropdown = ft.Dropdown(
            label="Tipo de Item",
            options=[
                ft.DropdownOption(
                    key=MenuTypes.ENTRADA.value,
                    content=ft.Text(MenuTypes.ENTRADA.value)
                ),
                ft.DropdownOption(
                    key=MenuTypes.PLATO_PRINCIPAL.value,
                    content=ft.Text(MenuTypes.PLATO_PRINCIPAL.value)
                ),
                ft.DropdownOption(
                    key=MenuTypes.POSTRE.value,
                    content=ft.Text(MenuTypes.POSTRE.value)
                ),
                ft.DropdownOption(
                    key=MenuTypes.BEBIDA.value,
                    content=ft.Text(MenuTypes.BEBIDA.value)
                )
            ],
            on_change=self.update_item_menu,
            width=250
        )
        
        self.items_dropdown = ft.Dropdown(
            label="Select Item",
            width=250
        )
        
        self.assign_btn = ft.ElevatedButton(
            text="Asignar Cliente",
            on_click=self.assign_client,
            disabled=True,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.GREEN_700,
                color=ft.Colors.WHITE
            )
        )
        
        self.add_item_btn = ft.ElevatedButton(
            text="Agregar Item",
            on_click=self.add_item_order,
            disabled=True,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.BLUE_700,
                color=ft.Colors.WHITE
            )
        )
        
        self.liberar_btn = ft.ElevatedButton(
            text="Liberar Mesa",
            on_click=self.liberar_mesa,
            disabled=True,
            style=ft.ButtonStyle(
                bgcolor=ft.Colors.RED_700,
                color=ft.Colors.WHITE
            )
        )
        
        self.summary_order = ft.Text(
            "Empty",
            size=14
        )
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=self.table_info,
                        bgcolor=ft.Colors.BLUE_GREY_900,
                        padding=10,
                        border_radius=8
                    ),
                    self.group_size_input,
                    self.assign_btn,
                    self.divider,
                    self.type_item_dropdown,
                    self.items_dropdown,
                    self.add_item_btn,
                    self.divider,
                    self.liberar_btn,
                    self.divider,
                    ft.Text(
                        "Resumen del Pedido:",
                        size=16,
                        weight="bold"
                    ),
                    ft.Container(
                        content=self.summary_order,
                        bgcolor=ft.Colors.BLUE_GREY_900,
                        padding=10,
                        border_radius=8
                    ),
                ],
                expand=1,
                scroll=ft.ScrollMode.ALWAYS
            )
        )
    
    def update_item_menu(self, event):
        type = self.type_item_dropdown.value
        self.items_dropdown.options = []
        
        if type == None:
            type = self.type_item_admin.value
        
        if type == None:
            type = self.type_item_delete.value
        
        type = MenuTypes(type)
        
        if type == MenuTypes.ENTRADA:
            items = self.restaurant.menu.entradas
        elif type == MenuTypes.PLATO_PRINCIPAL:
            items = self.restaurant.menu.platos_principales
        elif type == MenuTypes.POSTRE:
            items = self.restaurant.menu.postres
        elif type == MenuTypes.BEBIDA:
            items = self.restaurant.menu.bebidas
        else:
            items = []
        
        self.items_dropdown.options = [
            ft.DropdownOption(item.name) for item in items
        ]
        if event and event.page:
            event.page.update()
    
    def main(self, page: ft.Page):
        page.title = "Restaurant"
        page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
        page.theme_mode = ft.ThemeMode.DARK

        title = ft.Text(
            "Restaurant",
            size=30,
            weight="bold"
        )
        
        self.divider = ft.Divider()
        self.vertical_divider = ft.VerticalDivider()
        
        self.tabs = ft.Tabs(
            selected_index=0,
            animation_duration=300,
            tabs=[
                ft.Tab(
                    text="Mesera",
                    icon=ft.Icons.PERSON,
                    content=self.create_view_mesera()
                ),
                ft.Tab(
                    text="Cocina",
                    icon=ft.Icons.RESTAURANT,
                    content=self.create_view_cocina()
                ),
                ft.Tab(
                    text="Caja",
                    icon=ft.Icons.POINT_OF_SALE,
                    content=self.create_view_box()
                ),
                ft.Tab(
                    text="Administración",
                    icon=ft.Icons.ADMIN_PANEL_SETTINGS,
                    content=self.create_view_admin()
                )
            ],
            expand=1
        )
        
        content = ft.Column(
            controls=[
                self.tabs
            ],
            expand=1
        )
        
        page.add(
            title,
            self.divider,
            content,
            self.divider
        )

def main():
    restaurant = RestaurantGUI()
    ft.app(target=restaurant.main)

if __name__ == "__main__":
    main()