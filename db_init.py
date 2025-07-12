import mysql.connector
# Establishing a connection to MySQL
connection = mysql.connector.connect( 
    host = "localhost",
    user = "root",
    password = ""
)
#Define the database name
database_name = 'stock_market'

# Creating a cursor object using the cursor() method
cursor = connection.cursor()

# Creating a cursor object using the cursor() method
cursor = connection.cursor()

def creating_database():
    try:
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS {database_name}")
        print(f"Database '{database_name}' created successfully!")
    except mysql.connector.Error as error:
        print(f"Failed to create database: {error}")

def create_table_swing_trade():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="stock_market",
            autocommit=True
        )
        cursor = connection.cursor()
    except mysql.connector.Error as error:
        print(f"Failed to connect to database: {error}")

    # Connect to the newly created database
    try:
        connection.database = database_name
    except mysql.connector.Error as error:
        print(f"Failed to connect to database: {error}")

    swing_trade_table = """
        CREATE TABLE IF NOT EXISTS swing_trade (
            sno INTEGER PRIMARY KEY AUTO_INCREMENT,
            entry_price FLOAT NOT NULL,
            exit_price FLOAT NOT NULL,
            target_price FLOAT NOT NULL,
            quant FLOAT NOT NULL,
            total_amount FLOAT,
            stock_name VARCHAR(50) NOT NULL,
            date_time VARCHAR(50) NOT NULL
        )
        """
    # Execute the SQL commands to create tables
    try:
        cursor.execute(swing_trade_table)
        # cursor.execute(create_table2)
        connection.commit()
        print("Tables created successfully!")
    except mysql.connector.Error as error:
        print(f"Failed to create tables: {error}")
    finally:
        # Closing the cursor and connection
        cursor.close()
        connection.close()