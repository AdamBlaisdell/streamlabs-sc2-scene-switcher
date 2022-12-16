import tkinter as tk
from tkinter import ttk
import controller


def running_status_updated(*args):
    if running_status_text.get() == "Running":
        running_status_label.config(foreground="green")
    elif running_status_text.get() == "Stopping...":
        running_status_label.config(foreground="orange")
    else:
        running_status_label.config(foreground="red")


def status_event_updated(*args):
    if "Error: " in status_event_text.get():
        status_event_label.config(foreground="red")
    else:
        status_event_label.config(foreground="black")


root = tk.Tk()
root.geometry("600x400")
frm = ttk.Frame(root, padding=10)
frm.place()
root.title("SC2 Scene Switcher")
s = ttk.Style()
s.configure('.', font=('Arial', 13))


# labels
main_label = ttk.Label(root, text="SC2 Scene Switcher", font=("Ariel", 19))
main_label.place(x=155, y=20)
token_label = ttk.Label(root, text="Token", font=("Ariel", 13))
token_label.place(x=50, y=60)
oog_label = ttk.Label(root, text="Out of game scene")
oog_label.place(x=50, y=142)
ig_label = ttk.Label(root, text="In game scene")
ig_label.place(x=250, y=142)
status_label = ttk.Label(root, text="Status: ", font=("Arial", 12),)
status_label.place(x=315, y=234)

running_status_text = tk.StringVar(root, "Not Running")
running_status_label = ttk.Label(root, textvariable=running_status_text, font=("Arial", 12), foreground="red")
running_status_label.place(x=370, y=234)
running_status_text.trace('w', running_status_updated)

status_event_text = tk.StringVar(root, "")
status_event_label = ttk.Label(root, textvariable=status_event_text, font=("Arial", 12))
status_event_label.place(x=50, y=290)
status_event_text.trace('w', status_event_updated)

# buttons
ttk.Button(root, text="Save", command=controller.save_scene_names).place(x=450, y=170)
ttk.Button(root, text="Start", command=controller.start_websocket_loop).place(x=50, y=230)
ttk.Button(root, text="Stop", command=controller.stop_websocket_loop).place(x=180, y=230)
ttk.Button(root, text="Save", command=controller.save_token).place(x=450, y=90)

# entries
token_field = ttk.Entry(root, width=34, font=("Arial", 14), show='*')
token_field.place(x=50, y=90)
ig_name_field = ttk.Entry(root, width=16, font=("Arial", 14))
ig_name_field.place(x=250, y=170)
print(controller.get_variable("config.yaml", "ig_scene_name"))
ig_name_field.insert(0, controller.get_variable("config.yaml", "ig_scene_name"))
oog_name_field = ttk.Entry(root, width=16, font=("Arial", 14))
oog_name_field.place(x=50, y=170)
oog_name_field.insert(0, controller.get_variable("config.yaml", "oog_scene_name"))

root.mainloop()
