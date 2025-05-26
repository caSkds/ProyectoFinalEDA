import tkinter as tk
import random 

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



def getNeighborBombs(gameMap: list, x, y):
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= x + i < 10 and 0 <= y + j < 10:
                if gameMap[x + i][y + j] == 500:
                    count += 1
    return count

for i in range(0,10):
        for j in range(0,10):
            if map[i][j] != 500:
                map[i][j] = getNeighborBombs(map, i, j)


for i in range(0,10):
    print(map[i])





def buttonClick(gameMap: list, name : str,buttonSet : list):
    #print(name)
    if gameMap[int(name[0])][int(name[1])] == 500:
        buttonSet[int(name[0])][int(name[1])]["text"] = "BOMB!"
    else:
        buttonSet[int(name[0])][int(name[1])]["text"] =getNeighborBombs(gameMap,int(name[0]), int(name[1]))
        #print(f"{getNeighborBombs(gameMap,int(name[0]),int(name[1]))} bombs around {name}")
    



# Create buttons for the grid

for i in range(0,10):
    for j in range(0,10):
        currentName = str(i)+str(j)
        button  =tk.Button(myApp,
                name=str(i)+str(j), 
                command =  lambda buttonName = currentName: buttonClick(map,buttonName,buttons))
        #print(str(i)+str(j))
        button.grid(
            row = i,
            column = j
        )
        #print(type(map[i][j]))
        buttons[i][j] = button




myApp.mainloop()