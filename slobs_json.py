import json


def get_connect_json(token):
    return json.dumps({
        "jsonrpc": "2.0",
        "id": 1,
        "method": "auth",
        "params": {"resource": "TcpServerService",
                   "args": [token]}
    })


get_scenes = json.dumps({
    "jsonrpc": "2.0",
    "id": 2,
    "method": "getScenes",
    "params": {
        "resource": "ScenesService"
    }
})


get_active_scene = json.dumps({
    "jsonrpc": "2.0",
    "id": 3,
    "method": "activeSceneId",
    "params": {
        "resource": "ScenesService"
    }
})


def get_switch_to_in_game_json(in_game_id):
    return json.dumps({
        "jsonrpc": "2.0",
        "id": 4,
        "method": "makeSceneActive",
        "params": {
            "resource": "ScenesService",
            "args": [
                in_game_id
            ]
        }
    })


def get_switch_to_out_of_game_json(out_of_game_id):
    return json.dumps({
        "jsonrpc": "2.0",
        "id": 5,
        "method": "makeSceneActive",
        "params": {
            "resource": "ScenesService",
            "args": [
                out_of_game_id
            ]
        }
})