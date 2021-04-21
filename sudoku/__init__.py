def solve(board):
    find = find_empty(board)
    if not find:
        return True
    col, row = find
    for i in range(1, length ** 2 + 1):
        if is_valid(board, i, (row, col)):
            board[row][col] = i
            if solve(board):
                return True
            board[row][col] = 0
    return False


def find_empty(board):
    return (
        find[0]
        if (
            find := [
                (i // length ** 2, i % length ** 2)
                for i in range(length ** 4)
                if board[i % length ** 2][i // length ** 2] == 0
            ]
        )
        else []
    )


def is_valid(board, num, pos):
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


def model(board):
    length = int(len(board) ** 0.25)
    board = [board[i * length ** 2 : (i + 1) * length ** 2] for i in range(length ** 2)]
    return length, board


board = [
    0,
    0,
    6,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    8,
    7,
    0,
    6,
    0,
    9,
    0,
    0,
    1,
    0,
    5,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    7,
    0,
    4,
    0,
    0,
    0,
    0,
    7,
    9,
    0,
    0,
    2,
    5,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    0,
    3,
    0,
    0,
    1,
    0,
    0,
    0,
    0,
    0,
    6,
    0,
    0,
    8,
    0,
    0,
    1,
    0,
    0,
    0,
    3,
    0,
    0,
    4,
    0,
    0,
    3,
    0,
    9,
    0,
]
length, board = model(board)
points = [[i % length ** 2, i // length ** 2] for i in range(length ** 4)]


def main():
    return solve(board)
