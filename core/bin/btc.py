# <!-- [SS-0]: Meta Data -----> #
VERSION = '0.2.29'
DATE = '5.5.25'
DESC = 'Convert Images to ICO Format'
DEV = 'AngrySatan666'

# <!-- [SS-1]: Imports -----> #
import os, sys
import qrcode
from bitcoinlib.wallets import Wallet
from io import BytesIO
import json
import argparse
import base64
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from models import Members, db

# <!-- [SS-2]: Global Variables -----> #
_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# <!-- [SS-3]: Helpful Functions -----> #
def gen_qr (data) :
    try :
        qr = qrcode.make(data=str)
        buffer = BytesIO()
        qr.save(buffer, format='PNG')
        qr_bytes = buffer.getvalue()
        buffer.close()
        return qr_bytes
    except Exception as e :
        return str(e)

def create (seed=None) :
    try :
        if seed :
            wallet = Wallet.create(keys=seed, network='bitcoin', witness_type='segwit')
        else:
            wallet = Wallet.create(key=1, network='bitcoin', witness_type='segwit')
        key = wallet.get_key()
        public = gen_qr(data=key.address)
        private = gen_qr(data=key.wif)
        public_b64 = base64.b64encode(public).decode('utf-8')
        private_b64 = base64.b64encode(private).decode('utf-8')
        return public_b64, private_b64
    except Exception as e :
        return str(e)

# <!-- [SS-4]: Script Functions -----> #
def main () :
    parser = argparse.ArgumentParser(description='Generate Bitcoin Wallet as Binary, Create Tranasctions')
    parser.add_argument('--cmd', action='store_true', help='Enable command mode')

    args = parser.parse_args()

    if args.cmd :
        try :
            data = json.load(sys.stdin)
            attachments = data.get('attachments', [])
            comment = data.get('comment', '')
            arguments = data.get('arguments', [])
            args_dict = {}
            for arg in arguments :
                if isinstance(arg, dict) :
                    args_dict.update(arg)
            if '--create_wallet' in args_dict :
                user = args_dict['--create_wallet']
                if '--seed' in args_dict :
                    seed = args_dict['--seed']
                    public, private = create (seed=seed)
                else :
                    public, private = create ()
                engine = create_engine('postgresql+psycopg2://postgres:tfukgobx@localhost:6666/intellicap')
                Session = sessionmaker(bind=engine)
                session = Session()
                try:
                    member = session.query(Members).filter_by(id=int(user)).first()
                    if member:
                        member.wallet_pub = public.encode('utf-8')
                        member.wallet_pri = private.encode('utf-8')
                        session.commit()
                    else:
                        pass
                finally:
                    session.close()
        except json.JSONDecodeError as e :
            response = json.dumps({"status": 404, "body": {"result": "Error: ", "message": "Json Decode Error: " + str(e)}})
        except Exception as e :
            response = json.dumps({"status": 500, "body": {"result": "Error: ", "message": str(e)}})
            return response

# <!-- [SS-5]: Runnit -----> #
if __name__ == '__main__':
    main()
