# py
# flet
import flet as ft
# third
# own

def main(page: ft.Page):
    page.title = "Rows and Columns"
    text = ft.Text('Text 1')
    text2 = ft.Text('Text 2')
    text3 = ft.Text('Text 3')
    row = ft.Row(
        controls=[text, text2, text3],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=50
    )
    btn = ft.FilledButton('Btn 1')
    btn2 = ft.FilledButton('Btn 2')
    btn3 = ft.FilledButton('Btn 3')
    row2 = ft.Row(
        controls=[btn, btn2, btn3],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=50
    )
    
    text_column = ft.Text('Text col 1 row 1')
    text_column2 = ft.Text('Text col 1 row 2')
    text_column3 = ft.Text('Text col 1 row 3')
    col = ft.Column(
        controls=[text_column, text_column2, text_column3],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=50
    )
    
    text_column4 = ft.Text('Text col 2 row 1')
    text_column5 = ft.Text('Text col 2 row 2')
    text_column6 = ft.Text('Text col 2 row 3')
    col2 = ft.Column(
        controls=[text_column4, text_column5, text_column6],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=50
    )
    
    row_columns = ft.Row(
        controls=[col, col2],
        alignment=ft.MainAxisAlignment.CENTER,
        spacing=50
    )
    
    page.add(row, row2, row_columns)

ft.app(target=main)