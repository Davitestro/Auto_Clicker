import customtkinter as tk
import json
import subprocess
import threading
import time
from keyboard import *


def save_settings():
    global when
    settings = {
        "click_interval": click_interval_var.get(),
        "mouse_button": m_button,
        "bind": bind_entry_combintation.get().strip()
    }
    with open("settings.json", "w") as f:
        json.dump(settings, f)
    status_label.configure(text="Settings saved")
    when = bind_entry_combintation.get().strip().lower()


def load_settings():
    global when
    try:
        with open("settings.json", "r") as f:
            settings = json.load(f)
            click_interval_var.set(settings.get("click_interval", 0))
            selected_option.set(options[settings["mouse_button"] - 1])
            bind_entry_combintation.insert(0,settings["bind"])
            status_label.configure(text="Settings loaded")
            when = settings["bind"]
    except FileNotFoundError:
        status_label.configure(text="No settings found")
        save_settings()


def toggle_cpp_program():
    global cpp_process
    is_acitve = False
    try:
        while True:
            if is_pressed((bind_entry_combintation.get()).strip()) and not is_acitve:
                cpp_process = subprocess.Popen("Clicker_System.exe")
                is_acitve = True
                status_label.configure(text="C++ program started")
                time.sleep(0.2)

            if is_pressed((bind_entry_combintation.get()).strip()) and is_acitve:
                cpp_process.kill()
                is_acitve = False
                status_label.configure(text="C++ program is not running")
                time.sleep(0.2)
    except:
        pass


def update_mouse_button(option):
    global m_button
    if option == "Left":
        m_button = 1
    elif option == "Right":
        m_button = 2
    else:
        raise ValueError("You can't input other button")


m_button = 1

root = tk.CTk()
root.title("AutoClicker Settings")

options = ["Left", "Right"]

selected_option = tk.StringVar(root)
selected_option.set(options[0])

click_interval_var = tk.DoubleVar()
bind_combination_var = tk.StringVar(value="Ctrl+Shift+C")

click_interval_label = tk.CTkLabel(root, text="Time between clicks:")
click_interval_entry = tk.CTkEntry(root, textvariable=click_interval_var)
mouse_button_label = tk.CTkLabel(root, text="Mouse Button:")
mouse_button_menu = tk.CTkOptionMenu(root, values=options, command=update_mouse_button)
bind_entry_label = tk.CTkLabel(root, text="Bind:")
bind_entry_combintation = tk.CTkEntry(root)
save_button = tk.CTkButton(root, text="Save Settings", command=save_settings)
status_label = tk.CTkLabel(root, text="")

click_interval_label.grid(row=0, column=0, sticky="w")
click_interval_entry.grid(row=0, column=1)
mouse_button_label.grid(row=1, column=0, sticky="w")
mouse_button_menu.grid(row=1, column=1)
bind_entry_label.grid(row=2, column=0, sticky="w")
bind_entry_combintation.grid(row=2, column=1)
save_button.grid(row=4, column=0)
status_label.grid(row=5, columnspan=2)

when = bind_entry_combintation.get().strip().lower()

load_settings()

cheking = threading.Thread(target=toggle_cpp_program)
cheking.start()

root.mainloop()
