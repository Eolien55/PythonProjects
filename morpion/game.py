import pygame as pg

total = 500
width = total // 3


class Board:
    def __init__(self):
        self.board = [["", "", ""], ["", "", ""], ["", "", ""]]
        self.selected = None
        self.who = 0
        self.finished = False

    def select(self, position):
        if self.finished:
            return
        if not self.board[position[0] // width][position[1] // width]:
            self.selected = (position[0] // width, position[1] // width)

    def play(self):
        if self.finished:
            return
        if self.selected:
            self.board[self.selected[0]][self.selected[1]] = (
                "O" if not abs(self.who) else "X"
            )
            self.who = ~self.who
            self.selected = None

    def check_won(self):
        won = []
        for row in range(3):
            if len(set(self.board[row])) == 1 and self.board[row][0] in ["O", "X"]:
                won.append([[row * width, 0], [row * width, 2 * width]])
        cols = [[self.board[j][i] for j in range(3)] for i in range(3)]
        for col in range(3):
            if len(set(cols[col])) == 1 and cols[col][0] in ["O", "X"]:
                won.append([[0, col * width], [2 * width, col * width]])
        diags = [
            [self.board[i][i] for i in range(3)],
            [self.board[i][-i - 1] for i in range(3)],
        ]
        for diag in range(2):
            if len(set(diags[diag])) == 1 and diags[diag][0] in ["O", "X"]:
                won.append([[0, diag * 2 * width], [2 * width, (2 - diag * 2) * width]])
        self.finished = bool(won)
        return won

    def draw(self, win):
        fnt = pg.font.SysFont("arial", 100)
        win.fill((255, 255, 255))
        won = list(self.check_won())
        for i in range(1, 3):
            pg.draw.line(win, (0, 0, 0), (i * width, 0), (i * width, width * 3), 2)
            pg.draw.line(win, (0, 0, 0), (0, i * width), (width * 3, i * width), 2)
        if self.selected:
            pg.draw.rect(
                win,
                (0, 0, 255),
                (self.selected[0] * width, self.selected[1] * width, width, width),
                5,
            )
        for i in range(3):
            for j in range(3):
                text = fnt.render(self.board[i][j], 1, (0, 0, 0))
                win.blit(
                    text,
                    (
                        i * width + (width / 2 - text.get_width() / 2),
                        j * width + (width / 2 - text.get_height() / 2),
                    ),
                )
        if won:
            for pos in won:
                pos[0] = (pos[0][0] + width / 2, pos[0][1] + width / 2)
                pos[1] = (pos[1][0] + width / 2, pos[1][1] + width / 2)
                pos = tuple(pos)
                pg.draw.line(
                    win,
                    (255, 0, 64),
                    (pos[0][0], pos[0][1]),
                    (pos[1][0], pos[1][1]),
                    10,
                )
        pg.display.update()


def main():
    pg.font.init()
    win = pg.display.set_mode((total, total))
    board = Board()
    pg.display.set_caption("Morpion")
    finished = False
    while not finished:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                finished = True
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_RETURN:
                    if board.selected:
                        board.play()
                if event.key == pg.K_r:
                    board.__init__()
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                board.select(pos)
        board.draw(win)
    pg.quit()


if __name__ == "__main__":
    main()
