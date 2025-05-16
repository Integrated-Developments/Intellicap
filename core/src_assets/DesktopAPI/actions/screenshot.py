import pyautogui
from PIL import Image
import io

def take_screenshot():
    """Take a screenshot and return it as a binary stream."""
    screenshot = pyautogui.screenshot()
    img_byte_arr = io.BytesIO()
    screenshot.save(img_byte_arr, format='PNG')
    img_byte_arr.seek(0)
    return img_byte_arr
