import tkinter as tk
from tkinter import ttk
import os
import winsound
import threading  # threading for handling background tasks
from PIL import Image, ImageTk

# Path to the sounds folder
SOUNDS_FOLDER = "sounds"

# Guitar sound file mapping
GUITAR_SOUNDS = {
    "E2": "1.wav",
    "A": "2.wav",
    "D": "3.wav",
    "G": "4.wav",
    "B": "5.wav",
    "E": "6.wav"
}

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

    # Load and rotate the image from the 'images' folder
    image_path = os.path.join(os.getcwd(), 'images', 'gibson.jpg')
    img = Image.open(image_path)
    
    # Resize the image to fit UI
    img = img.resize((400, 900), resample=Image.Resampling.LANCZOS)
    img = img.rotate(360, expand=True)
    
    img_tk = ImageTk.PhotoImage(img)

    # Create a label to display the image
    img_label = tk.Label(parent_frame, image=img_tk)
    img_label.image = img_tk  # Keep a reference so it’s not garbage collected
    img_label.place(x=100, y=100)  # Place image on the left side with some padding

    # Feedback label to show which string is playing
    feedback_label = tk.Label(parent_frame, text="", font=("Arial", 20), fg="black")
    feedback_label.pack(pady=10)    

    # Title label for guitar
    ttk.Label(parent_frame, text="Guitar Strings", font=("Arial", 30)).pack(pady=(10, 0))
    guitar_frame = ttk.Frame(parent_frame)
    guitar_frame.pack(pady=5)

    # Guitar frame to hold image and buttons
    guitar_frame = ttk.Frame(parent_frame)
    guitar_frame.pack()
    
    # Load and add the guitar headstock image
    guitar_tuner_path = os.path.join(os.getcwd(), 'images', 'guitarPegs.jpg')
    guitar_tuner_img = Image.open(guitar_tuner_path)
    guitar_tuner_img = guitar_tuner_img.resize((400, 600), resample=Image.Resampling.LANCZOS)
    guitar_tuner_img_tk = ImageTk.PhotoImage(guitar_tuner_img)
    guitar_tuner_label = tk.Label(guitar_frame, image=guitar_tuner_img_tk)
    guitar_tuner_label.image = guitar_tuner_img_tk  # Keep reference
    guitar_tuner_label.pack()

    # Guitar string buttons arranged below the image
    button_frame = ttk.Frame(guitar_frame)
    button_frame.pack()
    
    style = ttk.Style()
    style.configure("Large.TButton", font=("Arial", 20), padding=(10, 10))  # Increase padding for more height

    guitar_positions = [["D", "G"], ["A", "B"], ["E2", "E"]]
    for row, pair in enumerate(guitar_positions):
        for col, string_name in enumerate(pair):
            def on_click(sn=string_name):
                play_sound_file(GUITAR_SOUNDS[sn], sn, feedback_label)
            ttk.Button(button_frame, text=string_name, width=15, style="Large.TButton", command=on_click).grid(row=row, column=col, padx=10, pady=5)

    
     # Title label for ukulele
    ttk.Label(parent_frame, text="Ukulele Strings", font=("Arial", 30)).pack(pady=(20, 0))
    ukulele_frame = ttk.Frame(parent_frame)
    ukulele_frame.pack(pady=5)
    
    # Load and add the ukulele headstock image
    ukulele_tuner_path = os.path.join(os.getcwd(), 'images', 'ukTuners.jpg')
    ukulele_tuner_img = Image.open(ukulele_tuner_path)
    ukulele_tuner_img = ukulele_tuner_img.resize((400, 600), resample=Image.Resampling.LANCZOS)
    ukulele_tuner_img_tk = ImageTk.PhotoImage(ukulele_tuner_img)
    ukulele_tuner_label = tk.Label(parent_frame, image=ukulele_tuner_img_tk)
    ukulele_tuner_label.image = ukulele_tuner_img_tk  # Keep reference
    ukulele_tuner_label.pack()

    # Ukulele string buttons arranged below the image
    ukulele_button_frame = ttk.Frame(ukulele_frame)
    ukulele_button_frame.pack()
    
    ukulele_positions = [["G", "A"], ["C", "E"]]
    for row, pair in enumerate(ukulele_positions):
        for col, string_name in enumerate(pair):
            def on_click(sn=string_name):
                play_sound_file(UKULELE_SOUNDS[sn], sn, feedback_label)
            ttk.Button(ukulele_button_frame, text=string_name, width=15, style="Large.TButton", command=on_click).grid(row=row, column=col, padx=10, pady=5)
    
    # Stop button
    stop_button = ttk.Button(parent_frame, text="Stop Sound", command=lambda: stop_sound(feedback_label), width=20, style="Large.TButton")
    stop_button.pack(pady=20)

