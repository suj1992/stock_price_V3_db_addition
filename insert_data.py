import pymysql
pymysql.install_as_MySQLdb()
from flask import Flask, render_template, request, send_file, Response
import json
from flask_sqlalchemy import SQLAlchemy
with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
db = SQLAlchemy(app)

def register_models(db):
    class swing_trade(db.Model):
        __tablename__ = 'swing_trade'
        __table_args__ = {'extend_existing': True}

        sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
        entry_price = db.Column(db.Float, nullable=False)
        exit_price = db.Column(db.Float, nullable=False)
        target_price = db.Column(db.Float, nullable=False)
        quant = db.Column(db.Float, nullable=False)
        total_amount = db.Column(db.Float, nullable=True)
        stock_name = db.Column(db.String(50), nullable=False)
        date_time = db.Column(db.String(50), nullable=False)

    return swing_trade
