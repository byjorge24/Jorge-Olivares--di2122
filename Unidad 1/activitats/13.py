import random
import re

class ErrorEnterMassaMenut(Exception):
    pass
class ErrorEnterMassaGran(Exception):
    pass


i = random.randint(0,100)

print(i)

while (True):
    
    try:
        ValorIntroducido = input("Introduce un valor del 0 al 100: ")

        num_format = re.compile(r'^\-?[1-9][0-9]*$')
        it_is = re.match(num_format,ValorIntroducido)

        if it_is:
            print("Valor entero introducido correctamente!!!")
        else:
            break

        ValorIntroducido = int(ValorIntroducido)
        if ValorIntroducido > i:
            raise ErrorEnterMassaGran("ErrorEnterMassaGran")
        if ValorIntroducido < i:
            raise ErrorEnterMassaMenut("ErrorEnterMassaMenut")
        if ValorIntroducido == i:
            print("Has adivinat el numero!")
            break
        
    except Exception as e:
        print("Excepcion: " + repr(e))