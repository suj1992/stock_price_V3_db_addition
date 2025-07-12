from flask import Flask, render_template, request, send_file, Response
import json
from stock_pred_1 import risk_factor
from swing import risk_factor_swing
from news_analysis import analyze_sentiment
from mutual_web_scrap import web_scrap
from flask_sqlalchemy import SQLAlchemy
from io import StringIO
import csv
from datetime import datetime
import pymysql
import sqlite3
pymysql.install_as_MySQLdb()
from db_init import creating_database, create_table_swing_trade
from insert_data import register_models


with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
db = SQLAlchemy(app)
"""with open ('config.json', 'r') as c:
    params = json.load(c)["params"]
    print(params)
app.secret_key = 'super-secret-key'"""

@app.route("/")
def index():
    return render_template('index.html', params=params)

@app.route("/stock")
def stock():
    return render_template('stock_pred.html', params=params)

@app.route("/stock_swing")
def stock_swing():
    return render_template('swing.html', params=params)

@app.route("/stock_pred_swing", methods=['POST'])
def stock_pred_swing():
    if request.method == 'POST':
        #Get data from html
        entry = float(request.form.get('fname'))
        exit = float(request.form.get('lname'))
        stock_name = str(request.form.get('stock_name'))
        #Call the Function
        entry_1, exit_1, quant, target, total_amount, risk = risk_factor_swing(entry, exit)
        current_datetime = datetime.now()
        swing_trade = register_models(db)
        count = swing_trade.query.count()
        new_sl_no = count + 1
        
        # connect the data base
        new_trade = swing_trade(sno=new_sl_no, entry_price=entry, exit_price=exit, target_price=target,quant = quant, total_amount=total_amount, 
                                stock_name=stock_name, date_time = current_datetime)
        
        # Add the new trade to the database session and commit changes
        db.session.add(new_trade)
        db.session.commit()
        trades = swing_trade.query.all()

    # Render template with calculated values
    return render_template('charts_pred_swing.html', trades=trades)


@app.route("/download_csv/<filename>", methods=['GET'])
def download_csv(filename):
    
    file_path = f'output/{filename}'
    return send_file(file_path, as_attachment=True)



# Download CSV from Data Base
@app.route('/download_swing_csv')
def download_swing_csv():
    # Query the database to retrieve the data
    swing_trade = register_models(db)
    data = swing_trade.query.all()

    # Prepare CSV data
    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['Entry Price', 'Exit Price', 'Quantity','Target','Amount','Name', 'Date'])  # Add column headers
    for row in data:
        writer.writerow([row.entry_price, row.exit_price,row.quant,row.target_price,row.total_amount,row.stock_name,row.date_time ])  # Add row data

    # Create response with CSV data
    response = Response(output.getvalue(), mimetype='text/csv')
    response.headers['Content-Disposition'] = 'attachment; filename=swing_data.csv'
    return response

if __name__ == "__main__":
    creating_database()
    create_table_swing_trade()
    app.run(debug=True)