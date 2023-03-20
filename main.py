import turtle as tur
import time
import random

class SnakeGame():
    def __init__(self, color='green', width=600, heigth=600):
        """Inicializa los componentes del juego"""
        self._sc = tur.Screen()
        self._sc.title("Juego Snake")
        self._sc.bgcolor(color)
        self._sc.setup(width, heigth)
        self._sc.tracer(0)
        # Inicializa la serpiente
        self._t_snake = tur.Turtle()
        self._t_snake.speed(0)
        self._t_snake.shape("square")
        self._t_snake.color("black")
        self._t_snake.penup()
        self._t_snake.goto(0, 0)
        # Inicializar el texto que se muestra en la pantalla
        self._t_texto = tur.Turtle()
        self._t_texto.speed(0)
        self._t_texto.shape('square')
        self._t_texto.color('white')
        self._t_texto.penup()
        self._t_texto.hideturtle()
        self._t_texto.goto(0, (heigth / 2) - 40)
        # Atributos de la clase
        self._movimiento = None
        self._delay = 0.1
        self._puntaje = 0
        self._record = 0
        self._cuerpo = []
        # Asociacion de los movimientos y las teclas
        self._sc.listen()
        self._sc.onkeypress(self._subir, 'w')
        self._sc.onkeypress(self._bajar, 's')
        self._sc.onkeypress(self._izquierda, 'a')
        self._sc.onkeypress(self._derecha, 'd')
        self._width = width
        self._heigth = heigth
        # Saca texto en pantalla
        self._mostrar_score()
        # Inicializa la manzana
        self._t_manzana = tur.Turtle()
        self._t_manzana.speed(0)
        self._t_manzana.shape("circle")
        self._t_manzana.color("red")
        self._t_manzana.penup()
        self._x_manzana = random.randint(-(width / 2) + 10, (width / 2) - 10)
        self._y_manzana = random.randint(-(heigth / 2) + 10, (heigth / 2) - 10)
        self._t_manzana.goto(self._x_manzana, self._y_manzana)

    def _subir(self):
        if self._movimiento != 'bajar':
            self._movimiento = 'subir'

    def _bajar(self):
        if self._movimiento != 'subir':
            self._movimiento = 'bajar'

    def _izquierda(self):
        if self._movimiento != 'derecha':
            self._movimiento = 'izquierda'

    def _derecha(self):
        if self._movimiento != 'izquierda':
            self._movimiento = 'derecha'

    def _move(self):
        # Obtener las coordenadas de la cabeza de la serpiente
        x = self._t_snake.xcor()
        y = self._t_snake.ycor()
        # Mover cuerpo de la serpiente
        for i in range(len(self._cuerpo) - 1, 0, -1):
            cx = self._cuerpo[i - 1].xcor()
            cy = self._cuerpo[i - 1].ycor()
            self._cuerpo[i].goto(cx, cy)

        # Mover el segmento mas cercano a la cabeza
        if len(self._cuerpo) > 0:
            self._cuerpo[0].goto(x, y)

        if self._movimiento == 'subir':
            self._t_snake.sety(y + 20)
        elif self._movimiento == 'bajar':
            self._t_snake.sety(y - 20)
        elif self._movimiento == 'izquierda':
            self._t_snake.setx(x - 20)
        elif self._movimiento == 'derecha':
            self._t_snake.setx(x + 20)

    def jugar(self):
        while True:
            self._sc.update()
            self._colision()
            self._colision_cuerpo()
            self._colision_comida()
            time.sleep(self._delay)
            self._move()
        self._sc.mainloop()

    def _colision(self):
        y = self._t_snake.ycor()
        x = self._t_snake.xcor()
        if x >= ((self._width / 2) - 10) or x <= (((self._width / 2) - 10) * -1) or y >= (
                (self._heigth / 2) - 10) or y <= (((self._heigth / 2) - 10) * -1):
            self._reset()

    def _colision_comida(self):
        if self._t_snake.distance(self._t_manzana) < 20:
            self._x_manzana = random.randint(-(self._width / 2) + 10, (self._width / 2) - 10)
            self._y_manzana = random.randint(-(self._heigth / 2) + 10, (self._heigth / 2) - 10)
            self._t_manzana.penup()
            self._t_manzana.goto(self._x_manzana, self._y_manzana)
            self._crecer_snake()
            self._delay -= 0.001
            self._puntaje += 10
            self._mostrar_score()

    def _colision_cuerpo(self):
        for s in self._cuerpo:
            if s.distance(self._t_snake) < 20:
                self._reset()

    def _reset(self):
        time.sleep(1)
        self._movimiento = None
        self._t_snake.goto(0, 0)
        # Reiniciar el cuerpo de la serpiente
        for s in self._cuerpo:
            s.ht()
        self._cuerpo.clear()
        self._delay = 0.1
        if self._record < self._puntaje:
            self._record = self._puntaje
        self._puntaje = 0
        self._mostrar_score()

    def _crecer_snake(self):
        pixel = tur.Turtle()
        pixel.speed(0)
        pixel.shape("square")
        pixel.color("orange")
        pixel.penup()
        self._cuerpo.append(pixel)
        # self._t_cuerpo.goto(0,0)

    def _mostrar_score(self):
        self._t_texto.clear()
        self._t_texto.write("PUNTAJE: {} RECORD: {}".format(self._puntaje, self._record), align='center',
                            font=('Courier', 16, 'normal'))

juego_snake = SnakeGame()
juego_snake.jugar()