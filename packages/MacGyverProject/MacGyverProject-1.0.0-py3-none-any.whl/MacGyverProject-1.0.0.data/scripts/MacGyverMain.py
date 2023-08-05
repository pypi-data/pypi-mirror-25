#!python
# -*- coding: utf-8 -*-
"""
Created on Fri Sep  1 13:57:33 2017

The MacGyver Game, is a labyrinth where MacGyver needs to escape from
his best ennemie Murdoc. To escape, he will need to sleep Murdoc. To do that,
without all these three elements, if McGyver meets Murdoc, he will die.

This game is the part 3 of the Openclassrooms path. This path
give an Apps Developpers Python grad.

@author: fredericvidry
"""
# Importation of Mac Gyver Game module.
import MacGyverGame as mgg


# Class Main initialize the Game
class Main():
    def __init__(self):
        self.macgyvergame = mgg
        self.window = mgg.tk.Tk()
        self.window.title("McGyver Adventure")
        self.interface = mgg.Sprite(self.window)
        self.window.mainloop()

if __name__ == '__main__':
    Main()
