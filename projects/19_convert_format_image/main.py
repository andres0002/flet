# py
# flet
import flet as ft # type: ignore
# third
# owm
from delete_files_duplicates import find_duplicates, delete_file
from organize_files_by_type import organize_folder, file_types
from resize_images import batch_resize
from convert_image import convert_image, image_types

def main(page: ft.Page):
    page.title = "Convert Format of Image"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    
    title = ft.Text("Convert Format of Image", size=30, weight="bold")
    
    divider = ft.Divider()
    
    state = {
        "current_duplicates": [],
        "current_view": "duplicates",
        "resize_input_folder": "",
        "resize_output_folder": "",
        "selected_resize_input_folder": False,
        "selected_resize_output_folder": False,
        "convert_input_file": ""
    }
    
    def create_alert_dialog(title, description):
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
    
    selected_dir_text_resize_image_input = ft.Text(
        "Folder input: No se ha seleccionado ningun folder.",
        size=14,
        weight="bold"
    )
    
    selected_dir_text_resize_image_ouput = ft.Text(
        "Folder ouput: No se ha seleccionado ningun folder.",
        size=14,
        weight="bold"
    )
    
    selected_image_text_convert_of_image = ft.Text(
        "Selected image: No se ha seleccionado ninguna image.",
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
    
    result_text_resize_images = ft.Text(
        size=14,
        weight="bold",
        color="#00ff00",
        visible=False
    )
    
    result_text_convert_of_image = ft.Text(
        size=14,
        weight="bold",
        color="#00ff00",
        visible=False
    )
    
    text_field_resize_images_width = ft.TextField(
        label="Width",
        value="800",
        width=100,
        keyboard_type=ft.KeyboardType.NUMBER
    )
    text_field_resize_images_height = ft.TextField(
        label="Height",
        value="600",
        width=100,
        keyboard_type=ft.KeyboardType.NUMBER
    )
    
    dropdown_convert_of_image = ft.Dropdown(
        # editable=False,
        width=300,
        label="Format of Output",
        value="PNG",
        options=[
            ft.DropdownOption(
                key=key,
                content=ft.Text(
                    value=value,
                ),
            ) for key, value in image_types.items()
        ],
        # on_change=lambda _: print(dropdown_convert_of_image.value),
    )
    
    duplicates_list = ft.ListView(
        expand=1,
        spacing=20
    )
    
    def handle_convert_image():
        if not state["convert_input_file"]:
            dlg_modal = create_alert_dialog(
                "Select Image",
                "Debes seleccionar la image."
            )
            page.open(dlg_modal)
            return
        if dropdown_convert_of_image.value.lower() == state["convert_input_file"].split(".")[1]:
            dlg_modal = create_alert_dialog(
                "Type Image",
                "La image selected debe tener un type image diferente al de Format of Output."
            )
            page.open(dlg_modal)
            return
        try:
            convert_image(
                state["convert_input_file"],
                dropdown_convert_of_image.value
            )
            result_text_convert_of_image.value = "Image convertida exitosamente."
            result_text_convert_of_image.color = "#00ff00"
            result_text_convert_of_image.visible = True
            result_text_convert_of_image.update()
        except Exception as _:
            result_text_convert_of_image.value = "Error al convertir la image."
            result_text_convert_of_image.color = "#ff0000"
            result_text_convert_of_image.visible = True
            result_text_convert_of_image.update()
    
    def resize_images():
        if not state["selected_resize_input_folder"] or not state["selected_resize_output_folder"]:
            dlg_modal = create_alert_dialog(
                "No ha seleccionado el folder.",
                "Debe seleccionar tanto el folder de entrada como de salida."
            )
            page.open(dlg_modal)
            return
        if not text_field_resize_images_width.value.isdigit() or not text_field_resize_images_height.value.isdigit():
            dlg_modal = create_alert_dialog(
                "Debe ser number",
                "Tanto el width como el height deben ser números enteros positivos."
            )
            page.open(dlg_modal)
            return
        width = int(text_field_resize_images_width.value)
        height = int(text_field_resize_images_height.value)
        if width <= 0 or height <= 0:
            dlg_modal = create_alert_dialog(
                "Error: dimensiones",
                "Las dimensiones deben ser validas, mayores que zero."
            )
            page.open(dlg_modal)
            return
        try:
            batch_resize(
                state["resize_input_folder"],
                state["resize_output_folder"],
                "resized",
                width,
                height
            )
            result_text_resize_images.value = "Se redimencionaron las imagenes correctamente."
            result_text_resize_images.visible = True
            result_text_resize_images.update()
        except:
            result_text_resize_images.value = "Error al redimencionar las imagenes."
            result_text_resize_images.color = "#ff0000"
            result_text_resize_images.visible = True
            result_text_resize_images.update()
    
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
    
    is_folder_input = None
    
    def func_is_folder_input(boolean):
        nonlocal is_folder_input
        is_folder_input = boolean
    
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
            elif state["current_view"] == "resized_images":
                if is_folder_input:
                    state["resize_input_folder"] = event.path
                    state["selected_resize_input_folder"] = True
                    selected_dir_text_resize_image_input.value = f"Folder input: {event.path}"
                    selected_dir_text_resize_image_input.update()
                else:
                    state["resize_output_folder"] = event.path
                    state["selected_resize_output_folder"] = True
                    selected_dir_text_resize_image_ouput.value = f"Folder ouput: {event.path}"
                    selected_dir_text_resize_image_ouput.update()
            else: # soon
                pass
    
    # setting select folders.
    folder_picker = ft.FilePicker(on_result=handle_folder_picker)
    page.overlay.append(folder_picker)
    
    def handle_file_picker(event: ft.FilePickerResultEvent):
        if event.files and len(event.files) > 0:
            # print(event.files)
            file_path = event.files[0].path
            state["convert_input_file"] = file_path
            selected_image_text_convert_of_image.value = f"Selected image: {file_path}"
            selected_image_text_convert_of_image.update()
    
    #setting select files.
    file_picker = ft.FilePicker(on_result=handle_file_picker)
    file_picker.file_type = ft.FilePickerFileType.IMAGE
    file_picker.allowed_extensions = [
        "png", "jpg", "jpeg",
        "gif", "bmp", "webp"
    ]
    page.overlay.append(file_picker)
    
    def change_view(event):
        selected = event.control.selected_index
        content.controls.clear()
        if selected == 0:
            state["current_view"] = "duplicates"
            content.controls.append(duplicates_view)
        elif selected == 1:
            state["current_view"] = "organize"
            content.controls.append(organize_view)
        elif selected == 2:
            state["current_view"] = "resized_images"
            content.controls.append(resize_images_view)
        elif selected == 3:
            state["current_view"] = "convert_image"
            content.controls.append(convert_format_image_view)
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
                icon=ft.Icons.PHOTO_SIZE_SELECT_LARGE,
                label="Resized Images"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.TRANSFORM,
                label="Convert Image"
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
    
    resize_images_view = ft.Column(
        controls=[
            ft.Text("Resized Images", size=20, weight="bold"),
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        "Select Folder Input",
                        icon=ft.Icons.FOLDER_OPEN,
                        on_click=lambda _: (folder_picker.get_directory_path(), func_is_folder_input(True))
                    ),
                    ft.ElevatedButton(
                        "Select Folder Ouput",
                        icon=ft.Icons.FOLDER_OPEN,
                        on_click=lambda _: (folder_picker.get_directory_path(), func_is_folder_input(False))
                    ),
                ]
            ),
            selected_dir_text_resize_image_input,
            selected_dir_text_resize_image_ouput,
            ft.Text(
                "Dimensions of image:",
                size=14,
                weight="bold"
            ),
            ft.Row(
                controls=[
                    text_field_resize_images_width,
                    ft.Text("x"),
                    text_field_resize_images_height,
                    ft.Text("píxeles")
                ]
            ),
            ft.ElevatedButton(
                "Resize Images",
                icon=ft.Icons.PHOTO_SIZE_SELECT_LARGE,
                on_click=lambda _: resize_images()
            ),
            result_text_resize_images,
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Information:",
                            size=14,
                            weight="bold"
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("- Se procesarán files: (.jpg, .jpeg, and .png)."),
                                ft.Text("- Las images originals no serán modificadas."),
                                ft.Text("- Las resized images se guardarán con el prefijo 'resized_'."),
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
    
    convert_format_image_view = ft.Column(
        controls=[
            ft.Text("Convert Image", size=20, weight="bold"),
            ft.ElevatedButton(
                "Select Image",
                icon=ft.Icons.IMAGE,
                on_click=lambda _: file_picker.pick_files()
            ),
            selected_image_text_convert_of_image,
            dropdown_convert_of_image,
            ft.ElevatedButton(
                "Convert Image",
                icon=ft.Icons.TRANSFORM,
                on_click=lambda _: handle_convert_image()
            ),
            result_text_convert_of_image,
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Information:",
                            size=14,
                            weight="bold"
                        ),
                        ft.Column(
                            controls=[
                                ft.Text("- Formatos soportados: (PNG, JPEG, WEBP, BMP, GIF)."),
                                ft.Text("- La image original no será modificada."),
                                ft.Text("- La image converted se guardará en el mismo folder."),
                                ft.Text("- Al conventir a JPEG, las images con transparencia se convertirán a fondo blanco.")
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