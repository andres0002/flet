# py
import random
import string
# flet
import flet as ft # type: ignore
# third
# own

def main(page: ft.Page):
    page.title = "Generator of Password"
    page.theme_mode = ft.ThemeMode.DARK
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    title = ft.Text("Generator of Password", size=30, weight="bold")
    
    divider = ft.Divider()
    
    def generate_password(*, length, use_uppercase, use_numbers, use_symbols):
        characters = string.ascii_lowercase
        if use_uppercase:
            characters += string.ascii_uppercase
        if use_numbers:
            characters += string.digits
        if use_symbols:
            characters += string.punctuation
        return "".join(random.choice(characters) for _ in range(length))
    
    def update_password(_):
        password_field.value = generate_password(
            length=int(length_slider.value),
            use_uppercase=use_uppercase_switch.value,
            use_numbers=use_numbers_switch.value,
            use_symbols=use_symbols_switch.value
        )
        page.update()
    
    def copy_password(_):
        page.set_clipboard(password_field.value)
        page.open(ft.SnackBar(
                content=ft.Text("Password copied to clipboard.", color="#ffffff"),
                bgcolor="#000000"
            )
        )
    
    password_field = ft.TextField(
        read_only=True,
        text_style=ft.TextStyle(size=14, weight="bold")
    )
    length_slider = ft.Slider(
        min=8,
        max=30,
        value=12,
        divisions=22,
        label="Length {value}"
    )
    use_uppercase_switch = ft.Switch(label="Use Uppercase", value=False)
    use_numbers_switch = ft.Switch(label="Use Numbers", value=False)
    use_symbols_switch = ft.Switch(label="Use Symbols", value=False)
    btn_generate_password = ft.ElevatedButton(
        "Generate Password",
        on_click=update_password,
        icon=ft.Icons.REFRESH
    )
    btn_copy_password = ft.ElevatedButton(
        "Copy Password",
        on_click=copy_password,
        icon=ft.Icons.COPY
    )
    
    content = ft.Column(
        controls=[
            ft.Text("Generated Password", size=20, weight="bold"),
            password_field,
            ft.Text("Password Length", size=14, weight="bold"),
            length_slider,
            use_uppercase_switch,
            use_numbers_switch,
            use_symbols_switch,
            btn_generate_password,
            btn_copy_password
        ],
        expand=1,
        scroll=ft.ScrollMode.AUTO,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    main_content = ft.SafeArea(
        content=ft.Column(
            controls=[
                title,
                divider,
                content,
                divider
            ],
            expand=1,
            scroll=ft.ScrollMode.AUTO,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER
        ),
        top=True,      # proteger del notch y barra superior
        bottom=True,   # proteger de la barra de navegación inferior
        left=True,
        right=True
    )
    
    page.add(
        main_content
    )

ft.app(target=main)