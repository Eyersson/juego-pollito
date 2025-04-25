import turtle
import random
import time

# Configuración de la ventana
win = turtle.Screen()
win.title("Pollito Cruza la Calle")
win.bgcolor("lightgray")
win.setup(width=600, height=600)
win.tracer(0)  # Para mejorar el rendimiento

# Crear el pollito
pollito = turtle.Turtle()
pollito.shape("square")  # Forma simple del pollito
pollito.color("yellow")
pollito.penup()
pollito.goto(0, -250)
pollito.setheading(90)  # Apunta hacia arriba

# Mostrar vidas
vidas = 3
vida_turtle = turtle.Turtle()
vida_turtle.hideturtle()
vida_turtle.penup()
vida_turtle.goto(-280, 260)
vida_turtle.color("black")
vida_turtle.write(f"Vidas: {vidas}", font=("Arial", 16, "bold"))

# Mostrar puntaje
puntaje = 0
puntaje_turtle = turtle.Turtle()
puntaje_turtle.hideturtle()
puntaje_turtle.penup()
puntaje_turtle.goto(100, 260)
puntaje_turtle.color("black")
puntaje_turtle.write(f"Puntaje: {puntaje}", font=("Arial", 16, "bold"))

# Funciones para actualizar el puntaje
def actualizar_vidas():
    vida_turtle.clear()
    vida_turtle.write(f"Vidas: {vidas}", font=("Arial", 16, "bold"))

def actualizar_puntaje():
    puntaje_turtle.clear()
    puntaje_turtle.write(f"Puntaje: {puntaje}", font=("Arial", 16, "bold"))

# Funciones de control del pollito
def mover_arriba():
    y = pollito.ycor()
    if y < 280:
        pollito.sety(y + 20)

def mover_abajo():
    y = pollito.ycor()
    if y > -280:
        pollito.sety(y - 20)

def mover_izquierda():
    x = pollito.xcor()
    if x > -280:
        pollito.setx(x - 20)

def mover_derecha():
    x = pollito.xcor()
    if x < 280:
        pollito.setx(x + 20)

win.listen()
win.onkeypress(mover_arriba, "Up")
win.onkeypress(mover_abajo, "Down")
win.onkeypress(mover_izquierda, "Left")
win.onkeypress(mover_derecha, "Right")

# Crear los carros
carros = []

# Velocidad fija para todos los carros
velocidad_fija = 12  # Velocidad fija para los carros

# Crear más carros y asignarlos a los cuatro carriles
for _ in range(15):  # Aumentar la cantidad de carros
    carro = turtle.Turtle()
    carro.shape("square")
    carro.shapesize(stretch_wid=1, stretch_len=2)
    carro.color("black")  # Todos los carros serán negros
    carro.penup()

    # Asignamos cada carro a un carril en la autopista
    y = random.choice([-150, -50, 50, 150])  # Carriles en la autopista
    carro.goto(random.randint(-300, 300), y)

    # Dirección del carro según el carril
    if y == 150:  # Carril superior, movimiento hacia la izquierda
        carro.direction = "left"
    elif y == -150:  # Carril inferior, movimiento hacia la derecha
        carro.direction = "right"
    elif y == 50:  # Carril en el medio, movimiento hacia la izquierda
        carro.direction = "left"
    else:  # Carril en el medio, movimiento hacia la derecha
        carro.direction = "right"

    # Asignamos la velocidad fija a todos los carros
    carro.speed = velocidad_fija
    carros.append(carro)

# Dibujar la carretera (4 carriles)
lineas = turtle.Turtle()
lineas.hideturtle()
lineas.color("white")
lineas.pensize(2)
lineas.penup()
for y in range(-250, 300, 100):
    lineas.goto(-300, y)
    lineas.setheading(0)
    for _ in range(15):
        lineas.pendown()
        lineas.forward(10)
        lineas.penup()
        lineas.forward(30)

# Función para dibujar casas
def dibujar_casa(x, y):
    casa = turtle.Turtle()
    casa.hideturtle()
    casa.penup()
    casa.goto(x, y)
    casa.color("brown")
    casa.begin_fill()
    # Dibujar la base de la casa
    for _ in range(4):
        casa.forward(50)
        casa.right(90)
    casa.end_fill()
    
    casa.goto(x + 25, y + 50)  # Colocar el techo
    casa.begin_fill()
    # Dibujar el techo triangular
    for _ in range(3):
        casa.forward(50)
        casa.left(120)
    casa.end_fill()

# Dibujar casas a los lados de la carretera
for i in range(-280, 300, 100):
    if i != 0:  # Evitar colocar casas en el centro de la carretera
        dibujar_casa(i, 200)  # Lado izquierdo
        dibujar_casa(i, -250)  # Lado derecho

# Sonido de colisión
def sonido_colision():
    try:
        win.bgcolor("red")  # Cambio de color de fondo cuando choca
        time.sleep(0.2)
        win.bgcolor("lightgray")  # Restaurar el fondo
    except:
        pass

# Loop principal del juego
game_on = True
cooldown = 0  # Tiempo de invulnerabilidad temporal

while game_on:
    win.update()
    time.sleep(0.03)  # Velocidad del juego

    # Mover carros
    for carro in carros:
        x = carro.xcor()

        # Si el carro va hacia la izquierda
        if carro.direction == "left":
            carro.setx(x - carro.speed)
            if carro.xcor() < -320:  # Si se sale de la pantalla por la izquierda
                carro.setx(320)  # Vuelve al otro lado
                carro.sety(random.choice([150, 50]))  # Reaparece en la calzada izquierda

        # Si el carro va hacia la derecha
        elif carro.direction == "right":
            carro.setx(x + carro.speed)
            if carro.xcor() > 320:  # Si se sale de la pantalla por la derecha
                carro.setx(-320)  # Vuelve al otro lado
                carro.sety(random.choice([-150, -50]))  # Reaparece en la calzada derecha

        # Detectar colisión con el pollito
        if pollito.distance(carro) < 20:
            vidas -= 1
            sonido_colision()  # Sonido de colisión
            print(f"💥 ¡Te golpeó un carro! Vidas restantes: {vidas}")
            actualizar_vidas()
            pollito.goto(0, -250)  # Reiniciar posición del pollito

            if vidas == 0:
                print("💀 ¡El pollito perdió todas sus vidas!")
                game_on = False

    # Verificar si el pollito cruzó con éxito
    if pollito.ycor() > 280:
        puntaje += 1
        print("🎉 ¡El pollito cruzó la calle con éxito!")
        pollito.goto(0, -250)  # Reiniciar posición del pollito
        actualizar_puntaje()

# Final
print("¡Juego Terminado!")
turtle.done()


  

