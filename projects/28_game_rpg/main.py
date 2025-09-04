# py
# flet
import flet as ft # type: ignore
# third
# own
from place import Place
from object import Object
from character import Character
from player import Player

class Game:
    def __init__(self):
        self.player = None
        self.places = {}
        self.init_world()
    
    def init_world(self):
        # create places
        entrada = Place(
            "Entrada del Bosque",
            "Una clara entrada a un misterioso bosque."
        )
        bosque = Place(
            "Bosque Profundo",
            "Un bosque denso lleno de sombras."
        )
        cueva = Place(
            "Cueva Misteriosa",
            "Una cueva oscura con ecos extraños."
        )
        aldea = Place(
            "Aldea pacífica",
            "Una pequeña aldea con casas de madera."
        )
        # create objects
        espada = Object(
            "Espada",
            "Una espada brillante de acero."
        )
        pocion = Object(
            "Poción",
            "Una poción de curación de color verde."
        )
        llave = Object(
            "Llave",
            "Una llave antigua y misteriosa."
        )
        # create characters
        goblin = Character(
            "Goblin",
            "¡Grrr! ¡No pases por aquí humano!"
        )
        aldeano = Character(
            "Aldeano",
            "¡Bienvenido a nuestra humilde aldea!"
        )
        # add objects to places
        entrada.add_object(espada)
        bosque.add_object(pocion)
        cueva.add_object(llave)
        # add characters to places
        bosque.add_character(goblin)
        aldea.add_character(aldeano)
        # connect places
        entrada.connect("norte", bosque)
        bosque.connect("sur", entrada)
        bosque.connect("este", cueva)
        bosque.connect("oeste", aldea)
        cueva.connect("oeste", bosque)
        aldea.connect("este", bosque)
        # save places
        self.places = {
            "entrada": entrada,
            "bosque": bosque,
            "cueva": cueva,
            "aldea": aldea
        }
        # create player
        self.player = Player("Aventurero")
        self.player.current_place = entrada
    
    def process_command(self, command):
        command = command.strip().lower()
        if command.startswith("ir "):
            address = command[3:]
            return self.player.move(address)
        elif command.startswith("recoger "):
            name_object = command[8:]
            return self.player.collect_object(name_object)
        elif command.startswith("hablar "):
            name = command[7:]
            for character in self.player.current_place.characters:
                if character.name.lower() == name.lower():
                    return character.talk()
            return f"No hay ningún '{name}' aquí."
        elif command == "inventario":
            return self.player.show_inventory()
        elif command == "mirar":
            # place
            place = self.player.current_place
            info = f"🏞️ {place.name}\n{place.description}\n"
            # objects
            if place.objects:
                objects = [obj.name for obj in place.objects]
                info += f"Objects: {", ".join(objects)}\n"
                # characters
            if place.characters:
                characters = [character.name for character in place.characters]
                info += f"Personajes: {", ".join(characters)}\n"
            # address
            address = list(place.connections.keys())
            if address:
                info += f"Salidas: {", ".join(address)}"
            return info
        else:
            return "Comando no reconocido. Usa: ir [dirección], recoger [objeto], hablar [personaje], inventario, mirar"

def main(page: ft.Page):
    page.title = "Game RPG"
    page.theme_mode = ft.ThemeMode.DARK
    page.window.width = 800
    page.window.height = 600
    page.window.resizable = False
    
    # create instance game.
    game = Game()
    
    # components of UI.
    output_text = ft.Text(
        "¡Bienvenido al RPG Game!\n\nEscribe 'mirar' para obserbar tu entorno.\nComandos disponibles: ir [dirección], recoger [objeto], hablar [personaje], inventario, mirar",
        size=14,
        selectable=True,
        width=750,
        color=ft.Colors.GREEN_300
    )
    input_field = ft.TextField(
        # label="Command",
        hint_text="Escribe tu comando aquí...",
        width=600,
        autofocus=True,
        text_size=14
    )
    
    def execute_command(_):
        command = input_field.value.strip()
        if command:
            result = game.process_command(command)
            output_text.value += f"\n\n> {command}\n{result}"
            input_field.value = ""
            page.update()
    
    def on_key_down(event):
        if event.key == "Enter":
            execute_command(event)
    
    # events
    input_field.on_submit = execute_command
    page.on_keyboard_event = on_key_down
    
    # btn execute
    btn_execute = ft.ElevatedButton(
        text="Execute",
        on_click=execute_command
    )
    
    # btn clean
    def clean_screen(_):
        output_text.value = "Pantalla limpiada. Escribir 'mirar' para ver tu entorno."
        page.update()
    
    btn_clear = ft.ElevatedButton(
        text="Clean",
        on_click=clean_screen,
        color=ft.Colors.RED_300
    )
    
    # layout of interface
    page.add(
        ft.Container(
            content=ft.Column(
                controls=[
                    ft.Container(
                        content=ft.Text(
                            "🎮 Game RPG",
                            size=30,
                            weight="bold",
                            color=ft.Colors.BLUE_300
                        ),
                        alignment=ft.alignment.center
                    ),
                    ft.Divider(),
                    ft.Container(
                        content=output_text,
                        bgcolor=ft.Colors.GREY_900,
                        padding=20,
                        border_radius=8,
                        border=ft.border.all(2, ft.Colors.BLUE_300),
                        expand=1
                    ),
                    ft.Row(
                        controls=[
                            input_field,
                            btn_execute,
                            btn_clear
                        ]
                    ),
                    ft.Text(
                        "💡 Tip: Usa 'mirar' para explorar, 'ir [dirección]' para moverte, 'recoger [objeto]' para recoletar objects."
                    )
                ],
            ),
            expand=1
        )
    )

if __name__ == "__main__":
    ft.app(target=main)