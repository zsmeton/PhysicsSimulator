# __ main loop __ #
# does mostly graphics and game setup
# Library Imports:
import ctypes
import fileinput
import random
import re
import time

import pygame as pg

import GUI
import Planets as P
import game_loop as game

# Globals
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (204, 0, 0)
INACTIVE = (102, 102, 102)
ACTIVE = (56, 0, 94)

# get amount of planets for the simulation
amntOfPlanets = 0

# game setting booleans
weed = False
settings = {'walls': False, 'trails': False, 'cool_trail': False, 'strobe': False, 'aa': False, 't_step': 0.2}
setup = False


def get_settings():
    with open("settings.txt", 'r+') as data:
        for line in data:
            for setting in settings:
                if setting in line:
                    if 'False' in line:
                        settings[setting] = False
                    elif 'True' in line:
                        settings[setting] = True
                    else:
                        amount = re.findall("\d+\.\d+", line)
                        amount = float(amount[0])
                        settings[setting] = amount
    print(settings)


def setup_pygame():
    global myfont, screen, BackGround, clock, clear, WIDTH, HEIGHT
    # set up pygame
    pg.init()  # initializes screen full screen
    pg.mouse.set_cursor(*pg.cursors.diamond)
    ctypes.windll.user32.SetProcessDPIAware()
    true_res = (ctypes.windll.user32.GetSystemMetrics(0), ctypes.windll.user32.GetSystemMetrics(1))
    screen = pg.display.set_mode(true_res, pg.FULLSCREEN)
    pg.display.set_caption("Physics Simulator")
    clock = pg.time.Clock()  # used to manage how fast the screen updates
    myfont = pg.font.Font(None, 36)  # sets the font for text in pygame
    rect_x = 50
    rect_y = 50
    WIDTH, HEIGHT = pg.display.get_surface().get_size()  # gets the size of the screen for planet placement
    # image source :
    BackGround = GUI.Background('background_.jpg', [WIDTH / 2, HEIGHT / 2])
    print(WIDTH, HEIGHT)
    s_x = 27  # size of clearing box in x
    s_y = 27  # size of clearing box in y
    clear = pg.Surface((s_x, s_y))  # small clearing box for smaller screen updates
    clear.fill(BLACK)  # sets clearing box to black


# the loop which runs once game setup has been completed
def run_time(planet_list):
    global settings, setup
    new_simulation = False
    # Variable Creation
    t = 0
    screen.fill(BLACK)
    pg.display.flip()
    # --- Main Loop --- #
    while not new_simulation:
        # gets key events which add extra features to the simulation
        for event in pg.event.get():
            if event.type == pg.QUIT:
                pg.quit()
            elif event.type == pg.KEYUP:
                # exits code
                if event.key == pg.K_ESCAPE:
                    introScreen()
                # enable/disable wall collision
                elif event.key == pg.K_w:
                    settings['walls'] = not settings['walls']
                # enable/disable strobe planets
                elif event.key == pg.K_s:
                    settings['strobe'] = not settings['strobe']
                # enable/disable translucent trails
                elif event.key == pg.K_t:
                    settings['trails'] = not settings['trails']
                    if settings['cool_trail']:
                        settings['cool_trail'] = not settings['cool_trail']
                    elif not settings['cool_trail']:
                        screen.fill(BLACK)
                        pg.display.flip()
                # enable/disable solid trails
                elif event.key == pg.K_c:
                    settings['cool_trail'] = not settings['cool_trail']
                    if settings['trails']:
                        settings['trails'] = not settings['trails']
                    elif not settings['trails']:
                        screen.fill(BLACK)
                        pg.display.flip()
                elif event.key == pg.K_r:
                    new_simulation = True
                    screen.fill(BLACK)
                    pg.display.flip()
                    time.sleep(.5)
                    break

        # recalculates planets and their positions
        merge_list = game.update_planets(WIDTH, HEIGHT, planet_list, settings['t_step'], settings['walls'])
        if len(merge_list) > 2:
            for i in range(0, len(merge_list), 2):
                if merge_list[i] not in planet_list:
                    print("error x not in list")
                else:
                    planet_list.remove(merge_list[i])

        # deletes old drawings and replaces with black
        if not settings['trails'] and not settings['cool_trail']:
            if len(planet_list[0].pos_x_list) > 2:
                for planet in planet_list:
                    s = pg.Surface((round(planet.radius) * 3, round(planet.radius) * 3))
                    s.fill(BLACK)
                    screen.blit(s, (
                        planet.pos_x_list[-2] - planet.radius * 1.5, planet.pos_y_list[-2] - planet.radius * 1.5))
        # process for translucent tail
        if settings['cool_trail']:
            trails = False
            if len(planet_list[0].pos_x_list) > 2:
                for planet in planet_list:
                    s = pg.Surface((round(planet.radius) * 2.2, round(planet.radius) * 2.2))
                    s.fill(BLACK)
                    s.set_alpha(5)
                    screen.blit(s, (planet.pos_x_list[-2] - planet.radius, planet.pos_y_list[-2] - planet.radius))

        # draw each planet
        # strobe feature
        if not settings['strobe']:
            if weed:
                for planet in planet_list:
                    planet.draw(screen, image=True)
            else:
                for planet in planet_list:
                    planet.draw(screen, aa=settings['aa'])
        else:
            if weed:
                for planet in planet_list:
                    planet.draw(screen, image=True,
                                color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            else:
                for planet in planet_list:
                    planet.draw(screen, color=(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)),
                                aa=settings['aa'])

        # Prints time in simulation
        t = t + settings['t_step']
        time_text = str(round(t))
        screen.fill(BLACK, (30, 10, 110, 30))
        time_draw = myfont.render(time_text, 1, (255, 255, 255))
        screen.blit(time_draw, (30, 10))

        # update display
        pg.display.flip()

        # No limit to fps
        clock.tick(200000)


# main menu for the game
def introScreen():
    buttons = []
    random_button = GUI.Button("Random Generation", WIDTH / 2 - 500, HEIGHT / 2 + 100, 200, 50, INACTIVE, ACTIVE, random_loop)
    buttons.append(random_button)
    galaxy_button = GUI.Button("Galaxy Creation", WIDTH / 2 - 100, HEIGHT / 2 + 100, 200, 50, INACTIVE, ACTIVE, galaxy_creator)
    buttons.append(galaxy_button)
    quit_button = GUI.Button("Quit", WIDTH / 2 + 300, HEIGHT / 2 + 100, 200, 50, INACTIVE, ACTIVE, quit)
    buttons.append(quit_button)
    settings_button = GUI.Button("Settings", WIDTH - 350, HEIGHT - 200, 100, 50, INACTIVE, ACTIVE, set_page)
    buttons.append(settings_button)
    intro = True
    while intro:
        for event in pg.event.get():
            for button in buttons:
                button.handle_event(event)
            # print(event)
            if event.type == pg.QUIT:
                pg.quit()
                quit()
        screen.fill(BLACK)
        screen.blit(BackGround.image, BackGround.rect)
        large_text = pg.font.Font(None, 120)
        text_surf, text_rect = GUI.text_objects("PHYSICS SIMULATOR PRO: 2018", large_text)
        text_rect.center = ((WIDTH / 2), (HEIGHT / 2) - 200)
        screen.blit(text_surf, text_rect)
        for button in buttons:
            button.check_hover()
            button.draw(screen)

        pg.display.update()
        clock.tick(60)


# loop for random generation user input for how many planets which are then generated
def random_loop():
    global settings, setup, weed, amntOfPlanets
    weed = False
    setup = False
    game_is_running = True  # as long as the game is running this is true and the pygame window persists
    input_box = GUI.InputBox(WIDTH / 2 - 100, HEIGHT / 2, 200, 40)
    while game_is_running:
        user_input = None
        # takes user input in the form of a text box
        while not setup:
            # --- Set Up --- #
            # Create Planets
            for event in pg.event.get():
                if event.type == pg.KEYUP:
                    if event.key == pg.K_ESCAPE:
                        introScreen()
                user_input = input_box.handle_event(event)
                if user_input:
                    amntOfPlanets = int(user_input)
                    if amntOfPlanets == 420:
                        print("SMOKE WEED DAILY")
                        weed = True
                        amntOfPlanets = 42

            input_box.update()
            screen.fill(BLACK)
            screen.blit(BackGround.image, BackGround.rect)
            question = pg.font.Font(None, 40)
            text_surf, text_rect = GUI.text_objects("How many planets would you like?", question)
            text_rect.center = ((WIDTH / 2), (HEIGHT / 2) - 100)
            screen.blit(text_surf, text_rect)
            input_box.draw(screen)
            pg.display.flip()
            # checks if user input a value
            if user_input is not None:
                setup = True
                continue
        # randomly generates the amnt of planets inputted by user
        planet_list = []
        for j in range(amntOfPlanets):
            planet = P.Planet(WIDTH, HEIGHT)
            planet_list.append(planet)
        SUN = P.Planet(WIDTH, HEIGHT, sun=True)
        planet_list.append(SUN)
        run_time(planet_list)


# more interactive mode which allows users to set initial mass position and velocity of the planets
def galaxy_creator():
    global settings, setup, weed
    weed = False
    locals().update(settings)
    game_is_running = True  # as long as the game is running this is true and the pygame window persists
    planet_list = []
    slider_list = []
    color_list = []
    vector_list = []
    screen_limits = [WIDTH, HEIGHT]
    run = False
    tool_bar = GUI.ToolBar(WIDTH - 3, HEIGHT - 3, 275, 60)
    tool_selected = 0
    while game_is_running:
        done = False
        # after setup this runs the program
        if run:
            for planet in planet_list:
                planet.restart_planets()
            run_time(planet_list)
            for planet in planet_list:
                planet.restart_planets()
        while not done:
            object_selected = False
            # event handling
            for event in pg.event.get():
                selected = tool_bar.handle_event(event)
                if selected:
                    object_selected = True
                    tool_selected = tool_bar.active_tool()
                # -- event detection and result for each tool -- #
                # move tool
                if tool_selected is 0:
                    current_planet = None
                    for i, planet in enumerate(planet_list):
                        selected = planet.active_move
                        if selected:
                            current_planet = i
                            object_selected = True
                    for i, planet in enumerate(planet_list):
                        if object_selected:
                            if i is current_planet:
                                selected = planet.handle_event(event, tool_selected)
                                if not selected:
                                    object_selected = False
                        if not object_selected:
                            selected = planet.handle_event(event, tool_selected)
                            if selected:
                                object_selected = True
                # vector tool
                if tool_selected is 1:
                    for vector in vector_list:
                        active = vector.handle_event(event)
                        if active:
                            object_selected = True
                            vx, vy, planet = vector.get_value()
                            planet.planet_setup(vx_=vx, vy_=vy)
                        else:
                            vector_list.remove(vector)
                    if not object_selected:
                        for planet in planet_list:
                            if not object_selected:
                                selected = planet.handle_event(event, tool_selected)
                                if selected:
                                    velocity_vect = GUI.MouseVector(planet, planet.pos_x, planet.pos_y)
                                    vector_list.append(velocity_vect)
                                    object_selected = True
                # color tool
                if tool_selected is 2:
                    for color in color_list:
                        active = color.handle_event(event)
                        if active:
                            value, linked_object = color.get_value()
                            linked_object.planet_setup(color=value)
                            object_selected = True
                        else:
                            color_list.remove(color)
                    for planet in planet_list:
                        if not object_selected:
                            selected = planet.handle_event(event, tool_selected)
                            if selected:
                                color_slider = GUI.ColorSlider(planet, planet.pos_x, planet.pos_y, 100, 10,
                                                               screen_limits)
                                color_list.append(color_slider)
                                object_selected = True
                # mass tool
                elif tool_selected is 3:
                    for slider in slider_list:
                        active = slider.handle_event(event)
                        if active:
                            value, linked_object = slider.get_value()
                            linked_object.planet_setup(mass_=value)
                            object_selected = True
                        else:
                            slider_list.remove(slider)
                    for planet in planet_list:
                        if not object_selected:
                            selected = planet.handle_event(event, tool_selected)
                            if selected:
                                slider = GUI.Slider(planet, 1e9, 10e11, planet.pos_x, planet.pos_y, 100, 10,
                                                    screen_limits, ACTIVE)
                                slider_list.append(slider)
                                object_selected = True
                # delete tool
                elif tool_selected is 4:
                    for planet in planet_list:
                        selected = planet.handle_event(event, tool_selected)
                        if selected:
                            planet_list.remove(planet)
                            object_selected = True

                if event.type == pg.KEYUP:
                    if event.key == pg.K_ESCAPE:
                        introScreen()
                    elif event.key == pg.K_RETURN:
                        done = True
                        continue

                if event.type == pg.MOUSEBUTTONDOWN:
                    if not object_selected:
                        pos = pg.mouse.get_pos()
                        x = pos[0]
                        y = pos[1]
                        planet = P.Planet(WIDTH, HEIGHT, x, y)
                        planet_list.append(planet)
            # sets current planet list to initial planet list
            # clears screen
            screen.fill(BLACK)

            # --drawings for each tool-- #
            # move tool: no drawing
            # vector tool
            if tool_selected is 1:
                for vector in vector_list:
                    vector.draw(screen)
            # color tool
            elif tool_selected is 2:
                for color in color_list:
                    color.draw(screen)
            # mass tool
            elif tool_selected is 3:
                # draws slider
                for slider in slider_list:
                    slider.draw(screen)

            # draws planets
            for planet in reversed(planet_list):
                planet.draw(screen, aa=settings['aa'])
            # draws tool box
            tool_bar.draw(screen)
            # updates screen
            pg.display.flip()
        run = True


def set_page():
    global settings
    buttons = []
    setting_texts = []
    x_pos = -500
    y_sep = 100
    width = 200
    height = 50
    walls_button = GUI.Button("Walls", WIDTH / 2 + x_pos, HEIGHT / 2 - 2 * y_sep, width, height, INACTIVE, ACTIVE, state=settings['walls'], state_name='walls')
    buttons.append(walls_button)

    trails_button = GUI.Button("Trails", WIDTH / 2 + x_pos, HEIGHT / 2 - y_sep, width, height, INACTIVE, ACTIVE, state=settings['trails'], state_name='trails')
    buttons.append(trails_button)

    cool_trail_button = GUI.Button("Cool Trails", WIDTH / 2 + x_pos, HEIGHT / 2, width, height, INACTIVE, ACTIVE, state=settings['cool_trail'], state_name='cool_trail')
    buttons.append(cool_trail_button)

    strobe_button = GUI.Button("Strobe", WIDTH / 2 + x_pos, HEIGHT / 2 + y_sep, width, height, INACTIVE, ACTIVE, state=settings['strobe'], state_name='strobe')
    buttons.append(strobe_button)

    aa_button = GUI.Button("Anti-Aliasing", WIDTH / 2 + x_pos, HEIGHT / 2 + 2 * y_sep, width, height, INACTIVE, ACTIVE, state=settings['aa'], state_name='aa')
    buttons.append(aa_button)

    t_step_button = GUI.Button("Speed", WIDTH / 2 + x_pos, HEIGHT / 2 + 3 * y_sep, width, height, INACTIVE, ACTIVE, state=settings['t_step'], state_name='t_step')
    buttons.append(t_step_button)

    in_settings = True
    while in_settings:
        # --- Set Up --- #
        # Create Planets
        for event in pg.event.get():
            for button in buttons:
                output = button.handle_event(event)
                if output is not None:
                    print("the output is :", output)
            if event.type == pg.KEYUP:
                if event.key == pg.K_ESCAPE:
                    print(settings)
                    introScreen()
        screen.fill(BLACK)
        screen.blit(BackGround.image, BackGround.rect)
        settings_text = pg.font.Font(None, 120)
        text_surf, text_rect = GUI.text_objects("Settings", settings_text)
        text_rect.center = ((WIDTH / 2), (HEIGHT / 2) - 500)
        screen.blit(text_surf, text_rect)
        for button in buttons:
            setting = button.variable
            settings[setting] = button.state
            button.check_hover()
            button.draw(screen)

            try:
                for line in fileinput.input('settings.txt', inplace=True):
                    for setting in settings:
                        if setting in line:
                            line = line.replace("False", str(settings[setting]))
                            line = line.replace("True", str(settings[setting]))
                            if "True" not in line and "False" not in line:
                                line = "%s: %.1f" % (setting, settings[setting])
                            print(line)
            except FileExistsError:
                print("Error occurred try again")

        print(settings)
        locals().update(settings)

        for text in setting_texts:
            text.draw(screen)

        pg.display.update()
        clock.tick(60)


if __name__ == '__main__':
    get_settings()
    setup_pygame()
    introScreen()
    # Close the window and quit.
    pg.quit()
