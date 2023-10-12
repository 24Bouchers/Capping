import subprocess
from flask import Flask, app, flash, redirect, render_template, request
import pymysql

app = Flask(__name__)
app.secret_key = 'ArchFiber23'

@app.route('/')
@app.route('/index.html')
def main():
    return render_template('index.html')

def ping_ipv4():
    # Retrieve IP addresses from MariaDB
    conn = pymysql.connect(host='localhost', user='root', password='ArchFiber23', db='customer_data')
    cursor = conn.cursor()
    cursor.execute('SELECT ipv4_address FROM radacct;')
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
        name = request.form['radaact']
        mac_address = request.form['mac_address']
        ipv4_address = request.form['ipv4_address']
        ipv6_address = request.form['ipv6_address']

        # Connect to MariaDB
        conn = pymysql.connect(host='localhost', user='root', password='ArchFiber23', db='customer_data')
        cursor = conn.cursor()

        # Insert the device data into the database
        sql = '''INSERT INTO radaact (name, mac_address, ipv4_address, ipv6_address) 
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
    conn = pymysql.connect(host='localhost', user='root', password='ArchFiber23', db='customer_data')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    query = request.form.get('query') if request.method == 'POST' else None
    
    if query:
        # Query is searching from database based on name, mac address, ipv4 or ipv6 address
        # It is NOT case sensitive
        # Used Parameterized quieries to protect from SQL injections
        cursor.execute('''SELECT * FROM radaact 
                       WHERE name LIKE %s or mac_address LIKE %s or ipv4_address LIKE %s or ipv6_address LIKE %s;''', 
                       ('%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%'))
    else:
        cursor.execute('SELECT * FROM radaact;')

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('devices.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
