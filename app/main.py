from flask import Flask, jsonify
import mysql.connector
from datetime import datetime

app = Flask(__name__)

mysql_config = {
    'host': 'db', 
    'user': 'myuser', 
    'password': 'mypassword',  
    'database': 'mydatabase'  
}

conn = mysql.connector.connect(**mysql_config)

cursor = conn.cursor()

@app.route('/create_table')
def addtable_database():
    try:
        cursor.execute("DROP TABLE IF EXISTS mytable")
        cursor.execute("""
            CREATE TABLE mytable (
                id INT AUTO_INCREMENT PRIMARY KEY,
                data VARCHAR(255) NOT NULL
            )
        """)
        conn.commit()
        return jsonify({'okay': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/list')
def list_data_database():
    try:
        cursor.execute("SELECT * FROM mytable")
        result = cursor.fetchall()
        return jsonify({'data': result}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/add')
def insert_data_database():
    try:
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("INSERT INTO mytable (data) VALUES (%s)", [current_date])
        conn.commit()
        return jsonify({'okay': True}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500        

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
