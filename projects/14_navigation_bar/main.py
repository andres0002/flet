# py
# flet
import flet as ft # type: ignore
# third
# own

def main(page: ft.Page):
    page.title = "NavigationBar"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    def on_increment(_):
        nonlocal counter_value
        counter_value += 1
        counter_text.value = f"Counter: {counter_value}"
        page.update()
    
    def on_decrement(_):
        nonlocal counter_value
        counter_value -= 1
        counter_value = counter_value if counter_value >= 0 else 0
        counter_text.value = f"Counter: {counter_value}"
        page.update()
    
    counter_value = 0
    counter_text = ft.Text("Counter: 0", size=20, weight="bold")
    btn_increment = ft.ElevatedButton("Increment", on_click=on_increment)
    btn_decrement = ft.ElevatedButton("Decrement", on_click=on_decrement)
    
    content_home = ft.Column(
        controls=[
            ft.Text("Home", size=30, weight="bold"),
            counter_text,
            btn_increment,
            btn_decrement
            
        ],
        expand=1,
        scroll=ft.ScrollMode.AUTO
    )
    
    def show_home():
        page.controls.clear()
        page.add(content_home)
    
    def on_search(_):
        search_output.value = f"Se busco: {search_input.value}."
        search_input.value = ""
        page.update()
    
    search_input = ft.TextField(label="Search", hint_text="Enter here.")
    btn_search = ft.ElevatedButton("Search", on_click=on_search)
    search_output = ft.Text("", size=20, weight="bold")
    
    content_search = ft.Column(
        controls=[
            ft.Text("Search", size=30, weight="bold"),
            search_input,
            btn_search,
            search_output
        ],
        expand=1,
        scroll=ft.ScrollMode.AUTO
    )
    
    def show_search():
        page.controls.clear()
        page.add(content_search)
    
    def on_reset_brightness(_):
        slider.value = 50
        slider.label = "Brightness 50"
        page.update()
    
    slider = ft.Slider(
                min=0,
                max=100,
                value=50,
                divisions=10,
                label="Brightness {value}"
            )
    btn_setting = ft.ElevatedButton("Reset Brightness", on_click=on_reset_brightness)
    
    content_settings = ft.Column(
        controls=[
            ft.Text("Settings", size=30, weight="bold"),
            slider,
            btn_setting
        ],
        expand=1,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    def show_settings():
        page.controls.clear()
        page.add(content_settings)
    
    def on_change_navigation(event):
        selected_index = event.control.selected_index
        
        if selected_index == 0:
            show_home()
        elif selected_index == 1:
            show_search()
        else:
            show_settings()
        page.update()
    
    page.navigation_bar = ft.NavigationBar(
        selected_index=0,
        on_change=on_change_navigation,
        destinations=[
            ft.NavigationBarDestination(icon=ft.Icons.HOME, label="Home"),
            ft.NavigationBarDestination(icon=ft.Icons.SEARCH, label="Search"),
            ft.NavigationBarDestination(icon=ft.Icons.SETTINGS, label="Settings")
        ]
    )
    
    page.add(content_home)

ft.app(target=main)