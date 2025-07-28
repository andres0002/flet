# py
# flet
import flet as ft # type: ignore
# third
# own

def main(page: ft.Page):
    page.title = "Sticky Notes"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    title = ft.Text("My Sticky Notes", size=30, weight="bold")
    
    def delete_note(event):
        note = event.control.parent.parent.parent
        grid_view.controls.remove(note)
        page.update()
    
    def create_note(text):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.TextField(value=text, multiline=True, border_color="#444444"),
                    ft.Row(
                        controls=[
                            # ft.IconButton(ft.Icons.ADD),
                            # ft.IconButton(ft.Icons.EDIT),
                            ft.IconButton(ft.Icons.DELETE, on_click=delete_note)
                        ]
                    )
                ]
            ),
            border_radius=8,
            padding=10,
            bgcolor="#222222",
        )
    
    def add_note(_):
        grid_view.controls.append(create_note(f"Note {grid_view.controls.__len__() + 1}"))
        page.update()
    
    row = ft.Row(
        controls=[
            ft.IconButton(ft.Icons.ADD, on_click=add_note)
        ],
        alignment=ft.MainAxisAlignment.END
    )
    
    grid_view = ft.GridView(
        expand=1,
        max_extent=200,
        child_aspect_ratio=1
    )
    
    page.add(title, row, grid_view)

ft.app(target=main)