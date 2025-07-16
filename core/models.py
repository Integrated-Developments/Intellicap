from app import db

class StockAccount (db.Model) :
    __tablename__ = 'stock_account'
    date = db.Column (db.String, primary_key=True, comment='Date of the Entry')
    active = db.Column (db.Boolean, nullable=False, default=False, comment='Did Intellicap actively trade?')
    trade_day = db.Column (db.Integer, nullable=True, comment='If active, which Number of Day')
    open = db.Column (db.Float, nullable=False, comment='Opening Share-Price of the Day')
    high = db.Column (db.Float, nullable=False, comment='Highest Share-Price of the Day')
    low = db.Column (db.Float, nullable=False, comment='Lowest Share-Price of the Day')
    close = db.Column (db.Float, nullable=False, comment='Closing Share-Price of the Day')
    price = db.Column (db.Float, nullable=False, comment='Current Share-Price of Intellicap')

class Members (db.Model) :
    __tablename__ = 'members'
    id = db.Column (db.Integer, primary_key=True, comment='Unique ID of the Member')
    name = db.Column (db.String, nullable=False, unique=True, comment='Username of the Member')
    email = db.Column (db.String, nullable=False, unique=True, comment='Email of the Member')
    verification = db.Column (db.Boolean, nullable=False, default=False, comment='Verification Status of the Member')
    join = db.Column (db.DateTime, nullable=True, comment='Date of Member Verification')
    password = db.Column (db.String, nullable=False, comment='Password of the Member')
    wallet_pub = db.Column (db.LargeBinary, nullable=True, unique=True, comment='Public Key of Members Wallet')
    wallet_pri = db.Column (db.LargeBinary, nullable=True, unique=True, comment='Private Key of the Members Wallet')

class TransActions (db.Model) :
    __tablename__ = 'transactions'
    id = db.Column (db.Integer, primary_key=True, comment='Unique ID of the Transaction')
    member_id = db.Column (db.Integer, db.ForeignKey('members.id'), nullable=False, comment='ID of the Member who made the Transaction')
    date = db.Column (db.String, nullable=False, comment='Date of the Transaction')
    type = db.Column (db.String, nullable=False, comment='Type of Transaction(Buy/Sell)')
    shares = db.Column (db.Integer, nullable=False, comment='Number of Shares')
    price = db.Column (db.Float, nullable=False, comment='Price of the Shares')
    cap = db.Column (db.Float, nullable=False, comment='Capital of Intellicap at Transaction')


class CodeSessions(db.Model):
    __tablename__ = 'code_sessions'
    id = db.Column(db.Integer, primary_key=True, comment='Unique ID of the Code Session')
    user_id = db.Column(db.Integer, db.ForeignKey('members.id'), nullable=False, comment='ID of the User (Member)')
    tunnel_name = db.Column(db.String, nullable=False, comment='Name of the Cloudflare Tunnel')
    host_name = db.Column(db.String, nullable=False, comment='Host name for the tunnel (e.g., code-username-xyz.intellicap.org)')
    subdomain = db.Column(db.String, nullable=False, comment='Subdomain used for the tunnel')
    port = db.Column(db.Integer, nullable=False, comment='Local port used for the tunnel')
    creds_path = db.Column(db.String, nullable=False, comment='Path to the credentials file')
    config_path = db.Column(db.String, nullable=False, comment='Path to the tunnel config YAML file')
    created_at = db.Column(db.DateTime, server_default=db.func.now(), nullable=False, comment='Timestamp when the session was created')
    status = db.Column(db.String, nullable=True, comment='Status of the session (e.g., active, failed)')
    notes = db.Column(db.Text, nullable=True, comment='Additional notes or metadata')
