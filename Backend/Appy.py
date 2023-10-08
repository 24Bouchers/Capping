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
            port= 3307,
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
cur.execute("CREATE TABLE RADCHECK (Username CHAR(12) PRIMARY KEY)")
#Group Table
cur.execute("CREATE TABLE RADREPLYGROUP (Attribute VARCHAR(7) PRIMARY KEY)")
#User + Group
cur.execute("CREATE TABLE RADIUSUSERGROUP (Username CHAR(12), Attribute VARCHAR(7), FOREIGN KEY (Username) REFERENCES RADCHECK(Username), FOREIGN KEY (Attribute) REFERENCES RADREPLYGROUP(Attribute))")
#Used Text data type for Tags (Subject to change depending on how long tags might be or if we want to limit it)
cur.execute("CREATE TABLE RADREPLY ( Username CHAR(12) , IPv4 VARCHAR(15), IPv6 VARCHAR(39), Tags TEXT, FOREIGN KEY (Username) REFERENCES RADCHECK(Username))")

#Inserting the two Groups Into RADREPLYGROUPS (Default = Dynamic IP)
cur.execute("INSERT INTO RADREPLYGROUP(Attribute) VALUES (Default)")
cur.execute("INSERT INTO RADREPLYGROUP(Attribute) VALUES (Static)")

def ADD(MAC, IPv4, IPv6, Group, Tags):
    cur.execute("INSERT INTO RADCHECK(Username) VALUES ("+ MAC + ")")
    cur.execute("INSERT INTO RADREPLYGROUP(Attribute) VALUES ("+ Group + ")")
    cur.execute("INSERT INTO RADIUSUSERGROUP(Username, Attribute ) VALUES (" + MAC + " , " + Group + ")")
    cur.execute("INSERT INTO RADREPLY(Username, IPv4, IPv6, Tags ) VALUES (" + MAC + ", " + IPv4 + " , " + IPv6 + " , " + Tags + ")")






@app.route("/index")
def index():
    return "Connected to database"
if __name__ == "__main__":
    app.run()
    

   