For all things Game of Life, check out the website:
    https://conwaylife.com/wiki/Main_Page

    You can find info about the game of life, as well as 
    interesting starting states to try!


File Organization:
   main.py is the main program, and the other files are
   imported into it, so they need to be somewhere visible
   to main.py, for instance in the same folder.


How to get full enjoyment out of this code:

1) Run the main.py file as is and see what happens.

2) Edit line 130 of main.py to create your own starting state
   (the parse_rfe function will generate states given either
   a file path, or an rfe string. Look online to find some, or
   use some of the predifined ones in fun_start_states.py.

3) Check out the custom_rules.py file, and edit line 143 of 
   main.py to try a few other rules out. You can also create
   your own rule funcion, and put a call to that in at line 
   143 of main.py!


GUI tips:
   There are a lot of controls for the GUI. Try pressing the
   "Help" button to see a list.


Operating System:
   This code runs on Linux. I am not sure if it runs on Windows, 
   but if it throws errors, check the tkinter library importation.
   I believe Windows wants the line:

    from Tkinter import *
         ^
    instead of 

    from tkinter import *
         ^
