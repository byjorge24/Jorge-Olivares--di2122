llista = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

def par(numero):
    if numero % 2 == 0:
        return True

print("Imprimimos la funcion par usando el filter")
nova_llista_par = (list (filter(par, llista)))
print(nova_llista_par)

def senar(numero):
    if numero % 2 != 0:
        return True

print("Imprimimos la funcion senar usando el filter")
nova_llista_senar = (list (filter(senar, llista)))
print(nova_llista_senar)