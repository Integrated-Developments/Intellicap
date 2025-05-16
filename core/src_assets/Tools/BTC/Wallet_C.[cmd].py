Version = [0,0,1]
State = "CMD"

import sys
import json
import qrcode
from bitcoinlib.wallets import Wallet

def generate_qr(data, filename):
    """Generates and saves a QR code for the given data."""
    try:
        qr = qrcode.make(data)
        qr.save(filename)
    except Exception as e:
        return str(e)
    return None

def create_wallet():
    """Generates a new Bitcoin cold wallet and saves QR codes."""
    try:
        wallet = Wallet.create("ColdStorageWallet", keys=1, network="bitcoin", witness_type="segwit", db_uri=None)

        address = wallet.get_key().address
        private_key = wallet.get_key().wif

        # Generate QR codes
        error1 = generate_qr(address, "BTC_Public_QR.png")
        error2 = generate_qr(private_key, "BTC_Private_QR.png")

        # Save wallet info to text file
        with open("BTC_Wallet_Info.txt", "w") as f:
            f.write(f"Bitcoin Address: {address}\n")
            f.write(f"Private Key (WIF): {private_key}\n")

        # If QR generation failed, return failure
        if error1 or error2:
            return {"status": "fail", "message": error1 or error2}

        return {"status": "success", "address": address}
    
    except Exception as e:
        return {"status": "fail", "message": str(e)}

def main():
    """Reads JSON input from command line and executes the requested action."""
    if len(sys.argv) < 2:
        print(json.dumps({"status": "fail", "message": "No JSON input provided."}))
        return

    # Read JSON input
    json_input = sys.argv[1]

    try:
        data = json.loads(json_input)
    except json.JSONDecodeError:
        print(json.dumps({"status": "fail", "message": "Invalid JSON input."}))
        return

    if data.get("action") == "cold_wallet":
        result = create_wallet()
        print(json.dumps(result))

if __name__ == "__main__":
    main()

#   @MANUAL     python cold_wallet_offline.py '{"action": "cold_wallet"}'
#   @PAYLOAD    {"action" : "cold_wallet"}