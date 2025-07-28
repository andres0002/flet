# py
import random
import os
import base64
# flet
import flet as ft # type: ignore
# third
# own

def main(page: ft.Page):
    page.title = "Product Gallery"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    title = ft.Text("Product Gallery", size=30, weight="bold")
    
    divider = ft.Divider(color="#999999")
    
    def create_product(name, price, img):
        img_path = os.path.join(os.path.dirname(__file__), "assets", img)
        
        try:
            with open(img_path, "rb") as img_file:
                img_bytes = base64.b64encode(img_file.read()).decode()
        except FileNotFoundError:
            print(f"Warnig: La img {img} no exist in {img_path}")
            img_bytes = None
        
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Image(
                        src_base64=img_bytes,
                        # width=150,
                        # height=150,
                        fit=ft.ImageFit.CONTAIN,
                        error_content=ft.Text("Img NotFound")
                    ) if img_bytes else ft.Text("Img NotFound"),
                    ft.Text(
                        name,
                        size=16,
                        weight="bold"
                    ),
                    ft.Text(
                        f"${price}",
                        size=14
                    ),
                    ft.ElevatedButton(
                        "Add cart"
                    )
                ]
            ),
            bgcolor="#222222",
            padding=20,
            border_radius=8,
            alignment=ft.alignment.center,
            col={"sm": 12, "md": 6, "lg": 3}
        )
    
    gallery = ft.Column(
        controls=[
            ft.ResponsiveRow(
                controls=[
                    create_product(
                        f"Product {i + 1}",
                        f"{round(random.uniform(10, 1000000), 2)}",
                        f"product_{i}.jpg"
                    ) for i in range(12)
                ]
            )
        ],
        scroll=ft.ScrollMode.AUTO,
        expand=1
    )
    
    page.add(title, divider, gallery)

ft.app(target=main)