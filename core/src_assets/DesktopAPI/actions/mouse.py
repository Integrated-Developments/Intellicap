import pyautogui as py
import json
import argparse
from PIL import ImageGrab as ig
from flask import jsonify

def move_mouse(x, y):
    py.moveTo(x, y)
    fx = {
        "Mouse moved" : [f"{x}", f"{y}"]
    }
    print (json.dumps(fx))
    return fx, 666

def click_mouse(x=None, y=None, button="left"):
    if x is not None and y is not None:
        py.click(x, y, button=button)
        fx = {
            "Mouse clicked" : [f"{x}", f"{y}"],
            "button" : f"{button}"
        }
    else:
        pos = py.position()
        py.click(button=button)
        fx = {
            "Mouse clicked" : f"{pos}",
            "button" : f"{button}"
        }
    print (json.dumps(fx))
    return fx, 666

def drag_mouse(x, y, duration=0.5):
    py.dragTo(x, y, duration=duration)
    fx = {
        "Mouse dragged" : [f"{x}", f"{y}"],
        "time" : f"{duration}s"
    }
    print (json.dumps(fx))
    return fx, 666

def scroll_mouse(amount):
    py.scroll(amount)
    fx = {
        "Mouse scrolled" : f"{amount}"
    }
    print(json.dumps(fx))
    return fx, 666

def info():
    pos = py.position()
    screen = ig.grab()
    color = screen.getpixel(pos)
    fx = {
        "color": color,
        "pos": pos
    }
    print(json.dumps(fx))
    return fx, 666

def main():
    global api_key
    parser = argparse.ArgumentParser()
    parser.add_argument("--payload", type=str, required=True, help="JSON payload")
    args = parser.parse_args()

    try:
        payload = json.loads(args.payload)
    except json.JSONDecodeError:
        fx = ("Invalid JSON payload")
        return fx, 404

    action = payload.get("action")
    api_key = payload.get("api_key")
    function = payload["args"].get("function")
    args = payload.get("args", {})

    if action == "mouse":
        if function == "move":
            x = args.get("x", 0)
            y = args.get("y", 0)
            move_mouse(x, y)
        elif function == "click":
            x = args.get("x")
            y = args.get("y")
            button = args.get("button")
            click_mouse(x, y, button)
        elif function == "drag":
            x = args.get("x", 0)
            y = args.get("y", 0)
            duration = args.get("duration", 0.5)
            drag_mouse(x, y, duration)
        elif function == "info":
            info()
        elif function == "scroll" :
            amount = args.get("amount")
            scroll_mouse (amount=amount)
        else:
            print("Unknown function")
    else:
        print("Unknown action")

if __name__ == "__main__":
    main()
