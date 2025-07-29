# py
from datetime import datetime
# flet
import flet as ft # type: ignore
# third
from openpyxl import Workbook # type: ignore
# owm

def main(page: ft.Page):
    page.title = "DataTable and Excel"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    title = ft.Text("DataTable and Excel", size=30, weight="bold")
    
    divider = ft.Divider(color="#999999")
    
    input_name = ft.TextField(label="Name", hint_text="Enter name here")
    
    input_age = ft.TextField(label="Age", hint_text="Enter age here")
    
    def craete_dlg_modal(*, title, description):
        dlg_modal = ft.AlertDialog(
            modal=True,
            # title=ft.Text("Text Field Empty", text_align=ft.TextAlign.CENTER),
            title=ft.Text(title, text_align=ft.TextAlign.CENTER),
            # content=ft.Text("Debe teber ambos campos diligenciados."),
            content=ft.Text(description),
            actions=[
                ft.TextButton("Ok", on_click=lambda _: page.close(dlg_modal)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda _: print("Modal dialog dismissed!"),
        )
        return dlg_modal
    
    def add_row(_):
        if not input_age.value.isdigit():
            dlg_modal = craete_dlg_modal(
                title="Text Field Age",
                description="Debe ingresar un número entero positivo."
            )
            page.open(dlg_modal)
            return
        elif input_name.value not in [None, ""] and input_age.value not in [None, ""]:
            new_row = ft.DataRow(
                cells=[
                    ft.DataCell(
                        ft.Text(str(data_table.rows.__len__() + 1)),
                    ),
                    ft.DataCell(
                        ft.Text(input_name.value),
                    ),
                    ft.DataCell(
                        ft.Text(input_age.value),
                    )
                ]
            )
            
            data_table.rows.append(new_row)
            input_name.value = ""
            input_age.value = ""
            page.update()
            return
        dlg_modal = craete_dlg_modal(
            title="Text Field Empty",
            description="Debe teber ambos campos diligenciados."
        )
        page.open(dlg_modal)
    
    btn_add_row = ft.ElevatedButton("Add", on_click=add_row)
    
    def sanitize(val):
        if val is None:
            return ""
        if isinstance(val, (int, float)):
            return val
        return str(val).strip()
    
    def save_excel(_):
        wb = Workbook()
        ws = wb.active
        ws.title = "BBDD"
        ws.append(["ID", "Name", "Age"])
        for row in data_table.rows:
            ws.append([sanitize(getattr(cell.content, "value", None)) for cell in row.cells])
            # print([sanitize(getattr(cell.content, "value", None)) for cell in row.cells])
        date_current = datetime.now().strftime("%d_%m_%Y_%H_%M_%S")
        file_name = f"DataTable_and_Excel_{date_current}.xlsx"
        wb.save(file_name)
        
        snack_bar = ft.SnackBar(
            content=ft.Text(f"Data saved in {file_name}", color="#ffffff"),
            bgcolor='transparent'
        )
        page.overlay.append(snack_bar)
        snack_bar.open = True
        page.update()
    
    btn_export_excel = ft.ElevatedButton("Export Data to Excel", on_click=save_excel)
    
    data_table = ft.DataTable(
        bgcolor="#222222",
        border=ft.border.all(
            width=2,
            color="#444444"
        ),
        vertical_lines=ft.border.BorderSide(2, color="#444444"),
        horizontal_lines=ft.border.BorderSide(2, color="#444444"),
        columns=[
            ft.DataColumn(
                ft.Text("ID")
            ),
            ft.DataColumn(
                ft.Text("Name")
            ),
            ft.DataColumn(
                ft.Text("Age")
            )
        ],
        rows=[]
    )
    
    page.add(
        title,
        divider,
        input_name,
        input_age,
        btn_add_row, 
        btn_export_excel,
        data_table
    )

ft.app(target=main)