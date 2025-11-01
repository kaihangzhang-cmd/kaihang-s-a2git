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
feature 1-Random poetry selection without repetition
feature 2-Only an English user interface is provided, but the display of poetry supports bilingual (Chinese + English).
feature 3-Smooth fade-in/slide animation for the transition of verses
feature 4-Customize reusable button classes with hover/press feedback
feature 5-"Save" and "Save as TXT" functions
feature 6-An easily accessible top-down layout and a clear text hierarchy


## Screenshots
<img width="720" height="537" alt="屏幕截图 2025-11-01 120231" src="https://github.com/user-attachments/assets/a1f84b3f-76bb-495d-a69e-490918479196" />
Minimalist interface, displaying the "Show Poetry" button, prompt information and poetry display cards


## Setup
The running body requires the following code to be in the same folder as the body.
mode=Python
mode.id=jycessing.mode.PythonMode


## Usage
1. Click "Show a Poem" → A random Chinese poem and its translation will appear.
2. Press "Again" → the next non-repeated poem will be displayed.
3. Click "Collect" → Add the current poem to the saved list.
4. Press "Save Favorites (TXT)" → Export your list to a text file.


## Project Status
Completed
This project successfully demonstrated a smooth interaction design.
Future versions may incorporate features such as sound, keyboard control or adaptive typesetting.


## Room for Improvement
To-do List/Future Features
Allow users to import their own poetry files


## Acknowledgements
This project was inspired by:
The Scaling Everest interactive from The Washington Post (2016).
“Exploring Chinese Poetry using Adobe Spark Video” by Chung & Wang (2020).
Processing community tutorials on interactive art and generative design.
Special thanks to the UTS code class Thank you to the course and the teacher for inspiring the combination of code and art.


## Contact
Created by [Kaihang.Zhang@student.uts.edu.au) - feel free to contact me!
