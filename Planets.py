# ___ Planet Class __ #
# The main class used for the planetary objects

# library import
import random

import pygame as pg
from pygame import gfxdraw as gfx

import Vector as v
import globalFunctions as functions

# constant variables
G = 6.67408e-11  # gravitational constant
color_lighten = 10

# sets up random generator
random.seed()  # sets seed to time of run


class Planet:
    def __init__(self, w, h, x_=None, y_=None, vx_=0, vy_=0, sun=False):
        self.name = functions.random_char(5)
        self.mass = random.uniform(1, 7) * (10 ** random.uniform(9.5, 11))
        if x_ is None:
            self.pos_x = random.randint(15, w - 15)
            self.pos_y = random.randint(15, h - 15)
        else:
            self.pos_x = x_
            self.pos_y = y_
        self.vel_x = vx_
        self.vel_y = vy_
        self.accel_x = 0
        self.accel_y = 0
        self.R = random.randint(0, 255)
        self.G = random.randint(0, 255)
        self.B = random.randint(0, 255)
        self.pos_x_list = []
        self.pos_y_list = []
        if sun:
            self.mass = 8e11
            self.pos_x = w / 2
            self.pos_y = h / 2
            self.R = 255
            self.G = 255
            self.B = 0

        self.radius = round(functions.variable_mapping(self.mass, 1e9, 10e11, 4, 15))
        self.rect = self.update_hit_box()
        # intitial: x,y,vx,vy,mass,color
        self.initial_state = [self.pos_x, self.pos_y, self.vel_x, self.vel_y, self.mass, [self.R, self.G, self.B]]
        self.active_move = False
        self.velocity = v.Vector(self.vel_x, self.vel_y)

    def __str__(self):
        return self.name

    def update_hit_box(self):
        self.rect = pg.Rect(self.pos_x - ((self.radius * 3) / 2), self.pos_y - ((self.radius * 3) / 2), self.radius * 3,
                            self.radius * 3)
        return self.rect

    # static : method which detects user clicks planet to edit mass
    def handle_event(self, event, tool_):
        self.update_hit_box()
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicks on slide ball
            if tool_ is 0:
                if self.rect.collidepoint(event.pos):
                    # Toggle the active variable.
                    self.active_move = not self.active_move
                    return True
                else:
                    self.active_move = False
                    return False
            else:
                if self.rect.collidepoint(event.pos):
                    return True
        if self.active_move:
            x, y = pg.mouse.get_pos()
            self.planet_setup(x_=x, y_=y)

    # debugging function
    def draw_hit_box(self, screen):
        pg.draw.rect(screen, (255, 0, 0), self.rect, 1)

    # method : update position
    def update_pos(self, new_pos):
        self.pos_x = new_pos[0]
        self.pos_x_list.append(new_pos[0])
        self.pos_y = new_pos[1]
        self.pos_y_list.append(new_pos[1])
        return 0

    # method : update position
    def update_pos_x(self, x_):
        self.pos_x = x_
        self.pos_x_list.append(x_)
        return 0

    # method : update position
    def update_pos_y(self, y_):
        self.pos_y = y_
        self.pos_y_list.append(y_)
        return 0

    # ___ Velocity ___ # All velocity updaters limit velocity
    # method : # updates velocity after finding new position using acceleration
    def update_vel(self, new_vel):
        self.velocity.set(new_vel[0], new_vel[1])
        self.velocity.limit(functions.max_vel)
        self.vel_x = self.velocity.x
        self.vel_y = self.velocity.y
        return 0

    # method : updates velocity given x component
    def update_velocity_x(self, new_vel_x):
        self.velocity.set(new_vel_x, self.vel_y)
        self.velocity.limit(functions.max_vel)
        self.vel_x = self.velocity.x
        return 0

    # method :  updates velocity given y component
    def update_velocity_y(self, new_vel_y):
        self.velocity.set(self.vel_x, new_vel_y)
        self.velocity.limit(functions.max_vel)
        self.vel_y = self.velocity.y
        return 0

    # method : updates acceleration given a list [a_x, a_y]
    def update_accel(self, new_accel):
        self.accel_x = new_accel[0]
        self.accel_y = new_accel[1]
        return 0

    # method : draws antialiased circle
    def draw(self, screen, aa=False, color=None, image=None):
        if not aa:
            if color is None:
                pg.draw.circle(screen, (self.R, self.G, self.B), (round(self.pos_x), round(self.pos_y)), self.radius)
            else:
                pg.draw.circle(screen, color, (round(self.pos_x), round(self.pos_y)), self.radius)
        else:
            if color is None:
                gfx.aacircle(screen, round(self.pos_x), round(self.pos_y), self.radius, (self.R, self.G, self.B))
                gfx.filled_circle(screen, round(self.pos_x), round(self.pos_y), self.radius, (self.R, self.G, self.B))
            else:
                gfx.aacircle(screen, round(self.pos_x), round(self.pos_y), self.radius, color)
                gfx.filled_circle(screen, round(self.pos_x), round(self.pos_y), self.radius, color)

    # method : changes mass and updates radius accordingly
    def change_mass(self, mass_):
        self.mass = mass_
        self.radius = round(functions.variable_mapping(self.mass, 1e9, 10e11, 4, 15))

    def planet_setup(self, x_=None, y_=None, vx_=None, vy_=None, mass_=None, color=None):
        if x_ is not None:
            self.update_pos_x(x_)
            # intitial: x,y,vx,vy,mass,color
            self.initial_state[0] = x_
        if y_ is not None:
            self.update_pos_y(y_)
            self.initial_state[1] = y_
        if vx_ is not None:
            self.update_velocity_x(vx_)
            self.initial_state[2] = vx_
        if vy_ is not None:
            self.update_velocity_y(vy_)
            self.initial_state[3] = vy_
        if mass_ is not None:
            self.change_mass(mass_)
            self.initial_state[4] = mass_
        if color is not None:
            self.R = color[0]
            self.G = color[1]
            self.B = color[2]
            self.initial_state[5] = color

    def restart_planets(self):
        self.update_pos_x(self.initial_state[0])
        self.update_pos_y(self.initial_state[1])
        self.update_velocity_x(self.initial_state[2])
        self.update_velocity_y(self.initial_state[3])
        self.change_mass(self.initial_state[4])
        self.R = self.initial_state[5][0]
        self.G = self.initial_state[5][1]
        self.B = self.initial_state[5][2]

    # method : turns two planets into one planet where merge is applied to one of them
    def merge_planet(self, mass, position_x, position_y, color=None):
        if color is None:
            color = [0, 0, 0]
        self.change_mass(self.mass + mass)
        # limits planet mass so things don't get too out of hand
        if self.mass > 10e11:
            self.change_mass(10e11)
        self.pos_x = (self.pos_x + position_x) / 2
        self.pos_y = (self.pos_y + position_y) / 2
        # calculations to change colors
        # source : https://stackoverflow.com/questions/4255973/calculation-of-a-mixed-color-in-rgb
        r1 = self.R
        g1 = self.G
        b1 = self.B
        r2 = color[0]
        g2 = color[1]
        b2 = color[2]
        w1 = min(r1, min(g1, b1))
        w2 = min(r2, min(g2, b2))
        r1 -= w1
        g1 -= w1
        b1 -= w1
        r2 -= w2
        g2 -= w2
        b2 -= w2
        m1 = max(r1, max(g1, b1))
        m2 = max(r2, max(g2, b2))
        br = (m1 + m2) / (2 * 255.0)
        r3 = (r1 + r2) * br
        g3 = (g1 + g2) * br
        b3 = (b1 + b2) * br
        w3 = (w1 + w2) / 2
        r3 += w3
        g3 += w3
        b3 += w3
        r3 = r3 if r3 <= 255 else 255
        g3 = g3 if g3 <= 255 else 255
        b3 = b3 if b3 <= 255 else 255
        r3 = r3 if r3 >= 0 else 0
        g3 = g3 if g3 >= 0 else 0
        b3 = b3 if b3 >= 0 else 0
        self.R = round(r3)
        self.G = round(g3)
        self.B = round(b3)
