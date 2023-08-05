#! usr/bin python3
# coding:utf-8

"""Module containing all classes for the labyrinth game"""

import pygame
from pygame.locals import *

#Constants containing the paths of pictures files
#Use it to change the theme of the labyrinth
WALL_PICTURE = 'pictures/wall.png'
PLAYER_PICTURE = 'pictures/macgyver.png'
GUARDIAN_PICTURE = 'pictures/guardian.png'
#This Constant is not a complete path for this programme because it use
#different pictures
STUFF = 'pictures/stuff_'


class Sprite(pygame.sprite.Sprite):
    """Basic class used for all sprites of the game"""

    def __init__(self, picture, rect_x, rect_y):
        """Each sprite need at least a position"""
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load(picture).convert_alpha()

        self.rect = self.image.get_rect()

        self.rect.x = rect_x

        self.rect.y = rect_y


class Wall(Sprite):
    """Class used for all the walls of the labyrinth"""

    def __init__(self, rect_x, rect_y):
        """Builder, use the mother class builder"""
        Sprite.__init__(self, WALL_PICTURE, rect_x, rect_y)


class Player(Sprite):
    """Class representing the player character"""

    def __init__(self, rect_x, rect_y):
        """Builder, use mother class builder and add a score counter"""
        Sprite.__init__(self, PLAYER_PICTURE, rect_x, rect_y)
        #Count number of stuff for the victory condition
        self.score = 0

    def move(self, direction, wall_list):
        """Function used to make the character move"""
        #Create an instance of Sprite for comparing destination position
        #to the wall_list group and test if there is collision
        new_player = Player(self.rect.x, self.rect.y)

        if direction == K_DOWN:
            new_player.rect = new_player.rect.move(0, 40)
            if not pygame.sprite.spritecollide(new_player, wall_list, False):
                self.rect = new_player.rect
        elif direction == K_UP:
            new_player.rect = new_player.rect.move(0, -40)
            if not pygame.sprite.spritecollide(new_player, wall_list, False):
                self.rect = new_player.rect
        elif direction == K_LEFT:
            new_player.rect = new_player.rect.move(-40, 0)
            if not pygame.sprite.spritecollide(new_player, wall_list, False):
                self.rect = new_player.rect
        elif direction == K_RIGHT:
            new_player.rect = new_player.rect.move(40, 0)
            if not pygame.sprite.spritecollide(new_player, wall_list, False):
                self.rect = new_player.rect


class Stuff(Sprite):
    """Class representing the object that the player need to catch"""
    #Class variable used to generate 7 object on the map
    COUNT = 7

    def __init__(self, rect_x, rect_y):
        """Builder, use mother class builder"""
        #Use COUNT to generate object with different pictures
        stuff_picture = STUFF + str(Stuff.COUNT) + '.png'
        Sprite.__init__(self, stuff_picture, rect_x, rect_y)

    def position(self, rect_x, rect_y, player, wall_list):
        """Function used to test if position of the new object
        doesn't collide with another sprite and positionning the
        object if it's ok"""
        test_stuff = Stuff(0, 0)
        test_stuff.rect.x = rect_x
        test_stuff.rect.y = rect_y

        if not pygame.sprite.spritecollide(test_stuff, wall_list, False)\
         and not pygame.sprite.collide_rect(test_stuff, player):
            self.rect.x = rect_x
            self.rect.y = rect_y


class Guardian(Sprite):
    """Class representing the guardian, the final boss"""

    def __init__(self, rect_x, rect_y):
        """Builder, use the mother class builder"""
        Sprite.__init__(self, GUARDIAN_PICTURE, rect_x, rect_y)

