from flask import Flask, app, render_template, request
import mariadb

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def display_data():
    conn = mariadb.connect(host='10.10.9.43', user='root', password='', db='ArchFiber')
    cursor = conn.cursor(dictionary = True)
    
    query = request.form.get('query') if request.method == 'POST' else None
    
    if query:
        # Query is searching from database based on name, mac address, ipv4 or ipv6 address
        # It is NOT case sensitive
        # Used Parameterized quieries to protect from SQL injections
        cursor.execute('''SELECT * FROM Data 
                       WHERE name LIKE %s or mac_address LIKE %s or ipv4_address LIKE %s or ipv6_address LIKE %s;''', 
                       ('%' + query + '%', '%' + query + '%', '%' + query + '%', '%' + query + '%'))
    else:
        cursor.execute('SELECT * FROM customers;')

    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    return render_template('table_display.html', rows=rows)

if __name__ == '__main__':
    app.run(debug=True)
