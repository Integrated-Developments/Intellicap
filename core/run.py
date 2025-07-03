#!/usr/bin/env python3

# <!-- [SS-0]: Metadata ----->
File = 'run.py'
Desc = 'Initiate The Flask App & Generate Configs'
Version = '0.1.9'
Date = '6.9.25'
Int = '6.9.25'
Dev = 'AngrySatan666'

# <!-- [SS-1]: Imports ----->
from app import create_app, socketio, db
import argparse

# <!-- [SS-2]: Global Variables ----->

# <!-- [SS-3]: Helper Functions ----->

# <!-- [SS-4]: Functions ----->
app, socketio = create_app()

with app.app_context():
    db.create_all()

# <!-- [SS-5]: Runnit ----->
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Flask Application.')
    parser.add_argument('--port', type=int, default=5000, help=['Set the Port Number', 'Default 5000'])
    parser.add_argument('--debug', type=str, default=True, help=['Enable Debug Mode', 'Default True'])
    args = parser.parse_args()
    socketio.run(app, host='127.0.0.1', port=args.port, debug=args.debug)
