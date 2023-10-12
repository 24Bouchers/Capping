<<<<<<< HEAD
<<<<<<< HEAD
from flask import Flask, app, flash, redirect, render_template, request
import mariadb

app = Flask(__name__)
app.secret_key = 'ArchFiber23'


@app.route('/')
def main():
    return render_template('index.html')


@app.route('/index.html')
def index():
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
        conn = mariadb.connect(
            host='10.10.9.43', user='root', password='', db='customer_data')
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
    conn = mariadb.connect(host='10.10.9.43', user='root',
                           password='', db='customer_data')
    cursor = conn.cursor(mariadb.cursors.DictCursor)

    query = request.form.get('query') if request.method == 'POST' else None

=======
from flask import Flask, app, render_template, request
import mariadb
=======
import subprocess
from flask import Flask, app, flash, redirect, render_template, request
import pymysql
>>>>>>> f1f21b6 (Reload from Liam branch appy is now TableInit.py)

app = Flask(__name__)
app.secret_key = 'ArchFiber23'

@app.route('/')
@app.route('/index.html')
def main():
    return render_template('index.html')

def ping_ipv4():
    # Retrieve IP addresses from MariaDB
    conn = pymysql.connect(host='10.10.9.43', user='root', password='', db='customer_data')
    cursor = conn.cursor()
    cursor.execute('SELECT ipv4_address FROM customers;')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    
    # Ping IP addresses and count successes/failures
    successful_pings = 0
    failed_pings = 0
    
    for row in rows:
        ip = row[0]
        response = subprocess.run(['ping', '-c', '1', ip], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        
        if response.returncode == 0:
            successful_pings += 1
        else:
            failed_pings += 1
    
    # 3. Display results
    return render_template('index.html', successful_pings=successful_pings, failed_pings=failed_pings)

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
    
>>>>>>> 4aedf9e (Steve b (#5))
    if query:
        # Query is searching from database based on name, mac address, ipv4 or ipv6 address
        # It is NOT case sensitive
        # Used Parameterized quieries to protect from SQL injections
<<<<<<< HEAD
<<<<<<< HEAD
        cursor.execute('''SELECT * FROM customers 
                       WHERE name LIKE %s or mac_address LIKE %s or ipv4_address LIKE %s or ipv6_address LIKE %s;''',
=======
        cursor.execute('''SELECT * FROM Data 
=======
        cursor.execute('''SELECT * FROM customers 
>>>>>>> f1f21b6 (Reload from Liam branch appy is now TableInit.py)
                       WHERE name LIKE %s or mac_address LIKE %s or ipv4_address LIKE %s or ipv6_address LIKE %s;''', 
>>>>>>> 4aedf9e (Steve b (#5))
                       ('%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%'))
    else:
        cursor.execute('SELECT * FROM customers;')

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

<<<<<<< HEAD
<<<<<<< HEAD
    return render_template('devices.html', rows=rows)

=======
    return render_template('table_display.html', rows=rows)
>>>>>>> 4aedf9e (Steve b (#5))
=======
    return render_template('devices.html', rows=rows)
>>>>>>> f1f21b6 (Reload from Liam branch appy is now TableInit.py)

if __name__ == '__main__':
    app.run(debug=True)
