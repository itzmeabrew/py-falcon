import pygame as py
from pygame.locals import *
import random
import math
import time
import numpy as np

py.init()
# Set up the drawing window
WIDTH, HEIGHT = 700, 700
screen = py.display.set_mode((WIDTH, HEIGHT), py.HWSURFACE)
clock = py.time.Clock()

background = py.image.load("./assets/Grid3.png")
background = py.transform.scale(background, (WIDTH, HEIGHT))
background_position = 0
scroll_speed = 0.5
# sleep_time = 0.00008

###################################################Globals##############################################################

space = []  # List to store the random rectangles

RED = (255, 0, 0)
GREEN = (255, 255, 0)
INERTIA_FACTOR = 0.92
MAX_OBJECTS = 20
MAX_SCROLL = 20
CLOCK_RATE = 60
RUNNING = True
SCORE = 0

# #####################################################++++SPRITE CLASSES++++####################################################

spaceship_image = py.image.load("./assets/flcn.png")  # Replace "spaceship.png" with the actual file path of your spaceship image
spaceship_image = py.transform.scale(spaceship_image, (80, 100))  # Scale the image to the desired size


class SpaceShip(py.sprite.Sprite):
    def __init__(self, x, y):
        super(SpaceShip, self).__init__()
        self.image = spaceship_image
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(center=(x, y))

        self.speed = 2
        self.max_speed = 5
        self.inertia = INERTIA_FACTOR  # Inertia factor, controls how quickly the sprite slows down
        self.velocity = [0, 0]  # Initial velocity

        self.type = 0
        self.hp = 100

    def update(self, keys):
        if keys[py.K_a]:
            self.velocity[0] -= self.speed
        if keys[py.K_d]:
            self.velocity[0] += self.speed
        if keys[py.K_w]:
            self.velocity[1] -= self.speed
        if keys[py.K_s]:
            self.velocity[1] += self.speed

        # Apply inertia to both X and Y velocities
        self.velocity[0] *= self.inertia
        self.velocity[1] *= self.inertia

        # Limit speed
        speed_magnitude = py.math.Vector2(self.velocity).length()
        if speed_magnitude > self.max_speed:
            self.velocity[0] = (self.velocity[0] / speed_magnitude) * self.max_speed
            self.velocity[1] = (self.velocity[1] / speed_magnitude) * self.max_speed

        self.rect.move_ip(self.velocity[0], self.velocity[1])  # Update the sprite position based on the velocity
        self.rect.clamp_ip(screen.get_rect())  # Limit movement within screen bounds


tie1 = py.image.load("./assets/tie.png")  # Replace "spaceship.png" with the actual file path of your spaceship image
tie1 = py.transform.scale(tie1, (80, 100))  # Scale the image to the desired size
tie2 = py.image.load("./assets/tie2.png")  # Replace "spaceship.png" with the actual file path of your spaceship image
tie2 = py.transform.scale(tie2, (80, 100))  # Scale the image to the desired size


class TieFighter(py.sprite.Sprite):
    def __init__(self, x, y, var, speed=5):
        super(TieFighter, self).__init__()
        self.image = None
        if var == 1:
            self.image = tie1
        else:
            self.image = tie2
        self.image.set_colorkey((255, 255, 255), RLEACCEL)
        self.rect = self.image.get_rect(center=(x, y))

        self.type = 0
        self.hp = 10
        self.speed = speed

    def update(self):
        self.rect.move_ip(0, self.speed)
        if self.rect.top < 0:
            self.kill()


# ########################################## SPRITE OBJECTS #############################################################################

spaceship_x = WIDTH // 2
spaceship_y = HEIGHT - 100
millenium_falcon = SpaceShip(spaceship_x, spaceship_y)

# ###########################################################SPRITE-GROUP#################################################################

asteroids = py.sprite.Group()
ties = py.sprite.Group()
falcon = py.sprite.Group()
falcon.add(millenium_falcon)


def add_to_asteroids_grp(sprite):
    asteroids.add(sprite)


def add_to_tie_grp(sprite):
    ties.add(sprite)


################################################ TIMED-EVENTS ##########################################################################

# Create custom events for adding a new enemy and cloud
SCRL = py.USEREVENT + 1
py.time.set_timer(SCRL, 10000)

TIE = py.USEREVENT + 2
py.time.set_timer(TIE, 250)
ASRD = py.USEREVENT + 3
py.time.set_timer(ASRD, 300)


###################################################### Helper Function ##################################################################

def create_objects(event):
    if event.type == ASRD:
        new_tie = TieFighter()

def draw_sprites(board):
    falcon.draw(board)
    ties.draw(board)
    asteroids.draw(board)


################################################ Main  Function #########################################################################

def main(Running):
    global background_position, scroll_speed, SCORE
    health_flag = 0

    while Running:
        for event in py.event.get():
            if event.type == QUIT:  # Did the user click the window close button?
                Running = False
            elif event.type == SCRL and scroll_speed <= MAX_SCROLL:
                scroll_speed += 0.0001
            else:
                create_objects(event)

        screen.blit(background, (0, background_position))
        screen.blit(background, (0, background_position - HEIGHT))

        key = py.key.get_pressed()

        falcon.update(key)

        draw_sprites(screen)

        background_position += scroll_speed
        if background_position >= HEIGHT:
            background_position = 0  # Wrap the background around when it goes beyond the window height

        py.display.flip()
        clock.tick(CLOCK_RATE)

        SCORE = SCORE + 0.1

    # Done
    py.quit()


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

if __name__ == '__main__':
    main(RUNNING)
