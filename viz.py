#! python3 

import cmd, textwrap, random, time, arcade, os
from worldRooms import *
from worldItems import *
from worldCreatures import *
from variables import *
from random import randint
from colorama import init, Fore, Back, Style
from game import *

init(convert=True)


class RoomCreatures(arcade.Sprite):

    def update(self):
        pass

class Visuals(arcade.Window):
    """ An Arcade game. """

    def __init__(self, width, height, title):
        """ Constructor. """
        file_path = os.path.dirname(os.path.abspath(__file__))
        os.chdir(file_path)
        super().__init__(width, height, title)
        arcade.set_background_color(WINDOW_BACKGROUND_COLOR)
        self.adv = TextAdventureCmd()
        self.creature_list = arcade.SpriteList()
        self.creature_sprite = None

    def setup(self):
        pass

    def on_draw(self):
        """ Called whenever we need to draw the window. """
        global maxHealthbar
        if worldRooms[location].get(COLOR, False) != False:
            if worldRooms[location][COLOR] == 'RED':
                color = arcade.color.RED
            elif worldRooms[location][COLOR] == 'GREEN':
                color = arcade.color.GREEN
            elif worldRooms[location][COLOR] == 'YELLOW':
                color = arcade.color.YELLOW
            elif worldRooms[location][COLOR] == 'BLUE':
                color = arcade.color.BLUE
            elif worldRooms[location][COLOR] == 'MAGENTA':
                color = arcade.color.MAGENTA
            elif worldRooms[location][COLOR] == 'CYAN':
                color = arcade.color.CYAN
            elif worldRooms[location][COLOR] == 'GRAY':
                color = arcade.color.GRAY
            elif worldRooms[location][COLOR] == 'BEIGE':
                color = arcade.color.BEIGE
        else:
            color = arcade.color.WHITE
        arcade.start_render()
        arcade.set_background_color(color)
        arcade.draw_lrtb_rectangle_filled(0, WINDOW_WIDTH, (1/3)*WINDOW_HEIGHT, 0, arcade.color.BLACK)
        arcade.draw_lrtb_rectangle_outline(20, maxHealthbar, 180, 160, arcade.color.GREEN)
        arcade.draw_lrtb_rectangle_filled(20, self.healthbar, 180, 160, arcade.color.GREEN)
        arcade.draw_lrtb_rectangle_filled(WINDOW_WIDTH-40, WINDOW_WIDTH-40, (1/3)*WINDOW_HEIGHT-20, (1/3)*WINDOW_HEIGHT-40, arcade.color.GRAY)

        self.creature_list.draw()        

    def on_key_release(self, key, modifiers):
        if key == arcade.key.W:
            self.adv.do_north('north')
        elif key == arcade.key.A:
            self.adv.do_west('west')
        elif key == arcade.key.S:
            self.adv.do_south('south')
        elif key == arcade.key.D:
            self.adv.do_east('east')
        elif key == arcade.key.Z:
            self.adv.do_down('down')
        elif key == arcade.key.X:
            self.adv.do_up('up')
        elif key == arcade.key.Q:
            self.adv.do_attack('pig')

    def update(self, delta_time):
        """ Called to update our objects. Happens approximately 60 times per second. """
        self.healthbar = (stats[0]/maxHealth)*maxHealthbar
        
        if len(worldRooms[location][CREATURES]) > 0:
            for item in worldRooms[location][CREATURES]:
                self.creature_sprite = RoomCreatures("sprites/%s.png" % worldCreatures[item][SPRITE])
                self.creature_sprite.center_x = 400
                self.creature_sprite.center_y = 300
                self.creature_list.append(self.creature_sprite)
        else:
            for x in self.creature_list:
                if len(self.creature_list) > 0:
                    self.creature_list.pop()
        

def bork():
    window = Visuals(WINDOW_WIDTH, WINDOW_HEIGHT, WINDOW_TITLE)
    window.setup()
    arcade.run()

if __name__ == '__main__':
    #titleScreen()
    levelUp()
    equippedCheck()
    displayLocation(location)
    bork()
    TextAdventureCmd().cmdloop()