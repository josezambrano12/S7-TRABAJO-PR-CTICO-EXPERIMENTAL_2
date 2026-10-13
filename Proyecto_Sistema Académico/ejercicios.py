# Ejercicio 1
ciudades = ["Quito", "Guayaquil", "Quito", "Cuenca", "Guayaquil"]

vistas = set()     
unicas = []        
for ciudad in ciudades:
    if ciudad not in vistas:
        vistas.add(ciudad)
        unicas.append(ciudad)

print(unicas)

# Ejercicio 2
conteo = {}
for ciudad in ciudades:
    conteo[ciudad] = conteo.get(ciudad, 0) + 1     
print(conteo)

mas_repetida = max(conteo, key=conteo.get)
print(mas_repetida)

# Ejercicio 3
inscritos_matematica = {"juan","Luis","Marco"}
inscritos_ingles = {"Luis","Marco","Ruth"}
ambas = inscritos_matematica & inscritos_ingles
solo_mate   = inscritos_matematica - inscritos_ingles   
total       = len(inscritos_matematica | inscritos_ingles) 

print(sorted(ambas), sorted(solo_mate), total)

# Ejercicio 4
clientes = [{"id":1,"nombre":"Ana"},{"id":2,"nombre":"Luis"}]
indice = {cliente["id"]: cliente for cliente in clientes}
print(indice[2]["nombre"])       

# Ejercicio 5
ventas = [("enero", 1500), ("febrero", 1800), ("marzo", 1200)]
total = sum(monto for _mes, monto in ventas)

mejor_mes, mejor_monto = max(ventas, key=lambda venta: venta[1])

print(f"Total: {total}")
print(f"Mejor mes: {mejor_mes} con {mejor_monto}")

for mes, monto in ventas:              
    print(f"{mes:<10} {monto}")
