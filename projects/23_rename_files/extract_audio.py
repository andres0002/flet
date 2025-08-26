# py
import os
# flet
# third
from moviepy import VideoFileClip # type: ignore
# own

def extract_audios(input_folder, progress_callback=None):
    
    output_folder = os.path.join(input_folder, "audios").replace("\\", "/")
    
    # print(output_folder)

    os.makedirs(output_folder, exist_ok=True)
    
    videos = [
        f
        for f in os.listdir(input_folder)
        if f.lower().endswith((".mp4", ".avi", ".mov", ".mkv"))
    ]
    
    total_videos = len(videos)

    # Process every video in the folder input
    for index, filename in enumerate(videos, 1):
        input_path = os.path.join(input_folder, filename).replace("\\", "/")
        if os.path.isfile(input_path):
            try:
                # Llamar al progress_callback, si está definido.
                if progress_callback:
                    progress_callback(index, total_videos, filename)
                # print(f"Procesando: {filename}")
                # Cargar el file of video.
                video_clip = VideoFileClip(input_path)
                # Get of rute od output of audio.
                audio_output_path = os.path.join(output_folder, os.path.splitext(filename)[0] + ".mp3").replace("\\", "/")
                # Extraer el audio y save.
                video_clip.audio.write_audiofile(audio_output_path)
                # Close the clip.
                video_clip.close()
                # print(f"Audio extraído: {audio_output_path}")
            except Exception as _:
                pass

# input_folder = "./assets/files/Videos"
# output_folder = "./assets/files/Videos/audios"

# extract_audios(input_folder)