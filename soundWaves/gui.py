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
from PIL import Image, ImageTk  # Import Pillow for image handling

# Function to generate waveform
def generate_waveform(duration, frequency):
    sample_rate = 44100  # Samples per second
    t = np.linspace(0, duration, int(sample_rate * duration), endpoint=False)
    waveform = 0.5 * np.sin(2 * np.pi * frequency * t)
    return t, waveform

# Function to add multiple images
def add_images(parent_frame):
    image_files = ["gibson.jpg", "strat.jpg", "ukulele.jpg", "freqWaveExample.jpg", "epiphoneLPS.jpg"]  # Add more filenames here
    image_positions = [(200, 100), (2050, 1600), (200, 1100), (1000, 1600), (3150, 700)]  # position co-ordinates for images

    image_labels = []  # Store references to avoid garbage collection

    for i, filename in enumerate(image_files):
        image_path = os.path.join(os.getcwd(), "images", filename)

        if os.path.exists(image_path):  # Check if the image file exists
            img = Image.open(image_path)
            img = img.resize((400, 900), resample=Image.Resampling.LANCZOS)
            img = img.rotate(360, expand=True)

            if filename == "gibson.jpg":
                heading_label = tk.Label(parent_frame, text="The Gibson J45:", font=("Arial", 24, "bold"))
                heading_label.place(x=270, y=50)
            
            if filename == "strat.jpg":
                heading_label = tk.Label(parent_frame, text="A Fender Startocaster:", font=("Arial", 24, "bold"))
                heading_label.place(x=2300, y=1550)
                img = img.resize((900, 400), resample=Image.Resampling.LANCZOS)
            
            if filename == "ukulele.jpg":
                heading_label = tk.Label(parent_frame, text="A Ukulele:", font=("Arial", 24, "bold"))
                heading_label.place(x=310, y=1050)
            
            if filename == "freqWaveExample.jpg":
                heading_label = tk.Label(parent_frame, text="Example of a Frequency Wave at 888 Hz over 5 seconds:", font=("Arial", 24, "bold"))
                heading_label.place(x=1015, y=1550)  # Position the heading above the image
                img = img.resize((900, 400), resample=Image.Resampling.LANCZOS)

            if filename == "epiphoneLPS.jpg":
                heading_label = tk.Label(parent_frame, text="Epiphone Les Paul Studio:", font=("Arial", 24, "bold"))
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

# Function to create a tooltip effect
def create_tooltip(parent_frame):
    # Define the function to show/hide tooltip
    def show_instruction(event):
        instruction_label.place(x=2280, y=50)  # Show tooltip when hovering

    def hide_instruction(event):
        instruction_label.place_forget()  # Hide tooltip when moving away

    # Create the question mark label
    question_mark = tk.Label(parent_frame, text="?", font=("Helvetica", 30, "bold"), bg="yellow", relief="solid", width=2)
    question_mark.place(x=2200, y=50)  # Position the question mark

    # Bind hover events
    question_mark.bind("<Enter>", show_instruction)
    question_mark.bind("<Leave>", hide_instruction)

# Adding instructional text to the right side of the screen
    instruction_text = (
        "This page allows you to generate and play a sound with a specified frequency and duration.\n"
        "\n"
        "You can visualize the waveform of the sound as it plays.\n"
        "\n"
        "Enter the frequency (in Hz), set the duration (in seconds).\n"
        "\n"
        "Click 'Play Sound' to generate the sound wave & play the sound.\n"
    )
    instruction_label = tk.Label(parent_frame, text=instruction_text, font=("Helvetica", 25, "bold"), wraplength=1800, justify="left", bg="lightgray", relief="solid", padx=5, pady=5)  

# Main function to build the GUI
def gui_main(parent_frame):
    # Function to update the plot
    def update_plot(i):
        elapsed_time = time.time() - start_time
        if elapsed_time >= duration:
            ani.event_source.stop()
            return

        end_index = int((elapsed_time * 44100) / 1000)
        ax.clear()  # Clear previous plot

        # Plot the updated waveform
        ax.plot(t[:end_index], waveform[:end_index], color="blue")

        # Add axis labels and title
        ax.set(xlabel='Time (s)', ylabel='Amplitude', title=f'Sound Waveform - {frequency} Hz')
        ax.grid()

    # Play sound and plot the waveform
    def play_sound_and_plot():
        global t, waveform, frequency, ani, start_time, duration

        try:
            # Get user input for duration and frequency
            duration = float(duration_entry.get())  # Duration in seconds
            frequency = float(frequency_entry.get())  # Frequency in Hz

            # Generate waveform based on input
            t, waveform = generate_waveform(duration, frequency)

            # Update the frequency label to show the current frequency
            frequency_label.config(text=f"Frequency: {frequency} Hz")

            # Record the start time and start the sound in a background thread
            start_time = time.time()

            # Convert duration to milliseconds for winsound.Beep
            winsound_duration = int(duration * 1000)  # Convert seconds to milliseconds
            threading.Thread(target=lambda: winsound.Beep(int(frequency), winsound_duration)).start()

            # Start the animation to update the plot
            ani = FuncAnimation(fig, update_plot, interval=20, repeat=False)

            # Embed the plot in the Tkinter canvas
            canvas.draw()

        except ValueError:
            # Show error if the user enters invalid input
            messagebox.showerror("Invalid input", "Please enter valid integers for the duration and frequency.")

    # Load and display multiple images dynamically
    add_images(parent_frame)

    # Create the tooltip (question mark with hover effect)
    create_tooltip(parent_frame)

    # Create and place the input fields for duration and frequency
    tk.Label(parent_frame, text="Enter duration (s):", font=("Helvetica", 30)).pack(pady=5)
    duration_entry = tk.Entry(parent_frame, font=("Helvetica", 20), width=10)
    duration_entry.pack(pady=5)
    duration_entry.insert(0, "5")  # Default value is 5 seconds

    tk.Label(parent_frame, text="Enter frequency (Hz):", font=("Helvetica", 30)).pack(pady=5)
    frequency_entry = tk.Entry(parent_frame, font=("Helvetica", 16), width=10)
    frequency_entry.pack(pady=5)

    # Display frequency
    frequency_label = tk.Label(parent_frame, text="Frequency: - Hz", font=("Helvetica", 20))
    frequency_label.pack(pady=5)

    # Play sound button
    play_button = tk.Button(parent_frame, text="Play Sound", command=play_sound_and_plot, font=("Helvetica", 20))
    play_button.pack(pady=30)

    # Create a frame for the plot and set up the figure and axis
    plot_frame = tk.Frame(parent_frame, width=800, height=400, padx=100, pady=50)
    plot_frame.pack(pady=20)
    fig, ax = plt.subplots(figsize=(20, 10))

    # Add axis labels for the graph
    ax.set_xlabel('Time (seconds)', fontsize=18)
    ax.set_ylabel('Amplitude', fontsize=18)
    ax.set_title('Sound Waveform', fontsize=20)

    # Embed the plot in the Tkinter canvas
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.get_tk_widget().pack()
