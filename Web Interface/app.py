from flask import Flask, app, flash, redirect, render_template, request
import pymysql

app = Flask(__name__)
app.secret_key = 'ArchFiber23'

@app.route('/')
@app.route('/index.html')
def main():
    return render_template('index.html')

@app.route('/addDevice.html', methods=['GET', 'POST'])
def addDevice():
    if request.method == 'POST':
        # Get data from the form
        name = request.form['customer']
        mac_address = request.form['mac_address']
        ipv4_address = request.form['ipv4_address']
        ipv6_address = request.form['ipv6_address']

        # Connect to MariaDB
        conn = pymysql.connect(host='10.10.9.43', user='root', password='', db='customer_data')
        cursor = conn.cursor()

        # Insert the device data into the database
        sql = '''INSERT INTO customers (name, mac_address, ipv4_address, ipv6_address) 
                 VALUES (%s, %s, %s, %s)'''
        cursor.execute(sql, (name, mac_address, ipv4_address, ipv6_address))
        conn.commit()

        cursor.close()
        conn.close()

        flash('Device added successfully!')
        return redirect('/devices.html')

    return render_template('addDevice.html')

@app.route('/devices.html', methods=['GET', 'POST'])
def devices():
    conn = pymysql.connect(host='10.10.9.43', user='root', password='', db='customer_data')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    query = request.form.get('query') if request.method == 'POST' else None
    
    if query:
        # Query is searching from database based on name, mac address, ipv4 or ipv6 address
        # It is NOT case sensitive
        # Used Parameterized quieries to protect from SQL injections
        cursor.execute('''SELECT * FROM customers 
                       WHERE name LIKE %s or mac_address LIKE %s or ipv4_address LIKE %s or ipv6_address LIKE %s;''', 
                       ('%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%'))
    else:
        cursor.execute('SELECT * FROM customers;')

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('devices.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
