import tkinter as tk
from tkinter import ttk
import os
import winsound
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

# Global variable to track if the sound should stop
stop_playback = False

def play_sound_file(file_name, string_name, feedback_label):
    """
    Plays the specified sound file from the sounds folder in a loop until stopped
    and updates the feedback label with the string being played.
    """
    global stop_playback
    file_path = os.path.join(SOUNDS_FOLDER, file_name)
    
    if not os.path.exists(file_path):
        feedback_label.config(text=f"Error: {file_name} not found.", foreground="red")
        return
    
    stop_playback = False
    feedback_label.config(text=f"Playing: {string_name}", foreground="green")
    
    def play():
        winsound.PlaySound(file_path, winsound.SND_FILENAME | winsound.SND_ASYNC | winsound.SND_LOOP)
    
    threading.Thread(target=play, daemon=True).start()

def stop_sound(feedback_label):
    """Stops the currently playing sound and updates the feedback label."""
    global stop_playback
    stop_playback = True
    winsound.PlaySound(None, winsound.SND_ASYNC)  # Stop the looping sound
    feedback_label.config(text="Sound stopped.", foreground="black")

def build_instrument_tab(parent_frame):
    # Adding instructional text to the right side of the screen
    instruction_text = (
        "\n"
        "Here you can tune your instrument by ear.\n"
        "\n"
        "Select a button to listen to the sound.\n"
        "\n"
        "The sound will repeat in a loop until you select another button or press the stop button.\n"
        "\n"
        "Listen carefully to the sound and compare it to the sound of your instrument.\n"
        "\n"
        "Tune your instrument up or down to match that sound.\n"
    )
    instruction_label = tk.Label(parent_frame, text=instruction_text, font=("Helvetica", 25), wraplength=500, anchor="w")
    instruction_label.place(x=3000, y=50)

    # Feedback label to show which string is playing
    feedback_label = tk.Label(parent_frame, text="", font=("Arial", 20), fg="black")
    feedback_label.pack(pady=10)

    # Load and rotate the image from the 'images' folder
    image_path = os.path.join(os.getcwd(), 'images', 'guitars.jpg')
    img = Image.open(image_path)
    
    # Resize the image to fit UI
    img = img.resize((600, 900), resample=Image.Resampling.LANCZOS)
    img = img.rotate(360, expand=True)

    img_tk = ImageTk.PhotoImage(img)
    img_label = tk.Label(parent_frame, image=img_tk)
    img_label.image = img_tk  # Keep reference
    img_label.place(x=100, y=100)

    # Create a style for the buttons
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
        def on_click(sf=sound_file, sn=string_name):
            play_sound_file(sf, sn, feedback_label)
        ttk.Button(
            guitar_frame, text=string_name, width=20, command=on_click, style="TButton"
        ).pack(side=tk.LEFT, padx=5)

    # Title label for ukulele
    ttk.Label(parent_frame, text="Ukulele Strings", font=("Arial", 30)).pack(pady=(20, 0))
    ukulele_frame = ttk.Frame(parent_frame)
    ukulele_frame.pack(pady=5)

    for string_name, sound_file in UKULELE_SOUNDS.items():
        def on_click(sf=sound_file, sn=string_name):
            play_sound_file(sf, sn, feedback_label)
        ttk.Button(
            ukulele_frame, text=string_name, width=20, command=on_click, style="TButton"
        ).pack(side=tk.LEFT, padx=5)
    
    # Stop button
    stop_button = ttk.Button(parent_frame, text="Stop Sound", command=lambda: stop_sound(feedback_label), width=20, style="TButton")
    stop_button.pack(pady=20)
