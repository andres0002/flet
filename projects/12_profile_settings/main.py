# py
# flet
import flet as ft # type: ignore
# third
# own

def main(page: ft.Page):
    page.title = "Profile Settings"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    
    title = ft.Text("Profile Settings", size=30, weight="bold")
    
    divider = ft.Divider()
    
    def update_preview(_):
        preview_text.value = f"Name: {name_input.value}.\n"
        preview_text.value += f"Lastname: {lastname_input.value}.\n"
        preview_text.value += f"Age: {age_dropdown.value}.\n"
        preview_text.value += f"Gender: {gender_radio.value}.\n"
        preview_text.value += "Interests:"
        preview_text.value += "\n" if interests_checkbox.controls.__len__() > 0 else ""
        preview_text.value += f"{"\n".join([f"  {checkbox.label}." for checkbox in interests_checkbox.controls if checkbox.value])}"
        preview_text.value += "\n" if interests_checkbox.controls.__len__() > 0 else ""
        preview_text.value += f"Dark Mode: {"Active." if theme_switch.value else "Inactive."}"
        page.update()
    
    name_input = ft.TextField(label="Name", hint_text="Enter here.", on_change=update_preview)
    lastname_input = ft.TextField(label="Last Name", hint_text="Enter here.", on_change=update_preview)
    age_dropdown = ft.Dropdown(
        label="Edad",
        options=[
            ft.DropdownOption(
                str(age)
            ) for age in range(18, 101)
        ],
        # expand=1,
        on_change=update_preview
    )
    
    gender_radio = ft.RadioGroup(
        content=ft.Column(
            controls=[
                ft.Radio(value="Masculino", label="Masculino"),
                ft.Radio(value="Femenino", label="Femenino"),
                ft.Radio(value="Othor", label="Other")
            ]
        ),
        on_change=update_preview
    )
    
    interests = [
        "Art",
        "Tecnology",
        "Music",
        "Sport",
        "Travel"
    ]
    
    interests_checkbox = ft.Column(
        controls=[
            ft.Checkbox(label=interest, on_change=update_preview) for interest in interests
        ]
    )
    
    def toggle_theme(_):
        if not theme_switch.value:
            page.theme_mode = ft.ThemeMode.LIGHT
            page.update()
            return
        page.theme_mode = ft.ThemeMode.DARK
        page.update()
    
    theme_switch = ft.Switch(label="Dark Mode", value=True, on_change=lambda e: (toggle_theme(e), update_preview(e)))
    
    preview_text = ft.Text("Complete the form to preview the user data.", size=14, weight="bold")
    
    content = ft.Column(
        controls=[
            ft.Text("User data:", size=20, weight="bold"),
            name_input,
            lastname_input,
            age_dropdown,
            ft.Text("Gender:", size=20, weight="bold"),
            gender_radio,
            ft.Text("Interests:", size=20, weight="bold"),
            interests_checkbox,
            ft.Text("Theme:", size=20, weight="bold"),
            theme_switch,
            divider,
            ft.Text("Profile Preview:", size=20, weight="bold"),
            preview_text
        ],
        expand=1,
        scroll=ft.ScrollMode.AUTO
    )
    
    page.add(
        title,
        divider,
        content,
        divider
    )

ft.app(target=main)