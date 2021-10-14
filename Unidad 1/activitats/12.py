import os
from sys import is_finalizing

base_url= os.path.dirname(__file__)

try:

    f = open(os.path.join(base_url, "fichero.txt"), "r+")

except FileNotFoundError:
    
    print("El fichero no se ha econtrado!!!")

multiplicar = lambda x,y: x * y

sumar = lambda x,y: x + y

restar = lambda x,y: x - y

dividir = lambda x,y: x / y 

try:

    fichero1 =open(os.path.join(base_url, "ficherogenerado.txt"), "w")

except FileNotFoundError:

    print('No se ha encontrado el fichero!!!')

for i in f:

    numeroString = i.split(" ")

    if (numeroString[1] == "+"):

        numeroInt1 = int(numeroString[0])

        numeroInt2 = int(numeroString[2])
        
        try:

            resultado = sumar(numeroInt1, numeroInt2)

        except ValueError:

            print("En el fichero debe haber numeros")

        resultadoString = numeroString[0] + " " + numeroString[1] + " " + numeroString[2].rstrip('\n') + " " + "=" + " " + str(resultado)

        fichero1.write(resultadoString)

        print(numeroString[0], numeroString[1], numeroString[2].rstrip('\n'), "=", resultado)

    if (numeroString[1] == "-"):

        numeroInt1 = int(numeroString[0])

        numeroInt2 = int(numeroString[2])

        try:

            resultado = restar(numeroInt1, numeroInt2)
        
        except ValueError:

            print("En el fichero debe haber numeros")

        resultadoString = "\n" + numeroString[0] + " " + numeroString[1] + " " + numeroString[2].rstrip('\n') + " " + "=" + " " + str(resultado)

        fichero1.write(resultadoString)

        print(numeroString[0], numeroString[1], numeroString[2].rstrip('\n'), "=", resultado)

    if (numeroString[1] == "*"):
        
        numeroInt1 = int(numeroString[0])

        numeroInt2 = int(numeroString[2])

        try:

            resultado = multiplicar(numeroInt1, numeroInt2)
        
        except ValueError:

            print("En el fichero debe haber numeros")

        resultadoString = "\n" + numeroString[0] + " " + numeroString[1] + " " + numeroString[2].rstrip('\n') + " " + "=" + " " + str(resultado)

        fichero1.write(resultadoString)

        print(numeroString[0], numeroString[1], numeroString[2].rstrip('\n'), "=", resultado)

    if (numeroString[1] == "/"):
        
        numeroInt1 = int(numeroString[0])

        numeroInt2 = int(numeroString[2])

        try:

            resultado = dividir(numeroInt1, numeroInt2)

        except ZeroDivisionError:

            print("No se puede dividir por 0")

        resultadoString = "\n" + numeroString[0] + " " + numeroString[1] + " " + numeroString[2].rstrip('\n') + " " + "=" + " " + str(resultado)

        fichero1.write(resultadoString)

        print(numeroString[0], numeroString[1], numeroString[2].rstrip('\n'), "=", resultado)

f.close()