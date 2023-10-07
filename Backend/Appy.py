#python -m pip install flask
#pip3 install mariadb
#pip install mysql-connector-python
from flask import Flask
import mariadb
app = Flask(__name__)
conn = mariadb.connect(
         host='Localhost',
         port= 3306,
         user='root',
         password='ArchFiber23',
         
)
cur = conn.cursor()
cur.execute("DROP DATABASE ArchFiber")
cur.execute("CREATE DATABASE ArchFiber")
cur.execute("USE ArchFiber")
#Create Tables 

cur.execute("CREATE TABLE RADCHECK (Username CHAR(12) PRIMARY KEY)")
cur.execute("CREATE TABLE RADREPLYGROUP (Attribute VARCHAR(7) PRIMARY KEY)")
cur.execute("CREATE TABLE RADIUSUSERGROUP (Username CHAR(12), Attribute VARCHAR(7), FOREIGN KEY (Username) REFERENCES RADCHECK(Username), FOREIGN KEY (Attribute) REFERENCES RADREPLYGROUP(Attribute))")
#Used Text data type for Tags (Subject to change depending on how long tags might be or if we want to limit it)
cur.execute("CREATE TABLE RADREPLY ( Username CHAR(12) , IPv4 VARCHAR(15), IPv6 VARCHAR(39), Tags TEXT, FOREIGN KEY (Username) REFERENCES RADCHECK(Username))")

#Inserting the two Groups Into RADREPLYGROUPS (Default = Dynamic IP)
cur.execute("INSERT INTO RADREPLYGROUP(Attribute) VALUES ('Default')")
cur.execute("INSERT INTO RADREPLYGROUP(Attribute) VALUES ('Static')")



print(cur.execute("SELECT * FROM RADCHECK"))

@app.route("/index")
def index():
    return "Connected to database"
if __name__ == "__main__":
    app.run()
    

   