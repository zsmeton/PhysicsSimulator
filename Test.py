# Library Imports:
import pygame as pg

import Planets as p
import globalFunctions as gf

if __name__ == '__main__':
    planet_list = []
    default = 0
    for i in range(1, 4):
        planet = p.Planet(200, 200, 20, 20)
        planet.change_mass(1 * 10 ** 9.5)
        planet_list.append(planet)
    planet_x = dict.fromkeys(planet_list, default)
    planet_y = dict.fromkeys(planet_list, default)
    planet_x, planet_y = gf.accel_due_to_gravity(planet_x, planet_y, planet_list)
    print(planet_x)
    print(planet_y)


    # Close the window and quit.
    pg.quit()
