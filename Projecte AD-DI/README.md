# PROJECTE AD - DI

Projecte desenvolupat als mòduls DI-AD de l'IES Jaume II El Just de Tavernes De La Valldigna - Curs 21/22

## PART CLIENT DI

### Entrega DI-1

1. Modifica el header de l’aplicació per a que mostre el nom de l’aplicació Qualificacions App en
compte de Quasar App.
2. Modifica el header per a que mostre la data en valencià i amb el següent format Dimecres, 16 de
Febrer de 2021.
3. Elimina la paraula Essential Links del Drawer.
4. Modifica els víncles. Tots t’han de dirigir a altres parts de l’aplicació sobre la mateixa pestanya. Quan no estem autentificats a l’aplicació, s’ha de mostrar un link Login que vaja a l’arrel de
l’aplicació i un altre About que ens porte a about.
5. Modifica la pàgina inicial de l’aplicació per a que mostre un formulari de login, que demane
el nom d’usuari i la contrasenya. En cas de no estar registrat, s’ha de proporcionar un vincle a register.
6. Modifica la pàgina d’error per a que en cas d’anar a una pàgina que no existeix, mostre un missatge que li passarem a través d’un binding a una variable amb el valor «Pàgina no existent». Fes
el mateix amb el text del botó, que indicarà «Torna a l’inici».
7. Crea un formulari per a registrar-se. La informació que s’ha de passar ha de ser nom complet,
dni, username i password.
8. De moment els formularis no senviaran al servidor, però si que heu de preparar la seua validació
en la part del client.

### Entrega DI-2

1. Afegeix Vuex al teu projecte i fes que l’estat del Drawer siga global.
2. Afegix axios al projecte i prova, mitjançant qualsevol botó, que el servidor et respón.
3. Utilitza les APIs dels servidor per fer Login amb un usuari registrat prèviament al sistema. Guarda la informació que consideres important a Vuex.
4. Utilitza l’API de registre d’usuari del servidor per donar d’alta un nou usuari. Llança una notificació per a avisar a l’usuari que el registre és correcte i porta’l a la pantalla de Login.
5. Crea un component per a donar la benvinguda a l’aplicació al fer Login correctament. En cas de
no ser correcte el Login, has de llançar una notificació indicant la resposta del servidor.
6. En fer Login un usuari, has de canviar el Drawer, ara ja no mostrarà l’enllaç a Login, sinó:

    Un avatar a la part superior, de moment un per defecte per a tots
    
    Un enllaç a notes.
    
    Un enllaç a Logout.
    
    Mantin l’About.

## PART SERVIDOR AD

### Registre

El registre en un servei implica el tindre que donar-nos d’alta al servei. És per això que lu hem de passar informació al servei. Aquesta informació serà, empaquetada en un JSON:


```bash
{
    dni:"",
    username:"",
    password:"",
    full_name:"",
    avatar:""
}
```

Per tant el registre es deu implementar amb un POST /register, passant al body l’objecte anterior.

El dni que ens envien no el guardem enlloc en la nostra BBDD, però tindre una taula auxiliar, que no gestionareu desde el client. Aquesta taula es dirà DNI_PROFES i conté sols un llistat de DNI dels professors. La funció és que quan un usuari es registre, la manera de saber si és alumne o professor, és mitjançant aquest dni, i comprovar si està o no dins de dita taula DNI_PROFES.

Per tant el flux de treball será:
1. Rebre les dades i comprovar que els camps obligatories existeixen.
2. Comprovar que el username no està donat d’alta a la taula d’usuaris.
3. Verificar que el dni està o no a la taula de DNI_PROFES
4. Inserir en la taula de users.
5. Inserir en la taula de alumne o professor, depenent del resultat de l’apartat 3
6. Retornar la informació al client. Aquesta informació deu empaquetar-se en un JWT, i en l’apartat del payload contindrà com a dades:

```bash
{
    "user_id": 23,
    "username": "pepitou",
    "role": "profe",
    "iat": 1613503548,
    "exp": 1613589948
}
```

El token deu caducar a les dos hores i es rebrà un token per a regenerar-lo en cas necessari, com es veu a continuació:

```bash
{
    "ok": true,
    "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJ1c2VyX2lkIjoyMywidXNlcm5hbWUiOiJwZXBpdG91Iiwicm9InByb2ZlIiwiaWF0Ijox._kKsj8DIMi5Nvoi5nKitJlMivBkNgRgwQRHt9qThsSk",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJ1c2VyX2lkIjoyMywidXNlcm5hbWUiOiJwZXBpdG91Iiwicm9sZSI6InByb2ZlIiwiaWF0IjoxGu2fyRH1idm41xvAznDwzeIXEYsmZWKGCHbV1ZQs90Y","
}
```

### Login

Aquest apartat servira per a loguejar-se al sistema. Se suposa que el client ens enviara un nom i password per a validar-se. Obviament el client farà això perque encara no disposa de un token emés pel servidor.

Per tant el registre es deu implementar amb un POST /login, passant al body la següent informació.

```bash
{
    "username":"pepito",
    "password":"1234"
}
```

El fluxe de treball serà:
1. Comprovar que l’usuari i contrassenya és vàlid
2. Comprovar si dit usuari és professor o alumne
3. Generar els tokens i respondre

```bash
{
    "ok": true,
    "data": {
    "token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9eyJ1c2VyX2lkIjoyMiwidXNlcm5hbWUiOiJwZXBpdG8iLCJyb2xlIjoicHJvZmVzc29yIiwiaWF0.hoia_kM16pyG_V5bwj8rv_O_n5nwva-Jrlz_gHQH7xY",
    "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoyMiwidXNlcm5hbWUiOiJwZXBpdG8iLCJyb2xlIjoicHJvZmVzc29yIiwiaWF0.2-G_AFGyxLOM39EvuUhLyRT66ZjkPhpst4Am857cx3I",
    "avatar": {
        "type": "Buffer",
        "data": []
        }
    }
}
```

i dins del payload del token les mateixes dades que al registre:

```bash
{
    "user_id": 23,
    "username": "pepitou",
    "role": "profe",
    "iat": 1613503548,
    "exp": 1613589948
}
```