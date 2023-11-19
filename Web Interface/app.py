from flask import Flask, app, flash, redirect, render_template, request
import pymysql
from datetime import datetime, timedelta, date, timezone


app = Flask(__name__)
app.secret_key = 'ArchFiber23'

@app.route('/')
@app.route('/index.html', methods=['GET'])
def main():

    conn = pymysql.connect(host='10.10.9.43', user='root', password='', db='radius_netelastic')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    

    cursor.execute('select acctstarttime from radacct order by acctstarttime DESC;')

    stime = cursor.fetchall()
    cursor.close()
    conn.close()

    todayDate = date.today()

    currentTimeUTC = datetime.now(timezone.utc).strftime("%H:%M")
    currentTimeEST = datetime.now().strftime("%H:%M")
    yesterdayDate = str(todayDate - timedelta(days = 1))
    todayDate = str(todayDate)
    # yesterdayDate = str(yesterdayDate)
    # tempDate = "2023-10-31" # DELETE BEFORE DELIVER!!!!!----------------------------------------------------------------------------------
    # convert current time into minutes
    currentTimeSplit = str(currentTimeUTC).split(':')
    currentTimeEST = str(currentTimeEST).split(':')
    # counts down to the nearest 15 minute interval
    close15MinInterval =int(currentTimeSplit[1])
    minIntervalTimeEST = int(currentTimeEST[1])
    sameTime = True
    while close15MinInterval % 15 != 0:
        close15MinInterval -= 1
        minIntervalTimeEST -= 1 
        sameTime = False
    currentTimeMin = close15MinInterval + (int(currentTimeSplit[0])*60)

    
    # THESE ARE TEST VARIABLES!!
    # DELETE BEFORE PUSH TO FULL PRODUCTION
    # currentTimeMin = 60
    # yesterdayDate = "2023-10-09"
    # TODO delete temp code

    # list that will store the 15 minute interval numbers
    # going to be every 15 min for 6 hours
    intervals = [0] * 24
    hoursInMin = 360 # 360 represents 6 hours
    offset = 0

    # loop through the list of times given from acctstarttime
    for x in stime:
        # convert the acctstarttime into minutes
        splitDateTime = str(x.get('acctstarttime')).split() # separates date and time into 2 separate list elements

        if splitDateTime and splitDateTime[0] != 'None':
            splitTime = str(splitDateTime[1]).split(':')
            totalTimeMin = int(splitTime[1]) + (int(splitTime[0])*60)
            # since the time were comparing against is the closest 15 minute interval that has already passed
            # if a time appears that has todays date and is passed the time were checking from
            # it gets added to the most recent colom of the graph
            if totalTimeMin > currentTimeMin and splitDateTime[0] == todayDate and (totalTimeMin-currentTimeMin) <= 15 :
                intervals[0] += 1 
                offset = 1
            # check if at least 6 hours have passed since start of day 
            elif currentTimeMin >= hoursInMin:
                # makes sure the dates match
                # ------------------------------------------------------------------------
                #  SWITCH todayDate WITH tempDate SO IT FUNCTIONS WITH OUR DATA
                #  DELETE tempDate AND THIS MESSAGE BEFORE DELIVERY OF FINAL APPLICATION
                #-------------------------------------------------------------------------
                if splitDateTime[0] == todayDate:
                    # first finds out how many 15 minute intervals passed
                    diff = int(currentTimeMin/15) - int(totalTimeMin/15)
                    if diff <= len(intervals)-offset and diff > -1:
                        intervals[diff+offset] += 1
            # sees if there was a 6 hour diffrence max between times and thta date matches either today or yesterday
            elif (1440 - totalTimeMin) + currentTimeMin <= hoursInMin and (splitDateTime[0] == todayDate or splitDateTime[0] == yesterdayDate):
                if splitDateTime[0] == yesterdayDate:
                    # 1440 is the amount of minutes in a day
                    diff = int(currentTimeMin/15) + int((1440 - totalTimeMin)/15)
                    if diff <= len(intervals) and diff > -1:
                        intervals[diff+offset] += 1
                else:
                    diff = int(currentTimeMin/15) - int(totalTimeMin/15)
                    if diff <= len(intervals) and diff > -1:
                        intervals[diff+offset] += 1
        
    # the bottom labels of the line graph representing 15 minute increments
    labels = [''] * 25
    hourCount = 0
    startingHour = currentTimeEST[0]
    offset = 0
    for x in range(24):
        # if the current time is not a even 15 minunet interval the it will be added as the first place on the graph display
        # it then addes the the closest 15 minute interval that has passed as the second place in the display  
        if x == 0 and not sameTime:
            if int(currentTimeEST[0]) > 12:
                labels[x] = str(int(currentTimeEST[0])-12) + ':' + currentTimeEST[1] + ' pm'
            else:
                labels[x] = currentTimeEST[0] + ':' + currentTimeEST[1] + ' am'

            if int(currentTimeEST[0]) > 12:
                labels[x+1] = str(int(currentTimeEST[0])-12) + ':' + str(minIntervalTimeEST) + ' pm'
            else:
                labels[x+1] = currentTimeEST[0] + ':' + str(minIntervalTimeEST) + ' am'
            x = 2
            offset = 1
        else:
            # subtracts 15 minutes form previous time
            if int(minIntervalTimeEST) - 15 > 0:
                minIntervalTimeEST -= 15
                if int(currentTimeEST[0]) > 12:
                    labels[x+offset] = str(int(currentTimeEST[0])-12) + ':' + str(minIntervalTimeEST) + ' pm'
                else:
                    labels[x+offset] = currentTimeEST[0] + ':' + str(minIntervalTimeEST) + ' am' 
                
            # adjusts the hour value
            else: 
                if int(currentTimeEST[0]) > 12:
                    labels[x+offset] = str(int(currentTimeEST[0])-12) + ':00 pm'
                else:
                    labels[x+offset] = currentTimeEST[0] + ':00 am'  
                minIntervalTimeEST =60
                hourCount += 1
                currentTimeEST[0] = str(int(startingHour)-hourCount)
                # reset the hours for 12 am and 12 pm
                if currentTimeEST[0] == '0':
                    currentTimeEST[0] = '12'
                if int(currentTimeEST[0])  < 0:
                    currentTimeEST[0] = '23'
    # reverse the lists so they appear from right to left on webpage 
    del labels[-1]
    intervals.reverse()
    labels.reverse()
    return render_template('index.html', labels=labels, values=intervals)


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

@app.route('/editDevice/<callingstationid>')
def show_edit_device_page(callingstationid):
    # Fetch the device data from your database based on the callingstationid
    # Here you would retrieve the device data from the database and pass it to the template
    current_device_data = get_device_data(callingstationid)
    return render_template('editDevice.html', callingstationid=callingstationid, current_device_data=current_device_data)

def get_device_data(callingstationid):
    # Placeholder dictionary to store device data
    device_data = {}

    # Connect to the customer_data database
    try:
        # Establish a connection to the database
        conn = pymysql.connect(host='10.10.9.43', user='root', password='', db='customer_data')
        cursor = conn.cursor(pymysql.cursors.DictCursor)  # Use DictCursor to get data as a dictionary

        # SQL query to fetch the device data based on the callingstationid
        cursor.execute('SELECT username, callingstationid, framedipaddress, framedipv6address FROM radacct WHERE callingstationid = %s', (callingstationid,))
        
        # Fetch one record and store it in the device_data dictionary
        device_data = cursor.fetchone()

    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL Database: {e}")
        # Handle error appropriately, possibly setting device_data to None or a default value
        device_data = None
    finally:
        # Close the cursor and the connection
        cursor.close()
        conn.close()

    return device_data

@app.route('/updateDevice/<path:callingstationid>', methods=['POST'])
def update_device(callingstationid):
    # Get updated data from the form
    username = request.form.get('username')
    framedipaddress = request.form.get('framedipaddress')
    framedipv6address = request.form.get('framedipv6address')

    # Connect to the customer_data database
    try:
        conn = pymysql.connect(host='10.10.9.43', user='root', password='', db='customer_data')
        cursor = conn.cursor()

        # SQL query to update the device entry based on the callingstationid
        sql = '''UPDATE radacct 
                 SET username=%s, framedipaddress=%s, framedipv6address=%s 
                 WHERE callingstationid = %s'''
        cursor.execute(sql, (username, framedipaddress, framedipv6address, callingstationid))
        conn.commit()

        # Check if the update was successful
        if cursor.rowcount > 0:
            flash('Device updated successfully!')
        else:
            flash('No device was updated. Check if the device ID is correct.')

    except pymysql.MySQLError as e:
        print(f"Error while updating device: {e}")
        flash('Failed to update device. Please try again.')
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

    return render_template('/devices.html', rows=rows)

""" logs route draft code
@app.route('/logs.html', methods=['GET', 'POST'])
def logs():
    conn = pymysql.connect(host='10.10.9.43', user='root', password='', db='customer_data')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    query = request.form.get('query') if request.method == 'POST' else None
    
    if query:
        # probaly have to adjust the fields here in the SQL query based on the database schema, kinda just winging it
        cursor.execute('''SELECT LogID, time, callingstationid, reason FROM logs 
                       WHERE time LIKE %s OR callingstationid LIKE %s OR reason LIKE %s''',
                       ('%' + query + '%', '%' + query + '%', '%' + query + '%'))
    else:
        cursor.execute('SELECT LogID, time, callingstationid, reason FROM logs;')

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('logs.html', rows=rows)
"""

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5555)
