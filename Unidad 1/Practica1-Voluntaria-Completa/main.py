import pygame
import random
from pygame.constants import RLEACCEL, K_d, K_p
import os
import time
import sqlite3

from sqlite3 import Error

carpeta = os.path.dirname(__file__)

def sql_connection():
    
    try:

        con = sqlite3.connect('puntos.db')

        return con

    except Error:

        print(Error)

def sql_table(con):

    cursorObj = con.cursor()

    cursorObj.execute("CREATE TABLE IF NOT EXISTS scores(puntos integer PRIMARY KEY)")

    con.commit()

con = sql_connection()

# Aqui creamos la tabla scores, que tiene como clave primaria puntos, lo he comentado porque si no da error una vez la base de datos y la tabla esta creada.
sql_table(con)



from pygame.locals import (

    K_UP,
    K_DOWN,
    K_LEFT,
    K_RIGHT,
    K_ESCAPE,
    KEYDOWN,
    QUIT

)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

pygame.init()

def cargar_score(conexion):
    sql = "SELECT * FROM scores;"
    puntos = 0
    cursor = conexion.cursor()
    cursor.execute(sql)
    points = cursor.fetchall()
    list(points)
    for i in points:
        puntos = i[0]
    return puntos

high_score = cargar_score(con)

running2 = True

while running2:

    screen.fill((135, 206, 250))

    fontmenu = pygame.font.Font(os.path.join(carpeta, "recursos/beauty.ttf"), 48)

    menu_text = fontmenu.render("WELCOME TO MY PYGAME", True, (0, 0, 0))
    screen.blit(menu_text, (200, 90))

    score_text = fontmenu.render("MAX SCORE: " + str(high_score), True, (0, 0, 0))
    screen.blit(score_text, (275, 290))

    p_text = fontmenu.render("Press P to play", True, (0, 0, 0))
    screen.blit(p_text, (285, 490))
    
    pygame.display.flip()

    for event in pygame.event.get():

        if event.type == KEYDOWN:

            if event.key == K_p:

                running2 = False

        elif event.type == QUIT:

            running2 = False

# Iniciamos el mixer.
pygame.mixer.init()

# Cargamos y ejecutamos la musica de fondo.
pygame.mixer.music.load(os.path.join(carpeta, "recursos/Apoxode_-_Electric_1.ogg"))
pygame.mixer.music.play(loops=-1)

# Cargamos todos los fiheros de sonido.
move_up_sound = pygame.mixer.Sound(os.path.join(carpeta, "recursos/Rising_putter.ogg"))
move_down_sound = pygame.mixer.Sound(os.path.join(carpeta, "recursos/Falling_putter.ogg"))
collision_sound = pygame.mixer.Sound(os.path.join(carpeta, "recursos/Collision.ogg"))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super(Player, self).__init__()
        jet = os.path.join(carpeta, "recursos/jet.png")
        self.surf = pygame.image.load(jet).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                0,
                300,
            )
        )
    
    # Mueve el jugador dependiendo de la tecla que pulse el usuario
    def update(self, pressed_keys):
        if pressed_keys[K_UP]:
            self.rect.move_ip(0, -5)
            move_up_sound.play()
        if pressed_keys[K_DOWN]:
            self.rect.move_ip(0, 5)
            move_down_sound.play()
        if pressed_keys[K_LEFT]:
            self.rect.move_ip(-5, 0)
        if pressed_keys[K_RIGHT]:
            self.rect.move_ip(5, 0)

        # Mantiene el jugador dentro de la pantalla
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH
        if self.rect.top <= 0:
            self.rect.top = 0
        if self.rect.bottom >= SCREEN_HEIGHT:
            self.rect.bottom = SCREEN_HEIGHT

# Creamos la clase Enemy
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super(Enemy, self).__init__()
        enemy = os.path.join(carpeta, "recursos/missile.png")
        self.surf = pygame.image.load(enemy).convert()
        self.surf.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = random.randint(2* nivel, 10 + 3 * nivel)
    
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Creamos la clase Cloud
class Cloud(pygame.sprite.Sprite):
    def __init__(self):
        super(Cloud, self).__init__()
        cloud = os.path.join(carpeta, "recursos/cloud.png")
        self.surf = pygame.image.load(cloud).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20 , SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = 5

    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Creamos la clase Life
class Life(pygame.sprite.Sprite):
    def __init__(self):
        super(Life, self).__init__()
        life = os.path.join(carpeta, "recursos/corazon.png")
        self.surf = pygame.image.load(life).convert()
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center=(
                random.randint(SCREEN_WIDTH + 20, SCREEN_WIDTH + 100),
                random.randint(0, SCREEN_HEIGHT),
            )
        )
        self.speed = 3
    
    def update(self):
        self.rect.move_ip(-self.speed, 0)
        if self.rect.right < 0:
            self.kill()

# Definimos la variable color
color = (135, 206, 250)

# Definimos un contador
score = 0

# Definimos un segundo contador, que contara de 0 a 500, cada vez que sea 500 se añadira un nivel
score2 = 0

# Definimos la velocidad por defecto en la que se crean los enemigos
velocitat = 500

# Definimos para mostrar el contador
def show_velocity(x, y):
    score_text = font.render("Velocity: " + str(velocitat), True, (0, 0, 0))
    screen.blit(score_text, (x, y))

# Definimos una fuente
font = pygame.font.Font(os.path.join(carpeta, "recursos/beauty.ttf"), 48)

textX = 10
textY = 10

# Definimos para mostrar el contador
def show_score(x, y):
    score_text = font.render("Score: " + str(score), True, (0, 0, 0))
    screen.blit(score_text, (x, y))

# Definimos un contador
nivel = 1

LeveltextX = 650
LeveltextY = 10

# Definimos para mostrar el contador
def show_level(x, y):
    level_text = font.render("Level: " + str(nivel), True, (0, 0, 0))
    screen.blit(level_text, (x, y))    

# Definimos un contador de vidas
vidas = 3

vidaTextX = 650
vidaTextY = 550

# Definimos una función para mostrar las vidas
def show_vidas(x, y):
    vidas_text = font.render("Lifes: " + str(vidas), True, (0, 0, 0))
    screen.blit(vidas_text, (x, y))

# Definimos un reloj para tener una buena velocidad en el juego, y que no sea injugable
clock = pygame.time.Clock()


ADDLIFE = pygame.USEREVENT + 5
pygame.time.set_timer(ADDLIFE, random.randint(10000, 50000))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, velocitat)

ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

CHANGEDARK = pygame.USEREVENT + 3
pygame.time.set_timer(CHANGEDARK, 20000)

CHANGEDEFAULT = pygame.USEREVENT + 4
pygame.time.set_timer(CHANGEDEFAULT, 40000)

# Creamos el jugador
player = Player()

# Creamos un grupo de sprites para poder almacenar todos los sprites
lifes = pygame.sprite.Group()
enemies = pygame.sprite.Group()
clouds = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
all_sprites.add(player)

running = True



while running:
    
    for event in pygame.event.get():

        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:

                running = False
            
        elif event.type == QUIT:

            running = False
        
        elif event.type == ADDENEMY:

            # Creamos un nuevo enemigo y lo añadimos al grupo 'all_sprites'
            new_enemy = Enemy()
            enemies.add(new_enemy)
            all_sprites.add(new_enemy)
            
        elif event.type == ADDCLOUD:

            # Creamos un nuevo cloud y lo añadimos al grupo 'all_sprites'
            new_cloud = Cloud()
            clouds.add(new_cloud)
            all_sprites.add(new_cloud)

        elif event.type == ADDLIFE:

            new_life = Life()
            lifes.add(new_life)
            all_sprites.add(new_life)

        elif event.type == CHANGEDARK:

            color = (35, 35, 70)

        elif event.type == CHANGEDEFAULT:

            color = (135, 206, 250)

    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)

    for e in enemies:
        if e.rect.right < 10:            
            score += 10
            score2 += 10

    if (score != 0):
        if score2 == 500:
            nivel += 1
            velocitat = 100 + (450 - 50 * nivel)
            score2 = 0

    # Actualizamos la posición del enemigo
    enemies.update()

    # Actualizamos la posición del cloud
    clouds.update()

    # Actualizamos la posición de la vida
    lifes.update()

    screen.fill(color)

    show_vidas(vidaTextX, vidaTextY)

    show_level(LeveltextX, LeveltextY)

    show_score(textX, textY)

    # Dibujamos todos los sprites que esten almacenados en el grupo 'all_sprites'
    for entity in all_sprites:

        screen.blit(entity.surf, entity.rect)

    
    if pygame.sprite.spritecollide(player, enemies, True):

        collision_sound.play()

        vidas = vidas - 1

    if pygame.sprite.spritecollide(player, lifes, True):

        if vidas == 3:

            collision_sound.play()

            vidas = vidas

        else:

            collision_sound.play()

            vidas = vidas + 1


    if vidas == 0:
    
        player.kill()
        
        running = False

    pygame.display.flip()

    # Nos aseguramos de que el programa mantiene 60 frames por segundo
    clock.tick(60)

# Paramos y salimos del mixer de la musica.
pygame.mixer.music.stop()
pygame.mixer.quit()

running3 = True

while running3:

    screen.fill((135, 206, 250))

    fontmenu = pygame.font.Font(os.path.join(carpeta, "recursos/beauty.ttf"), 48)

    menu_text = fontmenu.render("LEVEL" + str(nivel), True, (0, 0, 0))
    screen.blit(menu_text, (350, 290))

    score_text3 = fontmenu.render("SCORE: " + str(score), True, (0, 0, 0))
    screen.blit(score_text3, (320, 490))

    p_text = fontmenu.render("GAME OVER", True, (0, 0, 0))
    screen.blit(p_text, (320, 90))
    
    if (score > high_score):

        congrats = fontmenu.render("¡¡¡CONGRATS!!! ¡¡¡NEW RECORD!!!", True, (0, 0, 0))
        screen.blit(congrats, (180, 225))

    pygame.display.flip()

    for event in pygame.event.get():

        if event.type == KEYDOWN:

            if event.key == K_ESCAPE:

                running3 = False

        elif event.type == QUIT:

            running3 = False

if (score > high_score):

    try:
        sqliteConnection = sqlite3.connect('puntos.db')
        cursor = sqliteConnection.cursor()
        print("Connected to SQLite")

        sqlite_insert_with_param = """INSERT INTO scores
                            (puntos) 
                            VALUES (?);"""

        data_tuple = (score, )
        cursor.execute(sqlite_insert_with_param, data_tuple)
        sqliteConnection.commit()
        print("Python Variables inserted successfully into scores(puntos)")

        cursor.close()

    except sqlite3.Error as error:
        print("Failed to insert Python variable into sqlite table", error)
    finally:
        if sqliteConnection:
            sqliteConnection.close()
            print("The SQLite connection is closed")