import pygame as py
import random
import math
import time
import numpy as np

py.init()

# Set up the drawing window
width, height = 600, 900
screen = py.display.set_mode((width, height))

background = py.image.load("./assets/Grid3.png")
background = py.transform.scale(background, (width, height))
background_position = 0
scroll_speed = 0
sleep_time = 0.00008

###################################################asssets######################################################3
tie_fighters = []  # List to store the random rectangles

laser_x = 0
laser_y = 0
laser_color = (255, 0, 0)

##############################################################

rectangle_image = py.image.load(
    "assets/tie.png")  # Replace "rectangle.png" with the actual file path of your rectangle image
rectangle_image = py.transform.scale(rectangle_image, (25, 25))  # Scale the image to the desired size


class TieFighter:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = rectangle_image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self):
        screen.blit(rectangle_image, (self.x, self.y))

    def get_rect(self):
        return self.rect


spaceship_image = py.image.load(
    "./assets/flcn.png")  # Replace "spaceship.png" with the actual file path of your spaceship image
spaceship_image = py.transform.scale(spaceship_image, (80, 100))  # Scale the image to the desired size
spaceship_speed = 0.5
spaceship_x = width // 2 - 50
spaceship_y = height - 100


class SpaceShip:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rect = spaceship_image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.max_speed = 2
        self.min_speed = -2
        self.spaceship_x_vel = 0
        self.spaceship_y_vel = 0

    def set_x_vel(self, vel):
        self.spaceship_x_vel += spaceship_speed * vel

    def set_y_vel(self, vel):
        self.spaceship_y_vel += spaceship_speed * vel

    def draw(self):
        screen.blit(spaceship_image, (self.x, self.y))

    def get_rect(self):
        return self.rect


class Laser:
    def __init__(self, x, y):
        self.laser_width = 2
        self.laser_height = 10
        self.laser_color = (255, 0, 0)
        self.laser_speed = 0.5
        self.max_laser_speed = 2
        self.laser_vel = 0
        self.laser_x = x
        self.laser_y = y
        self.laser_state = True

    def draw(self, laser_color):
        self.laser_color = laser_color
        # self.laser_x = laser_x
        # self.laser_y = laser_y
        # self.laser_width = laser_width
        # self.laser_height = laser_height

        py.draw.rect(screen, self.laser_color, (self.laser_x, self.laser_y, self.laser_width, self.laser_height))


############################################################################################################

millenium_falcon = SpaceShip(spaceship_x, spaceship_y)
laserx = Laser(laser_x, laser_y)


##########################################################################################################

def check_collision():
    for rectx, _ in tie_fighters:
        if millenium_falcon.get_rect().colliderect(rectx):
            # Handle collision response here
            print("Collision occurred")


def fire_laser():
    if laserx.laser_state:
        laserx.laser_state = False
        laserx.laser_x = millenium_falcon.x + 40
        laserx.laser_y = millenium_falcon.y


################################################ Main  Function ################################################

Running = True
while Running:
    # Did the user click the window close button?
    for event in py.event.get():
        if event.type == py.QUIT:
            running = False
        elif event.type == py.KEYDOWN:
            if event.key == py.K_SPACE:
                fire_laser()

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

    millenium_falcon.spaceship_x_vel *= 0.96
    millenium_falcon.spaceship_y_vel *= 0.96

    # Limit the maximum speed
    spaceship_velocity_x = np.clip(millenium_falcon.spaceship_x_vel, millenium_falcon.min_speed,
                                   millenium_falcon.max_speed)
    spaceship_velocity_y = np.clip(millenium_falcon.spaceship_y_vel, millenium_falcon.min_speed,
                                   millenium_falcon.max_speed)

    # Update spaceship position based on velocity
    # tx = millenium_falcon.x
    # ty = millenium_falcon.y
    # tx += spaceship_velocity_x
    # ty += spaceship_velocity_y
    # millenium_falcon.x = np.clip(tx, 0, width - 80)
    # millenium_falcon.y = np.clip(ty, 0, height - 100)
    millenium_falcon.x = np.clip(millenium_falcon.x + spaceship_velocity_x, 0, width - 80)
    millenium_falcon.y = np.clip(millenium_falcon.y + spaceship_velocity_y, 0, height - 100)
    # print(spaceship_velocity_x)

    if not laserx.laser_state:
        laserx.laser_vel += laserx.laser_speed
        laserx.laser_vel *= 0.95
        laserx.laser_vel = min(laserx.laser_vel, laserx.max_laser_speed)
        # print(laser_vel)
        laserx.laser_y -= laserx.laser_vel
        if laserx.laser_y < 0:
            laserx.laser_state = True

    ############################################################++++++++++++++++++++#################################################################33

    background_position += scroll_speed
    # Wrap the background around when it goes beyond the window height
    if background_position >= height:
        background_position = 0

    # Generate a new random rectangle and add it to the list
    if len(tie_fighters) < 15:  # Limit to 5 rectangles
        rect_width = 20
        rect_height = 20
        # Generate rect_x at least 50 pixels away from the last drawn rectangle
        if len(tie_fighters) == 0:
            rect_x = width / 2
            rect_y = height - 20
        else:
            last_rect = tie_fighters[-1][0]
            # print(last_rect)
            # min_x = min(random.choice([last_rect.x - 50, last_rect.x + last_rect.width + 50]), width)
            min_x = min(last_rect.x - 400, 0)
            # print(min_x)
            max_x = width
            rect_x = random.randint(min_x, max_x)
            rect_y = random.randint(-height, 0)  # Start rectangles above the screen

        rect_color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
        # rect = py.Rect(rect_x, rect_y, rect_width, rect_height)
        # print(rect)
        rect = TieFighter(rect_x, rect_y)
        tie_fighters.append((rect, rect_color))

    # Draw the background image
    screen.blit(background, (0, background_position))
    screen.blit(background, (0, background_position - height))

    # Update and draw the rectangles
    i = 0  # print(rectangles)
    while i < len(tie_fighters):
        rect, color = tie_fighters[i]
        rect.y += math.ceil(scroll_speed)
        # print(float("{:.3f}".format(scroll_speed)) <= 0)
        # fl_speed = float("{:.4f}".format(scroll_speed))
        # print(sleep_time)
        time.sleep(sleep_time)
        # sleep_time = min(0,float("{:.4f}".format(sleep_time - 0.00001)))
        # Move rectangles down with scroll speed
        # print(rect)
        rect.draw()
        # Check if the rectangle has left the screen
        if rect.y > height:
            # Remove the rectangle from the list
            tie_fighters.pop(i)
        else:
            i += 1

    ################################### Events #################################################

    check_collision()

    #################################### Draw ##################################################
    millenium_falcon.draw()
    # screen.blit(spaceship_image, (spaceship_x, spaceship_y))
    # py.draw.circle(screen, spaceship_color, (spaceship_x, spaceship_y), spaceship_radius)
    if not laserx.laser_state:
        laserx.draw(laser_color)
        # py.draw.rect(screen, laser_color, (laser_x, laser_y, laserx.laser_width, laserx.laser_height))

    # check_collision()
    py.display.flip()
    if scroll_speed <= 1:
        scroll_speed += 0.01
    # scroll_speed += 0.01
    # print(scroll_speed)

# Done
py.quit()
