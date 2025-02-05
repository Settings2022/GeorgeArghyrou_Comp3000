import tkinter as tk
from tkinter import ttk
import os
import simpleaudio as sa
import threading  # threading for handling background tasks
from PIL import Image, ImageTk

# Path to the sounds folder
SOUNDS_FOLDER = "sounds"

# Ukulele sound file mapping
UKULELE_SOUNDS = {
    "G": "G.wav",  
    "C": "C.wav",
    "E": "E.wav",
    "A": "A.wav"
}

# Global variable to hold the play_obj, so we can stop it later
current_play_obj = None
stop_requested = False  # To track if stop has been requested

def play_sound_file(file_name):
    """
    Plays the specified sound file from the sounds folder in a loop.
    """
    global current_play_obj, stop_requested

    stop_requested = False  # Reset stop flag when a new sound starts

    file_path = os.path.join(SOUNDS_FOLDER, file_name)
    
    if os.path.exists(file_path):
        wave_obj = sa.WaveObject.from_wave_file(file_path)
        current_play_obj = wave_obj.play()
        
        while not stop_requested:
            continue  # Keep looping until stop is requested
    else:
        print(f"Sound file {file_name} not found.")

def stop_sound():
    """Stops the sound if it's playing."""
    global current_play_obj, stop_requested
    if current_play_obj:
        stop_requested = True  # Set stop flag
        current_play_obj.stop()
        print("Sound stopped.")

def build_instrument_tab(parent_frame):
    # Adding instructional text to the right side of the screen
    instruction_text = (
        "\n"
        "Here you can tune your instrument by ear.\n"
        "\n"
        "Select a button to listen to the sound.\n"
        "\n"
        "Tune your instrument up or down to match that sound.\n"
    )
    instruction_label = tk.Label(parent_frame, text=instruction_text, font=("Helvetica", 25), wraplength=500, anchor="w")
    instruction_label.place(x=3000, y=50)

    # Load and rotate the image from the 'images' folder
    image_path = os.path.join(os.getcwd(), 'images', 'guitars.jpg')
    img = Image.open(image_path)
    img = img.resize((900, 600), resample=Image.Resampling.LANCZOS)
    img = img.rotate(-90, expand=True)
    img_tk = ImageTk.PhotoImage(img)
    img_label = tk.Label(parent_frame, image=img_tk)
    img_label.image = img_tk  # Keep reference
    img_label.place(x=100, y=100)

    # Create a style for the stop button
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 20))

    # Title label for guitar
    ttk.Label(parent_frame, text="Guitar Strings", font=("Arial", 30)).pack(pady=(10, 0))
    guitar_frame = ttk.Frame(parent_frame)
    guitar_frame.pack(pady=5)

    guitar_sounds = {
        "E2": "1.wav",
        "A": "2.wav",
        "D": "3.wav",
        "G": "4.wav",
        "B": "5.wav",
        "E": "6.wav"
    }

    for string_name, sound_file in guitar_sounds.items():
        def on_click(sf=sound_file):
            stop_sound()
            threading.Thread(target=play_sound_file, args=(sf,), daemon=True).start()
        ttk.Button(
            guitar_frame, text=string_name, width=20, command=on_click, style="TButton"
        ).pack(side=tk.LEFT, padx=5)

    # Title label for ukulele
    ttk.Label(parent_frame, text="Ukulele Strings", font=("Arial", 30)).pack(pady=(20, 0))
    ukulele_frame = ttk.Frame(parent_frame)
    ukulele_frame.pack(pady=5)

    for string_name, sound_file in UKULELE_SOUNDS.items():
        def on_click(sf=sound_file):
            stop_sound()
            threading.Thread(target=play_sound_file, args=(sf,), daemon=True).start()
        ttk.Button(
            ukulele_frame, text=string_name, width=20, command=on_click, style="TButton"
        ).pack(side=tk.LEFT, padx=5)

    stop_button = ttk.Button(parent_frame, text="Stop Sound", command=stop_sound, width=20, style="TButton")
    stop_button.pack(pady=20)
