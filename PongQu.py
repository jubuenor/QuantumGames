import random
import pygame
from pygame import mixer
import sys

pygame.init()
mixer.init()


screen = pygame.display.set_mode((1280, 720))
screen.fill((0, 0, 0))


class Entidad:
    def __init__(self, x, y, movx, movy):
        self.x = x
        self.y = y
        self.movx = movx
        self.movy = movy

    def get_x(self):
        return self.x

    def get_y(self):
        return self.y

    def get_movx(self):
        return self.movx

    def get_movy(self):
        return self.movy

    def set_x(self, x):
        self.x = x

    def set_y(self, y):
        self.y = y

    def set_movx(self, movx):
        self.movx = movx

    def set_movy(self, movy):
        self.movy = movy


class Paddle(Entidad):
    img = [pygame.image.load("Paddle/Normal/1.png"), pygame.image.load("Paddle/Normal/2.png"),
           pygame.image.load("Paddle/Normal/3.png"), pygame.image.load("Paddle/Normal/4.png"),
           pygame.image.load("Paddle/Normal/5.png"), pygame.image.load("Paddle/Normal/6.png"),
           pygame.image.load("Paddle/Normal/7.png"), pygame.image.load("Paddle/Normal/8.png")]
    img2 = [pygame.image.load("Paddle/Grande/1.png"), pygame.image.load("Paddle/Grande/2.png"),
            pygame.image.load("Paddle/Grande/3.png"), pygame.image.load("Paddle/Grande/4.png"),
            pygame.image.load("Paddle/Grande/5.png"), pygame.image.load("Paddle/Grande/6.png"),
            pygame.image.load("Paddle/Grande/7.png"), pygame.image.load("Paddle/Grande/8.png")]
    img3 = [pygame.image.load("Paddle/Power_up/1.png"), pygame.image.load("Paddle/Power_up/2.png"),
            pygame.image.load("Paddle/Power_up/3.png"), pygame.image.load("Paddle/Power_up/4.png"),
            pygame.image.load("Paddle/Power_up/5.png"), pygame.image.load("Paddle/Power_up/6.png"),
            pygame.image.load("Paddle/Power_up/7.png"), pygame.image.load("Paddle/Power_up/8.png")]

    sprite = 0
    power_up = False
    power_up_time = 0
    estado = False
    xaux = 0

    def __init__(self, x, y, movx, movy):
        super().__init__(x, y, movx, movy)

    def animacion(self):
        if self.sprite > 7:
            self.sprite = 0
        else:
            if not self.power_up:
                self.sprite += 0.075
            else:
                self.sprite += 0.033

    def draw(self,Game):
        if not self.estado and not self.power_up:
            screen.blit(self.img[int(self.sprite)], (Game.paddle.get_x() - 50, Game.paddle.get_y() - 10))
        elif self.estado and not self.power_up:
            screen.blit(self.img2[int(self.sprite)], (Game.paddle.get_x() - 100, Game.paddle.get_y() - 10))

        if self.power_up:
            screen.blit(self.img3[int(self.sprite)], (Game.paddle.get_x() - 100 - self.xaux * 2, Game.paddle.get_y() - 10))
            if self.sprite > 7:
                self.estado = True
                self.power_up = False
                self.xaux = 50
            elif self.sprite + 1 / int(self.sprite + 1) == 1:
                self.xaux += 7

    def mov(self,Game):
        x, y = pygame.mouse.get_pos()
        Game.paddle.set_x(x)


class Bola(Entidad):
    global score
    img = pygame.image.load("Bola/1.png")
    img2 = [pygame.image.load("Bola/Vanish/1.png"), pygame.image.load("Bola/Vanish/2.png"),
            pygame.image.load("Bola/Vanish/3.png"), pygame.image.load("Bola/Vanish/4.png"),
            pygame.image.load("Bola/Vanish/5.png"), pygame.image.load("Bola/Vanish/6.png"),
            pygame.image.load("Bola/Vanish/7.png"), pygame.image.load("Bola/Vanish/8.png")]
    sprite = 0
    vanish_estado = False

    def __init__(self, x, y, movx, movy, estado):
        super().__init__(x, y, movx, movy)
        self.estado = estado
        self.hits = -1

    def draw(self):
        screen.blit(self.img, (self.x - 10, self.y - 10))

    def mov(self):
        self.x += self.movx
        self.y += self.movy

        if self.x > 1280:
            self.movx = -self.movx
        if self.x < 0:
            self.movx = -self.movx

        if self.y > 720:
            self.estado = False
        if self.y < 0:
            self.movy = -self.movy

    def hit(self, brick,Game):
        if random.randint(1, 2) == 1:
            brick.set_vida(brick.get_vida() - 1)
            self.hits += 1
            Game.score += 100 + self.hits * 50
            mixer.find_channel().play(Game.hit_sonido)
        else:
            mixer.find_channel().play(Game.vanish_sonido)
            self.vanish_estado = True
            self.hits = 0

    def vanish(self):
        if self.vanish_estado:
            if self.sprite > 7:
                self.sprite = 0
                self.vanish_estado = False
                self.estado = False
            else:
                screen.blit(self.img2[int(self.sprite)], (self.x - 10, self.y - 10))
                self.sprite += 0.075

    def get_estado(self):
        return self.estado

    def set_estado(self, estado):
        self.estado = estado


class Brick(Entidad):
    img = [pygame.image.load("Brick/1.png"), pygame.image.load("Brick/2.png"), pygame.image.load("Brick/3.png"),
           pygame.image.load("Brick/4.png")]  ##120x60-61

    def __init__(self, x, y, movx, movy, vida):  ##100,50
        super().__init__(x, y, movx, movy)
        self.vida = vida

    def draw(self):
        if 0 <= self.vida < 4:
            screen.blit(self.img[3 - self.vida], (self.x, self.y))

    def get_vida(self):
        return self.vida

    def set_vida(self, vida):
        self.vida = vida


class Mapa:  ##9x3
    matriz = []

    def __init__(self):
        for i in range(9):
            for j in range(3):
                self.matriz.append(Brick(100 + 120 * i, 50 + 60 * j, 0, 0, random.randint(0, 3)))

    def draw(self):
        for obj in self.matriz:
            obj.draw()


class Background(Entidad):
    win_img = pygame.image.load("Background/win.png").convert_alpha()
    lose_img = pygame.image.load("Background/lose.png").convert_alpha()

    opacidad = 0

    def __init__(self, x, y, movx, movy, img):
        super().__init__(x, y, movx, movy)
        self.img = img

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

    def fade(self, img, x, y):
        global lose

        if self.opacidad < 255:
            self.opacidad += 5
        else:
            return True
        img.set_alpha(self.opacidad)
        screen.blit(img, (x, y))
        pygame.time.delay(4)
        pygame.display.update()

    def set_img(self, img):
        self.img = img


class Power_up(Entidad):

    def __init__(self, x, y, movx, movy, estado, img):
        super().__init__(x, y, movx, movy)
        self.estado = estado
        self.xaux = x
        self.img = img

    def mov(self):
        self.y += self.movy
        self.x += self.movx
        if 0 < self.x < 1280:
            self.movx = -self.movx

        if self.xaux - random.randint(50, 100) < self.x < self.xaux + random.randint(50, 100):
            self.movx = random.uniform(-3, 3)
        if self.y > 720:
            self.estado = False

    def draw(self):
        screen.blit(self.img, (self.x - 31, self.y - 26))

    def hit(self, x, xaux, y,Game):
        if x - xaux - 50 < self.x < x + xaux + 50 and y - 10 < self.y < y + 10:
            mixer.find_channel().play(Game.power_up_sonido)
            self.estado = False
            return True

    def get_estado(self):
        return self.estado

    def set_estado(self, estado):
        self.estado = estado

    def set_xaux(self, xaux):
        self.xaux = xaux


class Maquina(Entidad):
    img = pygame.image.load("Maquina/1.png")
    estado = False

    def __init__(self, x, y, movx, movy):
        super().__init__(x, y, movx, movy)

    def draw(self):
        screen.blit(self.img, (self.x, self.y))

    def mov(self):
        if self.x > 1230 and not self.estado:
            self.x -= self.movx
        elif self.x <= 1230:
            self.estado = True

        if self.estado and self.x < 1380:
            self.x += self.movx
        elif self.x >= 1380:
            self.estado = False
            self.x = 1380


class Texto(Entidad):
    fuente = pygame.font.Font('freesansbold.ttf', 24)

    def __init__(self, x, y, movx, movy, color, texto):
        super().__init__(x, y, movx, movy)
        self.texto = texto
        self.color = color

    def draw(self):
        img = self.fuente.render(self.texto, True, self.color)
        screen.blit(img, (self.x, self.y))

    def get_texto(self):
        return self.texto

    def set_texto(self, texto):
        self.texto = texto

class PongQu():
    def __init__(self):
        self.hit_sonido = mixer.Sound("Sonidos/hit.wav")
        self.vanish_sonido = mixer.Sound("Sonidos/vanish.wav")
        self.power_up_sonido = mixer.Sound("Sonidos/power_up.wav")
        self.maquina_sonido = mixer.Sound("Sonidos/maquina.wav")
        fondo_sondo = mixer.Sound("Sonidos/fondo.wav")
        self.contador_sonido = mixer.Sound("Sonidos/contador.wav")
        self.continuar_sonido = mixer.Sound("Sonidos/continuar.wav")
        Canal_0 = mixer.Channel(0)
        mixer.set_num_channels(64)
        Canal_0.set_volume(0.1)
        Canal_0.play(fondo_sondo, -1)
        self.running = True
        self.score = 0
        pygame.display.set_caption("Quantum Brick Breaker")
    def run(self):
        self.paddle = Paddle(640, 650, 0, 0)
        bolas = [Bola(200, 496, 1.5, 0, True), Bola(618, 496, 1.5, 0, True)]  # Bola(400, 400, 1.5, 1.5, True)
        pbolas = Power_up(random.randint(20, 1260), random.randint(-400, -50), random.uniform(-1, 1), 0,
                        True, pygame.image.load("Power_up/1.png"))
        ppaddle = Power_up(random.randint(20, 1260), random.randint(-400, -50), random.uniform(-1, 1), 0,
                        True, pygame.image.load("Power_up/2.png"))
        maquina = Maquina(1380, 300, 1, 0)
        mapa1 = Mapa()
        background = Background(0, 0, 0, 0, pygame.image.load("Background/2.png").convert_alpha())
        scoreimg = Texto(15, 681, 0, 0, (255, 255, 255), str("Score: " + str(self.score)))
        ppaddlehud = Texto(35, 25, 0, 0, (255, 255, 255), "")
        tiempoimg = Texto(600, 400, 0, 0, (255, 255, 255), "")
        win = False
        lose = False
        bricks_destruidos = 0
        intro = True
        intro_estado = 1
        tiempo = 0
        tiempo_estado = True
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    sys.exit()
                if event.type == pygame.KEYUP:
                    if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and lose:
                        mixer.find_channel().play(self.contador_sonido)
                        self.paddle.__init__(640, 650, 0, 0)
                        bolas[0].__init__(400, 400, 0, 0, True)
                        tiempo = pygame.time.get_ticks() / 1000
                        tiempo_estado = True
                        pbolas.__init__(random.randint(20, 1260), random.randint(-400, -50), random.uniform(-1, 1),
                                        random.randint(1, 2), True, pygame.image.load("Power_up/1.png"))
                        pbolas.set_xaux(pbolas.get_x())
                        ppaddle.__init__(random.randint(20, 1260), random.randint(-400, -50), random.uniform(-1, 1),
                                        random.randint(1, 2), True, pygame.image.load("Power_up/2.png"))
                        ppaddle.set_xaux(self.paddle.get_x())
                        mapa1.__init__()
                        self.score = 0
                        lose = False
                        background.opacidad = 0

                    if (event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER) and intro:
                        mixer.find_channel().play(self.continuar_sonido)
                        intro_estado += 1
                        if intro_estado == 6:
                            mixer.find_channel().play(self.contador_sonido)

            if intro:
                background.draw()
                if intro_estado == 1:
                    if background.fade(pygame.image.load("Intro/1.png"), 115, 82):
                        screen.blit(pygame.image.load("Intro/1.png"), (115, 82))
                        background.opacidad = 0
                        intro_estado += 1
                if intro_estado == 2:
                    screen.blit(pygame.image.load("Intro/1.png"), (115, 82))
                    if background.fade(pygame.image.load("Intro/2.png"), 114, 322):
                        screen.blit(pygame.image.load("Intro/2.png"), (114, 322))
                        background.opacidad = 0
                        intro_estado += 1
                if intro_estado == 3:
                    screen.blit(pygame.image.load("Intro/1.png"), (115, 82))
                    screen.blit(pygame.image.load("Intro/2.png"), (114, 322))

                if intro_estado == 4:
                    if background.fade(pygame.image.load("Intro/3.png"), 114, 82):
                        screen.blit(pygame.image.load("Intro/3.png"), (114, 82))
                        background.opacidad = 0
                        intro_estado += 1

                if intro_estado == 5:
                    screen.blit(pygame.image.load("Intro/3.png"), (114, 82))
                    bolas[0].draw()
                    bolas[0].mov()
                    if bolas[0].get_x() > 401 and tiempo_estado:
                        screen.blit(pygame.image.load("Brick/2.png"), (411, 466))
                        bolas[0].set_movx(-bolas[0].get_movx())
                        tiempo = pygame.time.get_ticks() / 1000
                        tiempo_estado = False
                    elif bolas[0].get_x() <= 401:
                        screen.blit(pygame.image.load("Brick/1.png"), (411, 466))
                    if pygame.time.get_ticks() / 1000 >= tiempo + 1 and not tiempo_estado:
                        bolas[0].set_x(200)
                        tiempo_estado = True
                        bolas[0].set_movx(-bolas[0].get_movx())
                    elif pygame.time.get_ticks() / 1000 <= tiempo + 1:
                        screen.blit(pygame.image.load("Brick/2.png"), (411, 466))

                    if bolas[1].get_estado():
                        bolas[1].draw()
                        bolas[1].mov()
                    screen.blit(pygame.image.load("Brick/1.png"), (818, 466))
                    if bolas[1].get_x() > 808:
                        bolas[1].set_estado(False)
                        bolas[1].vanish_estado = True
                        bolas[1].vanish()
                    if bolas[1].sprite > 7:
                        bolas[1].__init__(618, 496, 1.5, 0, True)
                        bolas[1].vanish_estado = False
                        bolas[1].sprite = 0
                    pygame.display.update()

                if intro_estado == 6:
                    intro = False
                    background.set_img(pygame.image.load("Background/1.png").convert_alpha())
                    bolas.pop(1)
                    bolas[0].__init__(400, 400, 0, 0, True)
                    tiempo = pygame.time.get_ticks() / 1000
            if not lose and not intro:
                background.draw()
                scoreimg.draw()
                scoreimg.set_texto(str("Score: " + str(self.score)))
                mapa1.draw()
                self.paddle.draw(self)
                self.paddle.animacion()
                self.paddle.mov(self)
                if tiempo_estado:
                    if pygame.time.get_ticks() / 1000 >= tiempo + 4:
                        bolas[0].set_movx(1.5)
                        bolas[0].set_movy(1.5)
                        tiempo_estado = False
                        ppaddle.set_movy(random.randint(1, 2))
                        pbolas.set_movy(random.randint(1, 2))
                    else:
                        tiempoimg.set_texto(str(int(tiempo + 3.5 - pygame.time.get_ticks() / 1000)))
                        tiempoimg.draw()

                # Colisiones

                for bola in bolas:
                    if bola.vanish_estado:
                        bola.vanish()
                    if bola.estado and not bola.vanish_estado:
                        bola.draw()
                        bola.mov()
                        if self.paddle.get_x() - 50 - self.paddle.xaux <= bola.get_x() <= self.paddle.get_x() and self.paddle.get_y() - 10 <= bola.get_y() <= self.paddle.get_y() + 10:
                            bola.set_y(bola.get_y() - 10)
                            mixer.find_channel().play(self.hit_sonido)
                            bola.set_movy(-bola.get_movy())
                            bola.set_movx(bola.get_movx() - 0.25)
                        if self.paddle.get_x() <= bola.get_x() <= self.paddle.get_x() + 50 + self.paddle.xaux and self.paddle.get_y() - 10 <= bola.get_y() <= self.paddle.get_y() + 10:
                            bola.set_y(bola.get_y() - 10)
                            bola.set_movy(-bola.get_movy())
                            bola.set_movx(bola.get_movx() + 0.25)
                            mixer.find_channel().play(self.hit_sonido)

                        for brick in mapa1.matriz:
                            if 0 <= brick.get_vida() < 4:
                                if brick.get_x() <= bola.get_x() - 10 <= brick.get_x() + 120:
                                    if brick.get_y() <= bola.get_y() + 10 <= brick.get_y() + 10 and bola.get_movy() > 0:
                                        bola.set_movy(-bola.get_movy())
                                        bola.hit(brick,self)
                                    if brick.get_y() + 50 <= bola.get_y() - 10 <= brick.get_y() + 60 and bola.get_movy() < 0:
                                        bola.set_movy(-bola.get_movy())
                                        bola.hit(brick,self)
                                if brick.get_y() + 10 <= bola.get_y() - 10 <= brick.get_y() + 50:
                                    if brick.get_x() <= bola.get_x() <= brick.get_x() + 40:
                                        bola.set_movx(-bola.get_movx())
                                        bola.hit(brick,self)
                                    if brick.get_x() + 80 <= bola.get_x() - 10 <= brick.get_x() + 120:
                                        bola.set_movx(-bola.get_movx())
                                        bola.hit(brick,self)

                                if brick.get_vida() < 0:
                                    bricks_destruidos += 1

                # Power_ups

                if pbolas.get_estado():
                    pbolas.draw()
                    pbolas.mov()
                    if pbolas.hit(self.paddle.get_x(), self.paddle.xaux, self.paddle.get_y(),self):
                        pbolas.set_estado(False)
                        for i in range(len(bolas)):
                            bolas.append(
                                Bola(bolas[i].get_x(), bolas[i].get_y(), -bolas[i].get_movx(), bolas[i].get_movy(), True))
                            bolas.append(
                                Bola(bolas[i].get_x(), bolas[i].get_y(), bolas[i].get_movx(), -bolas[i].get_movy(), True))
                else:
                    if random.randint(1, 1) == 1:
                        pbolas.__init__(random.randint(20, 1260), random.randint(-400, -50), random.uniform(-1, 1),
                                        random.randint(1, 2), True, pygame.image.load("Power_up/1.png"))
                        pbolas.set_xaux(pbolas.get_x())

                if ppaddle.get_estado() and not self.paddle.estado:
                    ppaddle.draw()
                    ppaddle.mov()
                    if ppaddle.hit(self.paddle.get_x(), self.paddle.xaux, self.paddle.get_y(),self):
                        ppaddle.set_estado(False)
                        self.paddle.power_up = True
                        self.paddle.power_up_time = pygame.time.get_ticks() / 1000

                else:
                    if random.randint(1, 1) == 1:
                        ppaddle.__init__(random.randint(20, 1260), random.randint(-400, -50), random.uniform(-1, 1),
                                        random.randint(1, 2), True, pygame.image.load("Power_up/2.png"))
                        ppaddle.set_xaux(self.paddle.get_x())
                # Maquina

                if maquina.estado and maquina.get_x() < 1380:
                    maquina.mov()
                    maquina.draw()

                # self.paddle

                if self.paddle.estado:
                    screen.blit(pygame.image.load("Power_up/2.png"), (10, 10))
                    ppaddlehud.set_texto(str(int(self.paddle.power_up_time + 6.5 - pygame.time.get_ticks() / 1000)))
                    ppaddlehud.draw()
                    ##print(pygame.time.get_ticks() / 1000, "==", self.paddle.power_up_time + 5)
                    if pygame.time.get_ticks() / 1000 >= self.paddle.power_up_time + 6:
                        self.paddle.estado = False
                        self.paddle.xaux = 0

                # Eliminar y agregar bolas

                if len(bolas) > 1:
                    for i in range(len(bolas)):
                        if i < len(bolas) > 1:
                            if not bolas[i].get_estado():
                                bolas.pop(i)
                else:
                    if not bolas[0].get_estado() and bolas[0].get_y() < 720:
                        maquina.mov()
                        maquina.draw()
                        if maquina.estado:
                            mixer.find_channel().play(self.maquina_sonido)
                            bolas[0].__init__(maquina.get_x() + 20, maquina.get_y() + 35, -1.5, 1.5, True)

            if len(bolas) == 1 and not bolas[0].get_estado() and bolas[0].get_y() > 720:
                if background.fade(pygame.image.load("Background/lose.png").convert_alpha(), 0, 0):
                    screen.blit(pygame.image.load("Background/lose.png").convert_alpha(), (0, 0))
                    scoreimg.draw()
                    lose = True
            if bricks_destruidos == len(mapa1.matriz):
                if background.fade(pygame.image.load("Background/win.png").convert_alpha(), 0, 0):
                    screen.blit(pygame.image.load("Background/win.png").convert_alpha(), (0, 0))
                    scoreimg.draw()
                    win = True

            pygame.display.update()