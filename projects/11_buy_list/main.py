# py
# flet
import flet as ft # type: ignore
# third
# own

def main(page: ft.Page):
    page.title = "Buy List"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    title = ft.Text("Buy List", size=30, weight="bold")
    
    divider = ft.Divider()
    
    def create_alert_modal(*, title, description):
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text(title, text_align=ft.TextAlign.CENTER),
            content=ft.Text(description),
            actions=[
                ft.TextButton("Ok", on_click=lambda _: page.close(dlg_modal)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
            on_dismiss=lambda e: print("Modal dialog dismissed!"),
        )
        return dlg_modal
    
    shopping_list = ft.Column(scroll=ft.ScrollMode.AUTO, expand=1)
    
    def add_article(_):
        if name_input.value in ["", None] or amount_input.value in ["", None]:
            dlg_modal = create_alert_modal(
                title="Text Filed Empty",
                description="Ambos filed text se deben diligenciar."
            )
            page.open(dlg_modal)
            return
        if not amount_input.value.isdigit():
            dlg_modal = create_alert_modal(
                title="Text Filed Quantity",
                description="Debe ser un número positivo."
            )
            page.open(dlg_modal)
            return
        if int(amount_input.value) == 0:
            amount_input.value = "1"
            page.update()
        category_text = ft.Text(f"Category: {categories[0]}", size=14, weight="bold")
        def update_category(event):
            category_text.value = f"Category: {event.control.value}"
            page.update()
        category_dropdown = ft.Dropdown(
            options=[
                ft.DropdownOption(
                    key=value,
                    content=ft.Text(value)
                ) for value in categories
            ],
            value=categories[0],
            on_change=update_category
        )
        
        new_item = ft.ListTile(
            leading=ft.Checkbox(
                value=False
            ),
            title=ft.Text(f"{name_input.value} (x{amount_input.value})"),
            subtitle=ft.Row(
                controls=[
                    category_text,
                    category_dropdown
                ]
            ),
            trailing=ft.IconButton(
                icon=ft.Icons.DELETE,
                icon_color="#ff0000",
                on_click=lambda _: (shopping_list.controls.remove(new_item), page.update())
            )
        )
        
        shopping_list.controls.append(new_item)
        name_input.value = ""
        amount_input.value = ""
        page.update()
    
    categories = [
        "Sin category",
        "Alimentos",
        "Limpieza",
        "Electrónica",
        "Ropa"
    ]
    
    name_input = ft.TextField(label="Name Article", hint_text="Enter here.")
    amount_input = ft.TextField(label="Quantity", hint_text="Enter here.", width=120)
    btn_add_to_list = ft.ElevatedButton("Add to List", on_click=add_article)
    
    def clear_list(_):
        shopping_list.controls.clear()
        page.update()
    
    def show_stats(_):
        if shopping_list.controls.__len__() > 0:
            total_items = shopping_list.controls.__len__()
            checked_items = sum([1 for item in shopping_list.controls if item.leading.value])
            category_counts = {}
            for item in shopping_list.controls:
                category = item.subtitle.controls[1].value
                category_counts[category] = category_counts.get(category, 0) + 1
            
            stats_text = f"Total: {total_items}, Comprados: {checked_items}, Pendientes: {total_items - checked_items}\n"
            stats_text += "Categories:\n" + "\n".join([f"{cat}: {count}" for cat, count in category_counts.items()])
            
            snack = ft.SnackBar(
                content=ft.Text(
                    stats_text,
                    color="#ffffff"
                ),
                bgcolor="#222222"
            )
            page.overlay.append(snack)
            snack.open = True
            page.update()
    
    btn_stats = ft.ElevatedButton("Stats", on_click=show_stats)
    
    content = ft.Column(
        controls=[
            ft.Text("Article", size=20, weight="bold"),
            ft.Row(
                controls=[
                    name_input,
                    amount_input
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            btn_add_to_list,
            divider,
            ft.Text("Actions", size=20, weight="bold"),
            ft.Row(
                controls=[
                    ft.ElevatedButton(
                        "Clear List",
                        on_click=clear_list
                    ),
                    btn_stats
                ],
                alignment=ft.MainAxisAlignment.CENTER
            ),
            divider,
            shopping_list
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