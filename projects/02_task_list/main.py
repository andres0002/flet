# py
# flet
import flet as ft
# third
# own

def main(page: ft.Page):
    page.title = "Task List"
    
    text = ft.Text("Text...")
    
    page.add(text)

ft.app(target=main)