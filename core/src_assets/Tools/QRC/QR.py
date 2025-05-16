import qrcode
import random
import string
import json
import os
import sys

def base () :
    _dir = os.path.dirname(os.path.abspath(sys.argv[0]))
    patf = os.path.join(_dir, "Entry.json")
    with open(patf, 'r') as fx :
        data = json.load(fx)
    key_length = data.get('key', 32)
    url = data.get('url', [])
    return key_length, url

def generate_api_key (length) :
    chars = (string.ascii_lowercase + string.ascii_uppercase + string.digits +
             "?/,@,$,#,%,^,&,*,(,),-,_,<,>,[,],{,},~,!,+,×,÷,=,")
    return ''.join(random.choice(chars) for _ in range(length))

def generate_qr_code(url_list, key_length, output_dir) :
    for fx in url_list :
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(fx)
        qr.make(fit=True)
        file_name = f"{generate_api_key(key_length)}.png"
        img = qr.make_image(fill_color="black", back_color="white")
        file_path = os.path.join(output_dir, file_name)
        img.save(file_path)
        print(f"QR Code saved as: {file_path}")

def main () :
    key_length, url_list = base()
    output_dir = os.path.join(os.path.dirname(os.path.abspath(sys.argv[0])), "QRCodes")
    os.makedirs(output_dir, exist_ok=True)
    generate_qr_code(url_list, key_length, output_dir)

if __name__ == "__main__" :
    main()