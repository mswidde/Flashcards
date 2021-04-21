#
#   Entry point for flashcards program
#   just does some initialization and then hands over the control to the gui
#

import tkinter as tk
import common
import data
import gui


def main():

    # pick up ini file
    common.load_ini()

    # create instance for flashcards object
    # also tries to load the cards - first from cache, and if that fails from the file
    # if both fail we just have zero flashcards and the user should load a proper md file
    common.myFlashcards = data.flashcards()
    common.myFlashcards.loadCards()

    # Initiate GUI window
    root = tk.Tk()
    gui.TkinterGui(root)

    # start GUI
    root.mainloop()


main()
