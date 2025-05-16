Version = [0,0,1]
State = "SCR"

import qrcode
from bitcoinlib.wallets import Wallet

# Create a new wallet (offline)
wallet = Wallet.create("ColdStorageWallet", keys=1, network="bitcoin", witness_type="segwit", db_uri=None)

# Get the first address and private key
address = wallet.get_key().address
private_key = wallet.get_key().wif

# Generate QR codes
def generate_qr(data, filename):
    qr = qrcode.make(data)
    qr.save(filename)

# Save QR codes in the root directory
generate_qr(address, "BTC_Public_QR.png")
generate_qr(private_key, "BTC_Private_QR.png")

# Save string data as a text file for reference
with open("BTC_Wallet_Info.txt", "w") as f:
    f.write(f"Bitcoin Address: {address}\n")
    f.write(f"Private Key (WIF): {private_key}\n")

print("QR codes and wallet information saved successfully.")
print(f"Public Address: {address}")
print(f"Private Key: {private_key}")
