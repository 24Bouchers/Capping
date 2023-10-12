from flask import Flask, render_template
import pymysql

app = Flask(__name__)

@app.route('/')
def display_data():
<<<<<<< HEAD
<<<<<<< HEAD
    conn = mariadb.connect(host='10.10.9.43', user='root', password='', db='customer_data')
    cursor = conn.cursor(mariadb.cursors.DictCursor)
    cursor.execute('SELECT * FROM customers;')
=======
    conn = mariadb.connect(host='10.10.9.43', user='root', password='', db='ArchFiber')
    cursor = conn.cursor(mariadb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Data;')
>>>>>>> 4aedf9e (Steve b (#5))
=======
    conn = pymysql.connect(host='10.10.9.43', user='root', password='', db='customer_data')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM customers;')
>>>>>>> f1f21b6 (Reload from Liam branch appy is now TableInit.py)
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('table_display.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
