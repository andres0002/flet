# py
# flet
import flet as ft # type: ignore
# third
# owm
from delete_files_duplicates import find_duplicates, delete_file
from organize_files_by_type import organize_folder, file_types

def main(page: ft.Page):
    page.title = "Order Files By Type"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    
    title = ft.Text("Order Files By Type", size=30, weight="bold")
    
    divider = ft.Divider()
    
    state = {
        "current_duplicates": [],
        "current_view": "duplicates"
    }
    
    selected_dir_text = ft.Text(
        "No se ha seleccionado ningun folder.",
        size=14,
        weight="bold"
    )
    
    selected_dir_text_organize = ft.Text(
        "No se ha seleccionado ningun folder.",
        size=14,
        weight="bold"
    )
    
    result_text = ft.Text(
        size=14,
        weight="bold",
        color="#00ff00",
        visible=False
    )
    
    result_text_organize = ft.Text(
        size=14,
        weight="bold",
        color="#00ff00",
        visible=False
    )
    
    duplicates_list = ft.ListView(
        expand=1,
        spacing=20
    )
    
    def delete_all_duplicates(_):
        deleted_count = 0
        failed_count = 0
        for dup_file, _ in state["current_duplicates"][:]:
            if delete_file(dup_file):
                deleted_count += 1
            else:
                failed_count += 1
        duplicates_list.controls.clear()
        state["current_duplicates"] = []
        delete_all_btn.visible = False
        if failed_count == 0:
            result_text.value = f"Se {"eliminaron" if deleted_count > 1 else "elimino"} exitosamente {deleted_count} {"files." if deleted_count > 1 else "file."}"
            result_text.color = "#00ff00"
        else:
            result_text.value = f"Se eliminaron {deleted_count} files. Fallaron {failed_count}."
            result_text.color = "#ff0000"
        duplicates_list.update()
        result_text.update()
        delete_all_btn.update()
    
    delete_all_btn = ft.ElevatedButton(
        "Delete All Files Duplicates",
        color="#ff0000",
        icon=ft.Icons.DELETE_SWEEP,
        visible=False,
        on_click=delete_all_duplicates
    )
    
    def delete_duplicate(filepath):
        if delete_file(filepath):
            result_text.value = f"File eliminado: {filepath}"
            result_text.color = "#00ff00"
            for control in duplicates_list.controls[:]:
                if filepath in control.controls[0].value:
                    duplicates_list.controls.remove(control)
            state["current_duplicates"] = [
                (dup, orig)
                for dup, orig in state["current_duplicates"]
                if dup != filepath
            ]
            if not state["current_duplicates"]:
                delete_all_btn.visible = False
        else:
            result_text.value = f"Error al eliminar: {filepath}."
            result_text.valor = "#ff0000"
        duplicates_list.update()
        result_text.update()
        delete_all_btn.update()
    
    def scan_directory(directory):
        duplicates_list.controls.clear()
        state["current_duplicates"] = find_duplicates(directory)
        if not state["current_duplicates"]:
            result_text.value = "No se encontraron files duplicates."
            result_text.color = "#ff9500"
            result_text.visible = True
            
            delete_all_btn.visible = False
        else:
            result_text.value = f"Se encontraron {len(state['current_duplicates'])} files duplicates."
            result_text.color = "#00ff00"
            result_text.visible = True
            
            delete_all_btn.visible = True
            
            for dup_file, original in state["current_duplicates"]:
                dup_row = ft.Row(
                    controls=[
                        ft.Text(
                            f"Duplicate: {dup_file}\nOriginal: {original}",
                            size=12,
                            expand=1,
                            color="#009dff"
                        ),
                        ft.ElevatedButton(
                            "Delete",
                            color="#ff0000",
                            on_click=lambda _, path=dup_file: delete_duplicate(path)
                        )
                    ]
                )
                duplicates_list.controls.append(dup_row)
        delete_all_btn.update()
        duplicates_list.update()
        result_text.update()
    
    def organize_directory(directory):
        try:
            organize_folder(directory)
            result_text_organize.value = f"Se a organizado el folder exitosamente."
            result_text_organize.color = "#00ff00"
            result_text_organize.visible = True
            result_text_organize.update()
        except Exception as _:
            result_text_organize.value = f"A ocurrido un error al organizar el folder."
            result_text_organize.color = "#ff0000"
            result_text_organize.visible = True
            result_text_organize.update()
    
    def handle_folder_picker(event: ft.FilePickerResultEvent):
        if event.path:
            if state["current_view"] == "duplicates":
                selected_dir_text.value = f"Folder selected: {event.path}"
                selected_dir_text.update()
                scan_directory(event.path)
            elif state["current_view"] == "organize":
                selected_dir_text_organize.value = f"Folder selected: {event.path}"
                selected_dir_text_organize.update()
                organize_directory(event.path)
            else: # soon
                pass
    
    folder_picker = ft.FilePicker(on_result=handle_folder_picker)
    page.overlay.append(folder_picker)
    
    def change_view(event):
        selected = event.control.selected_index
        content.controls.clear()
        if selected == 0:
            state["current_view"] = "duplicates"
            content.controls.append(duplicates_view)
        elif selected == 1:
            state["current_view"] = "organize"
            content.controls.append(organize_view)
        else:
            state["current_view"] = "soon"
            content.controls.append(soon_view)
        page.update()
    
    navigation_rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=200,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.DELETE,
                label="Duplicates"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.FOLDER_COPY,
                label="Organize"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.MORE_HORIZ_OUTLINED,
                label="Soon"
            )
        ],
        on_change=change_view
    )
    
    duplicates_view = ft.Column(
        controls=[
            ft.Text("Duplicates", size=20, weight="bold"),
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        "Select Folder",
                        icon=ft.Icons.FOLDER_OPEN,
                        on_click=lambda _: folder_picker.get_directory_path()
                    ),
                    delete_all_btn
                ]
            ),
            selected_dir_text,
            result_text,
            ft.Container(
                content=duplicates_list,
                border=ft.border.all(2, color="#0000ff"),
                border_radius=8,
                padding=20,
                margin=ft.margin.only(top=10),
                expand=True
            )
        ],
        expand=1,
        # horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    organize_view = ft.Column(
        controls=[
            ft.Text("Organize", size=20, weight="bold"),
            ft.ElevatedButton(
                "Select Folder",
                icon=ft.Icons.FOLDER_OPEN,
                on_click=lambda _: folder_picker.get_directory_path()
            ),
            selected_dir_text_organize,
            result_text_organize,
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Los files serán organizados en los siguientes folders:",
                            size=14,
                            weight="bold"
                        ),
                        ft.Column(
                            controls=[
                                ft.Text(f"- {folder_name}: ({", ".join(exts)}).") for folder_name, exts in file_types.items()
                            ]
                        )
                    ]
                ),
                border=ft.border.all(2, color="#0000ff"),
                border_radius=8,
                padding=20,
                margin=ft.margin.only(top=10),
                expand=1
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.START
    )
    
    soon_view = ft.Column(
        controls=[
            ft.Text("Soon", size=20, weight="bold")
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    content = ft.Column(
        controls=[
            duplicates_view
        ],
        expand=1
    )
    
    main_content = ft.Row(
        controls=[
            navigation_rail,
            ft.VerticalDivider(),
            content
        ],
        expand=1
    )
    
    page.add(
        title,
        divider,
        main_content,
        divider
    )

if __name__ == "__main__":
    ft.app(target=main)