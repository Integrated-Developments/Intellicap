from flask import Flask, render_template, request, redirect, url_for, send_from_directory, send_file
import requests as rq
import json
import datetime as dt
import time as ti
import os
import random
import string
from actions.screenshot import take_screenshot
from actions.application import open_application
from actions.ocr import extract_text_from_image
from typing import Optional
from ctypes import CDLL, c_char_p
# Import Union from typing
from typing import Union

## --- Directory --- ##
_dir = ("/home/testing666/mysite/")
dat_dir = (f"{_dir}/dynamic/")
sta_dir = os.path.join(os.getcwd(), 'static')
css_dir = (f"{sta_dir}css/")
img_dir = (f"{sta_dir}img/")
js_dir = (f"{sta_dir}js/")
txt_dir = (f"{sta_dir}txt/")
html_dir = (f"{_dir}templates/")


usr_dat = None
# Correct the type annotation for str_gen
str_gen: dict[str, Union[str, int, dict[str, str]]] = {"result": "", "count": 0, "strings": {}}

## --- Load Data --- ##
def Data(save: Optional[bool] = False) -> None:
    global usr_dat
    patty = os.path.join(dat_dir, "usr.json")
    if not save:
        with open(patty, 'r') as f:
            raw = json.load(f)
            usr_dat = json.dumps(raw, indent=4)
    else:
        with open(patty, 'w') as f:
            json.dump(usr_dat, f, indent=4, sort_keys=True)
Data(save=False)

## ---------- Snippet Functions ---------- ##
def prints(*args: str) -> None:
    for txt in args:
        print(txt)
        print("")

def inputs(arg: str, sens: Optional[str] = None) -> str:
    if sens == "cap":
        fx = input(f"{arg}").upper()
    else:
        fx = input(f"{arg}").lower()
    print("")
    return fx

def Timer(x: int, direction: int, randomize: bool) -> None:
    if direction == 1:  # Counts from 0 to x
        if randomize:
            choice = random.uniform(x * 0.5, x * 1.5)
            for i in range(1, int(choice) + 1):
                print(f"{i}sec...")
                ti.sleep(1)
        else:
            for i in range(1, x + 1):
                print(f"{i}sec...")
                ti.sleep(1)
    elif direction == 0:  # Counts from x to 0
        if randomize:
            choice = random.uniform(x * 0.5, x * 1.5)
            for i in range(int(choice), 0, -1):
                print(f"{i}sec...")
                ti.sleep(1)
        else:
            for i in range(x, 0, -1):
                print(f"{i}sec...")
                ti.sleep(1)

# Load the Rust library
rust_lib = CDLL('./core/src_assets/DesktopAPI/bin/rust_component.so')

# Define the function signature
rust_lib.generate_string.argtypes = [c_char_p]
rust_lib.generate_string.restype = c_char_p

def Generate_String(char: int, debug: bool = False) -> str:
    if debug:
        pass
    result = rust_lib.generate_string(str(char).encode('utf-8'))
    return result.decode('utf-8')

## ---------- THE FLASK ---------- ##
app = Flask(__name__, root_path=_dir, static_folder=sta_dir, template_folder=html_dir)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('static/img','favicon.ico', mimetype='image/vnd.microsoft.icon'), 666

@app.route('/', methods=['GET'])
def landingpage () :
    return render_template('main.html')

@app.route('/signup', methods=['GET'])
def newuser() -> str:
    return "It works!"

@app.route('/login', methods=['GET', 'POST'])
def olduser() -> str:
    return "Welcome back!"

@app.route('/screenshot', methods=['GET'])
def screenshot():
    """Endpoint to take a screenshot and return it as a file."""
    screenshot_stream = take_screenshot()
    return send_file(screenshot_stream, mimetype='image/png', as_attachment=True, download_name='screenshot.png')

@app.route('/open_app', methods=['POST'])
def open_app():
    """Endpoint to open an application."""
    app_path = request.json.get('path') if request.json else None
    if not app_path or not os.path.exists(app_path):
        return {"error": "Invalid application path."}, 400
    result = open_application(app_path)
    return {"message": result}

@app.route('/ocr', methods=['POST'])
def ocr() -> Union[dict, tuple]:
    """Endpoint to extract text from an uploaded image."""
    if 'image' not in request.files:
        return {"error": "No image file provided."}, 400
    image = request.files['image']
    if not image.filename:
        return {"error": "Invalid image file."}, 400
    image_path = os.path.join('temp', image.filename)
    image.save(image_path)
    try:
        text = extract_text_from_image(image_path)
        return {"text": text}
    finally:
        os.remove(image_path)
