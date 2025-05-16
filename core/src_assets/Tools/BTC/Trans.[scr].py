Version = [0,0,1]
State = "SCR"

import requests
from bitcoinlib.transactions import Transaction
from bitcoinlib.keys import Key

# ===== User Inputs ===== #
# Replace with real BTC addresses and private key before running
RECEIVING_ADDRESS = "bc1qreceivingaddress..."
AMOUNT = 0.0001  # BTC to send
SENDING_ADDRESS = "bc1qsendingaddress..."
PRIVATE_KEY = "L1exampleprivatekey..."

def send_btc(receiving_address, amount, sending_address, private_key):
    """
    Creates, signs, and broadcasts a Bitcoin transaction.
    
    :param receiving_address: The BTC address that will receive the funds.
    :param amount: The amount of BTC to send.
    :param sending_address: The BTC address from which funds will be sent.
    :param private_key: The private key of the sending address.
    :return: A dictionary with transaction success or failure details.
    """
    try:
        # Create a transaction object
        tx = Transaction()

        # Load the private key
        key = Key(private_key)

        # Add an input from the sending address
        tx.add_input(sending_address)

        # Add an output to the receiving address
        tx.add_output(receiving_address, amount)

        # Sign the transaction with the private key
        tx.sign(key.private_hex)

        # Convert to raw transaction format
        raw_tx = tx.as_hex()

        # Broadcast transaction (uses Blockstream API)
        response = requests.post("https://blockstream.info/api/tx", data=raw_tx)

        # Check if the transaction was successfully broadcasted
        if response.status_code == 200:
            return {
                "status": "success",
                "txid": response.text.strip(),
                "message": "Transaction successfully broadcasted."
            }
        else:
            return {
                "status": "fail",
                "message": f"Transaction failed to broadcast. Response: {response.text}"
            }

    except Exception as e:
        return {
            "status": "fail",
            "message": f"Error occurred: {str(e)}"
        }

# ===== Execute the Transaction ===== #
result = send_btc(RECEIVING_ADDRESS, AMOUNT, SENDING_ADDRESS, PRIVATE_KEY)
print(result)
