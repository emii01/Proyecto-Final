import pygame
import sys

pygame.init()

###ventana   
ANCHO = 800
ALTO = 600
VENTANA = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Brick Breaker")

BLANCO = (255, 255, 255)
NEGRO = (0, 0, 0)
ROJO = (255, 0, 0)
AZUL = (0, 0, 255)

FPS = 60
clock = pygame.time.Clock()

corazon = pygame.image.load("corazon.png")
corazon = pygame.transform.scale(corazon, (32, 32))

vidas = 3

MAX_VELOCIDAD = 7
INCREMENTO_VELOCIDAD = 0.3

###clase pelota
class Pelota:
    def __init__(self, x, y, radio, velocidad_x, velocidad_y):
        self.x = x
        self.y = y
        self.radio = radio
        self.velocidad_x = velocidad_x
        self.velocidad_y = velocidad_y

    def mover(self):
        self.x += self.velocidad_x
        self.y += self.velocidad_y

        ###rebote en los bordes
        if self.x - self.radio <= 0 or self.x + self.radio >= ANCHO:
            self.velocidad_x *= -1
        if self.y - self.radio <= 0:
            self.velocidad_y *= -1

    def dibujar(self):
        pygame.draw.circle(VENTANA, BLANCO, (self.x, self.y), self.radio)

    def rect(self):
        return pygame.Rect(self.x - self.radio, self.y - self.radio, self.radio * 2, self.radio * 2)

###clase pala
class Pala:
    def __init__(self, x, y, ancho, alto, velocidad):
        self.rect = pygame.Rect(x, y, ancho, alto)
        self.velocidad = velocidad

    def mover(self, teclas):
        if teclas[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.velocidad
        if teclas[pygame.K_RIGHT] and self.rect.right < ANCHO:
            self.rect.x += self.velocidad

    def dibujar(self):
        pygame.draw.rect(VENTANA, AZUL, self.rect)

###clase ladrillos
class Ladrillo:
    def __init__(self, x, y, ancho, alto):
        self.rect = pygame.Rect(x, y, ancho, alto)

    def dibujar(self):
        pygame.draw.rect(VENTANA, ROJO, self.rect)

def manejar_colisiones(pelota, pala, ladrillos):
    ###colisión con la pala
    if pelota.rect().colliderect(pala.rect) and pelota.velocidad_y > 0:
        pelota.velocidad_y *= -1

    ###colisión con los ladrillos
    for ladrillo in ladrillos[:]:
        if pelota.rect().colliderect(ladrillo.rect):
            pelota.velocidad_y *= -1
            ladrillos.remove(ladrillo)

             ###incremento velocidad de la pelota
            if abs(pelota.velocidad_x) < MAX_VELOCIDAD:
                pelota.velocidad_x += INCREMENTO_VELOCIDAD if pelota.velocidad_x > 0 else -INCREMENTO_VELOCIDAD
            if abs(pelota.velocidad_y) < MAX_VELOCIDAD:
                pelota.velocidad_y += INCREMENTO_VELOCIDAD if pelota.velocidad_y > 0 else -INCREMENTO_VELOCIDAD

pelota = Pelota(ANCHO // 2, ALTO // 2, 10, 4, -4)
pala = Pala(ANCHO // 2 - 60, ALTO - 20, 120, 10, 6)
ladrillos = [Ladrillo(x, y, 60, 20) for x in range(0, ANCHO, 62) for y in range(0, 200, 22)]

running = True
while running:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            running = False

    teclas = pygame.key.get_pressed()

    pelota.mover()
    pala.mover(teclas)
    manejar_colisiones(pelota, pala, ladrillos)
   
    ###si la pelota cae fuera
    if pelota.y - pelota.radio > ALTO:
        vidas -= 1
        pelota.x, pelota.y = ANCHO // 2, ALTO // 2
        pelota.velocidad_x, pelota.velocidad_y = 4, -4
        if vidas == 0:
            print("¡Perdiste!")
            running = False

    VENTANA.fill(NEGRO)
    pelota.dibujar()
    pala.dibujar()
    for ladrillo in ladrillos:
        ladrillo.dibujar()

    ###condición fin del juego
    for i in range(vidas):
       VENTANA.blit(corazon, (10 + i * 40, 10))

    if not ladrillos:
        print("Ganaste!")
        running = False

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()