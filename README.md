# poem_buttem
> A program that gives you some famous poems each time you click. (The two files in the folder are integrated.)

## Table of Contents
* [General Info](#general-information)
* [Technologies Used](#technologies-used)
* [Features](#features)
* [Screenshots](#screenshots)
* [Setup](#setup)
* [Usage](#usage)
* [Project Status](#project-status)
* [Room for Improvement](#room-for-improvement)
* [Acknowledgements](#acknowledgements)
* [Contact](#contact)

## General Information
- My project is a poetic button completed using the python module of the processing software.
- There are moments when I wish to express some lines of poetry or verses, like Aristotle.   You can receive some ideas by clicking on the poem button whenever this happens.
- 
## Technologies Used
- Tech 1 - Button editing - Hover, press and release.
  In Processing, buttons are not built-in functions - you need to manually draw the button rect() and detect the mouse position by yourself.
To prevent each button (such as "Show", "Again", "Save", etc.) from repeating the same logic, you need to define a class to encapsulate the data and behavior of the buttons

   class Button(object):
    def __init__(self, label, x, y, w, h, primary=False):
        self.label = label
        self.x, self.y, self.w, self.h = x, y, w, h
        self.primary = primary
        self.hover = False
        self.down = False
        self.enabled = True
- Tech 2 -Immediately follow the lyrics - avoid repeating a line of poetry.
  The same poem may recur because random selection has no memorability.
  
  def show_new_poem():
    global current_index, used_indices, anim_alpha, anim_y, anim_active
    n = len(poems)
    if n == 0:
        toast("No poems available")
        return
    available = [i for i in range(n) if i not in used_indices]
    if not available:
        used_indices = []
        available = list(range(n))
    idx = random.choice(available)
    used_indices.append(idx)
    current_index = idx
    anim_alpha = 0
    anim_y = 10
    anim_active = True
- Tech 3 - Simple and clear layout - pure English interface, relatively clear hierarchical structure.

  buttons["show"]  = Button("Show a Poem", BTN_X, BTN_Y, BTN_W, BTN_H, primary=True)
buttons["again"] = Button("Again", BTN_AGAIN_X, BTN_AGAIN_Y, BTN_AGAIN_W, BTN_H)
buttons["fav"]   = Button("Favourite", FAV_LEFT_X, FAV_LEFT_Y, FAV_LEFT_W, FAV_LEFT_H)
buttons["save"]  = Button("Save Favourites (TXT)", SAVE_X, SAVE_Y, SAVE_W, SAVE_H)


## Features
List the ready features here:
- Awesome feature 1


