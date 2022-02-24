const sql = require("./db.js");

// constructor
const Notes = function(n) {
    this.id_alumne = n.id_alumne;
    this.id_profesor = n.id_profesor;
    this.id_assig = n.id_assig;
    this.cod_assig = n.cod_assig;
    this.nota= n.nota;
};

Notes.getAll = (id_alu,result) => {

    query="Select n.*,a.cod_assig from notes as n, assignatura as a "+ 
    "where n.id_assig=a.id_assig and n.id_alumne=${id_alu}";

    sql.query(query, (err, res) => {
        if (err) {
          console.log("error: ", err);
          result(true, err);
          return;
        }
        console.log("notes: ", res);
        result(null, res);
    });

};

module.exports=Notes;