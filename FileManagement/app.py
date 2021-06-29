import subprocess
import gi

gi.require_version("Gtk", "3.0")

from gi.repository import Gtk

running = False


def switch(event=None):
    global running
    if running:
        with open("/tmp/running_files_number", "w") as file:
            file.write("0")
        running = False
        label.set_label("Pas en train de classer")
    else:
        with open("/tmp/running_files_number", "w") as file:
            file.write("1")
        subprocess.Popen(
            ["python", "/home/elie/pythonprojects/FileManagement/run.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        running = True
        label.set_label("En train de classer")


window = Gtk.Window()
window.set_title("File manager")
window.set_default_size(200, 150)
window.set_resizable(False)

box = Gtk.Box(spacing=5, orientation=Gtk.Orientation.VERTICAL)
button = Gtk.Button(label="switch")
button.set_halign(Gtk.Align.CENTER)
label = Gtk.Label(label="Pas en train de classer")
box.pack_start(button, False, False, 0)
box.pack_start(label, True, True, 0)

window.add(box)

button.connect("clicked", switch)
window.connect("delete-event", Gtk.main_quit)

window.show_all()
Gtk.main()
