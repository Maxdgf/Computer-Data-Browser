from customtkinter import *
import customtkinter as ctk

def loadingScreen():
    root = ctk.CTkToplevel()
    root.title("Data is loading...")
    root.geometry("400x200")
    root.resizable(0, 0)
    root.grab_set()

    description = ctk.CTkLabel(root, text="Loading...", font=("Arial", 30), text_color="green")
    description.pack()

    progressbar = ctk.CTkProgressBar(root, orientation="horizontal", progress_color="lime")
    progressbar.pack(expand=True, fill="x")

    progressbar.start()

    root.attributes("-topmost", 1)

    root.after(3000, root.destroy)
