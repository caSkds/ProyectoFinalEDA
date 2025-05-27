import tkinter as tk
import random
import sys
myApp = tk.Tk()

#Número de bombas
bombs = 10

map = []
buttons = []

# Altura del juego
height  = 15

# Ancho del juego
width = 10
myApp.title("Mine Sweeper")

# Create a height x width grid for the matrix representation of the game 
# Create a height x width grid for the buttons
for i in range(0,height):
    newList = []
    for j in range(0,width):
        newList.append(0)
    map.append(newList)


for i in range(0,height):
    otherNewList = []
    for j in range(0,width):
        otherNewList.append(0)
    buttons.append(otherNewList)


#Función para visualizar el mapa en la terminal
#Solo usar para depuración 
def printMap(gameMap: list):
    for i in range(0,len(gameMap)):
        print(gameMap[i])


# Initialize the map with 0s and place bombs randomly
while bombs >0:
    for i in range(0,height):
        for j in range(0,width):
            if random.randint(0,100)<5 and bombs > 0 and map[i][j] == 0:
                map[i][j] = 500 # 500 is a bomb
                bombs -= 1





def getNeighborBombs(gameMap: list, x : int, y : int) -> int:
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= x + i < width and 0 <= y + j < height:
                if gameMap[y + j][x + i] == 500:
                    count += 1
    return count

for i in range(0,height):
        for j in range(0,width):
            if map[i][j] != 500:
                map[i][j] = getNeighborBombs(map,j,i)



#printMap(map)





def buttonClick(gameMap: list, name : str,buttonSet : list):
    buttonHeight =int(name[:name.index('F')])
    buttonWidth = int(name[name.index('e')+1:])

    if gameMap[buttonHeight][buttonWidth] == 500:
        buttonSet[buttonHeight][buttonWidth]["text"] = "BOMB!"
    else:
        buttonSet[buttonHeight][buttonWidth]["text"] =getNeighborBombs(gameMap,buttonWidth, buttonHeight)


def flag( event ):
    event.widget.config(text="F", bg="yellow")



# Create buttons for the grid

for i in range(0,height):
    for j in range(0,width):
        currentName = str(i)+str(False)+str(j)
        button  =tk.Button(myApp,
                name = str(i)  +str(j),
                command =  lambda buttonName = currentName: buttonClick(map,buttonName,buttons))
        #print(str(i)+str(j))
        button.grid(
            row = i,
            column = j
        )
        if sys.platform == "darwin":
            button.bind("<Button-2>", flag)
        else:
            button.bind("<Button-3>", flag)
        #print(type(map[i][j]))
        buttons[i][j] = button




myApp.mainloop()