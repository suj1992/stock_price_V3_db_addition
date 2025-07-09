import yfinance as yf
import pandas as pd
from flask import Flask, render_template, request, send_from_directory, session


app = Flask(__name__)

"""with open ('config.json', 'r') as c:
    params = json.load(c)["params"]
    print(params)
app.secret_key = 'super-secret-key'"""


@app.route("/")
def index():
    return render_template('index.html')

@app.route("/stock")
def stock():
    return render_template('stock_pred.html')

@app.route("/stock_pred_page", methods=['POST'])
def stock_pred():
    if request.method == 'POST':
        stock_ticker = request.form.get('fname')  
        stock_tenure = request.form.get('lname')  
        stock_time = request.form.get('time')

        print(stock_ticker)
        print(stock_tenure)
        print(stock_time)
    return render_template('stock_pred.html')




if __name__ == "__main__":
    app.run(debug=True)