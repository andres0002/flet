# py
# flet
import flet as ft # type: ignore
# third
# own

def main(page: ft.Page):
    page.title = "Tabs"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    title = ft.Text("Tabs", size=30, weight="bold")
    
    divider = ft.Divider(height=2)
    
    tabs = ft.Tabs(
        selected_index=0,
        animation_duration=500,
        tabs=[
            ft.Tab(
                text="Tasks",
                icon=ft.Icons.LIST_ALT,
                content=ft.ListView(
                    controls=[
                        ft.Text("Task 1"),
                        ft.Text("Task 2"),
                        ft.Text("Task 3"),
                        ft.Text("Task 4"),
                        ft.Text("Task 5"),
                        ft.Text("Task 6"),
                    ],
                    spacing=10,
                    padding=20
                )
            ),
            ft.Tab(
                text="Profile",
                icon=ft.Icons.PERSON,
                content=ft.ListView(
                    controls=[
                        ft.Text("Name: William Andres"),
                        ft.Text("Lastname: Ramirez Jimenez"),
                        ft.Text("Others...")
                    ],
                    spacing=10,
                    padding=20
                )
            ),
            ft.Tab(
                text="Setting",
                icon=ft.Icons.SETTINGS,
                content=ft.ListView(
                    controls=[
                        ft.Switch(
                            label="Notifications",
                            label_position=ft.LabelPosition.LEFT
                        ),
                        ft.Slider(
                            min=0,
                            max=100,
                            divisions=10,
                            label="Volume {value}%"
                        )
                    ],
                    spacing=10,
                    padding=20
                )
            )
        ]
    )
    
    page.add(title, divider, tabs)

ft.app(target=main)