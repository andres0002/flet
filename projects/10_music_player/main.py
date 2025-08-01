# py
import os
# flet
import flet as ft # type: ignore
# third
import pygame # type: ignore
from mutagen.mp3 import MP3 # type: ignore
import asyncio
# own

class Song:
    def __init__(self, filename):
        self.filename = filename
        self.title = os.path.splitext(filename)[0]
        self.duration = self.get_duration()
    
    def get_duration(self):
        audio = MP3(os.path.join("./assets", self.filename))
        return audio.info.length

async def main(page: ft.Page):
    page.title = "Music Player"
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    
    title = ft.Text("Music Player", size=30, weight="bold")
    
    divider = ft.Divider()
    
    pygame.mixer.init()
    
    playlist = [Song(file) for file in os.listdir("./assets") if file.endswith(".mp3")]
    
    current_song_index = 0
    
    song_info = ft.Text(size=20, weight="bold")
    current_song_time_text = ft.Text("00:00")
    current_song_duration_text = ft.Text("00:00")
    progress_bar = ft.ProgressBar(value=0)
    
    def load_song():
        pygame.mixer.music.load(os.path.join("./assets", playlist[current_song_index].filename))
    
    def pause_song(_):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            btn_play.icon = ft.Icons.PLAY_ARROW
        else:
            if pygame.mixer.music.get_pos() == -1:
                load_song()
                pygame.mixer.music.play()
            else:
                pygame.mixer.music.unpause()
            btn_play.icon = ft.Icons.PAUSE
        page.update()
    
    btn_play = ft.IconButton(icon=ft.Icons.PLAY_ARROW, on_click=pause_song)
    
    def change_song(delta):
        nonlocal current_song_index
        current_song_index = (current_song_index + delta) % playlist.__len__()
        load_song()
        pygame.mixer.music.play()
        update_song_info()
        btn_play.icon = ft.Icons.PAUSE
        page.update()
    
    btn_skip_previous = ft.IconButton(icon=ft.Icons.SKIP_PREVIOUS, on_click=lambda _: change_song(-1))
    btn_skip_next = ft.IconButton(icon=ft.Icons.SKIP_NEXT, on_click=lambda _: change_song(1))
    
    def format_time(seconds):
        minutes, seconds = divmod(int(seconds), 60)
        return f"{minutes:02d}:{seconds:02d}"
    
    def update_song_info():
        song = playlist[current_song_index]
        song_info.value = f"{song.title}"
        current_song_time_text.value = "00:00"
        current_song_duration_text.value = format_time(song.duration)
        progress_bar.value = 0
        page.update()
    
    async def update_progress_bar():
        while True:
            if not pygame.mixer.music.get_busy() and btn_play.icon == ft.Icons.PAUSE:
                # La canción terminó → pasar a la siguiente
                change_song(1)
            if pygame.mixer.music.get_busy():
                current_time = pygame.mixer.music.get_pos() / 1000
                progress_bar.value = current_time / playlist[current_song_index].duration
                current_song_time_text.value = format_time(current_time)
                page.update()
            await asyncio.sleep(1)
    
    content = ft.Column(
        controls=[
            song_info,
            ft.Row(
                controls=[
                    current_song_time_text,
                    current_song_duration_text
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN
            ),
            progress_bar,
            ft.Row(
                controls=[
                    btn_skip_previous,
                    btn_play,
                    btn_skip_next
                ],
                alignment=ft.MainAxisAlignment.CENTER
            )
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
    
    if playlist:
        load_song()
        update_song_info()
        page.update()
        await update_progress_bar()
    else:
        song_info.value = "No se encontraron canciones en la carpeta 'assets'."
        page.update()

ft.app(target=main)