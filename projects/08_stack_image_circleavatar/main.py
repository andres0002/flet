# py
# flet
import flet as ft # type: ignore
# third
# own

def main(page: ft.Page):
    page.title = "Stack, Image and CircleAvatar"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.scroll = "always"
    
    title = ft.Text("Stack, Image and CircleAvatar", size=30, weight="bold")
    
    divider = ft.Divider()
    
    def create_example(*, content):
        return ft.Container(
                content=content,
                border=ft.border.all(
                    width=2,
                    color="#aaaaaa"
                ),
                padding=5
            )
    
    stack = ft.Column(
        controls=[
            ft.Text("Stack", size=20, weight="bold"),
            ft.Text("Stack permite superponer widgets uno encima de otro."),
            create_example(
                content=ft.Stack(
                    controls=[
                        ft.Container(
                            width=200,
                            height=200,
                            bgcolor=ft.Colors.BLUE_900
                        ),
                        ft.Container(
                            width=150,
                            height=150,
                            bgcolor=ft.Colors.BLUE_700
                        ),
                        ft.Container(
                            width=100,
                            height=100,
                            bgcolor=ft.Colors.BLUE_500
                        ),
                        ft.Text(
                            "Stack",
                            weight="bold",
                            size=14,
                            style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
                        )
                    ],
                    alignment=ft.alignment.center
                ),
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    image = ft.Column(
        controls=[
            ft.Text("Image", size=20, weight="bold"),
            ft.Text("Image permite mostrar imgs desde distintas fuentes."),
            create_example(
                content=ft.Column(
                    controls=[
                        ft.Text(
                            "Img Internet",
                            size=14,
                            weight="bold",
                            style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
                        ),
                        ft.Image(
                            # src="https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT0vflpUn6HSQo2ismI4cWksPTaYUIia18NHA&s"
                            src="https://picsum.photos/276/200"
                        ),
                        ft.Text(
                            "Img Local",
                            size=14,
                            weight="bold",
                            style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
                        ),
                        ft.Image(
                            src="./assets/imgs/img1.jpg"
                        )
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                )
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    circle_avatar = ft.Column(
        controls=[
            ft.Text("CircleAvatar", size=20, weight="bold"),
            ft.Text("CircleAvatar crea un avatar circular, útil para perfiles de usuario."),
            create_example(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            "CircleAvatar Img Internet",
                                            size=14,
                                            weight="bold",
                                            style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
                                        ),
                                        ft.CircleAvatar(
                                            foreground_image_src="https://avatars.githubusercontent.com/u/5479693",
                                            radius=50
                                        )
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER
                                ),
                                ft.VerticalDivider(),
                                ft.Column(
                                    controls=[
                                        ft.Text(
                                            "CircleAvatar Text",
                                            size=14,
                                            weight="bold",
                                            style=ft.TextStyle(decoration=ft.TextDecoration.UNDERLINE)
                                        ),
                                        ft.CircleAvatar(
                                            content=ft.Text("WARJ", color="#ffffff"),
                                            radius=50,
                                            bgcolor="#222222"
                                        )
                                    ],
                                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                                )
                            ],
                            alignment=ft.MainAxisAlignment.CENTER,
                        ),
                        divider
                    ]
                )
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    page.add(
        title,
        divider,
        stack,
        divider,
        image,
        divider,
        circle_avatar,
        divider
    )

ft.app(target=main)