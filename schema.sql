CREATE TABLE IF NOT EXISTS swing_trade (
    sno INTEGER PRIMARY KEY AUTO_INCREMENT,
    entry_price FLOAT NOT NULL,
    exit_price FLOAT NOT NULL,
    target_price FLOAT NOT NULL,
    quant FLOAT NOT NULL,
    total_amount FLOAT,
    stock_name VARCHAR(50) NOT NULL,
    date_time VARCHAR(50) NOT NULL
);



import pymysql

@app.route("/stock_pred_swing", methods=['POST'])
def stock_pred_swing():
    if request.method == 'POST':
        entry = float(request.form.get('fname'))
        exit_price = float(request.form.get('lname'))
        stock_name = str(request.form.get('stock_name'))
        entry_1, exit_1, quant, target, total_amount, risk = risk_factor_swing(entry, exit_price)
        current_datetime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = pymysql.connect(host="localhost", user="root", password="", database="stock_market")
        cursor = conn.cursor()

        insert_query = """
        INSERT INTO swing_trade (
            entry_price, exit_price, target_price, quant, total_amount, stock_name, date_time
        ) VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(insert_query, (entry, exit_price, target, quant, total_amount, stock_name, current_datetime))
        conn.commit()
        cursor.execute("SELECT * FROM swing_trade")
        trades = cursor.fetchall()
        conn.close()

        return {"message": "Inserted successfully", "data": trades}
