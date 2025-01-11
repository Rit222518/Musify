let mysql = require("mysql");

let connectToDatabase = async () => {
  let connection = mysql.createConnection({
    host: "localhost",
    user: "root",
    password: "password",
    database: "Musify",
  });
  connection.connect((err) => {
    if (err) return err.message;
    console.log("Connected to the MySQL server.");
  });
  return connection;
};

module.exports = connectToDatabase;