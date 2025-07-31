# py
import time
# flet
import flet as ft # type: ignore
# third
# own

def main(page: ft.Page):
    page.title = "Download Files with Progress Bar and Progress Ring"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    title = ft.Text("Simulate File Download", size=30, weight=ft.FontWeight.BOLD)

    divider = ft.Divider()
    
    # files
    file_pdf = ft.Checkbox(label="file.pdf (2.5MB)", value=False)
    file_jpg = ft.Checkbox(label="file.jpg (5MB)", value=False)
    file_mp4 = ft.Checkbox(label="file.mp4 (50MB)", value=False)
    file_zip = ft.Checkbox(label="file.zip (100MB)", value=False)
    
    progress_bar = ft.ProgressBar(value=0)
    progress_ring = ft.ProgressRing(value=0)
    
    status_text = ft.Text("", size=14, weight="bold", visible=False)
    
    def handle_download(_):
        selected_files = []
        
        file_pdf.value and selected_files.append(file_pdf)
        file_jpg.value and selected_files.append(file_jpg)
        file_mp4.value and selected_files.append(file_mp4)
        file_zip.value and selected_files.append(file_zip)
        
        if not selected_files:
            status_text.value = "¡Selecione!, Al menos un file."
            status_text.color = "#ff9244"
            status_text.visible = True
            page.update()
            return
        progress_bar.value = 0
        progress_ring.value = 0
        page.update()
        
        total_size_files = sum([float(file.label.split('(')[1].split('MB')[0]) for file in selected_files])
        
        downloaded = 0
        
        for file in selected_files:
            file_zise = float(file.label.split('(')[1].split('MB')[0])
            status_text.value = f"Descargando: {file.label}..."
            status_text.color = "#00ff51"
            status_text.visible = True
            
            for _ in range(10):
                time.sleep(0.3)
                downloaded += file_zise / 10
                progress = min(downloaded / total_size_files, 1)
                progress_bar.value = progress
                progress_ring.value = progress
                page.update()
        
        status_text.value = f"Files descargados con exito."
        status_text.color = "#00ff51"
        status_text.visible = True
        page.update()
        
        time.sleep(1)
        progress_bar.value = 0
        progress_ring.value = 0
        status_text.value = ""
        file_pdf.value = False
        file_jpg.value = False
        file_mp4.value = False
        file_zip.value = False
        page.update()
    
    btn_download = ft.ElevatedButton("Start Download", on_click=handle_download)
    
    content = ft.Column(
        controls=[
            ft.Text("Select files for download", size=20, weight="bold"),
            file_pdf,
            file_jpg,
            file_mp4,
            file_zip,
            status_text,
            progress_bar,
            progress_ring,
            btn_download
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