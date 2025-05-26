# ProyectoFinalEDA

## Buscaminas
```python
import tkinter as tk
import random 
```
### Librerías
La manera en la que se crea el buscaminas es creando un arreglo bidimensional, el cual es la representación matricial de los botones del buscaminas. Cada valor es inicializado en 0, y posteriormente a n. buscaminas al azar (determinado por la variable `bombs`) se le asignará un valor de 500, representando este una mina. 

```python
myApp = tk.Tk()


bombs = 10

map = []
buttons = []

# Create a 10x10 grid for the matrix representation of the game 
# Create a 10x10 grid for the buttons
for i in range(0,10):
    newList = []
    for j in range(0,10):
        newList.append(0)
    map.append(newList)


for i in range(0,10):
    otherNewList = []
    for j in range(0,10):
        otherNewList.append(0)
    buttons.append(otherNewList)

# Initialize the map with 0s and place bombs randomly
while bombs >0:
    for i in range(0,10):
        for j in range(0,10):
            if random.randint(0,100)<5 and bombs > 0 and map[i][j] == 0:
                map[i][j] = 500 # 500 is a bomb
                bombs -= 1
```