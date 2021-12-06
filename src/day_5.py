from typing import List

from src.common import get_input


def day_4():
    input_lines = get_input(day=4)

    # First line are the numbers drawn, and the following are the bingo boards
    numbers_to_call = [int(x) for x in input_lines[0].split(',')]
    input_lines = input_lines[1:]

    # Slate's note: Pandas is a good solution for this, but as it's an external dependency
    # (despite being very well-used and documented), I'll disregard it
    bingo_boards: List[List[int]] = []
    size_of_board = 5

    for i in range(0, len(input_lines)):
        # Join across the new lines
        bingo_board = ' '.join(input_lines[i * size_of_board:(i+1) * size_of_board])
        # Split by space to get the numbers (and remove whitespace)
        bingo_boards.append([int(x) for x in bingo_board.split(' ') if x])

    # Foreach number that's drawn, check the boards.
    # A winning board has at least one complete row or column of marked numbers.
    # The score can now be calculated. Sum of all **unmarked** numbers on that board, multiply that by the number that
    # was just called when the board won to get the final score.
    drawn_numbers = numbers_to_call[:size_of_board]  # Small optimisation, we cannot win until at least the row size has been called
    for drawn_number in numbers_to_call[size_of_board:]:
        drawn_numbers.append(drawn_number)

        for n, bingo_board in enumerate(bingo_boards):
            if is_winner(bingo_board, drawn_numbers):
                score = calculate_score(bingo_board, drawn_numbers, drawn_number)
                print(f"Removing board [{n}/{len(bingo_boards)}] with score {score}")
                bingo_boards.remove(bingo_board)

    print("All done!")


def is_winner(board: List[int], called_numbers: List[int]):
    row_size = int(len(board) ** 0.5)
    for i in range(0, row_size):
        row = row_ints(i, row_size, board)
        row_wins = all(num in called_numbers for num in row)
        column = list(column_ints(i, row_size, board))
        column_wins = all(num in called_numbers for num in column)
        if row_wins or column_wins:
            # print(f"Winner: {row_size=} {row=} {row_wins=} {column=} {column_wins=}")
            # print(f" Board: {board=}")
            return True
    return False


def row_ints(row_index: int, row_size: int, board: List[int]):
    return board[row_index * row_size: (row_index + 1) * row_size]


def column_ints(column_index: int, row_size: int, board: List[int]):
    for i in range(column_index, row_size**2, row_size):
        yield board[i]


def calculate_score(board: List[int], drawn_numbers: List[int], last_drawn_number: int):
    # Sum of all **unmarked** numbers on that board, multiply that by the number that
    # was just called when the board won to get the final score.
    result = sum([num for num in board if num not in drawn_numbers])
    # print(f"{result=} * {last_drawn_number} = {result*last_drawn_number}")
    return result * last_drawn_number


if __name__ == '__main__':
    day_4()
