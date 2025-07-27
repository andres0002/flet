# py
# flet
import flet as ft
# third
# own

def main(page: ft.Page):
    page.title = "My app"
    page.horizontal_alignment = ft.CrossAxisAlignment.START
    text = ft.Text('Hello world...')
    text2 = ft.Text('XD...')
    
    def change_text2(event):
        text2.value = "Text changed..."
        page.update()
    
    def change_text2_reset(event):
        text2.value = "XD..."
        page.update()
    
    btn = ft.FilledButton(text="Change text2", on_click=change_text2)
    btn2 = ft.FilledButton(text="Change text2 reset", on_click=change_text2_reset)
    
    page.add(text, text2, btn, btn2)

ft.app(target=main)