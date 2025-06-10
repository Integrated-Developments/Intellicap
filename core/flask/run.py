#!/usr/bin/env python3

# <!-- [SS-0]: Metadata ----->
File = 'run.py'
Desc = 'Initiate The Flask App & Generate Configs'
Version = '0.1.4'
Date = '6.9.25'
Int = '6.9.25'
Dev = 'AngrySatan666'

# <!-- [SS-1]: Imports ----->
from app import create_app, socketio
import os
import argparse

# <!-- [SS-2]: Global Variables ----->
def sort_dir():
 # /2.1/ Flask Dir
  ## /2.1.1/ Flask Root Dir
    flsk_dir = os.path.dirname(os.path.abspath(__file__))

  ## /2.1.2/ Flask Blueprint Dir
    bp_dir = os.path.join(flsk_dir, 'bp')

  ## /2.1.3/ Flask Data Dir
    data_dir = os.path.join(flsk_dir, 'data')
    indata_dir = os.path.join(data_dir, 'inputs')
    outdata_dir = os.path.join(data_dir, 'outputs')

  ## /2.1.4/ Flask Database Dir
    db_dir = os.path.join(flsk_dir, 'database')
    dbmig_dir = os.path.join(db_dir, 'migrations')
    dbschema_dir = os.path.join(db_dir, 'schema')

  ## /2.1.5/ Flask Templates Dir
    html_dir = os.path.join(flsk_dir, 'templates')

  ## /2.1.6/ Flask Static Dir
    static_dir = os.path.join(flsk_dir, 'static')
    act_dir = os.path.join(static_dir, 'actions')
    css_dir = os.path.join(static_dir, 'css')
    img_dir = os.path.join(static_dir, 'img')
    js_dir = os.path.join(static_dir, 'js')
    txt_dir = os.path.join(static_dir, 'txt')

 # /2.2/ Core Dir
  ## /2.2.1/ Core Root Dir
    core_dir = os.path.dirname(flsk_dir)

# <!-- [SS-3]: Helper Functions ----->

# <!-- [SS-4]: Functions ----->
app, socketio = create_app()

# <!-- [SS-5]: Runnit ----->
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Run the Flask Application.')
    parser.add_argument('--port', type=int, default=5000, help=['Set the Port Number', 'Default 5000'])
    parser.add_argument('--debug', type=str, default=False, help=['Enable Debug Mode', 'Default False'])
    args = parser.parse_args()
    sort_dir()
    socketio.run(app, host='127.0.0.1', port=args.port, debug=args.debug)
