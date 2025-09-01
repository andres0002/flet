# py
from enum import Enum
# flet
import flet as ft # type: ignore
# third
# own

class ColorTypes(Enum):
    RED = "RED"
    BLUE = "BLUE"
    YELLOW = "YELLOW"
    PURPLE = "PURPLE"
    LIME = "LIME"
    BLACK = "BLACK"
    WHITE = "WHITE"

def main(page: ft.Page):
    page.title = "Web App"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    def create_dlg_modal(title, description):
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text(title, text_align=ft.TextAlign.CENTER),
            content=ft.Text(description),
            actions=[
                ft.TextButton("Ok", on_click=lambda e: page.close(dlg_modal)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        return dlg_modal
    
    title = ft.Text("Web App", size=30, weight="bold")
    
    input_name = ft.TextField(label="Name", hint_text="Enter name.")
    
    def handle_click(_):
        if input_name.value:
            text_greeting.value = f"¡Hola, {input_name.value}!"
            text_greeting.update()
            input_name.value = ""
            input_name.update()
        else:
            text_greeting.value = "Please, enter name."
            text_greeting.update()
    
    btn_elevated = ft.ElevatedButton(
        text="Gretting",
        on_click=handle_click
    )
    
    text_greeting = ft.Text("Hola", size=20, weight="bold")
    
    divider = ft.Divider()
    
    input_item = ft.TextField(label="Element", hint_text="Enter element.")
    
    def handle_add_click(_):
        if input_item.value == "":
            dlg_modal = create_dlg_modal(
                "Text Field",
                "Debe ingresar un element."
            )
            page.open(dlg_modal)
            return
        item_list.controls.append(ft.Text(f"- {input_item.value}"))
        item_list.update()
        input_item.value = ""
        input_item.update()
    
    btn_add_item = ft.ElevatedButton(
        text="Add Item",
        on_click=handle_add_click
    )
    
    item_list = ft.ListView()
    
    def handle_change(_):
        colorType = ColorTypes(dropdown_background_color.value)
        
        if colorType == ColorTypes.RED:
            page.bgcolor = ft.Colors.RED
        elif colorType == ColorTypes.BLUE:
            page.bgcolor = ft.Colors.BLUE
        elif colorType == ColorTypes.YELLOW:
            page.bgcolor = ft.Colors.YELLOW
        elif colorType == ColorTypes.PURPLE:
            page.bgcolor = ft.Colors.PURPLE
        elif colorType == ColorTypes.LIME:
            page.bgcolor = ft.Colors.LIME
        elif colorType == ColorTypes.BLACK:
            page.bgcolor = ft.Colors.BLACK
        elif colorType == ColorTypes.WHITE:
            page.bgcolor = ft.Colors.WHITE
        page.update()
    
    dropdown_background_color = ft.Dropdown(
        label="Select Background Color",
        options=[
            ft.DropdownOption(
                key=ColorTypes.BLACK.value,
                content=ft.Text(ColorTypes.BLACK.value)
            ),
            ft.DropdownOption(
                key=ColorTypes.WHITE.value,
                content=ft.Text(ColorTypes.WHITE.value)
            ),
            ft.DropdownOption(
                key=ColorTypes.RED.value,
                content=ft.Text(ColorTypes.RED.value)
            ),
            ft.DropdownOption(
                key=ColorTypes.BLUE.value,
                content=ft.Text(ColorTypes.BLUE.value)
            ),
            ft.DropdownOption(
                key=ColorTypes.YELLOW.value,
                content=ft.Text(ColorTypes.YELLOW.value)
            ),
            ft.DropdownOption(
                key=ColorTypes.PURPLE.value,
                content=ft.Text(ColorTypes.PURPLE.value)
            ),
            ft.DropdownOption(
                key=ColorTypes.LIME.value,
                content=ft.Text(ColorTypes.LIME.value)
            ),
        ],
        width=400,
        on_change=handle_change,
        value="BLACK"
    ) 
    
    content = ft.Column(
        controls=[
            ft.Text("Greeting", size=20, weight="bold"),
            ft.Row(
                controls=[
                    input_name,
                    btn_elevated
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            text_greeting,
            divider,
            ft.Text("Add", size=20, weight="bold"),
            ft.Row(
                controls=[
                    input_item,
                    btn_add_item
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            ft.Text("Dynamic List", size=20, weight="bold"),
            item_list,
            divider,
            ft.Text("Update Background Color", size=20, weight="bold"),
            dropdown_background_color
        ],
        expand=1,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    page.add(
        title,
        divider,
        content,
        divider
    )

ft.app(target=main, view=ft.WEB_BROWSER)