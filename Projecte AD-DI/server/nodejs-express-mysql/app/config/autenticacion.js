const jwt = require('jsonwebtoken');
const accessTokenSecret = 'laParaulaSecretaDelServidor';

const authenticateJWT = (req, res, next) => {
    // arrepleguem el JWT d'autoritzaciÃ³
    const authHeader = req.headers.authorization;

    if (authHeader) {

        // si hi ha toquen
        const token = authHeader.split(' ')[1];
        jwt.verify(token, accessTokenSecret, (err, user) => {
            if (err) {
                return res.sendStatus(403);
            }
            req.user = user;
            next();
        });

    } else {
        res.sendStatus(401);
    }
};

module.exports={authenticateJWT}