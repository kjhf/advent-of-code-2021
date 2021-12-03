import functools
from os import environ
from typing import List
import dotenv
import requests


dotenv.load_dotenv()
assert environ.get('SESSION_TOKEN'), "Please add SESSION_TOKEN to the env vars."


@functools.cache
def get_input(day: int, print_output: bool = False) -> List[str]:
    """Get the input for the day using the session token in the env vars."""
    url = f"https://adventofcode.com/2021/day/{day}/input"
    input_lines = requests.get(url, cookies={'session': environ["SESSION_TOKEN"]}).text.split('\n')
    input_lines = [line for line in input_lines if line]  # Filter out empty
    if print_output:
        print(input_lines)
    return input_lines
