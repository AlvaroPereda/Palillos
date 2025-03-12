import pandas as pd
import numpy as np
from queue import Queue

init_segment = np.asanyarray(pd.read_csv("pos_initial.csv"))
final_segment = np.asanyarray(pd.read_csv("pos_final.csv"))

operations = [
    [1,1], #abajo-derecha
    [1,-1], #abajo-izquierda
    [-1,1], #arriba-derecha
    [-1,-1] #arriba-izquierda
]

almacen_heuristic = []
numero_palillos = 0
numero_palillos_iniciales = 0
numero_huecos = 7

for fil in range(final_segment.shape[0]):
    for col in range(final_segment.shape[1]):
        if final_segment[fil][col] == "x":
            almacen_heuristic.append([fil,col])
            numero_palillos += 1
        if init_segment[fil][col] == "x":
            numero_palillos_iniciales += 1

if numero_palillos_iniciales != numero_palillos:
    print("El número de palillos inicial no es igual al número de palillos final.\nNO HAY SOLUCIÓN.\n")
    exit()


class Node:
    def __init__(self, value, parent=None):
        self.value = value
        self.children = []
        self.parent = parent
        self.heuristic = self.calculate_heuristic() 

    def add_child(self, value):
        child = Node(value, parent=self)
        self.children.append(child)
        return child

    def generate_childs(self):
        num_filas, num_columnas = self.value.shape
        for i in range(num_filas):
            for j in range(num_columnas):
                if self.value[i][j] == "x":
                    for op in operations:
                        new_i, new_j = i + op[0], j + op[1]
                        if 0 <= new_i < num_filas and 0 <= new_j < num_columnas:
                            if self.value[new_i][new_j] != "x":
                                new_value = self.value.copy()
                                new_value[i][j] = " "
                                new_value[new_i][new_j] = "x"
                                self.add_child(new_value)
                                if np.array_equal(new_value,final_segment):
                                    return self.children, True                        
        return self.children, False
    
    def calculate_heuristic(self): 
        heuristic = 0
        for fil in range(self.value.shape[0]): 
            for col in range(self.value.shape[1]): 
                if self.value[fil][col] == "x": 
                    found = False
                    for h in almacen_heuristic: 
                        if [fil, col]== h: 
                            found = True
                            break
                    if found:
                        break
                    heuristic += 1
        return heuristic
        

root = Node(init_segment)
cola = Queue()
children , finish = root.generate_childs()
for i in children:
    cola.put(i)

while not cola.empty() and not finish:
    nodo_actual = cola.get() 
    nuevos_hijos, finish = nodo_actual.generate_childs()
    
    for hijo in nuevos_hijos:
        cola.put(hijo)

    if finish:
        break

almacen = []
aux = list(cola.queue)
hijo = aux[-1]
almacen.insert(0,hijo)
while True:
    if hijo.parent == None:
        break
    almacen.insert(0,hijo.parent)
    hijo = hijo.parent

for i in almacen:
    print(i.value)
    print("")