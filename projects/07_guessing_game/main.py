# py
import random
# flet
import flet as ft # type: ignore
# third
# own

def main(page: ft.Page):
    page.title = "Guessing Game"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    
    title = ft.Text("Guessing Game", size=30, weight="bold")
    
    divider_header = ft.Divider()
    
    num_secret = random.randint(1, 10)
    num_try = 0
    
    num_secrect_result = ft.Text("Num Secret: ???")
    result_text = ft.Text("", visible=False)
    
    input_num = ft.TextField(label="You Try", width=154, keyboard_type=ft.KeyboardType.NUMBER, disabled=True)
    
    def increment(_):
        try:
            input_num.value = str(int(input_num.value) + 1) if (int(input_num.value) + 1) <= 10 else "10"
        except ValueError:
            input_num.value = "1"
        input_num.update()
    
    btn_arrow_up = ft.IconButton(
            icon=ft.Icons.ARROW_DROP_UP,
            on_click=increment,
            icon_size=18
        )

    def decrement(_):
        try:
            input_num.value = str(int(input_num.value) - 1) if (int(input_num.value) - 1) >= 1 else "1"
        except ValueError:
            input_num.value = "1"
        input_num.update()
    
    btn_arrow_down = ft.IconButton(
            icon=ft.Icons.ARROW_DROP_DOWN,
            on_click=decrement,
            icon_size=18
        )
    
    text_try = ft.Text(f"Intentos: {num_try}")
    
    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Text Field Empty", text_align=ft.TextAlign.CENTER),
        content=ft.Text("Debe selecionar un número entre 1 and 10."),
        actions=[
            ft.TextButton("Ok", on_click=lambda _: page.close(dlg_modal))
        ],
        actions_alignment=ft.MainAxisAlignment.END,
        on_dismiss=lambda _: print("Modal dialog dismissed!"),
    )
    
    def change_theme(_):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            btn_theme.text = "Dark Mode"
            page.update()
            return
        page.theme_mode = ft.ThemeMode.DARK
        btn_theme.text = "Light Mode"
        page.update()
    
    btn_theme = ft.ElevatedButton("Light Mode", on_click=change_theme)

    def verify_tryouts(_):
        if input_num.value in [""]:
            page.open(dlg_modal)
            return
        nonlocal num_try
        v_try = int(input_num.value)
        num_try += 1
        if v_try == num_secret:
            result_text.value = f"¡Correct! Lo adivinaste en {num_try} intento{"s" if num_try > 1 else ""}."
            result_text.color="#00ff00"
            result_text.visible = True
            btn_verify.disabled = True
            btn_reset.disabled = False
            btn_arrow_up.disabled = True
            btn_arrow_down.disabled = True
            num_secrect_result.value = f"Num secret: {num_secret}"
        elif v_try < num_secret:
            result_text.value = "¡Demasiado bajo!, Intenta de nuevo."
            result_text.color="#ff9500"
            result_text.visible = True
        else:
            result_text.value = "¡Demasiado alto!, Intenta de nuevo."
            result_text.color="#ff9500"
            result_text.visible = True
        text_try.value = f"Intentos: {num_try}"
        page.update()
    
    def reset_game(_):
        nonlocal num_try
        num_try = 0
        nonlocal num_secret
        num_secret = random.randint(1, 10)
        input_num.value = ""
        result_text.value = ""
        result_text.visible = False
        btn_verify.disabled = False
        btn_reset.disabled = True
        btn_arrow_up.disabled = False
        btn_arrow_down.disabled = False
        num_secrect_result.value = "Num secret: ???"
        page.update()

    btn_verify = ft.ElevatedButton("Check", on_click=verify_tryouts)
    btn_reset = ft.ElevatedButton("Reset Game", on_click=reset_game, disabled=True)
    
    column = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("Game"),
                                    ft.Text("Adivina el número entre 1 and 10"),
                                    ft.Row(
                                        controls=[
                                            input_num,
                                            ft.Column(
                                                spacing=0,
                                                controls=[
                                                    btn_arrow_up,
                                                    btn_arrow_down
                                                ]
                                            )
                                        ]
                                    ),
                                    ft.Row(
                                        controls=[
                                            btn_verify,
                                            btn_reset
                                        ],
                                        alignment=ft.MainAxisAlignment.CENTER
                                    )
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            padding=20,
                            border_radius=8
                        )
                    ),
                    ft.VerticalDivider(),
                    ft.Card(
                        content=ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.Text("Results"),
                                    num_secrect_result,
                                    text_try,
                                    result_text,
                                    btn_theme
                                ],
                                horizontal_alignment=ft.CrossAxisAlignment.CENTER
                            ),
                            padding=20,
                            border_radius=8
                        )
                    )
                ],
                alignment=ft.MainAxisAlignment.CENTER,
                vertical_alignment=ft.CrossAxisAlignment.START
            )
        ],
        expand=1
    )
    
    divider_footer = ft.Divider()
    
    page.add(title, divider_header, column, divider_footer)

ft.app(target=main)