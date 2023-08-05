#!python
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 10 17:59:25 2017

@author: fredericvidry

The MacGyver Game, is a labyrinth where MacGyver needs to escape from
his best ennemy Murdoc. To escape, he will need to sleep Murdoc. To do that,
he must find few accessories like a needle, a syringe and an ether beaker,
without all these three elements, if McGyver meets Murdoc, he will die.

This game is the part 3 of the Openclassrooms path. This path
give an Apps Developpers Python grad.
"""
# Importation of tkinter to use as UI.
import tkinter as tk
# Importation of Image and ImageTk to open and manage images.
from PIL import Image, ImageTk
# Importation of random to use for accessories generation.
import random
# Importation of json module in view to read a JSON file
import json
# Importation of Mac Gyver Main module
import MacGyverMain as mgm

import os

import sys


# McGyver's mouvement restriction for the project.
BLOCK_NUMBER = 15
PICTURE_SIZE = 32
# Images filepath used in MacGyverGame and JSON file filepath which contains
# labyrinth structure.
NEEDLE = "needle.gif"
SYRINGE = "syringe.gif"
ETHER_BEAKER = "ether_beaker.gif"
MURDOCWIN = "murdocwin.gif"
MCGYVERWIN = "mcgyverwin.gif"
JSON_FILE = "mcgyvergame_structure.json"
# Font settings used in accessories counters, the size is in pixel.
FONT = ("helvetica", "-32", "bold")


class Filepath:
    def __init__(self, filename):
        self.filename = filename

    @property
    def filepath(self):
        for syspath in sys.path:
            for root, dirs, files in os.walk(os.path.dirname(syspath)):
                if self.filename in files:
                    return os.path.join(root, self.filename)


# Interface class generates and pack the canvas this is a parent class
# of Sprite class.
class Interface:
    # Canvas width and height constant
    CANVAS_WIDTH = 800
    CANVAS_HEIGHT = 600

    # Initialize the Interface class which generates a canvas inside
    # the tkinter master 'window' sent by the Main class.
    # JSON file read.
    def __init__(self, window):
        self.window = window
        self.canvas = tk.Canvas(window, width=self.CANVAS_WIDTH,
                                height=self.CANVAS_HEIGHT, bg="black")
        self.json_filepath = Filepath(JSON_FILE)
        self.json_file = json.load(open(self.json_filepath.filepath))
        self.canvas.pack()


# Image class opens images then using PhotoImage.
class Images:
    def __init__(self, filepath):
        self.filepath = filepath
        self.image_filepath = Filepath(self.filepath)
        self.image = Image.open(self.image_filepath.filepath)

    # Image property returns the image itself.
    @property
    def gif(self):
        self.photo_image = ImageTk.PhotoImage(self.image)
        return self.photo_image

    # Image property returns the image's height.
    @property
    def height(self):
        return self.gif.height()

    # Image property returns the image's width.
    @property
    def width(self):
        return self.gif.width()


# Sprite class used to draw text and image inside window using canvas.
# Call Accesories and McGyver class.
class Sprite(Interface):
    def __init__(self, window):
        super().__init__(window)
        self.picture_array = []
        self.labyrinth()
        self.accessories = Accessories(self.canvas)
        self.mcgyver = McGyver(self.canvas, self.window)

    # Labyrinth function using JSON file to get coordinates attributes and
    # picture filepath.
    def labyrinth(self):
        for values in self.json_file:
            # Tag and filepath stored, using .pop method.
            self.tag = values.pop("name")
            self.filepath = values.pop("filepath")
            self.image = Images(self.filepath)
            self.picture = self.image.gif
            # the picture itself is stored insid an array to avoid a loose of
            # their pointer.
            self.picture_array.append(self.picture)
            for coordinates in values.items():
                self.y = int(coordinates[0]) * self.image.height
                for x in coordinates[1]:
                    self.x = x * self.image.width
                    self.draw_sprite(self.canvas, self.x, self.y, self.picture,
                                     self.tag)
                    if "HUD" in self.tag:
                        self.item_counter(self.x+self.image.width, self.y,
                                          FONT, self.tag+"_COUNTER")

    # Item_counter function used to draw accessories counter.
    def item_counter(self, x, y, font, tag):
        self.canvas.create_text(x, y, anchor=tk.NW, fill="white",
                                font=font, text="0", tags=tag)

    # Classmethod draw_sprite function used to draw sprites(walls, accesories,
    # characters). That classmethod is called by the Accessories class too.
    @classmethod
    def draw_sprite(cls, canvas, x, y, image, tag):
        canvas.create_image(x, y, anchor=tk.NW, image=image, tags=tag)


# Accessories class called in the Sprite class. It in charge of compute random
# coordinates used in the 3 accessories (needle, syringe, ether beaker).
# These accessories are place randomly place in the labyrinth and must not
# overlap a wall or a character.
class Accessories:
    def __init__(self, canvas):
        self.canvas = canvas
        # Images stored in local variables.
        self.needle = Images(NEEDLE)
        self.syringe = Images(SYRINGE)
        self.ether_beaker = Images(ETHER_BEAKER)
        self.needle_sprite = self.needle.gif
        self.syringe_sprite = self.syringe.gif
        self.ether_beaker_sprite = self.ether_beaker.gif
        # Accessories arrays initialized, these arrays are filled after
        # their draw with a canvas method find_withtag.
        self.needle_id = []
        self.syringe_id = []
        self.ether_beaker_id = []
        self.wall_id = self.canvas.find_withtag("WALL")
        self.mcgyver_id = self.canvas.find_withtag("MCGYVER")
        self.murdoc_id = self.canvas.find_withtag("MURDOC")
        # Inner function called.
        self.labyrinth_needle()
        self.labyrinth_syringe()
        self.labyrinth_ether_beaker()

    # Property used to generate random number for accessories ordinates and
    # abscissa.
    @property
    def random_coordinates(self):
        self.random_numbers = []
        self.coordinates = []
        for i in range(0, 2):
            self.random_numbers.append(
                    random.randint(1, BLOCK_NUMBER) * PICTURE_SIZE)
            self.coordinates.append(self.random_numbers[i])
        self.random_numbers.append(self.random_numbers[0] + PICTURE_SIZE)
        self.random_numbers.append(self.random_numbers[1] + PICTURE_SIZE)
        return self.random_numbers

    # Property used to test if there are overlapped objects.
    @property
    def collision_test(self):
        self.collision = []
        self.overlapping = self.canvas.find_overlapping(
                *self.random_coordinates)
        for collisions in self.overlapping:
            # collision array stores boolean values. If the coordinates sent
            # to that property are overlapping a wall, a character or an other
            # accessory the array will store a True value, else, a False value.
            self.collision.append(self.wall_id.__contains__(collisions))
            self.collision.append(self.mcgyver_id.__contains__(collisions))
            self.collision.append(self.murdoc_id.__contains__(collisions))
            self.collision.append(self.syringe_id.__contains__(collisions))
            self.collision.append(self.needle_id.__contains__(collisions))
            self.collision.append(
                    self.ether_beaker_id.__contains__(collisions))
        # Then the property returns a boolean value: if collision array
        # contains a True value, it will return True, else it will returns
        # False.
        return self.collision.__contains__(True)

    # These 3 following function are testing with a while loop the boolean
    # value sent back by the property collision_test.
    # If the value is True, that means there is an overlapping, so this
    # function call back the property until it has a False value.
    def labyrinth_needle(self):
        self.needle_test = self.collision_test
        while self.needle_test:
            self.needle_test = self.collision_test
        else:
            Sprite.draw_sprite(self.canvas, *self.coordinates,
                               self.needle_sprite, "NEEDLE")
            self.needle_id = self.canvas.find_withtag("NEEDLE")

    def labyrinth_syringe(self):
        self.syringe_test = self.collision_test
        while self.syringe_test:
            self.syringe_test = self.collision_test
        else:
            Sprite.draw_sprite(self.canvas, *self.coordinates,
                               self.syringe_sprite, "SYRINGE")
            self.syringe_id = self.canvas.find_withtag("SYRINGE")

    def labyrinth_ether_beaker(self):
        self.ether_beaker_test = self.collision_test
        while self.ether_beaker_test:
            self.ether_beaker_test = self.collision_test
        else:
            Sprite.draw_sprite(self.canvas, *self.coordinates,
                               self.ether_beaker_sprite, "ETHER_BEAKER")
            self.ether_beaker_id = self.canvas.find_withtag("ETHER_BEAKER")


# McGyver class
class McGyver:
    def __init__(self, canvas, window):
        self.window = window
        self.canvas = canvas
        self.x_coordinates, self.y_coordinates = self.canvas.coords("MCGYVER")
        self.coords = [self.x_coordinates, self.y_coordinates]
        self.wall = self.canvas.find_withtag("WALL")
        self.needle = self.canvas.find_withtag("NEEDLE")
        self.syringe = self.canvas.find_withtag("SYRINGE")
        self.ether_beaker = self.canvas.find_withtag("ETHER_BEAKER")
        self.murdoc = self.canvas.find_withtag("MURDOC")
        self.mcgyver_item = []
        self.canvas.focus_set()
        self.canvas.bind("<Key>", self.keyboard)

    def keyboard(self, event):
        self.key = event.keysym
        self.previous_coordinates = self.coords
        if self.key == "Up":
            self.coords = [self.coords[0], self.coords[1] - PICTURE_SIZE]
        elif self.key == "Down":
            self.coords = [self.coords[0], self.coords[1] + PICTURE_SIZE]
        elif self.key == "Right":
            self.coords = [self.coords[0] + PICTURE_SIZE, self.coords[1]]
        elif self.key == "Left":
            self.coords = [self.coords[0] - PICTURE_SIZE, self.coords[1]]
        self.overlapping = self.canvas.find_overlapping(
                self.coords[0], self.coords[1], self.coords[0] + PICTURE_SIZE,
                self.coords[1] + PICTURE_SIZE)
        self.collision_test(self.overlapping, self.coords[0], self.coords[1])
        self.item(self.overlapping)

    def collision_test(self, overlapping, x_coords, y_coords):
        self.collision = []
        for wall_collision in overlapping:
            self.collision.append(self.wall.__contains__(wall_collision))
        if not self.collision.__contains__(True):
            self.canvas.coords("MCGYVER", x_coords, y_coords)
        else:
            self.coords = self.previous_coordinates

    def item(self, overlapping):
        if overlapping.__contains__(*self.needle):
            self.mcgyver_item.append("NEEDLE")
            self.canvas.delete("NEEDLE")
            self.canvas.itemconfig("NEEDLE_HUD_COUNTER", text="1")
        elif overlapping.__contains__(*self.syringe):
            self.mcgyver_item.append("SYRINGE")
            self.canvas.delete("SYRINGE")
            self.canvas.itemconfig("SYRINGE_HUD_COUNTER", text="1")
        elif overlapping.__contains__(*self.ether_beaker):
            self.mcgyver_item.append("ETHER_BEAKER")
            self.canvas.delete("ETHER_BEAKER")
            self.canvas.itemconfig("ETHER_BEAKER_HUD_COUNTER", text="1")
        elif overlapping.__contains__(*self.murdoc):
            if len(self.mcgyver_item) == 3:
                self.canvas.delete("MURDOC")
                End(self.window, False)
            else:
                self.canvas.delete("MCGYVER")
                End(self.window, True)


class End:

    def __init__(self, lastwindow, end):
        self.lastwindow = lastwindow
        self.lastwindow.destroy()
        self.window = tk.Tk()
        if end is True:
            self.loose()
        else:
            self.win()
        self.window.mainloop()

    def loose(self):
        self.window.title("You Lost !!")
        self.murdoc = Images(MURDOCWIN)
        self.label = tk.Label(self.window, image=self.murdoc.gif)
        self.label.grid(row=0, column=0)
        self.game_over()

    def win(self):
        self.window.title("You Won !!")
        self.mcgyver = Images(MCGYVERWIN)
        self.label = tk.Label(self.window, image=self.mcgyver.gif)
        self.label.grid(row=0, column=0)
        self.game_over()

    def game_over(self):
        self.retry_button = tk.Button(self.window, text="Yes",
                                      command=self.retry, bg="black")
        self.end_button = tk.Button(self.window, text="No", command=self.end)
        self.retry_button.place(x=200, y=275)
        self.end_button.place(x=250, y=275)

    def retry(self):
        self.window.destroy()
        mgm.Main()

    def end(self):
        self.window.destroy()
