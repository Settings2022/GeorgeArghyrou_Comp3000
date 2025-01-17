import tkinter as tk
from tkinter import ttk
import os
from playsound import playsound
import numpy as np
import simpleaudio as sa
import threading

# Path to the sounds folder
SOUNDS_FOLDER = "sounds"

# Frequencies for ukulele strings (still using sine waves for ukulele)
UKULELE_FREQUENCIES = {
    "G": 392.00,  
    "C": 261.63,
    "E": 329.63,
    "A": 440.00
}

def play_frequency_in_background(frequency, duration):
    """Plays a sine wave at the specified frequency and duration in the background."""
    def play_sound():
    # Sampling information
        sample_rate = 44100  # 44.1 kHz sample rate
        t = np.linspace(0, duration, int(sample_rate * duration), False)  # Time array

        # Generate sine wave
        sine_wave = 0.5 * np.sin(2 * np.pi * frequency * t)

        # Convert to 16-bit PCM audio
        audio = (sine_wave * 32767).astype(np.int16)

        # Start playback
        play_obj = sa.play_buffer(audio, 1, 2, sample_rate)
        
        # Play in the background (does not block)
        play_obj.wait_done()

def play_sound_file(file_name):
    """
    Plays the specified sound file from the sounds folder.
    """
    file_path = os.path.join(SOUNDS_FOLDER, file_name)
    if os.path.exists(file_path):
        playsound(file_path)
        print(f"Attempting to play: {file_path}")
    else:
        print(f"Sound file {file_name} not found.")

def build_instrument_tab(parent_frame):
    """
    Populates the parent_frame (already a tab from frontPage.py)
    with guitar and ukulele buttons for playing corresponding sounds.
    """

    # Title and Entry for duration
    ttk.Label(parent_frame, text="Set Duration (seconds):", font=("Arial", 30)).pack(pady=(5, 0))
    duration_var = tk.StringVar(value="1.0")
    duration_entry = ttk.Entry(parent_frame, textvariable=duration_var, width=10)
    duration_entry.pack(pady=5)

    def get_duration():
        try:
            return float(duration_var.get())
        except ValueError:
            return 1.0  # Fallback if user input is invalid

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
            play_sound_file(sf)
        ttk.Button(
            guitar_frame,
            text=string_name,
            width=20,
            command=on_click
        ).pack(side=tk.LEFT, padx=5)

    # Title label for ukulele
    ttk.Label(parent_frame, text="Ukulele Strings", font=("Arial", 30)).pack(pady=(20, 0))

    # Frame for ukulele buttons
    ukulele_frame = ttk.Frame(parent_frame)
    ukulele_frame.pack(pady=5)

    for string_name, freq in UKULELE_FREQUENCIES.items():
        def on_click(f=freq):
            duration = get_duration()
            play_frequency_in_background(f, duration)
        ttk.Button(
            ukulele_frame,
            text=string_name,
            width=20,
            command=on_click
        ).pack(side=tk.LEFT, padx=5)
