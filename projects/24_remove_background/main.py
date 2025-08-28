# py
# flet
import flet as ft # type: ignore
# third
# own
from remove_background import remove_bg_img

def main(page: ft.Page):
    page.title = "Remove Background"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    # state variables
    state = {
        "input_select_image": ""
    }
    
    title = ft.Text("Remove Background", size=30, weight="bold")
    
    divider = ft.Divider()
    
    input_path = None
    
    def pick_file_result(event: ft.FilePickerResultEvent):
        if event.files:
            text_select_file.value = f"Selected Image: {event.files[0].path}"
            nonlocal input_path
            input_path = event.files[0].path
            state["input_select_image"] = input_path
            
            # show previw
            with open(input_path, "rb") as img:
                img_preview.src = input_path
                img_preview.visible = True
            btn_process_and_save.disabled = False
            page.update()
    
    pick_files_dialog = ft.FilePicker(
        on_result=pick_file_result
    )
    page.overlay.append(pick_files_dialog)
    
    btn_select_file = ft.ElevatedButton(
        text="Select Image",
        icon=ft.Icons.FILE_UPLOAD,
        on_click=lambda _: pick_files_dialog.pick_files(
            file_type=ft.FilePickerFileType.IMAGE
        )
    )
    
    text_select_file = ft.Text("Selected Image: No se ha seleccionado ninguna Img.")
    
    img_preview = ft.Image(
        width=300,
        height=300,
        fit=ft.ImageFit.CONTAIN,
        visible=False,
        border_radius=8
    )
    
    def save_file_result(event: ft.FilePickerResultEvent):
        if not event.path or not input_path:
            return
        text_result.visible = True
        text_result.value = "Process Img..."
        page.update()
        
        try:
            event_path = event.path
            if not event.path.endswith(".png"):
                event_path = f"{event.path}.png"
            remove_bg_img(input_path, event_path)
            text_result.value = "Processed Img exitosamente."
            text_result.color = "#00ff00"
            page.update()
        except Exception as _:
            text_result.value = "Error: Process Img."
            text_result.color = "#ff0000"
            page.update()
    
    save_file_dialog = ft.FilePicker(
        on_result=save_file_result
    )
    page.overlay.append(save_file_dialog)
    
    btn_process_and_save = ft.ElevatedButton(
        text="Process and Save",
        icon=ft.Icons.SAVE,
        disabled=True,
        on_click=lambda _: save_file_dialog.save_file(
            file_type=ft.FilePickerFileType.ANY,
            allowed_extensions=["png"],
            file_name="output.png"
        )
    )
    
    text_result = ft.Text(
        size=20,
        weight="bold",
        color="#00ff00",
        visible=False
    )
    
    content = ft.Column(
        controls=[
            btn_select_file,
            text_select_file,
            img_preview,
            btn_process_and_save,
            text_result
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

ft.app(target=main)