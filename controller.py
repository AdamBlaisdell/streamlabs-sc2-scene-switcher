import threading
import connections
import yaml
import gui
import websocket

stop = True
is_running = False


def set_variable(file_name, variable, value):
    try:
        with open(file_name) as f:
            set_missing_configs()
            doc = yaml.safe_load(f)
        doc[variable] = value
        with open(file_name, 'w') as f:
            yaml.safe_dump(doc, f, default_flow_style=False)
    except FileNotFoundError:
        with open("config.yaml", "x"):
            pass
        set_missing_configs()
        set_variable(file_name, variable, value)


def get_variable(file_name, var):
    try:
        with open(file_name) as f:
            doc = yaml.safe_load(f)
        return str(doc[var])
    except FileNotFoundError:
        with open("config.yaml", "x"):
            pass
        set_missing_configs()
        get_variable(file_name, var)


def set_missing_configs():
    with open("config.yaml") as f:
        doc = yaml.safe_load(f)
    if not doc:
        doc = {"TOKEN": None}
    if "TOKEN" not in doc:
        doc["TOKEN"] = None
    if "ig_scene_name" not in doc:
        doc["ig_scene_name"] = "SC2 IG"
    if "oog_scene_name" not in doc:
        doc["oog_scene_name"] = "SC2 OOG"
    with open("config.yaml", 'w') as f:
        yaml.safe_dump(doc, f, default_flow_style=False)


def start_websocket_loop():
    global stop
    global is_running
    if stop and not is_running:
        is_running = True
        stop = False
        try:
            thread = threading.Thread(target=connections.websocket_loop)
            thread.daemon = True
            thread.start()
        except websocket.WebSocketException as e:
            print(e)
    else:
        gui.status_event_text.set("Already running!")


def stop_websocket_loop():
    if gui.running_status_text.get() == "Running":
        gui.running_status_text.set("Stopping...")
    gui.status_event_text.set("")
    global stop
    stop = True


def save_token():
    set_variable("config.yaml", "TOKEN", gui.token_field.get())
    gui.token_field.delete(0, 'end')
    gui.status_event_text.set("Token saved")


def save_scene_names():
    set_variable("config.yaml", "oog_scene_name", gui.oog_name_field.get())
    set_variable("config.yaml", "ig_scene_name", gui.ig_name_field.get())
    gui.status_event_text.set("Scene names saved")

