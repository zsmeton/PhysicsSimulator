# __ Multi-Object calculations __#
# if it involves two or more planets or directly effects the game as a whole the function is here

import math
import random
import string

random.seed()

G = 6.67408e-11  # gravitational constant
coefficient_of_collision = 0.985  # variable to change how elastic collisions are
max_vel = 20


# generates string of random characters
# source : https://stackoverflow.com/questions/2823316/generate-a-random-letter-in-python
def random_char(y):
    return ''.join(random.choice(string.ascii_letters) for x in range(y))


# finds which planets are colliding and returns a list
def collision_detection(planet_list):
    collision = []
    for i in range(len(planet_list)):
        for j in range((i + 1), len(planet_list)):
            radius = math.sqrt(
                (planet_list[i].pos_x - planet_list[j].pos_x) ** 2 + (planet_list[i].pos_y - planet_list[j].pos_y) ** 2)
            if radius <= planet_list[i].radius + planet_list[j].radius:
                collision.append(planet_list[i])
                collision.append(planet_list[j])
    return collision


# finds the new velocity of two planets colliding
# source: http://www.emanueleferonato.com/2007/08/19/managing-ball-vs-ball-collision-with-flash/
def velocity_from_collision(planet1, planet2):
    dx = planet1.pos_x - planet2.pos_x
    dy = planet1.pos_y - planet2.pos_y
    collision_angle = math.atan2(dy, dx)
    magnitude_1 = math.sqrt(planet1.vel_x * planet1.vel_x + planet1.vel_y * planet1.vel_y)
    magnitude_2 = math.sqrt(planet2.vel_x * planet2.vel_x + planet2.vel_y * planet2.vel_y)
    direction_1 = math.atan2(planet1.vel_y, planet1.vel_x)
    direction_2 = math.atan2(planet2.vel_y, planet2.vel_x)
    new_x_vel_1 = magnitude_1 * math.cos(direction_1 - collision_angle)
    new_y_vel_1 = magnitude_1 * math.sin(direction_1 - collision_angle)
    new_x_vel_2 = magnitude_2 * math.cos(direction_2 - collision_angle)
    new_y_vel_2 = magnitude_2 * math.sin(direction_2 - collision_angle)
    final_x_vel_1 = ((planet1.mass - planet2.mass) * new_x_vel_1 + (planet2.mass + planet2.mass) * new_x_vel_2) / (
            planet1.mass + planet2.mass)
    final_x_vel_2 = ((planet1.mass + planet1.mass) * new_x_vel_1 + (planet2.mass - planet1.mass) * new_x_vel_2) / (
            planet1.mass + planet2.mass)
    final_y_vel_1 = new_y_vel_1
    final_y_vel_2 = new_y_vel_2
    ball_x_vel = math.cos(collision_angle) * final_x_vel_1 + math.cos(collision_angle + math.pi / 2) * final_y_vel_1
    ball_y_vel = math.sin(collision_angle) * final_x_vel_1 + math.sin(collision_angle + math.pi / 2) * final_y_vel_1
    ball2_x_vel = math.cos(collision_angle) * final_x_vel_2 + math.cos(collision_angle + math.pi / 2) * final_y_vel_2
    ball2_y_vel = math.sin(collision_angle) * final_x_vel_2 + math.sin(collision_angle + math.pi / 2) * final_y_vel_2
    # sets velocity using calculations
    new_velocities = [planet1, coefficient_of_collision * ball_x_vel, coefficient_of_collision * ball_y_vel, planet2,
                      coefficient_of_collision * ball2_x_vel, coefficient_of_collision * ball2_y_vel]
    return new_velocities


# calculates the acceleration due to gravity imparted by all other planets
def accel_due_to_gravity(planet_accel_x, planet_accel_y, planet_list):
    for i in range(len(planet_list)):
        for j in range(i + 1, len(planet_list)):
            if math.sqrt((planet_list[i].pos_x - planet_list[j].pos_x) ** 2 + (
                    planet_list[i].pos_y - planet_list[j].pos_y) ** 2) == 0:
                planet_list[i].update_pos = [planet_list[i].pos_x + .00001]
                planet_list[i].update_pos = [planet_list[i].pos_y + .00001]
            g_r = -(G / (math.sqrt((planet_list[i].pos_x - planet_list[j].pos_x) ** 2 + (
                    planet_list[i].pos_y - planet_list[j].pos_y) ** 2) ** 3))
            x_field = g_r * (planet_list[i].pos_x - planet_list[j].pos_x)
            y_field = g_r * (planet_list[i].pos_y - planet_list[j].pos_y)
            planet_accel_x[planet_list[i]] += x_field * planet_list[j].mass
            planet_accel_x[planet_list[j]] -= x_field * planet_list[i].mass
            planet_accel_y[planet_list[i]] += y_field * planet_list[j].mass
            planet_accel_y[planet_list[j]] -= y_field * planet_list[i].mass
    return planet_accel_x, planet_accel_y


# calculates new position using constant accel kinematics
def position(index, planet_list, time):
    pos_x = planet_list[index].pos_x + planet_list[index].vel_x * time + .5 * planet_list[index].accel_x * (time ** 2)
    pos_y = planet_list[index].pos_y + planet_list[index].vel_y * time + .5 * planet_list[index].accel_y * (time ** 2)
    new_position = [pos_x, pos_y]  # creates list for output so update of position can be done at end of update period
    return new_position


# calculates new velocity using constant accel kinematics
def velocity(index, planet_list, time):
    vel_x = planet_list[index].vel_x + planet_list[index].accel_x * time
    vel_y = planet_list[index].vel_y + planet_list[index].accel_y * time
    new_velocity = [vel_x, vel_y]  # creates list for output so update of position can be done at end of update period
    return new_velocity


# sees if planet has moved in a while
def position_change(planet):
    combine_tolerance = .001
    if len(planet.pos_x_list) < 3:
        return

    change_in_x = abs(planet.pos_x_list[-1] - planet.pos_x_list[-3])
    change_in_y = abs(planet.pos_y_list[-1] - planet.pos_y_list[-3])
    if change_in_x <= combine_tolerance and change_in_y <= combine_tolerance:
        return True
    else:
        return False


# if two planets have collided and don't separate they merge into one
def combine_planets(collision_list):
    combine_list = []
    for i in range(0, len(collision_list), 2):
        if position_change(collision_list[i]) and position_change(collision_list[i + 1]):
            combine_list.append(collision_list[i])
            combine_list.append(collision_list[i + 1])
    if combine_list:
        print(combine_list)
    return combine_list


# if a planet hits the wall reverse direction
def wall_collision(index, planet_list, w, h):
    if planet_list[index].pos_x >= w - planet_list[index].radius or planet_list[index].pos_x <= planet_list[
        index].radius:
        planet_list[index].update_velocity_x(-coefficient_of_collision * planet_list[index].vel_x)
    if planet_list[index].pos_y >= h - planet_list[index].radius or planet_list[index].pos_y <= planet_list[
        index].radius:
        planet_list[index].update_velocity_y(-coefficient_of_collision * planet_list[index].vel_y)


# maps a variables values based on old range and new range linearly
# source: https://stackoverflow.com/questions/929103/convert-a-number-range-to-another-range-maintaining-ratio
def variable_mapping(value, from_low, from_high, to_low, to_high):
    old_range = (from_high - from_low)
    new_range = (to_high - to_low)
    new_value = (((value - from_low) * new_range) / old_range) + to_low
    return new_value

class ListSwitch:
    def __init__(self, length):
        self.list = []
        for i in range(length):
            self.list.append(False)

    def set_on(self, index):
        for i in range(len(self.list)):
            if i != index:
                self.list[i] = False
            else:
                self.list[i] = True

    def get_on(self):
        for i, state in enumerate(self.list):
            if state:
                return i
