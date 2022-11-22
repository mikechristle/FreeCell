# ---------------------------------------------------------------------------
# FreeCell, PlayBox
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

class PlayBox:
    empty_boxes = 0

    # -----------------------------------------------------------------------
    def __init__(self, ix, iy):
        self.child = None
        self.x = 0
        self.y = 0
        self.card_top = 0
        self.image_width = ix
        self.image_height = iy

    # -----------------------------------------------------------------------
    # Add a card to the stack without checks
    # Used for initial game setup
    # -----------------------------------------------------------------------
    def init(self, card):
        child = self
        while child.child != None:
            child = child.child

        child.child = card
        card.parent = child
        card.child = None

    # -----------------------------------------------------------------------
    # Can only add a card if the box is empty, or if the bottom card has
    # the opposite color and the rank is one greater
    # -----------------------------------------------------------------------
    def add(self, card):

        # If first card
        if self.child is None:
            if card.parent is not None:
                card.parent.child = None
            self.child = card
            card.parent = self
            return True

        # If not first card
        else:
            child = self.child
            while child.child != None:
                child = child.child

            x = (card.suit ^ child.suit) & 2
            if x == 2 and card.rank == (child.rank - 1):
                if card.parent is not None:
                    card.parent.child = None
                child.child = card
                card.parent = child
                return True
            else:
                return False

    # -----------------------------------------------------------------------
    # Does this box, or any of it's children, contain these coordinates
    # Returns (card, box) tuple
    # -----------------------------------------------------------------------
    def click(self, x, y):

        # Check X coordinate
        rx = self.x + self.image_width
        if x < self.x or x >= rx:
            return None, None

        # If no cards on box
        if self.child == None:
            ry = self.y + self.image_height
            if self.y <= y < ry:
                return None, self
            else:
                return None, None

        # If cards on box
        # Find bottom of stack
        ty = self.y
        card = self.child
        while card.child != None:
            card = card.child
            ty += 40

        # Check stack bounds
        ry = ty + self.image_height
        if y < self.y or y > ry:
            return None, None

        # Check each card from bottom to top
        count = 0
        while True:
            by = ty + self.image_height
            if ty <= y < by:
                self.card_top = ty
                return card, self

            # Advance to next card
            card = card.parent
            ty -= 40
            count += 1
            if card == self:
                return None, None

            # Limit size of stack to count of empty boxes
            if count > PlayBox.empty_boxes:
                return None, None

            # Check that stack toggles the suit
            x = (card.suit ^ card.child.suit) & 2
            if x != 2 or card.rank != (card.child.rank + 1):
                return None, None

    # -----------------------------------------------------------------------
    def __repr__(self):
        return 'Play Box'
