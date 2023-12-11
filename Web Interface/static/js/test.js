const express = require('express');
const mysql = require('mysql');

const app = express();

// Use EJS as the templating engine
app.set('view engine', 'ejs');

// Create a connection to the MariaDB
const db = mysql.createConnection({
    host: '10.10.9.43',
    user: 'your_username',
    password: 'your_password',
    database: 'your_database'
});

db.connect((err) => {
    if (err) throw err;
    console.log('Connected to the database.');
});

app.get('/', (req, res) => {
    let sql = 'SELECT * FROM your_table';
    db.query(sql, (err, results) => {
        if (err) throw err;
        res.render('index', { data: results });
    });
});

app.listen(3000, () => {
    console.log('Server started on http://localhost:3000');
});
