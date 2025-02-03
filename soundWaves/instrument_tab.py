import tkinter as tk
from tkinter import ttk
import os
import numpy as np
import simpleaudio as sa
import threading  # threading for handling background tasks

# Path to the sounds folder
SOUNDS_FOLDER = "sounds"

# Frequencies for ukulele strings (still using sine waves for ukulele)
UKULELE_FREQUENCIES = {
    "G": 392.00,  
    "C": 261.63,
    "E": 329.63,
    "A": 440.00
}

# Global variable to hold the play_obj, so we can stop it later
current_play_obj = None
stop_requested = False  # To track if stop has been requested

def play_frequency_in_background(frequency):
    """Plays a sine wave at the specified frequency in a loop."""
    global current_play_obj, stop_requested

    # Sampling information
    sample_rate = 44100  # 44.1 kHz sample rate
    t = np.linspace(0, 1, int(sample_rate * 1), False)  # Time array for 1 second

    # Generate sine wave
    sine_wave = 0.5 * np.sin(2 * np.pi * frequency * t)

    # Convert to 16-bit PCM audio
    audio = (sine_wave * 32767).astype(np.int16)

    # Start playback in a loop (non-blocking)
    while not stop_requested:
        current_play_obj = sa.play_buffer(audio, 1, 2, sample_rate)

        # Wait until the sound finishes playing, then loop
        current_play_obj.wait_done()

    stop_requested = False  # Reset stop flag after playback is stopped

def play_sound_file(file_name):
    """
    Plays the specified sound file from the sounds folder in a loop.
    """
    global current_play_obj, stop_requested

    stop_requested = False  # Reset stop flag when a new sound starts

    file_path = os.path.join(SOUNDS_FOLDER, file_name)
    
    if os.path.exists(file_path):
        # Play the sound using simpleaudio (non-blocking)
        wave_obj = sa.WaveObject.from_wave_file(file_path)
        current_play_obj = wave_obj.play()
        
        # Loop the sound indefinitely
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
    """
    Populates the parent_frame (already a tab from frontPage.py)
    with guitar and ukulele buttons for playing corresponding sounds.
    """

    # Create a style for the stop button
    style = ttk.Style()
    style.configure("TButton", font=("Arial", 20))

    # Title label for guitar
    ttk.Label(parent_frame, text="Guitar Strings", font=("Arial", 30)).pack(pady=(10, 0))

    # Frame for guitar buttons
    guitar_frame = ttk.Frame(parent_frame)
    guitar_frame.pack(pady=5)

    # Map guitar strings to their corresponding sound files
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
            stop_sound()  # Stop any sound that may be currently playing
            threading.Thread(target=play_sound_file, args=(sf,), daemon=True).start()  # Start sound in a background thread
        ttk.Button(
            guitar_frame,
            text=string_name,
            width=20,
            command=on_click,
            style="TButton"  # Apply the style here
        ).pack(side=tk.LEFT, padx=5)

    # Title label for ukulele
    ttk.Label(parent_frame, text="Ukulele Strings", font=("Arial", 30)).pack(pady=(20, 0))

    # Frame for ukulele buttons
    ukulele_frame = ttk.Frame(parent_frame)
    ukulele_frame.pack(pady=5)

    for string_name, freq in UKULELE_FREQUENCIES.items():
        def on_click(f=freq):
            stop_sound()  # Stop any sound that may be currently playing
            threading.Thread(target=play_frequency_in_background, args=(f,), daemon=True).start()  # Start frequency in a background thread
        ttk.Button(
            ukulele_frame,
            text=string_name,
            width=20,
            command=on_click,
            style="TButton"  # Apply the style here
        ).pack(side=tk.LEFT, padx=5)

    # Stop button to stop any sound playing
    stop_button = ttk.Button(parent_frame, text="Stop Sound", command=stop_sound, width=20, style="TButton")
    stop_button.pack(pady=20)
