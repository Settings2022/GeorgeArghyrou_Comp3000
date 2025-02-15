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

# Function to create a tooltip for the instructional text
def create_tooltip(parent_frame, x, y, text):
    """
    Creates a tooltip effect for a given question mark (hover to reveal text).
    """

    def show_instruction(event):
        instruction_label.place(x=x + 50, y=y)  # Show tooltip near the question mark

    def hide_instruction(event):
        instruction_label.place_forget()  # Hide tooltip when moving away

    # Create the question mark label
    question_mark = tk.Label(parent_frame, text="?", font=("Helvetica", 30, "bold"),
                             bg="yellow", relief="solid", width=2)
    question_mark.place(x=x, y=y)  # Position the question mark

    # Bind hover events
    question_mark.bind("<Enter>", show_instruction)
    question_mark.bind("<Leave>", hide_instruction)

    # Instructional text label (Initially hidden)
    instruction_label = tk.Label(parent_frame, text=text, font=("Helvetica", 25, "bold"),
                                 wraplength=1200, justify="left", bg="lightgray",
                                 relief="solid", padx=5, pady=5)

# Function to add multiple images
def add_images(parent_frame):

    # GUI Setup
    label = tk.Label(parent_frame, text="Click a button to hear the sound.", font=("Helvetica", 40, "bold"))
    label.pack(pady=10)

    image_files = ["gibson.jpg", "strat.jpg", "ukulele.jpg", "sigma.jpg", "epiphone.jpg", "washburn.jpg", "epiphoneLPS.jpg"]  # Add more filenames here
    image_positions = [(100, 100), (1450, 1500), (100, 1150), (700, 100), (2560, 1050), (3250, 1050), (700, 1150) ]  # Position coordinates for images

    image_labels = []  # Store references to avoid garbage collection

    for i, filename in enumerate(image_files):
        image_path = os.path.join(os.getcwd(), "images", filename)

        if os.path.exists(image_path):  # Check if the image file exists
            img = Image.open(image_path)
            img = img.resize((400, 900), resample=Image.Resampling.LANCZOS)
            img = img.rotate(360, expand=True)

            if filename == "gibson.jpg":
                heading_label = tk.Label(parent_frame, text="The Gibson J45:", font=("Arial", 24, "bold"))
                heading_label.place(x=180, y=50)
            
            if filename == "strat.jpg":
                heading_label = tk.Label(parent_frame, text="A Fender Stratocaster:", font=("Arial", 24, "bold"))
                heading_label.place(x=1750, y=1450)
                img = img.resize((900, 400), resample=Image.Resampling.LANCZOS)

            if filename == "epiphoneLPS.jpg":
                heading_label = tk.Label(parent_frame, text="The Epiphone Les Paul Studio:", font=("Arial", 24, "bold"))
                heading_label.place(x=690, y=1100)
                img = img.resize((450, 900), resample=Image.Resampling.LANCZOS)
            
            if filename == "ukulele.jpg":
                heading_label = tk.Label(parent_frame, text="A Ukulele:", font=("Arial", 24, "bold"))
                heading_label.place(x=200, y=1100)
            
            if filename == "sigma.jpg":
                heading_label = tk.Label(parent_frame, text="A Sigma Parlour guitar:", font=("Arial", 24, "bold"))
                heading_label.place(x=750, y=50)  # Position the heading above the image
                img = img.resize((450, 900), resample=Image.Resampling.LANCZOS)

            if filename == "epiphone.jpg":
                heading_label = tk.Label(parent_frame, text="The Noel Gallagher Epiphone Riviera:", font=("Arial", 24, "bold"))
                heading_label.place(x=2500, y=1000)
                img = img.resize((450, 900), resample=Image.Resampling.LANCZOS)
            
            if filename == "washburn.jpg":
                heading_label = tk.Label(parent_frame, text="A Washburn Parlour guitar:", font=("Arial", 24, "bold"))
                heading_label.place(x=3260, y=1000)
                img = img.resize((450, 1000), resample=Image.Resampling.LANCZOS)

            img_tk = ImageTk.PhotoImage(img)

            # Create a label for the image
            img_label = tk.Label(parent_frame, image=img_tk)
            img_label.image = img_tk  # Keep a reference to prevent garbage collection
            img_label.place(x=image_positions[i][0], y=image_positions[i][1])  # Position the image
            image_labels.append(img_label)
        else:
            print(f"Warning: {filename} not found in the images folder!")

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
        "Each button represents a specific guitar or ukulele string in the headstock image.\n"
        "\n"
        "Select a button to play the sound of the guitar or ukulele string in standard tuning.\n"
        "\n"
        "The sound will repeat until you select another button or press the stop button.\n"
        "\n"
        "Listen carefully to the sound and compare it to the sound of your instrument.\n"
        "\n"
        "Tune your instrument up or down to match that sound.\n"
    )
    # Add tooltip for instructional text
    create_tooltip(parent_frame, x=2480, y=160, text=instruction_text)

    add_images(parent_frame)

    feedback_label = tk.Label(parent_frame, text="", font=("Arial", 20), fg="black")
    feedback_label.pack(pady=10)
    
    instrument_container = ttk.Frame(parent_frame)
    instrument_container.pack(pady=10)
    
    # Outer frame to create the shadow effect
    guitar_shadow = ttk.Frame(instrument_container, padding=5, style="Shadow.TFrame")
    guitar_shadow.grid(row=0, column=0, padx=50, pady=20)

    # Inner frame to contain the actual guitar section
    guitar_frame = ttk.Frame(guitar_shadow, padding=10, relief="raised", borderwidth=2)
    guitar_frame.pack()

    
    guitar_tuner_path = os.path.join(os.getcwd(), 'images', 'guitarPegs.jpg')
    guitar_tuner_img = Image.open(guitar_tuner_path)
    guitar_tuner_img = guitar_tuner_img.resize((400, 600), resample=Image.Resampling.LANCZOS)
    guitar_tuner_img_tk = ImageTk.PhotoImage(guitar_tuner_img)
    guitar_tuner_label = tk.Label(guitar_frame, image=guitar_tuner_img_tk)
    guitar_tuner_label.image = guitar_tuner_img_tk
    guitar_label = tk.Label(guitar_frame, text="Guitar Headstock", font=("Arial", 20, "bold"))
    guitar_label.pack()
    guitar_tuner_label.pack()
    
    button_frame = ttk.Frame(guitar_frame)
    button_frame.pack()
    
    guitar_positions = [["D", "G"], ["A", "B"], ["E2", "E"]]
    for row, pair in enumerate(guitar_positions):
        for col, string_name in enumerate(pair):
            def on_click(sn=string_name):
                play_sound_file(GUITAR_SOUNDS[sn], sn, feedback_label)
            # ttk.Button(button_frame, text=string_name, width=20, padding=15, command=on_click).grid(row=row, column=col, padx=10, pady=5)
            style = ttk.Style()
            style.configure("Large.TButton", font=("Arial", 20), padding=15)
            ttk.Button(button_frame, text=string_name, width=10, style="Large.TButton", command=on_click).grid(row=row, column=col, padx=10, pady=5)
    
    # Outer frame to create the shadow effect
    ukulele_shadow = ttk.Frame(instrument_container, padding=5, style="Shadow.TFrame")
    ukulele_shadow.grid(row=0, column=1, padx=50, pady=20)

    # Inner frame to contain the actual ukulele section
    ukulele_frame = ttk.Frame(ukulele_shadow, padding=10, relief="raised", borderwidth=2)
    ukulele_frame.pack()
    
    ukulele_tuner_path = os.path.join(os.getcwd(), 'images', 'ukulelePegs.jpg')
    ukulele_tuner_img = Image.open(ukulele_tuner_path)
    ukulele_tuner_img = ukulele_tuner_img.resize((400, 600), resample=Image.Resampling.LANCZOS)
    ukulele_tuner_img_tk = ImageTk.PhotoImage(ukulele_tuner_img)
    ukulele_tuner_label = tk.Label(ukulele_frame, image=ukulele_tuner_img_tk)
    ukulele_tuner_label.image = ukulele_tuner_img_tk
    ukulele_label = tk.Label(ukulele_frame, text="Ukulele Headstock", font=("Arial", 20, "bold"))
    ukulele_label.pack()
    ukulele_tuner_label.pack()
    
    ukulele_button_frame = ttk.Frame(ukulele_frame)
    ukulele_button_frame.pack()
    
    ukulele_positions = [["C", "E"], ["G", "A"]]
    for row, pair in enumerate(ukulele_positions):
        for col, string_name in enumerate(pair):
            def on_click(sn=string_name):
                play_sound_file(UKULELE_SOUNDS[sn], sn, feedback_label)
            style = ttk.Style()
            style.configure("Large.TButton", font=("Arial", 20), padding=15)
            ttk.Button(ukulele_button_frame, text=string_name, width=10, style="Large.TButton", command=on_click).grid(row=row, column=col, padx=10, pady=5)    
      
    # Frame to simulate box shadow for the stop button
    shadow_frame = tk.Frame(parent_frame, background="#aaaaaa", padx=3, pady=3)
    shadow_frame.pack(pady=20)

    # Stop button inside shadow frame
    stop_button = ttk.Button(shadow_frame, text="Stop Sound",
                            command=lambda: stop_sound(feedback_label),
                            width=20, style="Large.TButton")
    stop_button.pack()


    
