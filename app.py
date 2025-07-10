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

pymysql.install_as_MySQLdb()


with open('config.json', 'r') as c:
    params = json.load(c)["params"]

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = params['local_uri']
db = SQLAlchemy(app)
"""with open ('config.json', 'r') as c:
    params = json.load(c)["params"]
    print(params)
app.secret_key = 'super-secret-key'"""

class swing_trade(db.Model):
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entry_price = db.Column(db.Float, nullable=False)
    exit_price = db.Column(db.Float, nullable=False)
    target_price = db.Column(db.Float, nullable=False)
    quant = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=True)
    stock_name = db.Column(db.String(50), nullable=False)
    date_time = db.Column(db.String(50), nullable=False)

class intra_day_trade(db.Model):
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    entry_price = db.Column(db.Float, nullable=False)
    exit_price = db.Column(db.Float, nullable=False)
    target_price = db.Column(db.Float, nullable=False)
    total_amount = db.Column(db.Float, nullable=True)
    stock_name = db.Column(db.String(50), nullable=False)
    date_time = db.Column(db.String(50), nullable=False)

class news_analysis_table(db.Model):
    sno = db.Column(db.Integer, primary_key=True, autoincrement=True)
    news = db.Column(db.String, nullable=False)
    neg_no = db.Column(db.Float, nullable=False)
    neu_no = db.Column(db.Float, nullable=False)
    pos_no = db.Column(db.Float, nullable=True)
    overall_no = db.Column(db.Float, nullable=False)
    date_time = db.Column(db.String(50), nullable=False)



@app.route("/")
def index():
    return render_template('index.html', params=params)

@app.route("/stock")
def stock():
    return render_template('stock_pred.html', params=params)

@app.route("/stock_swing")
def stock_swing():
    return render_template('swing.html', params=params)

@app.route("/news_anlysis")
def news_analyis():
    return render_template('news_analysis.html', params=params)

@app.route("/web_scrap")
def web_scrap_grow():
    return render_template('web_scrap.html', params=params)

@app.route("/stock_pred_page", methods=['POST'])
def stock_pred():
    if request.method == 'POST':
        entry = request.form.get('fname')
        exit = request.form.get('lname')
        stock_name = str(request.form.get('stock_name'))
        entry_1,exit_1,quant, target,total_amount, risk = risk_factor(entry,exit)

        new_trade = intra_day_trade(entry_price=entry, exit_price=exit, target_price=target, total_amount=total_amount, stock_name=stock_name)
        
        db.session.add(new_trade)
        db.session.commit()
        trades = intra_day_trade.query.all()
        
        
    return render_template('charts_pred_intra.html', entry_1=entry_1, exit_1=exit_1,quant=quant,target=target, total_amount=total_amount, 
                           risk=risk,stock_name=stock_name, params=params, trades=trades)


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



@app.route("/news_sentiment", methods=['POST'])
def news_sentiment():
    if request.method == 'POST':
        # data collectd from UI
        news = request.form.get('blog_content')
        current_datetime = datetime.now()
        count = news_analysis_table.query.count()
        new_sl_no = count + 1
        # call the function
        news_analysis= analyze_sentiment(news)
        neg = news_analysis[0]
        neu = news_analysis[1]
        pos = news_analysis[2]
        over_all = news_analysis[3]
        #Enrty the data into database
        new_entry = news_analysis_table(sno = new_sl_no, news = news, neg_no= neg, neu_no = neu, pos_no = pos, overall_no =over_all, date_time = current_datetime)
        db.session.add(new_entry)
        db.session.commit()
        all_news = news_analysis_table.query.all()

    return render_template('news_chart.html',all_news_ui = all_news)

@app.route("/web_scarp_mutual", methods=['POST'])
def web_scarp_mutual():
    if request.method == 'POST':
        url = request.form.get('urls')
        output_file_new = url.split('/')[-1]

        output_file = output_file_new.replace('-', ' ')
        output_file = output_file.title()
        df = web_scrap(url)
        excel_file_path = f'output/{output_file_new}.csv'

        df.to_csv(excel_file_path, index=False)
        
        
    return render_template('web_scrap_chart.html', df=df, output_file=output_file,output_file_new=output_file_new, params=params)


@app.route("/download_csv/<filename>", methods=['GET'])
def download_csv(filename):
    
    file_path = f'output/{filename}'
    return send_file(file_path, as_attachment=True)



# Download CSV from Data Base
@app.route('/download_swing_csv')
def download_swing_csv():
    # Query the database to retrieve the data
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
    app.run(debug=True)