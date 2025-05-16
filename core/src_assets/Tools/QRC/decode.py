import cv2
from pyzbar.pyzbar import decode
import os
import sys

def base () :
    _dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    return _dir

def read_qr_code(image_path) :
    img = cv2.imread(image_path)
    decoded_objects = decode(img)
    results = [obj.data.decode('utf-8') for obj in decoded_objects]
    return results

def main () :
    _dir = base()
    qr_dir = os.path.join(_dir, "QRCodes")
    if not os.path.exists(qr_dir) :
        print("No QR codes directory found.")
        return
    
    files = [f for f in os.listdir(qr_dir) if f.endswith('.png')]
    if not files :
        print("No QR code images found.")
        return
    
    for file in files :
        file_path = os.path.join(qr_dir, file)
        results = read_qr_code(file_path)
        if results :
            print(f"Decoded text from {file}:")
            for result in results :
                print(result)
        else :
            print(f"No data found in {file}.")

if __name__ == "__main__" :
    main()