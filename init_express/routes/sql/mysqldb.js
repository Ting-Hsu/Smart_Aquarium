console.log("MySQL database conneteced successfully ! ! ")
const mysql = require('mysql2');
// create the connection to database
const connection = mysql.createConnection({  
  host: 'ppppp196.synology.me',
  user: 'aiot082021',
  password:"0bURRTg7O6x5lZ72",
  database: 'aiot082021',
  port:"33306"
});

module.exports = connection