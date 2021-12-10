from typing import Union, List, Optional

from src.common import get_input

BRACKETS = {
    ')': '(',
    ']': '[',
    '}': '{',
    '>': '<'
}
AUTOCOMPLETE_BRACKETS = {v: k for k, v in BRACKETS.items()}


def day_10():
    # Part 1: Do a stack, pop each pair, the first illegal character is added to a score.
    # Part 2: Do a stack, complete the end of the line. The autocomplete is scored.
    input_lines = get_input(day=10)
    illegal_chars = []
    autocomplete_lists: List[List[str]] = []
    for line in input_lines:
        output = process_line(line)
        if isinstance(output, str):
            illegal_chars.append(output)
        elif isinstance(output, list):
            autocomplete_lists.append(output)
        else:
            assert "Unknown return from process_line"
    print(f"Illegal Score (Part 1): {get_illegal_score(illegal_chars)}")
    print(f"Autocomplete Score (Part 2): {get_autocomplete_score(autocomplete_lists)}")


def process_line(line) -> Union[str, List[str]]:
    """Returns single char if illegal, or a list if completing. [] for a valid line."""
    stack = []
    for char in line:
        # If open bracket
        if char in BRACKETS.values():
            stack.append(char)
        else:
            # Get the open bracket for this close
            last = stack.pop()
            if last == BRACKETS[char]:
                pass  # Set matched
            else:
                return char

    # We're done, complete the stack (if there's nothing in the stack, [] is returned).
    autocomplete = []
    while len(stack):
        autocomplete.append(AUTOCOMPLETE_BRACKETS[stack.pop()])
    return autocomplete


def get_illegal_score(illegal_chars: Union[List[str], str]) -> int:
    if isinstance(illegal_chars, str):
        illegal_chars = [illegal_chars]

    score_lookup = {
        ')': 3,
        ']': 57,
        '}': 1197,
        '>': 25137
    }

    return sum((score_lookup[char] for char in illegal_chars))


def get_autocomplete_score(autocomplete_lists: List[List[str]]) -> int:
    # Start with a total score of 0.
    # Then, for each character, multiply the total score by 5 and then increase the total score by
    # the point value given for the character in the following table [...]
    # The winner is found by sorting all of the scores and then taking the middle score.
    score_lookup = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4
    }

    scores = []
    for line in autocomplete_lists:
        score = 0
        for char in line:
            score *= 5
            score += score_lookup[char]
        scores.append(score)

    scores.sort()
    middle_index = len(scores) // 2
    return scores[middle_index]


if __name__ == '__main__':
    day_10()
