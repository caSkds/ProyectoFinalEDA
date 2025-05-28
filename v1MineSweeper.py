import tkinter as tk
import random
import sys
import time
myApp = tk.Tk()

startTime = time.time()
gameFrame = tk.Frame(myApp)
gameFrame.pack()

#Número de bombas
bombs = 10
shields = 5
radars = 3
powerUps = 2



map = []
mapGenerated = False
buttons = []
specialButtons = {
    "shield" : 100,
    "radar" : 200,
    "powerUp" : 300,
    "bombs" : 500
}

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

# Adding every game object:
def addGameObject(gameMap: list, x_avoid :int, y_avoid : int, nProperty: int, propertyName :str):
    # Making sure the first cell is right next to a bomb
    startingX = x_avoid
    startingY = y_avoid
    if propertyName == "bombs":
        if startingX == width - 1:
            startingX = x_avoid -1
        if startingY == height - 1:
            startingY = y_avoid - 1
        if x_avoid != width - 1 and y_avoid != height - 1:
            gameMap[startingY+1][startingX+1] = specialButtons[propertyName]
        else:
            gameMap[startingY][startingX] = specialButtons[propertyName]
        nProperty -= 1
            
    nProperty -= 1
    while nProperty > 0:
        for i in range(0,height):
            for j in range(0,width):
                if i!= y_avoid and j!=x_avoid and gameMap[i][j] == 0:
                    if random.randint(0,100)<5 and nProperty > 0:
                        gameMap[i][j] = specialButtons[propertyName]
                        nProperty -= 1

# Initialize the map with 0s and place all objects randomly
def initializeMap(gameMap: list, x_0 : int, y_0:int, nBombs: int, nShields: int, nRadars:int, nPowerUps: int):
    global mapGenerated
    addGameObject(gameMap, x_0, y_0, nBombs, "bombs")
    addGameObject(gameMap, x_0, y_0, nShields, "shield")
    addGameObject(gameMap, x_0, y_0, nRadars, "radar")
    addGameObject(gameMap, x_0, y_0, nPowerUps, "powerUp")
    """
    # Fills the map with number of surrounding bombs
    for i in range(0,height):
            for j in range(0,width):
                if map[i][j] != 500:
                    map[i][j] = getNeighborBombs(map,j,i)
    """
    mapGenerated = True




# Gets the count of bombs surrounding a cell
def getNeighborBombs(gameMap: list, x : int, y : int) -> int:
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= x + i < width and 0 <= y + j < height:
                if gameMap[y + j][x + i] == 500:
                    count += 1
    return count




def radarEffect(gameMap: list, x: int, y: int, buttons: list): 
    # This function will reveal all the cells in a 3x3 area around the radar
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= x + i < width and 0 <= y + j < height:
                if gameMap[y + j][x + i] == 0:
                    buttons[y + j][x + i]["text"] = getNeighborBombs(gameMap, x + i, y + j)
                else:
                    buttons[y + j][x + i]["text"] = gameMap[y + j][x + i]





# Defines behavior for left click on a button
def buttonClick(gameMap: list, name : str,buttonSet : list):
    global mapGenerated

    buttonHeight =int(name[:name.index('F')])
    buttonWidth = int(name[name.index('e')+1:])
    if not mapGenerated:
        initializeMap(gameMap, buttonWidth, buttonHeight, bombs, shields, radars, powerUps)
        printMap(gameMap)


    if gameMap[buttonHeight][buttonWidth] == 500:
        buttonSet[buttonHeight][buttonWidth]["text"] = "BOMB!"
    elif gameMap[buttonHeight][buttonWidth] == 100:
        radarEffect(gameMap, buttonWidth, buttonHeight, buttonSet)
    elif gameMap[buttonHeight][buttonWidth] == 200:
        buttonSet[buttonHeight][buttonWidth]["text"] = "RADAR"
    elif gameMap[buttonHeight][buttonWidth] == 300: 
        buttonSet[buttonHeight][buttonWidth]["text"] = "POWER UP"
    else:
        buttonSet[buttonHeight][buttonWidth]["text"] =getNeighborBombs(gameMap,buttonWidth, buttonHeight)

# Defines flagging a button
def flag( event ):
    event.widget.config(text="F")




# Create buttons for the grid
for i in range(0,height):
    for j in range(0,width):
        currentName = str(i)+str(False)+str(j)
        button  =tk.Button(gameFrame,
                name = str(i)  +str(j),
                command =  lambda buttonName = currentName: buttonClick(map,buttonName,buttons))
        #print(str(i)+str(j))
        button.grid(
            row = i,
            column = j
        )
        #checks os for right click
        if sys.platform == "darwin":
            button.bind("<Button-2>", flag)
        else:
            button.bind("<Button-3>", flag)
        #print(type(map[i][j]))
        buttons[i][j] = button




myApp.mainloop()
