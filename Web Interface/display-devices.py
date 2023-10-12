from flask import Flask, render_template
import pymysql

app = Flask(__name__)

@app.route('/')
def display_data():
    conn = pymysql.connect(host='localhost', user='root', password='ArchFiber23', db='customer_data')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    cursor.execute('SELECT * FROM radacct;')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('table_display.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)