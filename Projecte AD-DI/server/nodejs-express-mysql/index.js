const express = require("express");
const cors = require("cors");
const app = express();

/*var corsOptions = {
  origin: "http://localhost:8081"
};
app.use(cors(corsOptions));*/

// parse requests of content-type - application/json
app.use(express.json());

// parse requests of content-type - application/x-www-form-urlencoded
app.use(express.urlencoded({ extended: true }));

// simple route
app.get("/", (req, res) => {
  res.json({ message: "Benvingut a QualificacionsApp" });
});

require("./app/routes/notes.routes.js")(app);
require("./app/routes/users.routes.js")(app);
// set port, listen for requests

const fs = require('fs');
const https = require('https');

const PORT = 5555;

https.createServer({
  key: fs.readFileSync('my_cert.key'),
  cert: fs.readFileSync('my_cert.crt')
}, app).listen(PORT, function(){
  console.log("Servidor HTTPS escoltant al port " + PORT + "...");
});

/* app.get('/hola', function(req, res){
  console.log('Hola, em note molt segur.');
}); */

/* const PORT = process.env.PORT || 8080;
app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}.`);
}); */
