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
    
    #########################
    # DEVICES REQUEST GRAPH #
    #########################

    cursor.execute('select acctstarttime from radacct order by acctstarttime DESC;')

    stime = cursor.fetchall()
    cursor.close()
    conn.close()

    todayDate = date.today()

    currentTimeUTC = datetime.now(timezone.utc).strftime("%H:%M")
    currentTimeEST = datetime.now().strftime("%H:%M")
    yesterdayDate = todayDate - timedelta(days = 1)
    todayDate = str(todayDate)
    yesterdayDate = str(yesterdayDate)
    tempDate = "2023-10-10" # DELETE BEFORE DELIVER!!!!!----------------------------------------------------------------------------------
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
    yesterdayDate = "2023-10-09"
    # TODO delete temp code

    # list that will store the 15 minute interval numbers
    # going to be every 15 min for 6 hours
    intervals = [0] * 24
    hoursInMin = 360 # 360 represents 6 hours
    # loop through the list of times given from acctstarttime
    for x in stime:
        # convert the acctstarttime into minutes
        splitDateTime = str(x.get('acctstarttime')).split() # separates date and time into 2 separate list elements

        if splitDateTime and splitDateTime[0] != 'None':
            splitTime = str(splitDateTime[1]).split(':')
            totalTimeMin = int(splitTime[1]) + (int(splitTime[0])*60)
            # print(totalTimeMin, splitDateTime[0])
            # since the time were comparing against is the closest 15 minute interval that has already passed
            # if a time appears that has todays date and is passed the time were checking from
            # it gets added to the most recent colom of the graph
            if totalTimeMin > currentTimeMin and splitDateTime[0] == tempDate:
                intervals[0] += 1 
            # check if at least 6 hours have passed since start of day 
            elif currentTimeMin >= hoursInMin:
                # makes sure the dates match
                # ------------------------------------------------------------------------
                #  SWITCH todayDate WITH tempDate SO IT FUNCTIONS WITH OUR DATA
                #  DELETE tempDate AND THIS MESSAGE BEFORE DELIVERY OF FINAL APPLICATION
                #-------------------------------------------------------------------------
                if splitDateTime[0] == tempDate:
                    # first finds out how many 15 minute intervals passed
                    diff = int(currentTimeMin/15) - int(totalTimeMin/15)
                    if diff <= len(intervals)-1 and diff > -1:
                        intervals[diff+1] += 1
            # sees if there was a 6 hour diffrence max between times and thta date matches either today or yesterday
            elif (1440 - totalTimeMin) + currentTimeMin <= hoursInMin and (splitDateTime[0] == todayDate or splitDateTime[0] == yesterdayDate):
                if splitDateTime[0] == yesterdayDate:
                    # 1440 is the amount of minutes in a day
                    diff = int(currentTimeMin/15) + int((1440 - totalTimeMin)/15)

                    if diff <= len(intervals) and diff > -1:
                        intervals[diff+1] += 1
                else:
                    diff = int(currentTimeMin/15) - int(totalTimeMin/15)
                    if diff <= len(intervals) and diff > -1:
                        intervals[diff+1] += 1
        
    # the bottom labels of the line graph representing 15 minute increments
    labels = [''] * 24
    hourCount = 0
    startingHour = currentTimeEST[0]
    for x in range(24):
        if x == 0 and not sameTime:
            if int(currentTimeEST[0]) > 12:
                labels[x] = str(int(currentTimeEST[0])-12) + ':' + currentTimeEST[1] + ' pm'
            else:
                labels[x] = currentTimeEST[0] + ':' + currentTimeEST[1] + ' am'
        else:
            # subtracts 15 minutes form previous time
            if int(minIntervalTimeEST) - 15 > 0:
                minIntervalTimeEST -= 15
                if int(currentTimeEST[0]) > 12:
                    labels[x] = str(int(currentTimeEST[0])-12) + ':' + str(minIntervalTimeEST) + ' pm'
                else:
                    labels[x] = currentTimeEST[0] + ':' + str(minIntervalTimeEST) + ' am' 
            # adjusts the hour value
            else: 
                if int(currentTimeEST[0]) > 12:
                    labels[x] = str(int(currentTimeEST[0])-12) + ':00 pm'
                else:
                    labels[x] = currentTimeEST[0] + ':00 am'  
                minIntervalTimeEST =60
                hourCount += 1
                currentTimeEST[0] = str(int(startingHour)-hourCount)
                if currentTimeEST[0] == '0':
                    currentTimeEST[0] = '12'
                if int(currentTimeEST[0])  < 0:
                    currentTimeEST[0] = '23'

    intervals.reverse()
    labels.reverse()
    return render_template('index.html', labels=labels, values=intervals)

################
# ALTER TABLES #
################

#Add Device
@app.route('/addDevice.html', methods=['GET', 'POST'])
def addDevice():
    if request.method == 'POST':
      
        # Get data from the form with default values
        p_username = request.form.get('MAC', default=None)
        p_ipv4 = request.form.get('IPv4', default=None)
        p_ipv6Prefix = request.form.get('IPv6 Prefix', default=None)
        p_ipv6 = request.form.get('IPv6', default=None)

        # Connect to MariaDB
        conn = pymysql.connect(host='10.10.9.43', user='root', password='', db='radius_netelastic')
        cursor = conn.cursor()

        # Insert the device data into the databases
        cursor.callproc('radius_netelastic.PROC_InsUpRadiusUser', (p_username, p_ipv4, p_ipv6Prefix, p_ipv6))
        cursor.execute('INSERT INTO radius_netelastic.logs(username, reason, time) VALUES (%s, %s, NOW())', (p_username, 'Added'))
        conn.commit()

        cursor.close()
        conn.close()

        flash('Device added successfully!')
        return redirect('/devices.html')

    return render_template('addDevice.html')

#Remove device
@app.route("/removeDevice", methods=["POST"])
def remove_device():
    p_username = request.form.get('username')
    
    # Connect to the radius_netelastic database
    conn = pymysql.connect(host='10.10.9.43', user='root', password='', db='radius_netelastic')
    cursor = conn.cursor()
    
    # SQL query to delete the device entry based on the MAC address
    try:
        cursor.callproc('radius_netelastic.PROC_DeleteRadiusUser', (p_username,))
        cursor.execute('INSERT INTO radius_netelastic.logs(username, reason, time) VALUES (%s, %s, NOW())', (p_username, 'Removed'))

        conn.commit()
    except Exception as e:
        print(f"Error while removing device: {e}")
    finally:
        cursor.close()
        conn.close()

    return redirect('/devices.html')

# Get the device information to edit
def get_device_data(username):
    # Placeholder dictionary to store device data
    device_data = {}

    # Connect to the radius_netelastic database
    try:
        # Establish a connection to the database
        conn = pymysql.connect(host='10.10.9.43', user='root', password='', db='radius_netelastic')
        cursor = conn.cursor(pymysql.cursors.DictCursor)  # Use DictCursor to get data as a dictionary

        # SQL query to fetch the device data based on the provided username
        sql = '''SELECT 
                    username, 
                    MAX(CASE WHEN attribute = 'Framed-IP-Address' THEN value END) AS 'Framed-IP-Address',
                    MAX(CASE WHEN attribute = 'Framed-IPv6-Prefix' THEN value END) AS 'Framed-IPv6-Prefix',
                    MAX(CASE WHEN attribute = 'Framed-IPv6-Address' THEN value END) AS 'Framed-IPv6-Address'
                FROM radreply
                WHERE username = %s
                GROUP BY username;'''

        cursor.execute(sql, (username,))

        # Fetch one record and store it in the device_data dictionary
        device_data = cursor.fetchone()

    except pymysql.MySQLError as e:
        print(f"Error connecting to MySQL Database: {e}")
        # Handle error appropriately, possibly setting device_data to None or a default value
        device_data = None
    finally:
        # Close the cursor and the connection
        if cursor:
            cursor.close()
        if conn:
            conn.close()

    return device_data

#Get The details For edit Page
@app.route('/editDevice/<username>')
def show_edit_device_page(username):
    # Fetch the device data from your database based on the callingstationid
    # Here you would retrieve the device data from the database and pass it to the template
    current_device_data = get_device_data(username)
    return render_template('editDevice.html', username=username, current_device_data=current_device_data)

#Update The Devices Page
@app.route('/updateDevice/<path:username>', methods=['POST'])
def update_device(username):
    # Get updated data from the form
    p_ipv4 = request.form.get('IPv4')
    p_ipv6Prefix = request.form.get('IPv6 Prefix')
    p_ipv6 = request.form.get('IPv6')

    # Connect to the radius_netelastic database
    try:
        conn = pymysql.connect(host='10.10.9.43', user='root', password='', db='radius_netelastic')
        cursor = conn.cursor()

        cursor.callproc('radius_netelastic.PROC_InsUpRadiusUser', (username, p_ipv4, p_ipv6Prefix, p_ipv6))
        cursor.execute('INSERT INTO radius_netelastic.logs(username, reason, time) VALUES (%s, %s, NOW())', (username, 'Edited'))
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

##################
# DISPLAY TABLES #
##################

#Display Devices
@app.route('/devices.html', methods=['GET', 'POST'])
def devices():
    conn = pymysql.connect(host='10.10.9.43', user='root', password='', db='radius_netelastic')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    query = request.form.get('query') if request.method == 'POST' else None
    
    if query:
        # Query is searching from database based on name, mac address, ipv4 or ipv6 address
        # It is NOT case sensitive
        # Used Parameterized quieries to protect from SQL injections
        cursor.execute('''SELECT username, 
                                MAX(CASE WHEN attribute = 'Framed-IP-Address' THEN value END) AS 'Framed-IP-Address',
                                MAX(CASE WHEN attribute = 'Framed-IPv6-Prefix' THEN value END) AS 'Framed-IPv6-Prefix',
                                MAX(CASE WHEN attribute = 'Framed-IPv6-Address' THEN value END) AS 'Framed-IPv6-Address'
                        FROM radreply 
                        WHERE username LIKE %s 
                            OR (MAX(CASE WHEN attribute = 'Framed-IP-Address' THEN value END) LIKE %s) 
                            OR (MAX(CASE WHEN attribute = 'Framed-IPv6-Prefix' THEN value END) LIKE %s) 
                            OR (MAX(CASE WHEN attribute = 'Framed-IPv6-Address' THEN value END) LIKE %s)
                        GROUP BY username;''', 
                    ('%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%'))

    else:
        cursor.execute('''SELECT
            username,
            MAX(CASE WHEN `attribute` = 'Framed-IP-Address' THEN value END) AS 'Framed-IP-Address',
            MAX(CASE WHEN `attribute` = 'Framed-IPv6-Prefix' THEN value END) AS 'Framed-IPv6-Prefix',
            MAX(CASE WHEN `attribute` = 'Framed-IPv6-Address' THEN value END) AS 'Framed-IPv6-Address'
            FROM radreply
            WHERE `attribute` IN ('Framed-IP-Address', 'Framed-IPv6-Prefix', 'Framed-IPv6-Address')
            GROUP BY username;
        ''')
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('/devices.html', rows=rows)

#Display Logs 
@app.route('/logs.html', methods=['GET', 'POST'])
def logs():
    conn = pymysql.connect(host='10.10.9.43', user='root', password='', db='radius_netelastic')
    cursor = conn.cursor(pymysql.cursors.DictCursor)
    
    query = request.form.get('query') if request.method == 'POST' else None
    
    if query:
        # probaly have to adjust the fields here in the SQL query based on the database schema, kinda just winging it
        cursor.execute('''SELECT logId, time, username, reason FROM logs 
                   WHERE time LIKE %s OR username LIKE %s OR reason LIKE %s''',
                   ('%' + query + '%', '%' + query + '%', '%' + query + '%'))

    else:
        cursor.execute('SELECT logID, time, username, reason FROM logs ORDER BY time DESC;')

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('logs.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5555)
