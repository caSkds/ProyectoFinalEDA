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

#### Radares 
Los radares primero 


#### Bombas

#### Escudos

#### Power Ups



### Victoria y derrota

## Pantalla final
