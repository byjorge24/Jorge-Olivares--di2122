import pygame
import random
from pygame.constants import RLEACCEL
import os
import time

carpeta = os.path.dirname(__file__)

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
        self.rect = self.surf.get_rect()
    
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
        self.speed = random.randint(5, 20)
    
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

pygame.init()

# Definimos un reloj para tener una buena velocidad en el juego, y que no sea injugable
clock = pygame.time.Clock()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

ADDENEMY = pygame.USEREVENT + 1
pygame.time.set_timer(ADDENEMY, 250)

ADDCLOUD = pygame.USEREVENT + 2
pygame.time.set_timer(ADDCLOUD, 1000)

# Creamos el jugador
player = Player()

# Creamos un grupo de sprites para poder almacenar todos los sprites
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


    pressed_keys = pygame.key.get_pressed()

    player.update(pressed_keys)

    # Actualizamos la posición del enemigo
    enemies.update()

    # Actualizamos la posición del cloud
    clouds.update()

    screen.fill((135, 206, 250))

    # Dibujamos todos los sprites que esten almacenados en el grupo 'all_sprites'
    for entity in all_sprites:

        screen.blit(entity.surf, entity.rect)

    if pygame.sprite.spritecollideany(player, enemies):

        collision_sound.play()
        
        time.sleep(1)

        player.kill()
        
        running = False

    pygame.display.flip()

    # Nos aseguramos de que el programa mantiene 60 frames por segundo
    clock.tick(60)

# Paramos y salimos del mixer de la musica.
pygame.mixer.music.stop()
pygame.mixer.quit()