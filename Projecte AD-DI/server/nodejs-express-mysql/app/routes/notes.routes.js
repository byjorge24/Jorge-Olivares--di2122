module.exports = app => {
    const notes = require("../controllers/notes.controllers.js");
    const A = require("../config/autenticacion.js");
    var router = require("express").Router();
    // Create a new Notes
    // router.post("/", notes.create);
    // Retrieve all Notes
    router.get("/", A.authenticateJWT, notes.findAll);
    // Retrieve all published Notes
    // router.get("/published", Notes.findAllPublished);
    // Retrieve a single Notes with id
    // router.get("/:id", Notes.findOne);
    // Update a Notes with id
    // router.put("/:id", Notes.update);
    // Delete a Notes with id
    // router.delete("/:id", Notes.delete);
    // Delete all Notes
    // router.delete("/", Notes.deleteAll);
    
    
    
    app.use('/notes', router);
  };