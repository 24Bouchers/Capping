from flask import Flask, render_template
import mariadb

app = Flask(__name__)

@app.route('/')
def display_data():
    conn = mariadb.connect(host='10.10.9.43', user='root', password='', db='customer_data')
    cursor = conn.cursor(mariadb.cursors.DictCursor)
    cursor.execute('SELECT * FROM customers;')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('table_display.html', rows=rows)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9830, debug=True)
