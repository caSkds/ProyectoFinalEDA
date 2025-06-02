# ProyectoFinalEDA

## Construcción de la aplicación
Antes de pensar en una aplicación de Tkinter se debe inicializar un objeto de tipo `Tk()`. 

```python
myApp = tk.Tk()
myApp.config(bg="black") #Color base de la ventana
myApp.geometry("900x600+300+150") #tamaño establecido y ubicacion inicial
# Configuración de la ventana principal
myApp.title("Mine Sweeper")
```
## Menú
Para el menu se usaron multiples widgets de tkinter, la declaracion y cada especificacion se definen para darle estilo "Neon" a pathfinder

```python
#Variable para el menu:
menu_frame = tk.Frame(myApp,bg="black")
name_label = tk.Label(menu_frame,
                          bg="black",
                          text="Pathfinder",
                          fg="white",
                          font=("arial",20),
                          anchor='center',
                          highlightbackground="purple",
                          highlightthickness=3,
                          pady=5)
play_frame = tk.Frame(menu_frame,
                          highlightbackground="green yellow",
                          highlightthickness=1)
play_button = tk.Button(play_frame,
                            width="15",
                            text="Iniciar juego",
                            bg="black",
                            fg="white",
                            font=("arial",15),
                            pady=5,
                            border=0,
                            activebackground="green yellow",
                            command=jugar)
score_frame = tk.Frame(menu_frame,
                           highlightbackground="green yellow",
                           highlightthickness=1)
score_button = tk.Button(score_frame,
                            width="15",
                            text="Puntuacion",
                            bg="black",
                            fg="white",
                            font=("arial",15),
                            pady=5,
                            border=0,
                            activebackground="green yellow")
exit_frame = tk.Frame(menu_frame,
                            highlightbackground="magenta2",
                            highlightthickness=1)
exit_button = tk.Button(exit_frame,
                            width="5",
                            text="Salir",
                            bg="black",
                            fg="white",
                            font=("arial",10),
                            pady=5,
                            command=salir,
                            border=0,
                            activebackground="magenta2")
```
Para la creacion del efecto neon y del borde colorido de cada boton se creo un Frame propio para cada uno, pues al no tener disponible un metodo directo para cambiar el color del borde de un boton, se hace visible el borde del Frame alrededor del boton
Ademas, el juego se incia al llamar a la funcion menu(), de la cual se puede manejar el juego entero.

```python
def menu(): #Funcion para el menu principal
    menu_frame.pack(fill="both", expand="True",)
    name_label.pack(pady=60)
    play_frame.pack(pady=5)
    play_button.pack()
    score_frame.pack()
    score_button.pack()
    score_button.config(command = mostrarTop10)
    exit_frame.pack(pady=10)
    exit_button.pack()
```

## Buscaminas


### Creación del mapa


El mapa de buscaminas está dividido en 2. Uno es el arreglo que contiene a cada botón y el otro es el arreglo que contiene a la representación numérica de cada poder/ objeto (esto se discutirá más a detalle en la sección de objetos).

#### Ancho y alto

En el programa se declaran 2 variables. `width` y `height`, que especifican el ancho y el largo del mapa de buscaminas a crear. 

```python 
# Altura del juego
height  = 15
# Ancho del juego
width = 15
```

#### Representación matricial del mapa
El mapa está representado numéricamente con una matriz, la cual es encargada de almacenar los valores correspondientes a las casillas donde hay algún poder. Para esto se crean `height` número de listas de `width`elementos 

```python 
map = []

for i in range(0,height):
    newList = []
    for j in range(0,width):
        newList.append(0)
    map.append(newList)

```

> En la sección [creación de objetos](#creación-de-objetos) se discutirá como se añaden estos elementos al mapa


#### Representación gráfica del mapa


El juego de buscaminas está construido sobre un `frame` de nombre `gameFrame`
```python
gameFrame = tk.Frame(myApp,
                     bg="black",
                     highlightbackground="green yellow",
                    highlightthickness=1)
```
>- En la versión de mac se omite lo siguiente:
```python
gameFrame.pack(propagate = False)
```



El proceso para representar gráficamente al mapa es muy similar a cómo se creó el mapa. La diferencia es que esta lista bidimensional será llenada con objetos de tipo botón de Tkinter. Similar a antes, se usan 2 ciclos for anidados para agregar botones, a los cuales se les da un nombre correspondiente a sus coordenadas en y y en x separado por la palabra `False`. Conforme se añade cada botón se ejecuta la función `pack()`para mostrarlo

- Cada botón está posicionado dentro de un frame para darle estilo a cada casilla
- Dicha casilla se va  posicionando de acuerdo a la iteración de los ciclos for anidados donde se encuentre. 
- De la misma manera, el nombre que se va iterando se convierte en el argumento de la función `buttonClick()``
- Se llama a una función lambda, pues de lo contrario la función se ejecutaría al momento de crear el objeto, no al momento de presionar cada botón


```python
# Create buttons for the grid
def createButtons():
    global buttons
    global map
    for i in range(0,height):
        for j in range(0,width):
            currentName = str(i)+str(False)+str(j)
            cell_frame = tk.Frame(gameFrame,
                                highlightbackground="purple",
                                highlightthickness=1,
                                bg="black",
                                width=40,
                                height=40)
            button  =tk.Button(cell_frame,
                    name = str(i)  +str(j),
                    
                    bg="#FFFFFF",
                    
                    border=0,
#Please reverse this stiling
                    fg="#000000",
                    width=4,
                    height=2,
                    activebackground="green yellow",
                    command =  lambda buttonName = currentName: buttonClick(map,buttonName,buttons))
            #print(str(i)+str(j))
            cell_frame.grid(
                row = i,
                column = j
            )
            
            '''
            button.grid(
                row = i,
                column = j
            )
            '''
            button.pack()
            #checks os for right click
            if sys.platform == "darwin":
                button.bind("<Button-2>", flag)
            else:
                button.bind("<Button-3>", flag)
            #print(type(map[i][j]))
            buttons[i][j] = button

```


> - El condicional de hasta abajo se explica  con más detalle en [la sección de banderas](#banderasclick-derecho)
> - Dada la manera en la que se renderiza una aplicación de Tkinter en Mac y en Windows, los parámetros `bg`y `fg`son distintos para ambas versiones
> - Similarmente, en la versión de mac se omite lo siguiente:
```python
Font = ("",20)
```
#### Creación de objetos
En este juego hay 4 objetos distintos:
- Casillas normales
- Casillas con bombas
- PowerUps
- Radares
- Escudos
Cada uno de estos objetos tiene su representación numérica

```python 
specialButtons = {
    "shield" : 100,
    "radar" : 200,
    "powerUp" : 300,
    "bombs" : 500
}
```
La cantidad de cada uno de estos objetos están determinados por sus variables correspondientes y pueden ser modificados según se desee:
```python 
#Número de poderes en el tablero
bombs = 40
shields = 5
radars = 3
powerUps = 2
```

 Hay una variable llamada `mapGenerated`, la cual es un booleano que le indica al juego si ya se creó el mapa o no. Esto se revisa al darle click al primer botón del mapa.

```python
    if not mapGenerated:
        initializeMap(gameMap, buttonWidth,buttonHeight, bombs, shields, radars, powerUps)
```

A su vez, esta función llama a una función llamada `addGameObject()`para cada objeto. Tras esto, la variable `mapGenerated`se cambia a verdadera.

```python 
# Initialize the map with 0s and place all objects randomly
def initializeMap(gameMap: list, x_0 : int, y_0:int, nBombs: int, nShields: int, nRadars:int, nPowerUps: int):
    global mapGenerated
    addGameObject(gameMap, x_0, y_0, nBombs, "bombs")
    addGameObject(gameMap, x_0, y_0, nShields, "shield")
    addGameObject(gameMap, x_0, y_0, nRadars, "radar")
    addGameObject(gameMap, x_0, y_0, nPowerUps, "powerUp")
    mapGenerated = True
```

La función `addGameObject`tiene un condicional para cuando la propiedad es una bomba. En este caso, agrega la bomba en una coordenada más en x y una coordenada más en y. Al menos que se encuentre en alguno de los bordes, en cuyo caso se le resta uno a la coordenada en x o en y. 

```python
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
```
Una vez programada esta excepción, en cada objeto nos fijamos en que su correspondiente representación matricial sea igual a 0 para evitar poner objetos donde mismo. Para esto, se crea un ciclo que itera por n. objetos a agregar y genera un número aleatorio. Si este es menor a 5, agrega ahí la propiedad. 

```python
    while nProperty > 0:
        for i in range(0,height):
            for j in range(0,width):
                if i!= y_avoid and j!=x_avoid and gameMap[i][j] == 0:
                    if random.randint(0,100)<5 and nProperty > 0:
                        gameMap[i][j] = specialButtons[propertyName]
                        nProperty -= 1
                        if propertyName == "powerUp":
                            gameMap[i][j] = specialButtons[propertyName] + random.randint(15,50)
```
> Para el powerUp, adicionalmente se le añade un número entre 15 y 50, que representa el potenciador que tendrá dicha casilla (entre 1.15x y 1.5x) en la puntuación final. Su funcionamiento se explica con más detalle en [Power Ups](#power-ups)


### Interacción con los botones
Como se puede ver, cada botón fue creado con un for y sigue el mismo comando: ` lambda buttonName = currentName: buttonClick(map,buttonName,buttons)`. 

Esto se hizo con una función lambda pues, si se quiere pasar una función con argumentos, esta se ejecuta automáticamente antes de presionar el botón, al menos que sea una función lambda.

Para diferenciar entre objetos, la función  `buttonClick()`diferencia entre cada tipo de casilla según la representación en el mapa. Es importante recordar que el nombre de cada botón está compuesto de 
$$ coordenadasEnY+ False + coordenadasEnX$$

Dado que podemos indexar los elementos de una cadena de carácteres tal como si fueran listas, la función `buttonClick()`usa el índice donde se ubica la 'F' como el índice hasta el cual terminan las coordenadas en y. Y el índice siguiente al índice correspondiente a la letra 'e' como la posición a partir de la cual comienzan los elementos a contemplar para obtener las coordenadas en x.

```python 
def buttonClick(gameMap: list, name : str,buttonSet : list):
    buttonHeight =int(name[:name.index('F')])
    buttonWidth = int(name[name.index('e')+1:])
```
> cabe notar que esta función solo toma de argumentos la representación matricial del mapa, el nombre del botón y la lista de botones; pues según se active cada objeto se irá modificando el texto de cada botón


Esta función empieza incrementando en 1 una variable global que rastrea cuantas casillas han sido cubiertas

- Al darle click a cada botón , se revisa que su representaión matricial no sea la de una bomba. Esto para incrementar la cantidad de casillas cubiertas en uno. Cuando es una bomba, primero se espera a que el mini juego acabe (o los escudos disminuyan) para incrementar en uno. Esto es para no ganar prematuramente. Esto se explica con más detalle en [victoria y derrota](#victoria-y-derrota)

#### Banderas/Click derecho
Las banderas son activadas con el click derecho. Durante el desarrollo se descubrió que Tkinter interpreta el click derecho de manera distinta para Windows (`<Button-3>`)como para MacOs (`<Button-2>`). Por esto en la función donde se crea cada botón se pone un condicional para aparear ya sea `<Button-2>` o `<Button-3>` a la función `flag()`

```python 
if sys.platform == "darwin":
            button.bind("<Button-2>", flag)
        else:
            button.bind("<Button-3>", flag)
```

Se usa una función flag la cual solo toma de parámetro a `event`el cual representa un objeto genérico de Tkinter.

```python

# Defines flagging a button
def flag( event ):
    global remainingFlags
    global currentFlags
    if event.widget["text"] == "🚩":
        remainingFlags +=1
        currentFlags +=1
        event.widget.config(text="")
    elif event.widget["text"] == "":
        remainingFlags -= 1
        event.widget.config(text="🚩")
```

> Se usa la variable `remainingFlags`y `currentFlags` las cuales sirven principalmente para avisar cuando se ha perdido o ganado. Su funcionamiento se explica con detalle en la sección [victoria y derrota](#victoria-y-derrota)

Hablando en términos de código, poner una bandera solo implica cambiar el texto del botón al emoji de una bandera 🚩. Una bandera no puede ser puesta en una casilla que ya fue descubierta. Por tanto solo se permite poner banderas en casilla cuyo texto sea nulo (establecido en el bloque `elif`). 

Para poder quitar una bandera está el bloque `if`, el cual revisa si el texto del botón actual es una bandera. De ser así, se cambia el texto para que sea nulo otra vez. No contemplar casos adicionales evita que una bandera pueda ser puesta sobre una casilla que fue previamente descubierta.



#### Casillas ordinarias
Cuando se le da click izquierdo a una casilla ordinaria, la función `clickButton()` primero revisa que la casilla no haya sido ya clickeada o revelada (esto se repite para cada uno de los objetos)
```python
    unclickedText = ["🚩", ""]  # Text for unclicked cell   

    if buttonSet[buttonHeight][buttonWidth]["text"]  in unclickedText:
        ...
        """
        Las condiciones para cada objeto se explicará en las próximas secciones
        """
        ...
     else:
        buttonSet[buttonHeight][buttonWidth]["text"] =getNeighborBombs(gameMap,buttonWidth, buttonHeight)
```
- Si la casilla no corresponde a ningún objeto, se llama a la función `getNeighborBombs()`
- Esta toma de argumento las coordenadas originales e itera en el eje x y en el eje y valores una unidad menor y una unidad mayor a la casilla actual (por ende el `range(-1,2)`). Si la iteración actual es menor a la altura o ancho del juego y encima la representación matricial es igual a 500 (el valor asignado a las bombas) se le agrega 1 a la variable `count()`, misma que se devuelve al final

```python
def getNeighborBombs(gameMap: list, x : int, y : int) -> int:
    count = 0
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= x + i < width and 0 <= y + j < height:
                if gameMap[y + j][x + i] == 500:
                    count += 1
    return count
```
#### Radares 
Los radares, iteran de la misma manera que la función que devuelve casillas restantes. Se verifica que al menos uno de los valores de `i`y `j`sean distintos de 0. Esto para asegurar que no estemos haciendo la revisión en la misma casilla. 
> Es importante recordar que al  presionar la casilla, el contador de cuantas casillas se han apretado ya se incrementó

Se aumenta las casillas ya cubiertas por cada celda revelada. Si su representación matricial es 0, su texto revela cuantas bombas hay alrededor.

- Si su representación matricial es de 100, se aplica la función `shieldEffect`tal como si se hubiera presionado para agregar automáticamente es escudo
- Si es un radar (representación matricial de 200), solo se cambia el texto
- Si su representación matricial es mayor a 300 y menor a 500 (powerUp), se llama a la función `powerUpEffect` tal como si hubiera sido presionado. 
- Si es una bomba (reprecentación matricial de 500) solo se cambia el texto, para que la bomba no pueda ser habilitada de nuevo.

```python 


    unclickedText = ["🚩", ""]  # Text for unclicked cell   

    if buttonSet[buttonHeight][buttonWidth]["text"]  in unclickedText:
        ...
        """
        Las condiciones para cada objeto se explicará en las próximas secciones
        """
        ...
    elif gameMap[buttonHeight][buttonWidth] == 200:
            radarEffect(gameMap, buttonWidth, buttonHeight, buttonSet)
            buttons[buttonHeight][buttonWidth]["text"] = str('📡 off')
        ...

```

```python
def radarEffect(gameMap: list, x: int, y: int, buttons: list): 
    # This function will reveal all the cells in a 3x3 area around the radar
    global casillasCubiertas
    global powerMultiplier
    global remainingShields
    unclickedText = ["🚩", ""]  # Text for unclicked cells
    for i in range(-1, 2):
        for j in range(-1, 2):
            if 0 <= x + i < width and 0 <= y + j < height:
                
                if i!= 0 or j!=0 :
                    
                    if buttons[y + j][x + i]["text"]  in unclickedText:
                        casillasCubiertas +=1
                        print(f"Casillas cubiertas added at {x+i}, {y+j}: {casillasCubiertas}")
                        if gameMap[y + j][x + i] == 0:
                            buttons[y + j][x + i]["text"] = getNeighborBombs(gameMap, x + i, y + j)
                        elif gameMap[y + j][x + i]  ==100:
                            shieldEffect(gameMap, x + i, y + j, buttons)
                            buttons[y + j][x + i]["text"] = str('🛡️')
                        elif gameMap[y + j][x + i] == 200:
                            buttons[y + j][x + i]["text"] = str('📡')
                        elif gameMap[y + j][x + i] >300 and gameMap[y + j][x + i] < 500:
                            powerUpEffect(gameMap, x + i, y + j, buttons)
                        # if it is a bomb
                        elif gameMap[y + j][x + i] == 500 and buttons[y + j][x + i]["text"]  in ["🚩", "💣"]:
                            buttons[y + j][x + i]["text"] = str('💣')

```


#### Bombas
Si se le da click a un botón vacío, la función `buttonClick` revisa si la cantidad de escudos restantes (`remainingShields`) es mayor a 0. Si no es así, se ejecuta la función `mostrarMinijuego()`. De lo contrario, solo se resta uno a los escudos restantes y se cambia el texto.

- Al final de esto se incrementan las casillas. Esto es para evitar ganar prematuramente.
```python


if buttonSet[buttonHeight][buttonWidth]["text"]  in unclickedText:
        
        if gameMap[buttonHeight][buttonWidth] == 500:
            
            if buttonSet[buttonHeight][buttonWidth]["text"] == "🚩":
                remainingFlags -= 1
            if remainingShields == 0:
                global mina_actual
                mina_actual = (buttonHeight, buttonWidth)
                mostrarMinijuego()
                
                
            else:
                remainingShields-=1
                shieldLabel.config(text="🛡️"+str(remainingShields))
                usedShields +=1
            buttonSet[buttonHeight][buttonWidth]["text"] = str('💣')
            remainingBombs -= 1
            casillasCubiertas +=1
            
        """
        Las condiciones para cada objeto se explicará en las próximas secciones
        """
        ...

```

#### Escudos
- Cuando la representación de un botón es un escudo, solo se llama a la función `shieldEffect()` Esta verifica que el bloque no haya sido clickeado, de ser así incrementa la variable `remainingShields()`en uno y actualiza el texto a mostrar en la parte superior del juego, donde se muestran los escudos restantes.

```python
def shieldEffect( gameMap: list, x: int, y: int, buttons: list):
    # Adds a shield to the game
    global remainingShields
    if buttons[y][x]["text"] == "🚩" or buttons[y][x]["text"] == "":
        remainingShields += 1
        shieldLabel.config(text="🛡️" + str(remainingShields))
        #buttons[y][x]["text"] = str('\t🛡️\n'+ str(getNeighborBombs(gameMap,x,y)))
        buttons[y][x]["text"] = "🛡️"
```

```python 

    unclickedText = ["🚩", ""]  # Text for unclicked cell   

    if buttonSet[buttonHeight][buttonWidth]["text"]  in unclickedText:
        ...
        """
        Las condiciones para cada objeto se explicará en las próximas secciones
        """
        ...
    elif gameMap[buttonHeight][buttonWidth] == 100:
            shieldEffect(gameMap, buttonWidth, buttonHeight, buttonSet)
        ...


```


#### Power Ups
- Es importante considerar que hay una función llamada `powerMultiplier`la cual acumula los potenciadores y al final se multiplica por la puntuación obtenida. 

Para este efecto, se llama a la función `powerUpEffect()` la cual  actualiza la variable `powerMultiplier` multiplicándolo por 1 + la representación matricial del poder menos 300 (por que 300 es el valor que diferencia a los poderes) dividido sobre 100

```python
def powerUpEffect(gameMap: list, x: int, y: int, buttons: list):
    global powerMultiplier
    if buttons[y][x]["text"] == "" or buttons[y][x]["text"] == "🚩":
        #buttons[y][x]["text"] = str(['⚡', getNeighborBombs(gameMap,x,y)])
        #buttons[y][x]["text"] = str(['⚡', getNeighborBombs(gameMap,x,y)])
        buttons[y][x]["text"] = str('⚡')
        buttons[y][x]["text"] = str('⚡')
        powerMultiplier = powerMultiplier * (1+((gameMap[y][x] - specialButtons["powerUp"])/100))
        print(f"Power multiplier: {powerMultiplier}")  # Debugging line to check the multiplier value
```

```python 

    unclickedText = ["🚩", ""]  # Text for unclicked cell   

    if buttonSet[buttonHeight][buttonWidth]["text"]  in unclickedText:
        ...
        """
        Las condiciones para cada objeto se explicará en las próximas secciones
        """
        ...
    elif gameMap[buttonHeight][buttonWidth] >= 300 and gameMap[buttonHeight][buttonWidth] < 500: 
            powerUpEffect(gameMap, buttonWidth, buttonHeight, buttonSet)
        ...


```
#### Mini Juego
### Victoria y derrota
- En caso de no desactivar una bomba a tiempo, se llama a la función `lose()`la cual  muestra la pantalla de pérdida
- Tras darle click a un botón se toma la suma de casillas clickeadas y banderas actuales. Si esta suma es igual al total de casillas en el tablero, se llama  a la misma función con un parámetro establecido en falso. Esto se verifica antes y después de darle click a un botón. Se calcula la puntuación obtenida de la siguiente manera:

$Puntuación =   (T_{Final}\cdot-0.001 +100)\cdot powerMultiplier \cdot \frac{casillasCubiertas + banderas}{totalCasillas}$

```python
finalTime = time.time() - startTime
    FinalScore = (finalTime*-0.001 + 100)* powerMultiplier * ((casillasCubiertas + currentFlags) / totalCasillas)
    FinalScore = round(FinalScore, 2) * 10000
```
Finalmente esto se imprime al usuario junto con un cuadro de texto para introducir nombre para la puntuación y botones para salir o volver a jugar

```python
def lose(lost: bool = True):
    global finalTime
    global casillasCubiertas
    global totalCasillas
    #print(finalTime)
    finalTime = time.time() - startTime
    FinalScore = (finalTime*-0.001 + 100)* powerMultiplier * ((casillasCubiertas + currentFlags) / totalCasillas)
    FinalScore = round(FinalScore, 2) * 10000
    print(f"Final Score: {FinalScore}") # Debugging line to check the final score

    gameFrame.pack_forget()
    infoFrame.pack_forget()

    for widget in loseFrame.winfo_children():
        widget.destroy()
    loseFrame.pack()
    # Crea el label de "You Lose" aquí
    loseLabel = tk.Label(loseFrame,
                         text="You Lose",
                         bg="black",
                         highlightbackground="purple",
                         highlightthickness=2,
                         fg="purple",
                         font=("arial", 50),
                         padx=5,
                         pady=5)
    if not lost:
        loseLabel.config(text="You Win")

    losetime = tk.Label(loseFrame,
                        font=("arial", 20),
                        text="Tiempo:\t" + str(round(finalTime, 2)),
                        bg="black",
                        fg="white")

    loseScore = tk.Label(loseFrame,
                         font=("arial", 20),
                         text="Puntuacion:\t" + str(round(FinalScore, 2)),
                         bg="black",
                         fg="white")

    lose_rePlay_Frame = tk.Frame(loseFrame,
                                highlightbackground="green yellow",
                                highlightthickness=1,
                                bg="black")
    lose_rePlay_Button = tk.Button(lose_rePlay_Frame,
                                  text="Reintentarlo",
                                  fg="green yellow",
                                  bg="black",
                                  font=("arial", 20),
                                  command=rePlay,
                                  border=0)
    lose_Menu_Frame = tk.Frame(loseFrame,
                             highlightbackground="green yellow",
                             highlightthickness=1,
                             bg="black")
    lose_Menu_Button = tk.Button(lose_Menu_Frame,
                                text="Menu",
                                fg="green yellow",
                                bg="black",
                                font=("arial", 20),
                                command=lose_menu,
                                border=0,
                                activebackground="green yellow")
    lose_exit_Frame = tk.Frame(loseFrame,
                             highlightbackground="magenta2",
                             highlightthickness=1,
                             bg="black")
    lose_exit_Button = tk.Button(lose_exit_Frame,
                                text="Salir",
                                fg="magenta2",
                                bg="black",
                                font=("arial", 20),
                                command=salir,
                                border=0,
                                activebackground="magenta2")

    # pedir nombre y guardar puntaje
    def guardar():
        nombre = nombreEntry.get()
        if nombre.strip():
            guardarPuntaje(nombre, FinalScore)
        else:
            messagebox.showwarning("Aviso", "Por favor, ingresa un nombre.")

    formFrame = tk.Frame(loseFrame, bg="black")
    nombreLabel = tk.Label(formFrame,
                           text="Nombre:",
                           bg="black",
                           fg="white",
                           font=("arial", 14))
    nombreEntry = tk.Entry(formFrame,
                           font=("arial", 14),
                           bg="gray20",
                           fg="white",
                           insertbackground="white",
                           relief="flat",
                           width=15)
    guardarBtn = tk.Button(formFrame,
                          text="Guardar",
                          command=guardar,
                          font=("arial", 14),
                          bg="green yellow",
                          fg="black",
                          activebackground="yellow",
                          activeforeground="black",
                          relief="flat",
                          padx=8,
                          pady=3)

    # Empaquetar la pedida de nombre en horizontal
    nombreLabel.pack(side="left", padx=(0,5))
    nombreEntry.pack(side="left", padx=(0,5))
    guardarBtn.pack(side="left")

    # Empaqueta los widgets en el orden correcto
    loseLabel.pack(pady=50)
    losetime.pack()
    loseScore.pack(pady=20)
    lose_rePlay_Button.pack()
    lose_rePlay_Frame.pack(pady=40)
    lose_Menu_Button.pack()
    lose_Menu_Frame.pack(pady=5)
    lose_exit_Button.pack()
    lose_exit_Frame.pack(pady=20)
    formFrame.pack(pady=15) # frame para agrupar y alinear el formulario de nombre y botón guarda

```
## Pantalla final
Al determinar si se pierde o se gana, se muestra la pantalla final, esta se compone de widgets creados de forma similar al menu
```python
loseFrame.pack()
    # Crea el label de "You Lose" aquí
    loseLabel = tk.Label(loseFrame,
                         text="You Lose",
                         bg="black",
                         highlightbackground="purple",
                         highlightthickness=2,
                         fg="purple",
                         font=("arial", 50),
                         padx=5,
                         pady=5)
    if not lost:
        loseLabel.config(text="You Win")

    losetime = tk.Label(loseFrame,
                        font=("arial", 20),
                        text="Tiempo:\t" + str(round(finalTime, 2)),
                        bg="black",
                        fg="white")

    loseScore = tk.Label(loseFrame,
                         font=("arial", 20),
                         text="Puntuacion:\t" + str(round(FinalScore, 2)),
                         bg="black",
                         fg="white")

    lose_rePlay_Frame = tk.Frame(loseFrame,
                                highlightbackground="green yellow",
                                highlightthickness=1,
                                bg="black")
    lose_rePlay_Button = tk.Button(lose_rePlay_Frame,
                                  text="Reintentarlo",
                                  fg="green yellow",
                                  bg="black",
                                  font=("arial", 20),
                                  command=rePlay,
                                  border=0)
    lose_Menu_Frame = tk.Frame(loseFrame,
                             highlightbackground="green yellow",
                             highlightthickness=1,
                             bg="black")
    lose_Menu_Button = tk.Button(lose_Menu_Frame,
                                text="Menu",
                                fg="green yellow",
                                bg="black",
                                font=("arial", 20),
                                command=lose_menu,
                                border=0,
                                activebackground="green yellow")
    lose_exit_Frame = tk.Frame(loseFrame,
                             highlightbackground="magenta2",
                             highlightthickness=1,
                             bg="black")
    lose_exit_Button = tk.Button(lose_exit_Frame,
                                text="Salir",
                                fg="magenta2",
                                bg="black",
                                font=("arial", 20),
                                command=salir,
                                border=0,
                                activebackground="magenta2")
    formFrame = tk.Frame(loseFrame, bg="black")
    nombreLabel = tk.Label(formFrame,
                           text="Nombre:",
                           bg="black",
                           fg="white",
                           font=("arial", 14))
    nombreEntry = tk.Entry(formFrame,
                           font=("arial", 14),
                           bg="gray20",
                           fg="white",
                           insertbackground="white",
                           relief="flat",
                           width=15)
    guardarBtn = tk.Button(formFrame,
                          text="Guardar",
                          command=guardar,
                          font=("arial", 14),
                          bg="green yellow",
                          fg="black",
                          activebackground="yellow",
                          activeforeground="black",
                          relief="flat",
                          padx=8,
                          pady=3)
```
y estos se empaquetan en el orden correcto:
```python
    loseLabel.pack(pady=50)
    losetime.pack()
    loseScore.pack(pady=20)
    lose_rePlay_Button.pack()
    lose_rePlay_Frame.pack(pady=40)
    lose_Menu_Button.pack()
    lose_Menu_Frame.pack(pady=5)
    lose_exit_Button.pack()
    lose_exit_Frame.pack(pady=20)
    formFrame.pack(pady=15)
```
En la pantalla final se proponen 3 botones ademas del Entry para guardar el puntaje asociado con un nombre, el primero boton permite reintentar el juego desde 0, para ello es necesario volver a crear los botones y reiniciar todas las variables globales del mapa, esto se realiza en la funcion rePlay()
```python
def rePlay():
    global map, buttons, mapGenerated, remainingShields, startTime, casillasCubiertas, currentFlags, remainingBombs, remainingFlags
    # Oculta el frame de derrota y muestra el del juego
    startTime = time.time()
    loseFrame.pack_forget()
    infoFrame.pack()
    gameFrame.pack()
    # Limpiar el frame del juego
    for widget in gameFrame.winfo_children():
        widget.destroy()
    # Reiniciar variables
    map = []
    buttons = []
    mapGenerated = False
    remainingShields = 0
    casillasCubiertas = 0
    currentFlags = 0
    remainingBombs = bombs
    remainingFlags = bombs
    # Volver a crear la matriz y los botones
    for i in range(height):
        newList = []
        for j in range(width):
            newList.append(0)
        map.append(newList)
    for i in range(height):
        otherNewList = []
        for j in range(width):
            otherNewList.append(0)
        buttons.append(otherNewList)
    for i in range(height):
        for j in range(width):
            currentName = str(i)+str(False)+str(j)
            cell_frame = tk.Frame(gameFrame,
                                  highlightbackground="purple",
                                  highlightthickness=1,
                                  bg="black",
                                  width=40,
                                  height=40)
            cell_frame.grid(row=i, column=j)
            
            button  = tk.Button(cell_frame,
                    name = str(i)  +str(j),
                    bg="black",
                    
                    border=0,
                    fg="white",
                    width=4,
                    height=2,
                    activebackground="green yellow",
                    command =  lambda buttonName = currentName: buttonClick(map,buttonName,buttons))
            button.pack()
            if sys.platform == "darwin":
                button.bind("<Button-2>", flag)
            else:
                button.bind("<Button-3>", flag)
            buttons[i][j] = button
```
 El boton Salir funciona gracias a la funcion salir()
 ```python
def salir():
    myApp.destroy()
```
Para guardar la puntuacion se llama a la funcion guardaarpuntaje.

## Sistema de Puntajes

### Algoritmo de ordenamiento - Quicksort

Se implementa una versión personalizada del algoritmo `quicksort` que permite ordenar las puntuaciones en orden descendente, considerando la posición `[1]` de cada tupla (es decir, el puntaje del jugador).

```python
def quicksort(lista):
    if len(lista) <= 1:
        return lista
    
    pivote = lista[0]
    iguales = [pivote]
    mayores = []
    menores = []

    for elemento in lista[1:]:
        if elemento[1] > pivote[1]:
            mayores.append(elemento)
        elif elemento[1] < pivote[1]:
            menores.append(elemento)
        else:
            iguales.append(elemento)

    return quicksort(mayores) + iguales + quicksort(menores)
```

> Este algoritmo divide la lista en elementos mayores, menores e iguales al pivote, aplicando recursividad. Así se asegura que los puntajes más altos estén al inicio.

---

### Guardado de puntajes

La función `guardarPuntaje()` es responsable de almacenar las puntuaciones de los jugadores en un archivo de Excel (`puntajes.xlsx`). Se asegura de conservar solo el **mejor puntaje de cada jugador**.

```python
def guardarPuntaje(nombre, puntaje, archivo="puntajes.xlsx"):
    if os.path.exists(archivo):
        libro = load_workbook(archivo)
        hoja = libro.active
    else:
        libro = Workbook()
        hoja = libro.active
        hoja.append(["Nombre", "Puntaje"])

    datos = {}
    for fila in hoja.iter_rows(min_row=2, values_only=True):
        nombreExistente, puntajeExistente = fila
        if nombreExistente not in datos or puntajeExistente > datos[nombreExistente]:
            datos[nombreExistente] = puntajeExistente

    if nombre in datos:
        if puntaje > datos[nombre]:
            datos[nombre] = puntaje
    else:
        datos[nombre] = puntaje

    libro.remove(hoja)
    hoja = libro.create_sheet(title="Sheet")
    hoja.append(["Nombre", "Puntaje"])
    for nombreGuardado, puntajeGuardado in datos.items():
        hoja.append([nombreGuardado, puntajeGuardado])

    libro.save(archivo)
    print(f"Puntaje guardado: {nombre} - {puntaje}")
```

> La función verifica si el archivo ya existe. Si no, lo crea. Luego compara los puntajes previos y solo guarda el nuevo si es mayor. Finalmente, sobrescribe la hoja entera con los datos actualizados.

---

### Mostrar Top 10

La función `mostrarTop10()` se encarga de leer el archivo de puntajes, ordenarlos con `quicksort()` y desplegar en pantalla los 10 mejores puntajes.

```python
def mostrarTop10(archivo="puntajes.xlsx"):
    if not os.path.exists(archivo):
        print("Archivo no encontrado.")
        return

    libro = load_workbook(archivo)
    hoja = libro.active

    datos = []
    for fila in hoja.iter_rows(min_row=2, values_only=True):
        nombre, puntaje = fila
        datos.append((nombre, puntaje))

    datosOrdenados = quicksort(datos)
    top10 = datosOrdenados[:10]

    mensaje = ""
    for i, (nombre, puntaje) in enumerate(top10, start=1):
        mensaje += f"{i}. {nombre} - {puntaje}\n"

    menu_frame.pack_forget()
    top_Frame.pack()
    top_Label.config(text=mensaje)
    return_Button_Frame.pack()
```

> Se muestran los datos directamente en la interfaz gráfica con etiquetas `tk.Label` y estructuras `tk.Frame`.

---

### Regresar al menú

```python
def return_Frame():
    top_Frame.pack_forget()
    return_Button_Frame.pack_forget()
    menu_frame.pack()
```

> Esta función permite regresar al menú principal desde el Top 10, ocultando los marcos que ya no se necesitan.

---

### Interfaz gráfica del Top 10

Se define un nuevo `Frame` junto con sus etiquetas (`Label`) y botón (`Button`) que permite mostrar la tabla de posiciones con estilo visual coherente al resto de la aplicación.

```python
top_Frame = tk.Frame(myApp,
                     bg="black",
                     highlightbackground="magenta3",
                     highlightthickness=1,
                     width="500",
                     height="600")
top_Frame.pack_propagate(False)

top_title_Label = tk.Label(top_Frame,
                           bg="black",
                           font = ("",30),
                           fg="white",
                           text="Top Score")

top_Label = tk.Label(top_Frame,
                     text="",
                     bg="black",
                     fg="white",
                     font = ("",20),
                     pady=20)

return_Button_Frame = tk.Frame(myApp,
                               bg="black",
                               highlightbackground="green yellow",
                               highlightthickness=1)

return_Button = tk.Button(return_Button_Frame,
                          bg="black",
                          fg="white",
                          text="Regresar",
                          font = ("",20),
                          command=return_Frame
                          )

top_title_Label.pack(pady=50)
top_Label.pack()
return_Button.pack()
```

> El botón "Regresar" ejecuta la función `return_Frame()` que permite volver al menú principal.
