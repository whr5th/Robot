import curses, time
from gopigo import *

#--------------------------------------
def input_char(message):
    try:
        win = curses.initscr()
        win.addstr(0, 0, message)
        while True: 
            ch = win.getch()
            if ch in range(32, 127): break
            time.sleep(0.05)
    except: raise
    return chr(ch)
#--------------------------------------
c = input_char('Press w to move forward:')

if c.upper() == 'W':
	fwd()
if c.upper() == 'X':
        curses.endwin()

#	inp = input()
#	if inp=='w':
#		fwd()
#	elif inp=='x':
#		stop()
