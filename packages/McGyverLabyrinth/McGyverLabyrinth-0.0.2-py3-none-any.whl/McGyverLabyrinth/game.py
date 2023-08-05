#! usr/bin/env python3
# coding:utf-8

"""Labyrinth game. The player (McGyver) need to collect 7 item and find the 
path to the guardian to win the game"""

import random as rd

import pygame
from pygame.locals import *
import pandas as pd

import class_game as cl

pygame.init()
#window of the game
window = pygame.display.set_mode((680, 680), RESIZABLE)
backgroud = pygame.Surface([680, 680])
window.blit(backgroud, (0, 0))
#Make the character move while the key is supported
pygame.key.set_repeat(400, 30)

#Create sprite groups use for drawing sprites and collision management
edge_list = pygame.sprite.Group()
wall_list = pygame.sprite.Group()
stuff_list = pygame.sprite.Group()
all_sprite = pygame.sprite.Group()


def create_border():
    """Create the borders of the window"""
    for i in range(0, 680, 40):
        border_left = cl.Wall(0, i)
        border_right = cl.Wall(640, i)
        border_up = cl.Wall(i, 0)
        border_down = cl.Wall(i, 640)
        wall_list.add(border_left, border_right, border_up, border_down)
        all_sprite.add(border_left, border_right, border_up, border_down)

def data_from_csv(csv_file):
    """Read a csv file and retrun dataframe"""
    data = pd.read_csv(csv_file, sep=',', header=None, dtype=str)
    return data

def update_screen():
    """Function used after each keydown event, to update the screen.
    First, it test if victory condition is ok or not."""
    if win_condition == 'no':
        gameover = pygame.image.load('pictures/gameover.png').convert()
        window.blit(gameover, (0, 0))
    elif win_condition == 'yes':
        youwin = pygame.image.load('pictures/win.png').convert()
        window.blit(youwin, (0, 0))
    else:
        window.blit(backgroud,(0,0))
        all_sprite.draw(window)
    pygame.display.flip()


#Read the csv file containing the labyrinth
labyrinthe_map = data_from_csv('level.csv')

#Use the fonction to create border of the window
create_border()

#Variable to start drawing the labyrinth after the border of the window
x_pos = 40
y_pos = 40

#Generation of Labyrinth
#Use the values of the csv file to design labyrinth
for row, series in labyrinthe_map.iterrows():
    x_pos = 40
    for columns, series in labyrinthe_map.iteritems():
        #Create walls
        if labyrinthe_map.iloc[row, columns] == '1':
            wall = cl.Wall(x_pos, y_pos)
            #Add in groups for drawing and collision management
            wall_list.add(wall)
            all_sprite.add(wall)
        #Create player character
        elif labyrinthe_map.iloc[row, columns] == 'start':
            player = cl.Player(x_pos, y_pos)
            #Add to the all_sprite group for drawing
            all_sprite.add(player)
        #Create guardian
        elif labyrinthe_map.iloc[row, columns] == 'finish':
            guardian = cl.Guardian(x_pos, y_pos)
            #Add to the all_sprite group for drawing
            all_sprite.add(guardian)
        x_pos = x_pos + 40
    y_pos = y_pos + 40

#Generation of items
#item are position
while cl.Stuff.COUNT != 0:
    #fonction de creation
    stuff = cl.Stuff(0, 0)
    while pygame.sprite.spritecollide(stuff, wall_list, False)\
     or pygame.sprite.spritecollide(stuff, stuff_list, False):
        rect_x = rd.randrange(40, 600, 40)
        rect_y = rd.randrange(40, 600, 40)
        stuff.position(rect_x, rect_y, player, wall_list)
    #Add to the groups for drawing and collision management
    stuff_list.add(stuff)
    all_sprite.add(stuff)
    cl.Stuff.COUNT -= 1

#While this condition is different than 'yes' or 'no', the game continue
win_condition = ''
#While this variable is not 0 the window of the game is active
continuer = 1

#Main loop
while continuer:
    for event in pygame.event.get():
        if event.type == QUIT:
            continuer = 0
        elif event.type == KEYDOWN:
            direction = event.key
            player.move(direction, wall_list)
            #When the player touch an item, he kill it and get one point
            if pygame.sprite.spritecollide(player, stuff_list, True):
                player.score += 1
            #Test if the player touch the guardian
            elif pygame.sprite.collide_rect(player, guardian):
                if player.score == 7:
                    win_condition = 'yes'
                else:
                    win_condition = 'no'
    update_screen()
