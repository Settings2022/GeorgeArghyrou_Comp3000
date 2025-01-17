import tkinter as tk
from tkinter import ttk
from gui import gui_main
from gui2 import gui2_main
from gui3 import gui3_main
from gui3_plot import gui3_plot_main
from guiRecord import guiRecord_main
from lowPassFilter import low_pass_filter_main
from instrument_tab import build_instrument_tab
from autoTune import GuitarTunerApp

# Placeholder functions for the features
def open_gui(parent_frame):
    gui_main(parent_frame)

def open_gui2(parent_frame):
    gui2_main(parent_frame)

def open_gui3(parent_frame):
    gui3_main(parent_frame)

def open_gui3_plot(parent_frame):
    gui3_plot_main(parent_frame)

def open_guiRecord(parent_frame):
    guiRecord_main(parent_frame)

def open_low_pass_filter(parent_frame):
    low_pass_filter_main(parent_frame)

def open_instrument_tab(parent_frame):
    build_instrument_tab(parent_frame)

# Initialize Guitar Tuner tab
def open_guitar_tuner_tab(parent_frame):
    app = GuitarTunerApp(parent_frame)

# Main Application
def main_interface():
    root = tk.Tk()
    root.title("Final Year Project: Unified Interface")
    
    # Maximize window on startup
    root.state('zoomed')
    
    # Create a notebook (tabbed interface)
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # Create frames for each tab
    tab1_frame = tk.Frame(notebook)
    tab2_frame = tk.Frame(notebook)
    tab3_frame = tk.Frame(notebook)
    tab4_frame = tk.Frame(notebook)
    tab5_frame = tk.Frame(notebook)
    tab6_frame = tk.Frame(notebook)
    tab7_frame = tk.Frame(notebook)
    guitar_tuner_frame = tk.Frame(notebook)

    # Configure style once
    style = ttk.Style()
    style.configure('TNotebook.Tab', padding=[50, 25], font=('Arial', '14'))

    # Add tabs to the notebook
    notebook.add(tab1_frame, text="Play a sound")
    notebook.add(tab2_frame, text="PlayDisplay .wav")
    notebook.add(tab3_frame, text="See .wav stats")
    notebook.add(tab4_frame, text="Plot .wav graph")
    notebook.add(tab5_frame, text="Record")
    notebook.add(tab6_frame, text="Low Pass Filter Graph")
    notebook.add(tab7_frame, text="Tune by Ear")
    notebook.add(guitar_tuner_frame, text="Tuner App.")  # Add Guitar Tuner tab

    # Initialize each GUI within its respective tab
    open_gui(tab1_frame)
    open_gui2(tab2_frame)
    open_gui3(tab3_frame)
    open_gui3_plot(tab4_frame)
    open_guiRecord(tab5_frame)
    open_low_pass_filter(tab6_frame)
    open_instrument_tab(tab7_frame)
    open_guitar_tuner_tab(guitar_tuner_frame)  # Initialize Guitar Tuner tab

    # Start the tkinter main loop
    root.mainloop()

# Run the main interface
main_interface()
