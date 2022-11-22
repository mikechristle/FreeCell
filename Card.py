# ---------------------------------------------------------------------------
# FreCell, Card
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

class Card:
    _suits = ('H', 'D', 'C', 'S')

    # -----------------------------------------------------------------------
    def __init__(self, suit, rank, img):
        self.suit = suit
        self.rank = rank
        self.img = img
        self.child = None
        self.parent = None

    # -----------------------------------------------------------------------
    def clear(self):
        self.child = None
        self.parent = None

    # -----------------------------------------------------------------------
    def text(self):
        s = self.__repr__()
        if self.child is not None:
            s += '  child = ' + self.child
        if self.parent is not None:
            s += '  parent = ' + self.parent
        return s + '\n\n'

    # -----------------------------------------------------------------------
    def __repr__(self):
        return f'{self.rank + 1} of {Card._suits[self.suit]}'
