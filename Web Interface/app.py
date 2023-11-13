from flask import Flask, app, flash, redirect, render_template, request
import pymysql
from datetime import datetime, timedelta, date

app = Flask(__name__)
app.secret_key = 'ArchFiber23'

@app.route('/')
@app.route('/index.html', methods=['GET'])
def main():

    conn = pymysql.connect(host='10.10.9.43', user='root', password='', db='customer_data')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    query = request.form.get('query') if request.method == 'POST' else None
    
    if query:
        # Query is searching from database based on name, mac address, ipv4 or ipv6 address
        # It is NOT case sensitive
        # Used Parameterized quieries to protect from SQL injections
        pass
        # cursor.execute('''SELECT * FROM radacct 
        #                WHERE username LIKE %s or callingstationid LIKE %s or framedipaddress LIKE %s or framedipv6address LIKE %s;''', 
        #                ('%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%'))
    else:
        cursor.execute('SELECT acctstarttime FROM radacct;')

    stime = cursor.fetchall()
    cursor.close()
    conn.close()

    todayDate = date.today()
    currentTime = datetime.now().strftime("%H:%M:%S")
    yesterdayDate = todayDate - timedelta(days = 1)
    todayDate = str(todayDate)
    yesterdayDate = str(yesterdayDate)
    tempDate = "2023-11-05" # DELETE BEFORE DELIVER!!!!!----------------------------------------------------------------------------------

    # convert current time into minutes
    currentTimeSplit = str(currentTime).split(':')
    currentTimeMin = int(currentTimeSplit[1]) + (int(currentTimeSplit[0])*60)
    # THIS IS A TEST VARIABLE!!
    # DELETE BEFORE PUSH TO FULL PRODUCTION
    currentTimeMin = 60
    # list that will store the 15 minute interval numbers
    # going to be every 15 min for 6 hours
    intervals = [0] * 24
    # loop through the list of times given from acctstarttime
    for x in stime:
        # convert the acctstarttime into minutes
        splitDateTime = str(x.get('acctstarttime')).split() # separates date and time into 2 separate list elements
        splitTime = str(splitDateTime[1]).split(':')
        totalTimeMin = int(splitTime[1]) + (int(splitTime[0])*60)
        print(totalTimeMin, splitDateTime[0])
        # check if at least 6 hours have passed since start of day 
        if currentTimeMin >= 360:
            # makes sure the dates match
            # ------------------------------------------------------------------------
            #  SWITCH todayDate WITH tempDate SO IT FUNCTIONS WITH OUR DATA
            #  DELETE tempDate AND THIS MESSAGE BEFORE DELIVERY OF FINAL APPLICATION
            #-------------------------------------------------------------------------
            if splitDateTime[0] == tempDate:
                    # first finds out how many 15 minute intervals passed
                    diff = int(currentTimeMin/15) - int(totalTimeMin/15)
                    if diff <= len(intervals) and diff > -1:
                        intervals[diff] += 1
        
        # sees if there was a 6 hour diffrence max between times and thta date matches either today or yesterday
        elif (1440 - totalTimeMin) + currentTimeMin <= 360 and (splitDateTime[0] == todayDate or splitDateTime[0] == yesterdayDate):
            if splitDateTime[0] == yesterdayDate:
                diff = int(currentTimeMin/15) + int((1440 - totalTimeMin)/15)
                if diff <= len(intervals) and diff > -1:
                            intervals[diff] += 1
            else:
                diff = int(currentTimeMin/15) - int(totalTimeMin/15)
                if diff <= len(intervals) and diff > -1:
                            intervals[diff] += 1


    # the bottom labels of the line graph representing 15 minute increments
    labels = [
        "now - 15 min", "15 - 30 min", "30 - 45 min", "45 min - 1 hour ",
        "1 hour - 1:15 min", "15 - 30 min", "30 - 45 min", "45 - 2 hours",
        "2 hours - 15 min", "15 - 30 min"  ,"30 - 45 min", "45 min - 3 hours",
        "3 hours - 15 min", "15 - 30 min", "30 - 45 min", "45 min - 4 hours",
        "4 hours - 15 min", "15 - 30 min", "30 - 45 min", "45 min - 5 hours",
        "5 hours - 15 min", "15 - 30 min", "30 - 45 min", "45 min - 6 hours"
    ]
    
    return render_template('index.html', labels=labels, values=intervals)
    # the bottom labels of the line graph
    labels = [
        "2000",
        "2001",
        "2002",
        "2003",
        "2004",
        "2005",
        "2006",
        "2007",    
    ]
    # the value that each data point represents
    values = [100,200,300,400,502,557,604,700]

    return render_template('index.html', labels=labels, values=values)


@app.route('/addDevice.html', methods=['GET', 'POST'])
def addDevice():
    if request.method == 'POST':
      
        # Get data from the form with default values
        name = request.form.get('username', default=None)
        mac_address = request.form.get('callingstationid', default=None)
        ipv4_address = request.form.get('framedipaddress', default=None)
        ipv6_address = request.form.get('framedipv6address', default=None)

        # Connect to MariaDB
        conn = pymysql.connect(host='10.10.9.43', user='root', password='', db='customer_data')
        cursor = conn.cursor()

        # Insert the device data into the database
 
        sql = '''INSERT INTO radacct (username, callingstationid, framedipaddress, framedipv6address) 
                 VALUES (%s, %s, %s, %s)'''
        cursor.execute(sql, (name, mac_address, ipv4_address, ipv6_address))
        conn.commit()

        cursor.close()
        conn.close()

        flash('Device added successfully!')
        return redirect('/devices.html')

    return render_template('addDevice.html')

@app.route("/removeDevice", methods=["POST"])
def remove_device():
    mac = request.form.get("mac")
    
    # Connect to the customer_data database
    conn = pymysql.connect(host='10.10.9.43', user='root', password='', db='customer_data')
    cursor = conn.cursor()
    
    # SQL query to delete the device entry based on the MAC address
    query = "DELETE FROM radacct WHERE callingstationid = %s"  # Assuming 'callingstationid' stores the MAC addresses
    try:
        cursor.execute(query, (mac,))
        conn.commit()
    except Exception as e:
        print(f"Error while removing device: {e}")
    finally:
        cursor.close()
        conn.close()

    return redirect('/devices.html')

@app.route('/devices.html', methods=['GET', 'POST'])
def devices():
    conn = pymysql.connect(host='10.10.9.43', user='root', password='', db='customer_data')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    query = request.form.get('query') if request.method == 'POST' else None
    
    if query:
        # Query is searching from database based on name, mac address, ipv4 or ipv6 address
        # It is NOT case sensitive
        # Used Parameterized quieries to protect from SQL injections
        cursor.execute('''SELECT * FROM radacct 
                       WHERE username LIKE %s or callingstationid LIKE %s or framedipaddress LIKE %s or framedipv6address LIKE %s;''', 
                       ('%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%'))
    else:
        cursor.execute('SELECT username, callingstationid, framedipaddress, framedipv6address FROM radacct;')

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('devices.html', rows=rows)

""" logs route draft code
@app.route('/logs.html', methods=['GET', 'POST'])
def logs():
    conn = pymysql.connect(host='10.10.9.43', user='root', password='', db='customer_data')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    query = request.form.get('query') if request.method == 'POST' else None
    
    if query:
        # probaly have to adjust the fields here in the SQL query based on the database schema, kinda just winging it
        cursor.execute('''SELECT logId, time, username, reason FROM logs 
                       WHERE time LIKE %s OR username LIKE %s OR reason LIKE %s''',
                       ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
    else:
        cursor.execute('SELECT LogID, time, username, reason FROM logs;')

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('logs.html', rows=rows)
"""

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
