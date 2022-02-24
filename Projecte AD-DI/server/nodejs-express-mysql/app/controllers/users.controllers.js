const User = require("../models/users.model.js");
// Create and Save a new User
exports.register = (req, res) => {
    // Validate request
    if (!req.body) {
      res.status(400).send({
        message: "Content can not be empty!"
      });
    }
    // Create a User
    const user = new User({
        dni: req.body.dni,
        username: req.body.username,
        password: req.body.password,
        full_name: req.body.full_name
    });
    // Save User in the database
    User.register(user, (err, data) => {
      if (err)
        res.status(500).send({
          message:
            err.message || "Some error occurred while creating the User."
        });
      else res.send(data);
    });
  };
  exports.login = (req, res) => {
    // Validate request
    if (!req.body) {
      res.status(400).send({
        message: "Content can not be empty!"
      });
    }
    // Create a User
    const user = new User({
        dni: req.body.dni,
        username: req.body.username,
        password: req.body.password,
        full_name: req.body.full_name
    });
    // Save User in the database
    User.login(user, (err, data) => {
      if (err)
        res.status(500).send({
          message:
            err.message || "Some error occurred while creating the User."
        });
      else res.send(data);
    });
  };