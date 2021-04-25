import pygame as pg

width = 200


class Board:
    def __init__(self):
        self.board = [
            ["", "", ""],
            ["", "", ""],
            ["", "", ""]
        ]
        self.selected = None
        self.who = 0

    def select(self, position):
        if not self.board[position[1]//width][position[0]//width]:
            self.selected = (position[1]//width, position[0]//width)

    def play(self):
        if self.selected:
            self.board[self.selected[0]][self.selected[1]
                                         ] = "O" if not abs(self.who) else "X"
            self.who = ~self.who

    def draw(self, win):
        win.fill((255, 255, 255))
        won = list(self.check_won())
        if won:
            won[0] = (won[0][0]+width/2, won[0][1]+width/2)
            won[1] = (won[1][0]+width/2, won[1][1]+width/2)
            won = tuple(won)
            pg.draw.line(win, (0, 0, 0), ())
