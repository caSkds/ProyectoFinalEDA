import tkinter as tk
import random 

myApp = tk.Tk()


bombs = 10

map = []
buttons = []
height  = 15
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


for i in range(0,height):
    print(map[i])





def buttonClick(gameMap: list, name : str,buttonSet : list):
    global height, width
    #print(name)
    #print(name[:name.index('F')],name[name.index('e')+1:])


    buttonHeight =int(name[:name.index('F')])
    buttonWidth = int(name[name.index('e')+1:])

    if gameMap[buttonHeight][buttonWidth] == 500:
        buttonSet[buttonHeight][buttonWidth]["text"] = "BOMB!"
    else:
        buttonSet[buttonHeight][buttonWidth]["text"] =getNeighborBombs(gameMap,buttonWidth, buttonHeight)
        #print(f"{getNeighborBombs(gameMap,int(name[0]),int(name[1]))} bombs around {name}")
    



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
        #print(type(map[i][j]))
        buttons[i][j] = button




myApp.mainloop()