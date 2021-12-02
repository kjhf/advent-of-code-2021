from os import environ
import dotenv
import requests


def day_1(session_token):
    # Get the input
    url = 'https://adventofcode.com/2021/day/1/input'
    input_lines = requests.get(url, cookies={'session': session_token}).text.split('\n')
    print(input_lines)

    # Count the number of times a depth measurement increases from the previous measurement.
    # (There is no measurement before the first measurement.)
    larger = 0
    for i in range(0, len(input_lines) - 2):  # -2 as final is '' and does not have a change
        this_el = int(input_lines[i])
        next_el = int(input_lines[i+1])
        if next_el > this_el:
            larger += 1

    print(larger)


if __name__ == '__main__':
    dotenv.load_dotenv()
    day_1(environ.get('SESSION_TOKEN'))
