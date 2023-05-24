import pygame as py
from pygame.locals import *
import random
import math
import time
import numpy as np

py.init()
# Set up the drawing window
width, height = 700, 1000
screen = py.display.set_mode((width, height), py.HWSURFACE)
clock = py.time.Clock()

background = py.image.load("./assets/Grid3.png")
background = py.transform.scale(background, (width, height))
background_position = 0
scroll_speed = 0
# sleep_time = 0.00008

###################################################Globals##############################################################

space = []  # List to store the random rectangles

LASER_X = 0
LASER_Y = 0
LASER_COLOR_RED = (255, 0, 0)
LASER_COLOR_GREEN = (255, 255, 0)
INERTIA_FACTOR = 0.92
MAX_OBJECTS = 20
MAX_SCROLL = 20
CLOCK_RATE = 50
RUNNING = True
SCORE = 0

######################################################++++ASSETS++++####################################################

tief1 = py.image.load("assets/tie.png")  # Replace "rectangle.png" with the actual file path of your rectangle image
tief1 = py.transform.scale(tief1, (25, 25))  # Scale the image to the desired size
tief2 = py.image.load("assets/tie2.png")  # Replace "rectangle.png" with the actual file path of your rectangle image
tief2 = py.transform.scale(tief2, (25, 25))


class TieFighter:
    def __init__(self, x, y, var):
        self.type = "TIE"
        self.speed = 0
        self.x = x
        self.y = y
        self.x_vel: int = 0
        self.y_vel: int = 0
        self.speed: int = 1
        if var == 1:
            self.image = tief1
        elif var == 2:
            self.image = tief2
        else:
            self.image = tief1

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return self.image.get_rect()


spaceship_image = py.image.load("./assets/flcn.png")  # Replace "spaceship.png" with the actual file path of your spaceship image
spaceship_image = py.transform.scale(spaceship_image, (80, 100))  # Scale the image to the desired size
spaceship_x = width // 2 - 50
spaceship_y = height - 100


class SpaceShip:
    def __init__(self, x, y):
        self.type = "MSHIP"
        self.x: int = x
        self.y: int = y
        self.max_speed: int = 8
        self.min_speed: int = -8
        self.x_vel: int = 0
        self.y_vel: int = 0
        self.speed: int = 1
        self.hit_points = 100

    def set_x_vel(self, vel):
        self.x_vel += self.speed * vel
        # print(self.spaceship_x_vel)

    def set_y_vel(self, vel):
        self.y_vel += self.speed * vel

    def draw(self):
        screen.blit(spaceship_image, (self.x, self.y))

    @staticmethod
    def get_rect():
        return spaceship_image.get_rect()


class Laser:
    def __init__(self, x=0, y=0, laser_Speed=20):
        self.type = "LASER"
        self.laser_width = 2
        self.laser_height = 10
        self.laser_color = (255, 0, 0)
        self.speed = 1
        self.max_speed = laser_Speed
        self.y_vel = 0
        self.x_vel = 0
        self.direction = 0
        self.x = x
        self.y = y
        self.laser_ready = True

    def draw(self, laser_color):
        self.laser_color = laser_color
        # self.laser_x = laser_x
        # self.laser_y = laser_y
        # self.laser_width = laser_width
        # self.laser_height = laser_height
        py.draw.rect(screen, self.laser_color, (self.x, self.y, self.laser_width, self.laser_height))

    def get_rect(self):
        return py.Rect(self.x, self.y, self.laser_width, self.laser_height)


astr1 = py.image.load("assets/asteroid1.png")  # Replace "rectangle.png" with the actual file path of your rectangle image
astr1 = py.transform.scale(astr1, (40, 40))  # Scale the image to the desired size
astr2 = py.image.load("assets/asteroid2.png")  # Replace "rectangle.png" with the actual file path of your rectangle image
astr2 = py.transform.scale(astr2, (35, 35))


class Asteroid:
    def __init__(self, x, y, var):
        self.type = "ASTEROID"
        self.x = x
        self.y = y
        self.x_vel: int = 0
        self.y_vel: int = 0
        self.speed: int = 0
        self.max_speed = 0
        if var == 1:
            self.image = astr1
        elif var == 2:
            self.image = astr2
        else:
            self.image = astr2

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return self.image.get_rect()


health = py.image.load("assets/health.png")  # Replace "rectangle.png" with the actual file path of your rectangle image
health = py.transform.scale(health, (20, 20))


class HealthIcon:
    def __init__(self, x, y):
        self.type = "HP"
        self.x = x
        self.y = y
        self.image = health
        self.x_vel: int = 0
        self.y_vel: int = 0
        self.speed: int = 0
        self.max_speed = 0

    def draw(self):
        screen.blit(self.image, (self.x, self.y))

    def get_rect(self):
        return self.image.get_rect()


explosion = py.image.load("./assets/exp_sprite.png")


# print(explosion.get_height())
# explosion = py.transform.scale(explosion, (100, 800))
# print(explosion.get_width())

class Explotion:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.image = explosion
        self.columns = 5
        self.rows = 5
        self.sprite_width = self.image.get_width() // self.columns
        self.sprite_height = self.image.get_height() // self.rows
        self.sprites = []
        self.current_frame = 0  # Current frame index
        self.frame_duration = 0.2  # Duration (in seconds) for each frame
        self.frame_timer = 0
        self.explosion_active = False
        # Populate the sprites list with individual subsurfaces
        for row in range(self.rows):
            for col in range(self.columns):
                sx = col * self.sprite_width
                sy = row * self.sprite_height
                sprite = self.image.subsurface((sx, sy, self.sprite_width, self.sprite_height))
                self.sprites.append(sprite)
        # Animation properties

    def update(self, dt):
        self.frame_timer += dt
        # Check if it's time to switch to the next frame
        # print(self.current_frame)
        if self.frame_timer >= self.frame_duration:
            self.frame_timer = 0  # Reset the frame timer
            self.current_frame += 1  # Move to the next frame
            # Check if all frames have been shown
            #

    def draw(self, x=None, y=None):
        x = self.x if x is None else x
        y = self.y if y is None else y
        current_sprite = self.sprites[self.current_frame]
        screen.blit(current_sprite, (x, y))

    def finished(self):
        # print(self.current_frame == (len(self.sprites) - 1))
        if self.current_frame == (len(self.sprites) - 1):
            self.current_frame = 0
            return True
        else:
            return False

    def get_rect(self):
        return self.image.get_rect()


########################################################################################################################

millenium_falcon = SpaceShip(spaceship_x, spaceship_y)
laserx = Laser(LASER_X, LASER_Y)
lasery = Laser(laser_Speed=5)
# print(lasery.laser_ready)
new_explosion = Explotion()


#######################################################################################################################3

def check_collision(space):
    falcon_pos = millenium_falcon.get_rect().move(millenium_falcon.x, millenium_falcon.y)

    if falcon_pos.colliderect(lasery.get_rect()) and not lasery.laser_ready:
        # print("you are shot")
        lasery.laser_ready = True
        millenium_falcon.hit_points -= 15
        print(millenium_falcon.hit_points, "- 10")

    for rectx in space:
        # py.draw.rect(screen, (255, 0, 0), millenium_falcon.get_rect().move(millenium_falcon.x, millenium_falcon.y))
        # py.draw.rect(screen, (255, 255, 0), laserx.get_rect())
        rect_pos = rectx.get_rect().move(rectx.x, rectx.y)
        if falcon_pos.colliderect(rect_pos):
            # print(millenium_falcon.get_rect(), rectx.get_rect())
            # Handle collision response here
            if rectx.type == "HP":
                space.remove(rectx)
                millenium_falcon.hit_points = min(millenium_falcon.hit_points + 15, 100)
                print(millenium_falcon.hit_points, "+ 15")
            else:
                space.remove(rectx)
                millenium_falcon.hit_points -= 15
                print(millenium_falcon.hit_points, "- 15")
            break
            # print("Collision occurred MF")
            # break
        if rectx.type != "HP" and laserx.get_rect().colliderect(rect_pos) and not laserx.laser_ready:
            # print("Coll laser")
            # py.draw.rect(screen, (255, 255, 0), (rect_pos.x, rect_pos.y, 10, 10))
            laserx.laser_ready = True
            # laserx.draw(LASER_COLOR)
            new_explosion.explosion_active = True  # Set the explosion flag to activate animation
            new_explosion.x = rect_pos.x - 50
            new_explosion.y = rect_pos.y
            space.remove(rectx)
            break


def draw_falcon():
    global RUNNING
    # print(millenium_falcon.hit_points)
    # print(millenium_falcon.hit_points < 0)
    if millenium_falcon.hit_points >= 0:
        millenium_falcon.draw()
    else:
        print("You dead, score = ", int(SCORE), " my cat plays better than you")
        RUNNING = False
        py.quit()


def draw_collision():
    if new_explosion.explosion_active:
        if new_explosion.finished():
            new_explosion.explosion_active = False
        else:
            new_explosion.update(1)  # Update the explosion animation
            new_explosion.draw()  # Draw the explosion
        # py.display.flip()


def init_laserA(direction=0):
    if laserx.laser_ready and not new_explosion.finished():
        laserx.laser_ready = False
        laserx.x = millenium_falcon.x + 40
        laserx.y = millenium_falcon.y
        laserx.direction = direction


def init_laserB(x, y, direction=0):
    # print(lasery.laser_ready)
    if lasery.laser_ready:
        lasery.laser_ready = False
        lasery.x = x
        lasery.y = y
        lasery.direction = direction


def laser_directive():
    if not laserx.laser_ready:
        laserx.y_vel += laserx.speed
        laserx.y_vel *= INERTIA_FACTOR
        laserx.y_vel = min(laserx.y_vel, laserx.max_speed)
        # print(laserx.laser_vel)
        laserx.y -= laserx.y_vel
        if laserx.y < 0:
            laserx.laser_ready = True

    if not lasery.laser_ready:
        lasery.y_vel += laserx.speed
        lasery.y_vel *= INERTIA_FACTOR
        lasery.y_vel = min(lasery.y_vel, lasery.max_speed)

        lasery.x_vel += laserx.speed
        lasery.x_vel *= INERTIA_FACTOR
        lasery.x_vel = min(lasery.x_vel, lasery.max_speed)
        # print(laserx.laser_vel)
        lasery.y += lasery.y_vel
        lasery.x += lasery.direction * lasery.x_vel
        if lasery.y < 0 or lasery.y > height:
            lasery.laser_ready = True


def draw_laser():
    if not laserx.laser_ready:
        laserx.draw(LASER_COLOR_GREEN)
    if not lasery.laser_ready:
        lasery.draw(LASER_COLOR_RED)


def render_space(space):
    # Update and draw the rectangles
    i = 0  # print(rectangles)
    # lsx = len(space)
    while i < len(space):
        # print(i,len(space))
        spaceObject = space[i]
        type = spaceObject.type
        init_speed = int(math.ceil(scroll_speed) + spaceObject.speed)
        # print(type)
        cx = random.randint(0, len(space))
        if type == "TIE" and i == cx:
            direction_x = int(millenium_falcon.x - spaceObject.x)
            direction_y = int(millenium_falcon.y - spaceObject.y)
            length = int(math.sqrt(direction_x ** 2 + direction_y ** 2))
            # print(direction_y, direction_y)
            # print("length", length)
            if length != 0:
                direction_x /= length
                direction_y /= length

            # Set velocity based on the normalized direction and speed
            # spaceObject.x_vel += direction_x * init_speed
            spaceObject.x_vel *= 0.1
            # spaceObject.x += spaceObject.x_vel
            spaceObject.x = int(spaceObject.x + (direction_x * init_speed))
            spaceObject.y = int(spaceObject.y + (direction_y * init_speed))
            # print(spaceObject.x)
            init_laserB(spaceObject.x, spaceObject.y, direction_x)

        else:
            spaceObject.y += init_speed

            # spaceObject.y = int((spaceObject.y + direction_y)*spaceObject.speed)

        # time.sleep(sleep_time)
        spaceObject.draw()
        # Check if the rectangle has left the screen
        if spaceObject.y > height:
            # Remove the rectangle from the list
            space.pop(i)
        else:
            i += 1


################################################ Main  Function ########################################################

def main(Running):
    global background_position, scroll_speed, SCORE
    health_flag = 0

    while Running:
        # Did the user click the window close button?
        for event in py.event.get():
            if event.type == py.QUIT:
                Running = False
            elif event.type == py.KEYDOWN:
                if event.key == py.K_SPACE:
                    init_laserA()

        keys = py.key.get_pressed()
        # Update spaceship position based on pressed keys
        if keys[py.K_w]:
            # spaceship_y_vel -= spaceship_speed
            millenium_falcon.set_y_vel(-1)
        if keys[py.K_s]:
            millenium_falcon.set_y_vel(1)
        if keys[py.K_a]:
            millenium_falcon.set_x_vel(-1)
        if keys[py.K_d]:
            millenium_falcon.set_x_vel(1)

        ################################################################################################################
        clock.tick(CLOCK_RATE)
        ######################################################+++++++FALCOM CONTROL+++++++##############################

        millenium_falcon.x_vel *= INERTIA_FACTOR
        millenium_falcon.y_vel *= INERTIA_FACTOR

        # Limit the maximum speed
        spaceship_velocity_x = np.clip(millenium_falcon.x_vel, millenium_falcon.min_speed, millenium_falcon.max_speed)
        spaceship_velocity_y = np.clip(millenium_falcon.y_vel, millenium_falcon.min_speed, millenium_falcon.max_speed)

        # Update spaceship position based on velocity
        millenium_falcon.x = np.clip(millenium_falcon.x + spaceship_velocity_x, 0, width - 80)
        millenium_falcon.y = np.clip(millenium_falcon.y + spaceship_velocity_y, 0, height - 100)
        # print(millenium_falcon.spaceship_x_vel,spaceship_velocity_x)
        ############################################################++++++++ Background ++++++++++++####################

        background_position += scroll_speed
        # Wrap the background around when it goes beyond the window height
        if background_position >= height:
            background_position = 0

        ############################################################++++++++ Generator ++++++++++++#####################
        # Generate a new random rectangle and add it to the list
        SPACE_LENGTH = len(space)
        if SPACE_LENGTH <= MAX_OBJECTS:  # Limit to 5 rectangles
            # rect_width = 20
            # rect_height = 20
            # Generate rect_x at least 50 pixels away from the last drawn rectangle
            if SPACE_LENGTH == 0:
                rect_x = width / 2
                rect_y = height - 20
            else:
                last_rect = space[-1]
                # print(last_rect.x)
                # min_x = min(random.choice([last_rect.x - 50, last_rect.x + last_rect.width + 50]), width)
                min_x = int(np.clip(last_rect.x - 400, 0, last_rect.x + 250))
                # print(min_x)
                max_x = width
                # print(min_x, max_x)
                rect_x = random.randint(max(min_x, 0), min(max_x, width - 30))
                rect_y = random.randint(-height // 2, 0)  # Start rectangles above the screen

            # rect_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            # rect = py.Rect(rect_x, rect_y, rect_width, rect_height)
            # print(rect)
            var = random.randint(1, 2)
            speed_modifer = random.randint(0, 2)
            random_draw = random.randint(1, 100) % 2

            if random_draw == 0:
                new_tie = TieFighter(rect_x, rect_y, var)
                new_tie.speed = speed_modifer
                space.append(new_tie)
            elif random_draw == 1:
                new_asteroid = Asteroid(rect_x, rect_y, var)
                new_asteroid.speed = speed_modifer
                space.append(new_asteroid)
            else:
                pass

            if SPACE_LENGTH == MAX_OBJECTS and millenium_falcon.hit_points < 100:
                # print(health_flag)
                if health_flag > 1250:
                    new_health = HealthIcon(rect_x + 50, rect_y + 50)
                    space.append(new_health)
                    health_flag = 0
                else:
                    health_flag += SPACE_LENGTH

        # Draw the background image
        screen.blit(background, (0, background_position))
        screen.blit(background, (0, background_position - height))

        ################################### Events #####################################################################

        laser_directive()
        check_collision(space) if SPACE_LENGTH > 15 else print("Wait powering up")

        #################################### Draw #####################################################################

        render_space(space)
        draw_falcon()
        draw_laser()
        draw_collision()  # Draw the explosion

        ###########################################Screen###############################################################

        py.display.flip()
        if scroll_speed <= MAX_SCROLL:
            scroll_speed += 0.001
        # scroll_speed += 0.01
        SCORE = SCORE + 0.1
        # print(int(SCORE))
        # print(scroll_speed)

    # Done
    py.quit()


# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////////

if __name__ == '__main__':
    main(RUNNING)
