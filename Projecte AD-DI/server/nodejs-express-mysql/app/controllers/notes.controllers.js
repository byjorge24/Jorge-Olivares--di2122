const Notes = require("../models/notes.model.js");

// Retrieve all Notes from the database (with condition).
exports.findAll = (req, res) => {
  if (req.user.role!='alumne'){
    res.status(400).send("Solo pueden consultar alumnos");
  }
  Notes.getAll(title, (err, data) => {
    if(err)
      res.status(500).send({
        "ok":false,
        "error":err
      });
    else{
    // retornar les dades al client
      res.status(200).send(
        {
        "ok":true,
        "data":data
        }
      )
    }
  });
};