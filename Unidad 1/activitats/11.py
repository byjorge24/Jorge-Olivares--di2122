import os
from sys import is_finalizing

base_url= os.path.dirname(__file__)

f = open(os.path.join(base_url, "fichero.txt"), "r+")

multiplicar = lambda x,y: x * y

sumar = lambda x,y: x + y

restar = lambda x,y: x - y

dividir = lambda x,y: x / y

fichero1 =open(os.path.join(base_url, "ficherogenerado.txt"), "w")

for i in f:

    numeroString = i.split(" ")

    if (numeroString[1] == "+"):

        numeroInt1 = int(numeroString[0])

        numeroInt2 = int(numeroString[2])

        resultado = sumar(numeroInt1, numeroInt2)

        resultadoString = numeroString[0] + " " + numeroString[1] + " " + numeroString[2].rstrip('\n') + " " + "=" + " " + str(resultado)

        fichero1.write(resultadoString)

        print(numeroString[0], numeroString[1], numeroString[2].rstrip('\n'), "=", resultado)

    if (numeroString[1] == "-"):

        numeroInt1 = int(numeroString[0])

        numeroInt2 = int(numeroString[2])

        resultado = restar(numeroInt1, numeroInt2)

        resultadoString = "\n" + numeroString[0] + " " + numeroString[1] + " " + numeroString[2].rstrip('\n') + " " + "=" + " " + str(resultado)

        fichero1.write(resultadoString)

        print(numeroString[0], numeroString[1], numeroString[2].rstrip('\n'), "=", resultado)

    if (numeroString[1] == "*"):
        
        numeroInt1 = int(numeroString[0])

        numeroInt2 = int(numeroString[2])

        resultado = multiplicar(numeroInt1, numeroInt2)

        resultadoString = "\n" + numeroString[0] + " " + numeroString[1] + " " + numeroString[2].rstrip('\n') + " " + "=" + " " + str(resultado)

        fichero1.write(resultadoString)

        print(numeroString[0], numeroString[1], numeroString[2].rstrip('\n'), "=", resultado)

    if (numeroString[1] == "/"):
        
        numeroInt1 = int(numeroString[0])

        numeroInt2 = int(numeroString[2])

        resultado = dividir(numeroInt1, numeroInt2)

        resultadoString = "\n" + numeroString[0] + " " + numeroString[1] + " " + numeroString[2].rstrip('\n') + " " + "=" + " " + str(resultado)

        fichero1.write(resultadoString)

        print(numeroString[0], numeroString[1], numeroString[2].rstrip('\n'), "=", resultado)

f.close()