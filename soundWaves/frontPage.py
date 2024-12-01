import tkinter as tk
from tkinter import messagebox
from tkinter import ttk
from gui import gui_main
from gui2 import gui2_main
from gui3 import gui3_main
from gui3_plot import gui3_plot_main
from guiRecord import guiRecord_main
from lowPassFilter import low_pass_filter_main

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

# Main Application
def main_interface():
    root = tk.Tk()
    root.title("Final Year Project: Unified Interface")
    root.geometry("800x600")

    # Create a notebook (tabbed interface)
    notebook = ttk.Notebook(root)
    notebook.pack(fill="both", expand=True)

    # Create frames for each tab
    tab1_frame = ttk.Frame(notebook)
    tab2_frame = ttk.Frame(notebook)
    tab3_frame = ttk.Frame(notebook)
    tab4_frame = ttk.Frame(notebook)
    tab5_frame = ttk.Frame(notebook)
    tab6_frame = ttk.Frame(notebook)

    # Add tabs to the notebook
    notebook.add(tab1_frame, text="Play Frq Hz Gui")
    notebook.add(tab2_frame, text="Play & Display wav file Gui2")
    notebook.add(tab3_frame, text="Display wav file stats Gui3")
    notebook.add(tab4_frame, text="Plot wav graphically Gui3_plot")
    notebook.add(tab5_frame, text="Make a recording GuiRecord")
    notebook.add(tab6_frame, text="Low Pass Filter Graph")

    # Initialize each GUI within its respective tab
    open_gui(tab1_frame)
    open_gui2(tab2_frame)
    open_gui3(tab3_frame)
    open_gui3_plot(tab4_frame)
    open_guiRecord(tab5_frame)
    open_low_pass_filter(tab6_frame)

    # Start the tkinter main loop
    root.mainloop()

# Run the main interface
main_interface()
