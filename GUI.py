# __ Classes for Graphical Interface __ #

import pygame as pg
from pygame import gfxdraw as gfx

import Planets as P
import Vector
import globalFunctions as functions

# color constants
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (204, 0, 0)
INACTIVE = (190, 190, 190)
ACTIVE = (80, 80, 80)
YELLOW = (255, 255, 0)
BLUE = (50, 50, 255)
GREY = (200, 200, 200)
ORANGE = (200, 100, 50)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
TRANS = (1, 1, 1)

# initializes pygame
pg.init()
# sets up the font for the game
BoxFont = pg.font.Font(None, 32)
ButtonFont = pg.font.Font(None, 25)
VectorFont = pg.font.Font(None, 12)


# background image class
# source : https://stackoverflow.com/questions/28005641/how-to-add-a-background-image-into-pygame
class Background(pg.sprite.Sprite):
    def __init__(self, image_file, location):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pg.image.load(image_file)
        self.rect = self.image.get_rect()
        self.rect.center = location


# input box
# source : https://stackoverflow.com/questions/46390231/how-to-create-a-text-input-box-with-pygame
class InputBox:
    def __init__(self, x, y, w, h, text=''):
        self.rect = pg.Rect(x, y, w, h)
        self.color = INACTIVE
        self.text = text
        self.txt_surface = BoxFont.render(text, True, self.color)
        self.active = False

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = not self.active
            else:
                self.active = False
            # Change the current color of the input box.
            self.color = CYAN if self.active else INACTIVE
        if event.type == pg.KEYDOWN:
            if self.active:
                if event.key == pg.K_RETURN:
                    if self.text.isdigit():
                        return self.text
                    else:
                        self.text = ''
                elif event.key == pg.K_BACKSPACE:
                    self.text = self.text[:-1]
                else:
                    self.text += event.unicode
                # Re-render the text.
                self.txt_surface = BoxFont.render(self.text, True, self.color)

    def update(self):
        # Resize the box if the text is too long.
        width = max(200, self.txt_surface.get_width() + 10)
        self.rect.w = width

    def draw(self, screen):
        # Blit the text.
        screen.blit(self.txt_surface, (self.rect.x + 85, self.rect.y + 11))
        # Blit the rect.
        pg.draw.rect(screen, self.color, self.rect, 2)


def text_objects(text, font):
    text_surface = font.render(text, True, CYAN)
    return text_surface, text_surface.get_rect()


# button class light weight version of
# source : https://github.com/Mekire/pygame-button/blob/master/button/button.py
# with elements of
# source : https://pythonprogramming.net/pygame-buttons-part-1-button-rectangle/
class Button:
    def __init__(self, msg, x, y, w, h, ic, ac, action=None, state=None, state_name=None):
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.action = action
        self.inactive_c = ic
        self.active_c = ac
        self.color = self.inactive_c
        self.msg = msg
        self.text_surf, self.text_rect = text_objects(self.msg, ButtonFont)
        self.text_rect.center = ((x + (w / 2)), (y + (h / 2)))
        self.active = False
        self.state = state
        self.variable = state_name
        if self.state is not None:
            self.text_state = SettingsText(self.x, self.y, self.state)

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                if self.action is not None:
                    self.action()
                if self.state is not None:
                    if isinstance(self.state, bool):
                        self.state = not self.state
                    elif isinstance(self.state, float):
                        if self.state <= 2:
                            self.state += 0.1
                        else:
                            self.state = 0.1
                    self.text_state.update_text(self.state)
                    return self.state

    def check_hover(self):
        if self.rect.collidepoint(pg.mouse.get_pos()):
            if not self.active:
                self.active = True
        else:
            self.active = False

    def draw(self, screen):
        if self.active:
            self.color = self.active_c
            pg.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))
            if self.state is not None:
                self.text_state.draw(screen)
        else:
            self.color = self.inactive_c
            pg.draw.rect(screen, (119, 119, 119), (self.x - 5, self.y - 5, self.w + 10, self.h + 10))
            pg.draw.rect(screen, self.color, (self.x, self.y, self.w, self.h))
            if self.state is not None:
                self.text_state.draw(screen)
        # Blit the text.
        screen.blit(self.text_surf, self.text_rect)


# slider GUI class
class Slider:
    def __init__(self, linked_, min_val, max_val, x, y, length, width, screen_size, color):
        object_x = x
        object_y = y
        self.screen = screen_size
        self.linked_object = linked_
        self.width = width
        self.length = length
        self.inactive_c = (94, 0, 85)
        self.active_c = (9, 0, 94)
        self.active = False
        self.color = self.inactive_c
        self.color_o = self.active_c
        self.bar_c = color
        self.x, self.y = self._set_location(object_x, object_y)
        self.value = 0
        self.min = min_val
        self.max = max_val
        self.orient = "horizontal"
        self.placement = round((self.y + self.width / 2))
        self.slide_radius = round(self.width / 1.5)
        if isinstance(linked_, P.Planet):
            self.slide_pos = int(functions.variable_mapping(linked_.mass, min_val, max_val, 0, 100))
        elif isinstance(linked_, int):
            self.slide_pos = int(functions.variable_mapping(linked_, min_val, max_val, 0, 100))
        else:
            self.slide_pos = 0
        self.rect = pg.Rect(x, y, self.slide_radius * 2, self.slide_radius * 2)
        self._update_hit_box()

    def _update_hit_box(self):
        if self.width <= self.length:
            self.orient = "horizontal"
            self.placement = round((self.y + self.width / 2))
            self.rect = pg.Rect((self.x + self.slide_pos - self.slide_radius), self.placement - self.slide_radius,
                                self.slide_radius * 2, self.slide_radius * 2)
        else:
            self.orient = "vertical"
            self.placement = round((self.x + self.length / 2))
            self.rect = pg.Rect((self.x + self.length / 2) - self.slide_radius,
                                (self.y + self.slide_pos) - self.slide_radius, self.slide_radius * 2,
                                self.slide_radius * 2)

    def _set_location(self, x, y):
        temp_x = x - (self.length + 35)
        temp_y = y + self.width * 3
        limits = self.screen
        if temp_x <= 0:
            temp_x = x + self.length + 10
        if temp_y >= limits[1] - 70:
            temp_y = y - (self.width * 3)
        return temp_x, temp_y

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicks on slide ball
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = True
                self.color = self.active_c
                self.color_o = self.inactive_c
                return True
            elif self.active:
                self.active = False
                self.color = self.inactive_c
                self.color_o = self.active_c
                self._update_hit_box()
                return True
            else:
                self.active = False
                return False
            # Change the current color of the input box.
        if self.active:
            mouse = pg.mouse.get_pos()
            if self.orient is "horizontal":
                self.slide_pos = mouse[0] - self.x
                if self.slide_pos > self.length:
                    self.slide_pos = self.length
                if self.slide_pos <= 0:
                    self.slide_pos = 0
            else:
                self.slide_pos = mouse[1] - self.y
                if self.slide_pos > self.width:
                    self.slide_pos = self.width
        return True

    def draw(self, screen):
        offset = 4
        pg.draw.rect(screen, (119, 119, 119),
                     (self.x - round(offset / 2), self.y - round(offset / 2), self.length + offset, self.width + offset))
        pg.draw.rect(screen, self.bar_c, (self.x, self.y, self.length, self.width))

        if self.orient is "horizontal":
            gfx.aacircle(screen, self.x + self.slide_pos, self.placement, self.slide_radius + round(offset / 2),
                         self.color)
            gfx.filled_circle(screen, self.x + self.slide_pos, self.placement, self.slide_radius + round(offset / 2),
                              self.color)
            gfx.aacircle(screen, self.x + self.slide_pos, self.placement, self.slide_radius - round(offset / 2),
                         self.color_o)
            gfx.filled_circle(screen, self.x + self.slide_pos, self.placement, self.slide_radius - round(offset / 2),
                              self.color_o)
            # Blit the text.
            # screen.blit(self.text_surf, self.text_rect)
        else:
            gfx.aacircle(screen, self.placement, self.y + self.slide_pos, self.slide_radius + round(offset / 2),
                         self.color)
            gfx.filled_circle(screen, self.placement, self.y + self.slide_pos, self.slide_radius + round(offset / 2),
                              self.color)
            gfx.aacircle(screen, self.placement, self.y + self.slide_pos, self.slide_radius - round(offset / 2),
                         self.color_o)
            gfx.filled_circle(screen, self.placement, self.y + self.slide_pos, self.slide_radius - round(offset / 2),
                              self.color_o)
            # Blit the text.
            # screen.blit(self.text_surf, self.text_rect)

    def get_value(self):
        self.value = functions.variable_mapping(self.slide_pos, 0, 100, self.min, self.max)
        return self.value, self.linked_object


class Tool(pg.sprite.Sprite):
    def __init__(self, image_file, location):
        pg.sprite.Sprite.__init__(self)  # call Sprite initializer
        self.image = pg.image.load(image_file)
        self.rect = self.image.get_rect()
        self.location = location
        self.rect.midleft = location

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # If the user clicks on slide ball
            if self.rect.collidepoint(event.pos):
                return True
            else:
                return False


class ToolBar:
    def __init__(self, x, y, l, w):
        self.spacing = 55
        self.x = x
        self.y = y
        self.offset = 2
        self.length = l + self.offset * 2
        self.width = w + self.offset * 2
        self.rect = pg.Rect(x, y, self.length, self.width)
        self.rect.bottomright = [x, y]
        self.outline = pg.Rect(x, y, self.length+6, self.width+6)
        self.outline.bottomright = [x+3, y+3]
        self.highlight = pg.Rect(x, y, 50, 50)
        self.tool_list = []
        self.tool_states = functions.ListSwitch(5)

    def draw(self, screen):
        pg.draw.rect(screen, CYAN, self.outline)
        pg.draw.rect(screen, (50, 50, 50), self.rect)
        pg.draw.rect(screen, (100, 100, 100), self.highlight)
        location = [self.x - self.length + self.offset, self.y - (self.width / 2) + self.offset]
        move = Tool('physics_arrow.png', location)
        screen.blit(move.image, move.rect)
        location = [self.x - self.length + self.offset + self.spacing, self.y - (self.width / 2) + self.offset]
        vector = Tool('physics_vector.png', location)
        screen.blit(vector.image, vector.rect)
        location = [self.x - self.length + self.offset + self.spacing * 2, self.y - (self.width / 2) + self.offset]
        color = Tool('physics_color.png', location)
        screen.blit(color.image, color.rect)
        location = [self.x - self.length + self.offset + self.spacing * 3, self.y - (self.width / 2) + self.offset]
        mass = Tool('physics_mass.png', location)
        screen.blit(mass.image, mass.rect)
        location = [self.x - self.length + self.offset + self.spacing * 4, self.y - (self.width / 2) + self.offset]
        delete = Tool('physics_delete.png', location)
        screen.blit(delete.image, delete.rect)
        self.tool_list = [move, vector, color, mass, delete]

    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                print("Bar Hit")
                for i, tool in enumerate(self.tool_list):
                    state = tool.handle_event(event)
                    if state:
                        self.tool_states.set_on(i)
                index = self.tool_states.get_on()
                self.highlight.midleft = self.tool_list[index].location
                return True
            else:
                return False

    def active_tool(self):
        return self.tool_states.get_on()


class ColorSlider:
    def __init__(self, linked, x_, y_, length, width, screen_size):
        self.x = x_
        self.y = y_
        self.l = length
        self.w = width
        self.screen_limit = screen_size
        self.r = linked.R
        self.g = linked.G
        self.b = linked.B
        self.linked_object = linked
        self.offset = 30
        self.slider_r = Slider(self.r, 0, 255, self.x, self.y, self.l, self.w, self.screen_limit, (255, 0, 10))
        self.slider_g = Slider(self.g, 0, 255, self.x, self.y + self.offset, self.l, self.w, self.screen_limit,
                               (10, 255, 10))
        self.slider_b = Slider(self.b, 0, 255, self.x, self.y + self.offset * 2, self.l, self.w, self.screen_limit,
                               (10, 0, 255))
        self.rect = pg.Rect(x_, y_, length, width * 3 + 2 * self.offset)
        self.active = True

    def handle_event(self, event):
        r_active = self.slider_r.handle_event(event)
        g_active = self.slider_g.handle_event(event)
        b_active = self.slider_b.handle_event(event)
        print(r_active, g_active, b_active)
        if r_active or g_active or b_active:
            return True
        else:
            print("exiting")
            self.active = False
            return False

    def draw(self, screen):
        self.slider_r.draw(screen)
        self.slider_g.draw(screen)
        self.slider_b.draw(screen)

    def get_value(self):
        self.r, nin = self.slider_r.get_value()
        print(self.r)
        self.g, nin = self.slider_g.get_value()
        print(self.g)
        self.b, nin = self.slider_b.get_value()
        print(self.b)
        return [round(self.r), round(self.g), round(self.b)], self.linked_object


class MouseVector:
    def __init__(self, linked, x, y):
        self.x = x
        self.y = y
        self.linked = linked
        self.origin = Vector.Vector(self.x, self.y)
        temp_ = Vector.Vector(linked.vel_x, linked.vel_y)
        self.mouse = temp_ + self.origin
        self.rect = linked.rect
        self.active = True
        # sets the lowest value for the vector as the radius of the planet so clicking near the surface is about 0 vel
        self.low = linked.radius
        self.max = 3



    def handle_event(self, event):
        if event.type == pg.MOUSEBUTTONDOWN:
            # first click turns it on
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                if not self.active:
                    self.mouse.set(self.x, self.y)
                return True
            # second click turns it off bu doesn't let other object instance happen
            elif self.active:
                print("almost off")
                self.active = False
                return True
            # turns off completely and allows others
            else:
                print("off")
                self.active = False
                return False
        else:
            return True

    def draw(self, screen):
        if self.active:
            x_, y_ = pg.mouse.get_pos()
            self.mouse.set(x_, y_)
            if self.origin.dist(self.mouse) > 100:
                self.mouse.sub(self.origin)
                self.mouse.limit(100)
                self.mouse.add(self.origin)
            end_point = [self.mouse.x, self.mouse.y]
            start_point = [self.origin.x, self.origin.y]
            pg.draw.aaline(screen, CYAN, start_point, end_point, True)
            vx,vy,other = self.get_value()
            vel = Vector.Vector(vx,vy)
            tool_tip = "%.2f" % vel.mag()
            text_surface = VectorFont.render(tool_tip, True, CYAN)
            text_rect = text_surface.get_rect()
            vel.normalize()
            text_rect.center = [x_+(30*vel.x), y_+(30*vel.y)]
            screen.blit(text_surface, text_rect)

    def get_value(self):
        print("mouse:", self.mouse, "origin:", self.origin, "dist:", self.origin.dist(self.mouse))
        result = self.mouse - self.origin
        vx_ = functions.variable_mapping(result.x, 0, 100, 0, self.max)
        vy_ = functions.variable_mapping(result.y, 0, 100, 0, self.max)
        print("returned", vx_, vy_)
        return vx_, vy_, self.linked


# source : https://gamedev.stackexchange.com/questions/26550/how-can-a-pygame-image-be-colored
def colorize(image, newColor):
    """
    Create a "colorized" copy of a surface (replaces RGB values with the given color, preserving the per-pixel alphas of
    original).
    :param image: Surface to create a colorized copy of
    :param newColor: RGB color to use (original alpha values are preserved)
    :return: New colorized Surface instance
    """
    image = image.copy()
    # zero out RGB values
    image.fill((0, 0, 0, 255), None, pg.BLEND_RGBA_MULT)
    # add in new RGB values
    image.fill(newColor[0:3] + (0,), None, pg.BLEND_RGBA_ADD)
    return image


class SettingsText:
    def __init__(self, x, y, setting):
        self.msg = str(setting)
        self.font = pg.font.Font(None, 22)
        self.text_surf, self.text_rect = text_objects(self.msg, self.font)
        self.x = x
        self.y = y

    def update_text(self, setting):
        print(self.msg)
        if isinstance(setting, float):
            self.msg = str("%.1f" % setting)
        elif isinstance(setting, bool):
            self.msg = str(setting)
        self.text_surf, self.text_rect = text_objects(self.msg, self.font)
        print(self.msg)

    def draw(self, screen):
        screen.blit(self.text_surf, (self.x, self.y))
