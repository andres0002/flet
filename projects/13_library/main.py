# py
# flet
import flet as ft # type: ignore
# third
# own

def main(page: ft.Page):
    page.title = "Library"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.DARK
    
    title = ft.Text("Library", size=30, weight="bold")
    
    divider = ft.Divider()
    
    def create_dialog_modal(*, title, description):
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
    
    def change_theme(_):
        if page.theme_mode == ft.ThemeMode.DARK:
            page.theme_mode = ft.ThemeMode.LIGHT
            btn_theme_icon.icon = ft.Icons.DARK_MODE
            page.update()
            return
        page.theme_mode = ft.ThemeMode.DARK
        btn_theme_icon.icon = ft.Icons.LIGHT_MODE
        page.update()
    
    btn_theme_icon = ft.IconButton(
        icon=ft.Icons.LIGHT_MODE,
        tooltip="Change Theme",
        on_click=change_theme
    )
    
    app_bar = ft.AppBar(
        title=title,
        center_title=True,
        actions=[btn_theme_icon],
        bgcolor=ft.Colors.SURFACE_CONTAINER_HIGHEST
    )
    
    books_view = ft.ListView(
        expand=1,
        padding=20,
        spacing=10,
        controls=[
            ft.Text("Books", size=20, weight="bold")
        ]
    )
    
    title_book_field = ft.TextField(
        label="Title Book",
        hint_text="Enter here."
    )
    
    author_name_field = ft.TextField(
        label="Full Name Author",
        hint_text="Enter here."
    )
    
    def list_tile_exist_in_books(title, subtitle, new_book):
        exists = [
            ctrl
            for ctrl in books_view.controls
            if isinstance(ctrl, ft.ListTile)
            and ctrl.title.value == title
            and ctrl.subtitle.value == subtitle
        ]

        if exists.__len__() > 0:
            dlg_modal = create_dialog_modal(
                title="Exists",
                description="Ya existe este book en books."
            )
            page.open(dlg_modal)
            return
        books_view.controls.append(new_book)
        title_book_field.value = ""
        author_name_field.value = ""
        page.update()
    
    def list_tile_exist_in_wishlist(title, subtitle, new_wishlist):
        exists = [
            ctrl
            for ctrl in wishlist_view.controls
            if isinstance(ctrl, ft.ListTile)
            and ctrl.title.value == title
            and ctrl.subtitle.value == subtitle
        ]

        if exists.__len__() > 0:
            dlg_modal = create_dialog_modal(
                title="Exists",
                description="Ya existe este book en el wishlist."
            )
            page.open(dlg_modal)
            return
        wishlist_view.controls.append(new_wishlist)
        page.update()
    
    def add_new_book(_):
        if title_book_field.value == "" or author_name_field.value == "":
            dlg_modal = create_dialog_modal(
                title="Text Field Empty",
                description="Ambos campos deben estar diligenciados."
            )
            page.open(dlg_modal)
            return
        
        new_wishlist = ft.ListTile(
            title=ft.Text(title_book_field.value, size=14, weight="bold"),
            subtitle=ft.Text(author_name_field.value if author_name_field.value != "" else "Unknown Author"),
            trailing=ft.PopupMenuButton(
                icon=ft.Icons.MORE_VERT,
                items=[
                    ft.PopupMenuItem(
                        text="Delete",
                        icon=ft.Icons.DELETE,
                        on_click=lambda _: (wishlist_view.controls.remove(new_wishlist), page.update())
                    )
                ]
            )
        )
        
        new_book = ft.ListTile(
            title=ft.Text(title_book_field.value, size=14, weight="bold"),
            subtitle=ft.Text(author_name_field.value if author_name_field.value != "" else "Unknown Author"),
            trailing=ft.PopupMenuButton(
                icon=ft.Icons.MORE_VERT,
                items=[
                    ft.PopupMenuItem(
                        text="Delete",
                        icon=ft.Icons.DELETE,
                        on_click=lambda _: (books_view.controls.remove(new_book), page.update())
                    ),
                    ft.PopupMenuItem(
                        text="Add to Wishlist",
                        icon=ft.Icons.ADD,
                        on_click=lambda _: list_tile_exist_in_wishlist(
                            new_wishlist.title.value,
                            new_wishlist.subtitle.value,
                            new_wishlist
                        )
                    )
                ]
            )
        )
        list_tile_exist_in_books(
            new_book.title.value,
            new_book.subtitle.value,
            new_book
        )
    
    add_book_view = ft.Column(
        controls=[
            ft.Text("Add new book", size=20, weight="bold"),
            title_book_field,
            author_name_field,
            ft.ElevatedButton(
                "Add Book",
                on_click=add_new_book
            )
        ],
        horizontal_alignment=ft.CrossAxisAlignment.CENTER
    )
    
    wishlist_view = ft.ListView(
        expand=1,
        padding=20,
        controls=[
            ft.Text("WishList", size=20, weight="bold")
        ]
    )
    
    def destination_change(event):
        index = event.control.selected_index
        content.controls.clear()
        
        if index == 0:
            content.controls.append(books_view)
        elif index == 1:
            content.controls.append(add_book_view)
        else:
            content.controls.append(wishlist_view)
        page.update()
    
    nav_rail = ft.NavigationRail(
        selected_index=0,
        label_type=ft.NavigationRailLabelType.ALL,
        min_width=100,
        min_extended_width=400,
        destinations=[
            ft.NavigationRailDestination(
                icon=ft.Icons.BOOK,
                label="Books"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.ADD,
                label="Add Book"
            ),
            ft.NavigationRailDestination(
                icon=ft.Icons.FAVORITE,
                label="Wishlist"
            )
        ],
        on_change=destination_change
    )
    
    content = ft.Column(
        controls=[
            books_view
        ],
        expand=1,
        scroll=ft.ScrollMode.AUTO
    )
    
    main_content = ft.Row(
        controls=[
            nav_rail,
            ft.VerticalDivider(),
            content
        ],
        expand=1,
        vertical_alignment=ft.CrossAxisAlignment.START
    )
    
    page.add(
        app_bar,
        divider,
        main_content,
        divider
    )

ft.app(target=main)