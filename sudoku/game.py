import pygame as pg
import requests as req
import json
import random
import time
import os

or_board = None


class Board:
    def __init__(self, THATSAboard):
        global or_board
        self.isblank = False
        self.gap = 75
        self.length, self.board = self.model(THATSAboard)
        empty, self.or_board = self.model(THATSAboard)
        open("or_board", "w").write(str(self.or_board))
        del empty
        self.points = [
            [i % (self.length ** 2), i // (self.length ** 2)]
            for i in range(self.length ** 4)
        ]
        self.squares = [
            [Square(self.board[j][i], (j, i)) for i in range(self.length ** 2)]
            for j in range(self.length ** 2)
        ]
        self.selected = self.squares[0][0]

    def blank(self):
        self.isblank = True
        self.board = [
            [0 for i in range(self.length ** 2)] for j in range(self.length ** 2)
        ]
        self.squares = [
            [Square(self.board[j][i], (j, i)) for i in range(self.length ** 2)]
            for j in range(self.length ** 2)
        ]
        open("or_board", "w").write(str(self.board))

    def change(self):
        for i in self.points:
            if self.squares[i[1]][i[0]].value != 0:
                if is_valid(
                    self.board,
                    self.squares[i[1]][i[0]].value,
                    (i[1], i[0]),
                    self.points,
                    self.length,
                ):
                    self.board[i[1]][i[0]] = self.squares[i[1]][i[0]].value
                    self.squares[i[1]][i[0]].value = self.board[i[1]][i[0]]
                else:
                    self.squares[i[1]][i[0]].value = 0

    def model(self, board):
        length = int(len(board) ** 0.25)
        board = [
            board[i * length ** 2 : (i + 1) * length ** 2] for i in range(length ** 2)
        ]
        return length, board

    def select(self, pos):
        pos = self.click(pos)
        self.selected.selected = False
        self.selected = self.squares[pos[1]][pos[0]]
        self.selected.selected = True

    def update_value(self, value):
        if self.board[self.selected.pos[0]][self.selected.pos[1]] != 0:
            return
        self.selected.value = value

    def draw(self, win):
        fnt = pg.font.SysFont("comicsans", 40)
        non_norm_vals = [
            [
                (self.squares[j][i].value, (j, i))
                for i in range(self.length ** 2)
                if self.squares[j][i].value != self.board[j][i]
                and self.squares[j][i].value != 0
            ]
            for j in range(self.length ** 2)
        ]
        empty = []
        for l in non_norm_vals:
            empty += l
        non_norm_vals = empty
        norm_vals = [
            [
                (self.board[j][i], (j, i))
                for i in range(self.length ** 2)
                if self.board[j][i] != 0
            ]
            for j in range(self.length ** 2)
        ]
        empty = []
        for l in norm_vals:
            empty += l
        norm_vals = empty
        right = [
            [(j, i) for i in range(self.length ** 2) if self.squares[j][i].right]
            for j in range(self.length ** 2)
        ]
        empty = []
        for l in right:
            empty += l
        right = empty
        win.fill((255, 255, 255))
        for i in range(1, self.length ** 2):
            if i % self.length == 0:
                thick = 4
            else:
                thick = 1
            pg.draw.line(
                win,
                (0, 0, 0),
                (0, i * self.gap),
                (self.gap * (self.length ** 2), i * self.gap),
                thick,
            )
            pg.draw.line(
                win,
                (0, 0, 0),
                (i * self.gap, 0),
                (i * self.gap, self.gap * (self.length ** 2)),
                thick,
            )
        pg.draw.rect(
            win,
            (0, 0, 255),
            (
                self.selected.pos[1] * self.gap,
                self.selected.pos[0] * self.gap,
                self.gap,
                self.gap,
            ),
            4,
        )
        for i in norm_vals:
            text = fnt.render(str(i[0]), 1, (0, 0, 0))
            win.blit(
                text,
                (
                    i[1][1] * self.gap + (self.gap / 2 - text.get_width() / 2),
                    i[1][0] * self.gap + (self.gap / 2 - text.get_height() / 2),
                ),
            )
        for i in non_norm_vals:
            text = fnt.render(str(i[0]), 1, (128, 128, 128))
            win.blit(text, (i[1][1] * self.gap + 5, i[1][0] * self.gap + 5))
        for i in right:
            pg.draw.rect(
                win,
                (0, 255, 0),
                (
                    i[1] * self.gap,
                    i[0] * self.gap,
                    self.gap,
                    self.gap,
                ),
                4,
            )
        pg.display.update()

    def click(self, pos):
        return (pos[0] // self.gap, pos[1] // self.gap)

    def clear(self):
        self.or_board = eval(open("or_board", "r").read())
        self.board = self.or_board
        for j in range(self.length ** 2):
            for i in range(self.length ** 2):
                self.squares[j][i].value = self.board[j][i]

    def solve_gui(self, win):
        for event in pg.event.get():
            pass
        board = self.board
        find = find_empty(self.board, self.length)
        if not find:
            for i in self.squares:
                for j in i:
                    j.right = False
            return True
        col, row = find
        for i in range(1, self.length ** 2 + 1):
            if is_valid(board, i, (row, col), self.points, self.length):
                self.board[row][col] = i
                self.squares[row][col].right = True
                self.draw(win)
                # time.sleep(0.001)
                if self.solve_gui(win):
                    return True
                self.board[row][col] = 0
                self.squares[row][col].right = False
        return False


class Square:
    def __init__(self, value, pos):
        self.right = False
        self.pos = pos
        self.value = value
        self.selected = False


def find_empty(board, length):
    return (
        find[0]
        if (
            find := [
                (i % length ** 2, i // length ** 2)
                for i in range(length ** 4)
                if board[i // length ** 2][i % length ** 2] == 0
            ]
        )
        else []
    )


def is_valid(board, num, pos, points, length):
    squares = [
        board[i[0]][i[1]]
        for i in points
        if i[0] // length == pos[0] // length and i[1] // length == pos[1] // length
    ]
    row = [board[i[0]][i[1]] for i in points if i[0] == pos[0]]
    col = [board[i[0]][i[1]] for i in points if i[1] == pos[1]]
    if (num not in squares) and (num not in row) and (num not in col):
        return True
    else:
        return False


def main():
    rand = random.randint(0, 100)
    if rand < 15:
        url = "easy"
    elif rand < 50:
        url = "medium"
    elif rand < 85:
        url = "hard"
    else:
        url = "expert"
    res = req.get(f"https://sudoku.com/api/getLevel/{url}")
    res = json.loads(res.text)
    board = [int(i) for i in res["desc"][0]]
    board = Board(board)
    pg.font.init()
    win = pg.display.set_mode(
        (board.gap * board.length ** 2, board.gap * board.length ** 2)
    )
    finished = False
    pg.display.set_caption("Sudoku")
    # im = pg.image.load("C:\\Users\\Elie\\PythonProjects\\sudoku\\icon.png")
    # pg.display.set_icon(im)
    key = None
    while not finished:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_1:
                    key = 1
                if event.key == pg.K_2:
                    key = 2
                if event.key == pg.K_3:
                    key = 3
                if event.key == pg.K_4:
                    key = 4
                if event.key == pg.K_5:
                    key = 5
                if event.key == pg.K_6:
                    key = 6
                if event.key == pg.K_7:
                    key = 7
                if event.key == pg.K_8:
                    key = 8
                if event.key == pg.K_9:
                    key = 9
                if event.key == pg.K_KP1:
                    key = 1
                if event.key == pg.K_KP2:
                    key = 2
                if event.key == pg.K_KP3:
                    key = 3
                if event.key == pg.K_KP4:
                    key = 4
                if event.key == pg.K_KP5:
                    key = 5
                if event.key == pg.K_KP6:
                    key = 6
                if event.key == pg.K_KP7:
                    key = 7
                if event.key == pg.K_KP8:
                    key = 8
                if event.key == pg.K_KP9:
                    key = 9
                if event.key == pg.K_DELETE:
                    board.clear()
                    key = None
                if event.key == pg.K_SPACE:
                    if not board.isblank:
                        board.clear()
                    board.solve_gui(win)
                if event.key == pg.K_RETURN:
                    board.change()
                if event.key == pg.K_r:
                    rand = random.randint(0, 100)
                    if rand < 15:
                        url = "easy"
                    elif rand < 50:
                        url = "medium"
                    elif rand < 85:
                        url = "hard"
                    else:
                        url = "expert"
                    res = req.get(f"https://sudoku.com/api/getLevel/{url}")
                    res = json.loads(res.text)
                    board = [int(i) for i in res["desc"][0]]
                    board = Board(board)
                if event.key == pg.K_RIGHT:
                    key = None
                    board.selected = board.squares[board.selected.pos[0]][
                        abs((board.selected.pos[1] + 1) % (board.length ** 2))
                    ]
                if event.key == pg.K_LEFT:
                    key = None
                    board.selected = board.squares[board.selected.pos[0]][
                        abs((board.selected.pos[1] - 1) % (board.length ** 2))
                    ]
                if event.key == pg.K_UP:
                    key = None
                    board.selected = board.squares[
                        abs((board.selected.pos[0] - 1) % (board.length ** 2))
                    ][board.selected.pos[1]]
                if event.key == pg.K_DOWN:
                    key = None
                    board.selected = board.squares[
                        abs((board.selected.pos[0] + 1) % (board.length ** 2))
                    ][board.selected.pos[1]]
                if event.key == pg.K_b:
                    board.blank()
            if event.type == pg.MOUSEBUTTONDOWN:
                key = None
                pos = pg.mouse.get_pos()
                board.select(pos)
        if key:
            board.update_value(key)
        board.draw(win)
    pg.quit()


main()
