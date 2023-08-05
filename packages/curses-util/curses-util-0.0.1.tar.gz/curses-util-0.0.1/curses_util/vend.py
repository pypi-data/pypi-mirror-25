#!/usr/bin/env python

import curses
import signal
import sys

items = []
scr = None
marked = set()
sh = 0
sw = 0
sel = 0
first = 0

mark_color_fg = None
mark_color_bg = None
select_color_bg = None
select_color_fg = None

def cursesinit():
    global scr
    scr = curses.initscr()

    curses.start_color()
    curses.init_pair(1, 0, 0)
    curses.curs_set(0)

    curses.noecho()
    curses.cbreak()
    scr.keypad(True)
    scr.clear()
    scr.refresh()
    return scr

def cursesclean():
    curses.echo()
    curses.nocbreak()
    curses.endwin()

def sigint(*args):
    cursesclean()
    sys.exit(1)

def draw_items(display):
    global items
    scr.erase()
    height, width = scr.getmaxyx()
    curses.init_pair(1, select_color_fg, select_color_bg)
    curses.init_pair(2, mark_color_fg, mark_color_bg)
    curses.init_pair(3, mark_color_fg, select_color_bg)

    select_colors = curses.color_pair(1)
    mark_colors = curses.color_pair(2)
    highlight_and_select_colors = curses.color_pair(3)

    display_items = items[first:first + height]

    display_items = map(lambda x: display(x).replace('\t','    '), display_items)
    for i,item in enumerate(display_items):
        if i == sel:
            item += (width - len(item) - 1) * " "
            if i + first in marked:
                scr.addstr(item, highlight_and_select_colors)
            else:
                scr.addstr(item, select_colors)
        elif i + first in marked:
            scr.addstr(item, mark_colors)
        else:
            scr.addstr(item)


        if i < (height - 1):
            scr.addstr("\n")

    scr.move(sel, 0)
    scr.refresh()

def unmark_items(num):
    base = first + sel
    for i in range(num):
        marked.discard(base + i)
    move_down(num)

def mark_items(num):
    nitems = len(items)
    base = first + sel

    if base + num > nitems:
        num = nitems - base

    for i in range(num):
        marked.add(base + i)

    move_down(num)

def move_up(num):
    global sel, first

    sel -= num

    if sel < 0:
        first -= -1 * sel
        sel = 0

    if first < 0:
        first = 0
        sel = 0

def move_down(num):
    global sel, first

    nitems = len(items)
    max_sel = nitems - 1 if sh > nitems else sh - 1
    max_first = 0 if sh > nitems else nitems - sh

    sel += num

    if sel > max_sel:
        if sh < nitems:
            first += sel - sh + 1
        if first > max_first:
            first = max_first
        sel = max_sel

def onresize():
    scr.clear()
    draw_items(items, sel, first)

def vend(litems, display):
    global sh, sw, sel, first, scr, items
    for item in items:
        if "\n" in item:
            raise Exception("Newline not permitted in menu items")


    items = litems
    sh, sw = scr.getmaxyx()
    sel = 0
    first = 0
    marked.clear()
    opnum = 0

    draw_items(display)
    while True:
        c = scr.getch()
        if chr(c) == 'g' and last_char == 'g':
            sel = 0
            first = 0
        elif chr(c) == 'G':
            if len(items) < sh:
                first = 0
                sel = len(items) - 1
            else:
                first = len(items) - sh
                sel = sh - 1
        elif c == curses.KEY_DOWN or chr(c) == 'j': #Up
            opnum = opnum if opnum else 1
            move_down(opnum)
            opnum = 0
        elif c == curses.KEY_UP or chr(c) == 'k': #Down
            opnum = opnum if opnum else 1
            move_up(opnum)
            opnum = 0
        elif c == 5: #ctrl-e
            opnum = opnum if opnum else 1

            osel = sel
            sel = sh - 1
            move_down(opnum)
            sel = osel

            opnum = 0
        elif c == 25: #ctrl-y
            opnum = opnum if opnum else 1

            osel = sel
            sel = 0
            move_up(opnum)
            sel = osel

            opnum = 0
        elif c == 6: #ctrl-f
            sel = sh - 1
            move_down(sh)
        elif c == 2: #ctrl-b
            sel = 0
            move_up(sh)
        elif chr(c) == '\n':
            cursesclean()
            return [ items[i] for i in marked ] if marked else [ items[first + sel] ]
        elif chr(c) == 'u':
            opnum = opnum if opnum else 1
            unmark_items(opnum)
            opnum = 0
        elif chr(c) == 'm':
            opnum = opnum if opnum else 1
            mark_items(opnum)
            opnum = 0
        elif chr(c) == 'M':
            if sh > len(items):
                sel = int((len(items) - 1) / 2)
            else:
                sel = int((sh - 1)/2)
        elif chr(c) == 'L':
            opnum = opnum if opnum else 1
            if sh > len(items):
                sel = len(items) - 1
            else:
                sel = sh - 1

            sel -= opnum - 1
            opnum = 0
        elif chr(c) == 'H':
            opnum = opnum if opnum else 1
            sel = opnum - 1
            opnum = 0
        elif c >= ord('0') and c <= ord('9'):
            opnum *= 10
            opnum += int(chr(c))
            curses

        last_char = chr(c)
        draw_items(display)
        
signal.signal(signal.SIGINT, sigint)

#Public API

        

class Menu():
    def __init__(self, mark_color_fg=curses.COLOR_MAGENTA,
                mark_color_bg=curses.COLOR_BLACK,
                select_color_bg=curses.COLOR_CYAN,
                select_color_fg=curses.COLOR_BLACK):
        self.mark_color_fg = mark_color_fg
        self.mark_color_bg = mark_color_bg
        self.select_color_bg = select_color_bg
        self.select_color_fg = select_color_fg

    def vend(self, items, display=lambda x: x):
        global mark_color_fg, mark_color_bg, select_color_bg, select_color_fg
        try:
            cursesinit()
            mark_color_fg = self.mark_color_fg
            mark_color_bg = self.mark_color_bg
            select_color_bg = self.select_color_bg
            select_color_fg = self.select_color_fg
            return vend(items, display)
        finally:
            cursesclean()
