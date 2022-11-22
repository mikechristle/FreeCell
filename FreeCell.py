# ---------------------------------------------------------------------------
# FreeCell
#
# History
# 21 Nov 2022 Mike Christle     Created
# ---------------------------------------------------------------------------
# MIT Licence
# Copyright 2022 Mike Christle
#
# Permission is hereby granted, free of charge, to any person obtaining a
# copy of this software and associated documentation files (the "Software"),
# to deal in the Software without restriction, including without limitation
# the rights to use, copy, modify, merge, publish, distribute, sublicense,
# and/or sell copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included
# in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE
# USE OR OTHER DEALINGS IN THE SOFTWARE.
# ---------------------------------------------------------------------------

import random

from tkinter import *
from PIL import Image, ImageTk
from Card import Card
from HoldBox import HoldBox
from StackBox import StackBox
from PlayBox import PlayBox

CANVAS_WIDTH = 1400
CANVAS_HEIGHT = 1000

DECK_IMAGE = 'DeckImage.png'
IMG_WIDTH = 144
IMG_HEIGHT = 200
DIVIDER = IMG_HEIGHT + 10
EMPTY_BOX_X = 2 * IMG_WIDTH
EMPTY_BOX_Y = 4 * IMG_HEIGHT

# Init Boxes
holds = (HoldBox(IMG_WIDTH, IMG_HEIGHT), HoldBox(IMG_WIDTH, IMG_HEIGHT),
         HoldBox(IMG_WIDTH, IMG_HEIGHT), HoldBox(IMG_WIDTH, IMG_HEIGHT))
stacks = (StackBox(IMG_WIDTH, IMG_HEIGHT), StackBox(IMG_WIDTH, IMG_HEIGHT),
          StackBox(IMG_WIDTH, IMG_HEIGHT), StackBox(IMG_WIDTH, IMG_HEIGHT))
plays = (PlayBox(IMG_WIDTH, IMG_HEIGHT), PlayBox(IMG_WIDTH, IMG_HEIGHT),
         PlayBox(IMG_WIDTH, IMG_HEIGHT), PlayBox(IMG_WIDTH, IMG_HEIGHT),
         PlayBox(IMG_WIDTH, IMG_HEIGHT), PlayBox(IMG_WIDTH, IMG_HEIGHT),
         PlayBox(IMG_WIDTH, IMG_HEIGHT), PlayBox(IMG_WIDTH, IMG_HEIGHT))

dnd_flag = False    # Drag and Drop flag
dnd_card = None     # Drag and Drop card stack
dnd_parent = None   # Drag and Drop stacks previous parent
dnd_x = 0           # Drag and Drop stacks X coordinate
dnd_y = 0           # Drag and Drop stacks Y coordinate
dnd_offset_x = 0    # Offset from click to corner of card
dnd_offset_y = 0    # Offset from click to corner of card
dnd_cursor = None   # Coordinates of cursor during move

undo_queue = []


# ---------------------------------------------------------------------------
def count_empty_boxes():
    boxes = 0

    for box in holds:
        if box.child is None:
            boxes += 1

    for box in plays:
        if box.child is None:
            boxes += 1

    PlayBox.empty_boxes = boxes


# ---------------------------------------------------------------------------
def click(x, y):

    card = box = None

    # Is this click on a play box
    if y > DIVIDER:
        for box in plays:
            card, box = box.click(x, y)
            if box is not None:
                break

    # Is this click on a hole box
    elif x < stacks[3].x:
        for box in holds:
            card, box = box.click(x, y)
            if box is not None:
                break

    # Then it must be a stack box
    else:
        for box in stacks:
            card, box = box.click(x, y)
            if box is not None:
                break

    return card, box


# ---------------------------------------------------------------------------
def mouse_down(e):
    global dnd_flag, dnd_parent, dnd_card
    global dnd_offset_x, dnd_offset_y

    if not dnd_flag:
        card, box = click(e.x, e.y)

        if card is not None:
            dnd_flag = True
            dnd_parent = card.parent
            dnd_card = card
            dnd_parent.child = None
            dnd_offset_x = e.x - box.x
            dnd_offset_y = e.y - box.card_top


# ---------------------------------------------------------------------------
def mouse_up(e):
    global dnd_flag

    if dnd_flag:
        dnd_flag = False

        # Find box under cursor
        card, box = click(e.x, e.y)

        # If a box is not found, try referencing the center of the card
        if box is None:
            x = e.x - dnd_offset_x + (IMG_WIDTH / 2)
            y = e.y - dnd_offset_y + (IMG_HEIGHT / 8)
            card, box = click(x, y)

        # If a box was clicked on, and the box accepts the card
        move = (dnd_card, dnd_card.parent)
        if box is not None and box.add(dnd_card):
            undo_queue.append(move)
            count_empty_boxes()

        # Else return cards to original location
        else:
            dnd_card.parent = dnd_parent
            dnd_parent.child = dnd_card

        paint()


# ---------------------------------------------------------------------------
def mouse_move(e):
    global dnd_cursor

    if dnd_flag:
        dnd_cursor = e
        paint()


# ---------------------------------------------------------------------------
def position_boxes():

    # Position Hold boxes
    x = 10
    for box in holds:
        box.x = x
        box.y = 10
        box.card_top = 10
        x += IMG_WIDTH + 10

    # Position Stack boxes
    canvas_width = canvas.winfo_width()
    x = canvas_width - 10 - IMG_WIDTH
    for box in stacks:
        box.x = x
        box.y = 10
        box.card_top = 10
        x -= IMG_WIDTH + 10

    # Position Play boxes
    dx = (canvas_width - (8 * IMG_WIDTH)) / 9
    x = dx
    dx += IMG_WIDTH
    y = IMG_HEIGHT + 20
    for box in plays:
        box.x = x
        box.y = y
        box.card_top = y
        x += dx


# ---------------------------------------------------------------------------
def paint():
    canvas.delete('all')

    # Paint Hold Boxes
    for box in holds:
        x = box.x
        y = box.y
        if box.child == None:
            canvas.create_image(x, y, anchor = NW, image = empty_box)
        else:
            canvas.create_image(x, y, anchor = NW, image = box.child.img)

    # Paint Stack Boxes
    for box in stacks:
        x = box.x
        y = box.y
        if box.child == None:
            canvas.create_image(x, y, anchor = NW, image = empty_box)
        else:
            child = box
            while child.child != None:
                child = child.child
            canvas.create_image(x, y, anchor = NW, image = child.img)

    # Paint Play Boxes
    for box in plays:
        x = box.x
        y = box.y
        if box.child == None:
            canvas.create_image(x, y, anchor = NW, image = empty_box)
        else:
            child = box.child
            while child != None:
                canvas.create_image(x, y, anchor = NW, image = child.img)
                child = child.child
                y += 40

    # Paint Drag and Drop cards
    if dnd_flag:
        x = dnd_cursor.x - dnd_offset_x
        y = dnd_cursor.y - dnd_offset_y
        card = dnd_card
        while card != None:
            canvas.create_image(x, y, anchor = NW, image = card.img)
            card = card.child
            y += 40


# ---------------------------------------------------------------------------
def menu_popup(event):
    try:
        popup.tk_popup(event.x_root, event.y_root, 0)
    finally:
        popup.grab_release()


# ---------------------------------------------------------------------------
def undo_move(_):
    if len(undo_queue) > 0:
        card, parent = undo_queue.pop()
        card.parent.child = None
        card.parent = parent
        parent.child = card
        paint()


# ---------------------------------------------------------------------------
def new_game():
    random.shuffle(deck)
    deal_cards()


# ---------------------------------------------------------------------------
def deal_cards():

    PlayBox.empty_boxes = 4
    position_boxes()
    undo_queue.clear()
    for card in deck:
        card.clear()

    for box in holds:
        box.child = None
    for box in plays:
        box.child = None
    for box in stacks:
        box.child = None

    idx = 0
    while idx < 52:
        for box in plays:
            card = deck[idx]
            card.child = None
            card.parent = None
            box.init(card)
            idx += 1
            if idx >= 52: break

    paint()


# ---------------------------------------------------------------------------
# Setup the window
# ---------------------------------------------------------------------------
top = Tk()
top.title('FreeCell')

popup = Menu(top, tearoff=0)
popup.add_command(label = "Start New Game", command = new_game)
popup.add_command(label = "Restart This Game", command = deal_cards)

top.attributes('-toolwindow', True)
top.bind("<Button-3>", menu_popup)
top.bind('<Control-z>', undo_move)

canvas = Canvas(
    top,
    width = CANVAS_WIDTH,
    height = CANVAS_HEIGHT,
    bg = '#007000'  #'dark green'
)
canvas.pack(side = RIGHT, fill = BOTH, expand = True)

# Build deck of cards
deck_img = Image.open(DECK_IMAGE)
deck = []
for suit in range(4):
    for rank in range(13):
        x = rank * IMG_WIDTH
        y = suit * IMG_HEIGHT
        img = deck_img.crop((x, y, x + IMG_WIDTH - 1, y + IMG_HEIGHT - 1))
        img = ImageTk.PhotoImage(img)
        deck.append(Card(suit, rank, img))

img = deck_img.crop((EMPTY_BOX_X, EMPTY_BOX_Y, EMPTY_BOX_X + IMG_WIDTH, EMPTY_BOX_Y + IMG_HEIGHT))
empty_box = ImageTk.PhotoImage(img)

canvas.bind('<Motion>', mouse_move)
canvas.bind( "<Button-1>", mouse_down)
canvas.bind( "<ButtonRelease-1>", mouse_up)

top.mainloop()
