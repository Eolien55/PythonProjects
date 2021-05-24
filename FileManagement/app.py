from tkinter import ttk
import tkinter as tk
import ttkthemes as themes
import subprocess

running = False


def switch():
    global running
    if running:
        with open("/tmp/running_files_number", "w") as file:
            file.write("0")
        running = False
        running_string.set("Pas en train de classer")
    else:
        with open("/tmp/running_files_number", "w") as file:
            file.write("1")
        subprocess.Popen(
            ["python", "/home/elie/pythonprojects/FileManagement/run.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        running = True
        running_string.set("En train de classer")


main = themes.ThemedTk(theme="arc")
main.configure(background="#F6F4F2")

running_string = tk.StringVar()
running_string.set("Pas en train de classer")
button_switch = ttk.Button(main, command=switch, text="switch")
label_running = ttk.Label(main, textvariable=running_string)
button_switch.pack()
label_running.pack()

main.mainloop()
