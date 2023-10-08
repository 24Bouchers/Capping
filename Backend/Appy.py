#python -m pip install flask
#pip3 install mariadb
#pip install mysql-connector-python
from flask import Flask
import mariadb
import sys

app = Flask(__name__)
try:
    conn = mariadb.connect(
            host='Localhost',
            port= 3306,
            user='root',
            password='ArchFiber23',
            
    )
except mariadb.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)
cur = conn.cursor()
cur.execute("DROP DATABASE ArchFiber")
cur.execute("CREATE DATABASE ArchFiber")
cur.execute("USE ArchFiber")
#Create Tables 

#User Table
cur.execute("CREATE TABLE RADCHECK (Username CHAR(17) PRIMARY KEY)")
#Group Table
cur.execute("CREATE TABLE RADREPLYGROUP (Attribute VARCHAR(7) PRIMARY KEY)")
#User + Group
cur.execute("CREATE TABLE RADIUSUSERGROUP (Username CHAR(17), Attribute VARCHAR(7), FOREIGN KEY (Username) REFERENCES RADCHECK(Username), FOREIGN KEY (Attribute) REFERENCES RADREPLYGROUP(Attribute))")
#Used Text data type for Tags (Subject to change depending on how long tags might be or if we want to limit it)
cur.execute("CREATE TABLE RADREPLY ( Username CHAR(17) , IPv4 VARCHAR(15), IPv6 VARCHAR(39), Tags TEXT, FOREIGN KEY (Username) REFERENCES RADCHECK(Username))")

#Inserting the two Groups Into RADREPLYGROUPS (Default = Dynamic IP)
cur.execute("INSERT INTO RADREPLYGROUP(Attribute) VALUES ('Default')")
cur.execute("INSERT INTO RADREPLYGROUP(Attribute) VALUES ('Static')")

#Add IP Address
def ADD(MAC, IPv4, IPv6, Group, Tags):
    cur.execute("INSERT INTO RADCHECK(Username) VALUES ('"+ MAC + "')")
    cur.execute("INSERT INTO RADIUSUSERGROUP(Username, Attribute ) VALUES ('" + MAC + "', '" + Group + "')")
    cur.execute("INSERT INTO RADREPLY(Username, IPv4, IPv6, Tags ) VALUES ('" + MAC + "', '" + IPv4 + "' , '" + IPv6 + "' , '" + Tags + "')")
#Delete User
def DELETE(MAC):
        cur.execute("DELETE FROM RADCHECK WHERE Username=" + MAC + ";")
        cur.execute("DELETE FROM RADIUSUSERGROUP WHERE Username=" + MAC + ";")
        cur.execute("DELETE FROM RADREPLY WHERE Username=" + MAC + ";")
#Edit


ADD("E4-CB-9E-F2-8A-B3","226.157.169.197", "::ffff:e29d:a9c5", "Static", "Up") #1
ADD("D4-DD-66-FA-AC-D0","176.70.83.195", "::ffff:b046:53c3", "Static", "WIP") #2
ADD("ED-A1-6D-DF-53-FC", "78.85.7.67", "::ffff:4e55:743", "Default", "") #3
ADD("90-CC-66-F7-AD-C7", "230.42.103.155", "::ffff:e62a:679b", "Static", "") #4"
ADD("4E-BB-99-8B-80-9A", "38.85.172.17", "::ffff:2655:ac11", "Default", "WIP") #5
ADD("EB-A9-C8-AE-4B-A4", "112.35.95.27", "::ffff:7023:5f1b", "Default", "Up") #6
ADD("E0-A6-E6-63-E7-C5", "85.2.105.239", "::ffff:5502:69ef", "Static", "" ) #7
ADD("FD-CF-D2-DD-BE-10", "62.105.227.15", "::ffff:3e69:e30f", "Static", "Down") #8
ADD("FD-5A-DD-13-F7-30", "80.60.112.68", "::ffff:503c:7044", "Static", "WIP") #9
ADD("DB-BB-9F-28-F3-9E", "198.136.19.231", "::ffff:c688:13e7", "Default", "") #10


@app.route("/index")
def index():
    return "Connected to database"
if __name__ == "__main__":
    app.run()
    

   