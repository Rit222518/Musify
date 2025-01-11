const express = require("express");
const app = express();
const path = require("path");
const connectToDatabase = require("./db");
const d = require("./data.json");

app.set("view engine", "ejs");
app.set("views", path.join(__dirname, "views"));
app.use(express.static(path.join(__dirname, 'public')));

app.use((req, res, next) => {
  if (req.originalUrl === '/favicon.ico' || req.originalUrl === `your-audio-file.mp3`) {
    res.status(204).end();
  } else {
    next();
  }
});

app.get("/", async (req, res) => {
  const connection = await connectToDatabase();
  connection.query("SELECT * FROM Songs", (err, result) => {
    res.render("index", { data: result, recommendations: Object.values(d) });
  });
});

app.get('/song/:id', (req, res) => {
  const id = req.params.id;
  const filePath = path.join(__dirname, `songs/${id}.mp3`);
  res.sendFile(filePath, (err) => {
      if (err) {
          console.error('Error sending file:', err);
          res.status(500).send('Error sending file');
      }
  });
});


app.listen(process.env.port || 3000);

console.log("Running at Port 3000");
