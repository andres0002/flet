# py
import math
# flet
import flet as ft # type: ignore
# third
# own

def main(page: ft.Page):
    page.title = "Calculator"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.window.width = 340
    page.window.height = 464
    
    def safe_eval(expression):
        expression = expression.replace("^", "**")
        safe_dict = {
            "sin": lambda x: math.sin(math.radians(x)),
            "cos": lambda x: math.cos(math.radians(x)),
            "tan": lambda x: math.tan(math.radians(x)),
            "sqrt": math.sqrt,
            "pi": math.pi,
            "radians": math.radians
        }
        return eval(expression, {"__builtins__": None}, safe_dict)
    
    def handle_btn_click(event):
        btn_value = event.control.data
        if btn_value == "=":
            try:
                result = f"{safe_eval(expression_filed.value):.10f}"
                expression_filed.value = result
            except Exception as _:
                expression_filed.value = "Error"
            page.update()
        elif btn_value == "C":
            expression_filed.value = ""
            page.update()
        else:
            expression_filed.value += btn_value
            page.update()
    
    title = ft.Text("Calculator", size=30, weight="bold")
    
    divider = ft.Divider()
    
    expression_filed = ft.TextField(
        value="",
        text_align=ft.TextAlign.RIGHT,
        # on_change=handle_text_field_change
    )
    
    rows = []
    rows.append(ft.Row(controls=[expression_filed], alignment=ft.MainAxisAlignment.CENTER))
    
    btns = [
        ["7", "8", "9", "/"],
        ["4", "5", "6", "*"],
        ["1", "2", "3", "-"],
        [".", "0", "=", "+"],
    ]
    
    for row in btns:
        btns_row = []
        for btn in row:
            btns_row.append(
                ft.ElevatedButton(
                    text=btn,
                    data=btn,
                    width=64,
                    on_click=handle_btn_click
                )
            )
        rows.append(ft.Row(btns_row, alignment=ft.MainAxisAlignment.CENTER))
    
    sci_btns = [
        ["sin", "cos", "tan", "sqrt"],
        ["(", ")", "^", "C"],
    ]
    
    for row in sci_btns:
        btns_row = []
        for btn in row:
            btns_row.append(
                ft.ElevatedButton(
                    text=btn,
                    data=btn,
                    width=64,
                    on_click=handle_btn_click
                )
            )
        rows.append(ft.Row(btns_row, alignment=ft.MainAxisAlignment.CENTER))
    
    content = ft.Column(
        controls=rows,
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