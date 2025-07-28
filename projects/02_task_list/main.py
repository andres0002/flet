# py
# flet
import flet as ft # type: ignore
# third
# own

def main(page: ft.Page):
    page.title = "Task List"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    title = ft.Text("My Task List", size=30, weight=ft.FontWeight.BOLD)
    
    text_filed = ft.TextField(
        hint_text="New task",
        
    )
    
    def select_task(event):
        selecteds = [item["name"].title.value for item in tasks if item["name"].leading.value]
        if selecteds.__len__() == 0:
            selected_tasks_text.value = ""
            page.update()
            return
        selected_tasks_text.value = f"Selected tasks: {", ".join(selecteds)}"
        page.update()
    
    def update_tasks():
        tasks_list_view.controls.clear()
        tasks_list_view.controls.extend([task["name"] for task in tasks])
        page.update()
    
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text(
            "Text Filed Empty",
            text_align=ft.TextAlign.CENTER
        ),
        content=ft.Text("Debe llenar el text field."),
        actions=[
            ft.TextButton("Ok", on_click=lambda e: page.close(dlg_modal))
        ],
        actions_alignment=ft.MainAxisAlignment.CENTER,
        on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )
    
    def add_task(event):
        if text_filed.value:
            task = ft.ListTile(
                title=ft.Text(text_filed.value),
                leading=ft.Checkbox(on_change=select_task)
            )
            tasks.append({"id": tasks.__len__(), "name": task})
            text_filed.value = ""
            update_tasks()
            return
        # Mostrar modal cuando el campo está vacío
        page.open(dlg_modal)
    
    btnAdd = ft.FilledButton(text="Add Task", on_click=add_task)
    
    tasks_list_view = ft.ListView(
        expand=1,
        spacing=3
    )
    
    selected_tasks_text = ft.Text("", size=20, weight=ft.FontWeight.BOLD)
    
    tasks = []
    
    page.add(title, text_filed, btnAdd, tasks_list_view, selected_tasks_text)

ft.app(target=main)