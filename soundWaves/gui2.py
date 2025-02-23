import tkinter as tk
from tkinter import messagebox
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import winsound
import threading
from matplotlib.animation import FuncAnimation
import time
import wave
import struct
from PIL import Image, ImageTk  # Import Pillow for image handling

# Initialize global variables
t = np.array([])
waveform = np.array([])
duration = 0
start_time = 0
ani = None

# Path to the sounds folder
RECORDINGS_FOLDER = "recordings"

# Function to get all .wav files in the 'soundWaves' folder
def get_wav_files():
    folder_path = RECORDINGS_FOLDER  # Use the SOUNDS_FOLDER path to get .wav files
    wav_files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if f.endswith('.wav')]
    return wav_files

# Get the list of .wav files
wav_files = get_wav_files()
if not wav_files:
    wav_files = ["No .wav files found"]

def get_selected_file_path():
    return selected_file.get()

def load_waveform(file_path):
    global t, waveform
    with wave.open(file_path, 'rb') as wav_file:
        sample_rate = wav_file.getframerate()
        num_frames = wav_file.getnframes()
        num_channels = wav_file.getnchannels()
        waveform = np.zeros(num_frames)
        for i in range(num_frames):
            frame = wav_file.readframes(1)
            if num_channels == 2:
                left, right = struct.unpack('<hh', frame)
                waveform[i] = (left + right) / 2
            else:
                waveform[i] = struct.unpack('<h', frame)[0]
        t = np.linspace(0, num_frames / sample_rate, num_frames, endpoint=False)
    return t, waveform

def play_sound_and_plot_from_file():
    global start_time, ani
    try:
        file_path = get_selected_file_path()
        load_waveform(file_path)
        start_time = time.time()
        threading.Thread(target=lambda: winsound.PlaySound(file_path, winsound.SND_FILENAME)).start()
        ani = FuncAnimation(fig, update_plot, interval=20, repeat=False)
        canvas.draw()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

def update_plot(i):
    global t, waveform
    elapsed_time = time.time() - start_time
    max_time = t[-1]
    if elapsed_time >= max_time:
        ani.event_source.stop()
        return
    end_index = int((elapsed_time / max_time) * len(t))
    ax.clear()
    ax.plot(t[:end_index], waveform[:end_index], color="blue")
    ax.set(xlabel='Time (s)', ylabel='Amplitude', title=f'Sound Waveform')
    ax.grid(True)

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
    instruction_label = tk.Label(parent_frame, text=text, font=("Helvetica", 30, "bold"), bg="black", fg="yellow",
                                 wraplength=1500, justify="left", relief="solid", padx=5, pady=5)

# Function to add multiple images
def add_images(parent_frame):
    image_files = ["gibson.jpg", "strat.jpg", "ukulele.jpg", "wavgui2.jpg", "epiphoneLPS.jpg"]  # Add more filenames here
    image_positions = [(200, 100), (2050, 1600), (200, 1100), (1000, 1600), (3150, 700)]  # position co-ordinates for images

    image_labels = []  # Store references to avoid garbage collection

    for i, filename in enumerate(image_files):
        image_path = os.path.join(os.getcwd(), "images", filename)

        if os.path.exists(image_path):  # Check if the image file exists
            img = Image.open(image_path)
            img = img.resize((400, 900), resample=Image.Resampling.LANCZOS)
            img = img.rotate(360, expand=True)

            if filename == "gibson.jpg":
                heading_label = tk.Label(parent_frame, text="The Gibson J45:", font=("Arial", 24, "bold"), bg="black", fg="yellow")
                heading_label.place(x=270, y=50)
            
            if filename == "strat.jpg":
                heading_label = tk.Label(parent_frame, text="A Fender Startocaster:", font=("Arial", 24, "bold"), bg="black", fg="yellow")
                heading_label.place(x=2300, y=1550)
                img = img.resize((900, 400), resample=Image.Resampling.LANCZOS)
            
            if filename == "ukulele.jpg":
                heading_label = tk.Label(parent_frame, text="A Ukulele:", font=("Arial", 24, "bold"), bg="black", fg="yellow")
                heading_label.place(x=310, y=1050)
            
            if filename == "wavgui2.jpg":
                heading_label = tk.Label(parent_frame, text="Example of a Frequency Wave at 888 Hz over 5 seconds:", font=("Arial", 24, "bold"), bg="black", fg="yellow")
                heading_label.place(x=1015, y=1550)  # Position the heading above the image
                img = img.resize((900, 400), resample=Image.Resampling.LANCZOS)

            if filename == "epiphoneLPS.jpg":
                heading_label = tk.Label(parent_frame, text="Epiphone Les Paul Studio:", font=("Arial", 24, "bold"), bg="black", fg="yellow")
                heading_label.place(x=3170, y=650)
                img = img.resize((450, 900), resample=Image.Resampling.LANCZOS)

            img_tk = ImageTk.PhotoImage(img)

            # Create a label for the image
            img_label = tk.Label(parent_frame, image=img_tk)
            img_label.image = img_tk  # Keep a reference to prevent garbage collection
            img_label.place(x=image_positions[i][0], y=image_positions[i][1])  # Position the image
            image_labels.append(img_label)
        else:
            print(f"Warning: {filename} not found in the images folder!")

def gui2_main(parent_frame):
    global selected_file, canvas, fig, ax

    # Set up the GUI inside the parent frame
    selected_file = tk.StringVar(parent_frame)
    selected_file.set(wav_files[0])

    # Adding instructional text to the right side of the screen
    instruction_text = (
        "First select a .wav file from the dropdown.\n"
        "Then click the 'Play Sound' button to play the sound.\n"
        "The waveform loads as the sound plays.\n"
        "All the listed files are saved in the 'recordings' folder.\n"
        "To make a recording go to the Record Tab.\n"
    )

    # Add tooltip for instructional text
    create_tooltip(parent_frame, x=2200, y=50, text=instruction_text)

    add_images(parent_frame) 

    # Dropdown to select .wav file
    tk.Label(parent_frame, text="Select .wav file:", font=("Helvetica", 25, "bold"), bg="black", fg="yellow").pack(pady=5)
    file_dropdown = tk.OptionMenu(parent_frame, selected_file, *wav_files)
    file_dropdown.config(width=20, height=2, font=("Helvetica", 25, "bold"))
    file_dropdown.pack(pady=5)

    # Adjust dropdown menu font
    menu = parent_frame.nametowidget(file_dropdown.menuname)
    menu.config(font=("Helvetica", 25))

    # Play button
    play_button = tk.Button(parent_frame, text="Play Sound", command=play_sound_and_plot_from_file, width=20, height=2, font=("Helvetica", 25, "bold"))
    play_button.pack(pady=20)

    # Plot frame and matplotlib figure
    plot_frame = tk.Frame(parent_frame, width=800, height=400)
    plot_frame.pack(pady=20)
    fig, ax = plt.subplots(figsize=(20, 10))

    # Add axis labels for the graph
    ax.set_xlabel('Time (s)', fontsize=18)
    ax.set_ylabel('Amplitude', fontsize=18)
    ax.set_title('Sound Waveform', fontsize=20)
    ax.grid(True)  # Enable grid for better clarity

    # Embed the figure in the Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.get_tk_widget().pack()
