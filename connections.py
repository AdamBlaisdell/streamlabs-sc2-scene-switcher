import requests
import websocket
import yaml
import json
import slobs_json
import controller
import gui
import time

slobs_url = "ws://127.0.0.1:59650/api/websocket"
sc2_url = "http://localhost:6119/ui"


def set_stop():
    gui.running_status_text.set("Not Running")
    controller.stop = True
    controller.is_running = False


def get_sc2_response():
    while not controller.stop:
        try:
            response = requests.post(sc2_url)
            if response.status_code == 200:
                return response.json()
        except requests.exceptions.RequestException:
            gui.status_event_text.set("Error: Not connected to SC2 game state")
            set_stop()


def websocket_connect(config):
    try:
        ws = websocket.WebSocket()
        ws.connect(slobs_url)
        send(ws, slobs_json.get_connect_json(config["TOKEN"]))
        ws.recv()
        return ws
    except ConnectionError:
        gui.status_event_text.set("Error: Could not connect to Streamlabs OBS")
        set_stop()


def send(ws, message):
    try:
        ws.send(message)
    except ConnectionError:
        gui.status_event_text.set("Error: Connection to Streamlabs OBS interrupted")
        set_stop()


def rcv(ws):
    try:
        return ws.recv()
    except ConnectionError:
        gui.status_event_text.set("Error: Could not connect to Streamlabs OBS")
        set_stop()


def load(item):
    try:
        return json.loads(item)
    except json.JSONDecodeError:
        gui.status_event_text.set("Error: Could not connect to Streamlabs OBS")
        set_stop()


def websocket_loop():
    with open("config.yaml") as read_file:
        config = yaml.safe_load(read_file)
    ws = websocket_connect(config)

    while not controller.stop:
        gui.running_status_text.set("Running")
        send(ws, slobs_json.get_scenes)
        scene_dict = load(rcv(ws))
        if not scene_dict or "error" in scene_dict:
            gui.status_event_text.set("Error: Streamlabs response error, token may be invalid.")
            print(scene_dict)
            set_stop()
            break

        in_game_id = ""
        out_of_game_id = ""
        for item in scene_dict["result"]:
            if item["name"] == config["oog_scene_name"]:
                out_of_game_id = item["id"]
            if item["name"] == config["ig_scene_name"]:
                in_game_id = item["id"]

        send(ws, slobs_json.get_active_scene)
        active_scene = load(rcv(ws))
        active_scene_id = active_scene["result"]
        gui.status_event_text.set("Checking for changes")

        sc2response = get_sc2_response()
        if not sc2response:
            set_stop()
            break
        if 'ScreenLoading/ScreenLoading' in sc2response['activeScreens'] \
                and active_scene_id != in_game_id:
            gui.status_event_text.set("Switching scene to in game.")
            j_switch_in_game = slobs_json.get_switch_to_in_game_json(in_game_id)
            send(ws, j_switch_in_game)
            rcv(ws)
        if 'ScreenBackgroundSC2/ScreenBackgroundSC2' in sc2response['activeScreens'] \
                and active_scene_id != out_of_game_id:
            gui.status_event_text.set("Switching scene to out of game.")
            j_switch_out_of_game = slobs_json.get_switch_to_out_of_game_json(out_of_game_id)
            send(ws, j_switch_out_of_game)
            rcv(ws)
        time.sleep(1.5)

        if controller.stop:
            ws.close()
            set_stop()
            gui.status_event_text.set("")


