#python -m pip install flask
#pip3 install mariadb
#pip install mysql-connector-python
from flask import Flask
import mariadb
app = Flask(__name__)
conn = mariadb.connect(
         host='10.10.9.43',
         port= 80,
         user='r00t',
         password='ArchFiber23',
         database='ArchFiber')
cur = conn.cursor()
@app.route("/index")
def index():
    return "Connected to database"
if __name__ == "__main__":
    app.run()