from ast import literal_eval
import time, sys
from datetime import datetime

class Color:
    """ANSI COLORS

    Color.FAIL --> bold red
    Color.INFORMATION --> bold blue
    Color.TITLE --> bold cyan
    Color.END
    """

    FAIL = "\033[91m\033[1m"
    INFORMATION = "\033[94m\033[1m"
    TITLE = "\033[96m\033[1m"
    END = "\033[0m"


def input_value_satisfying_condition(
    prompt="",
    is_valid=lambda _: True,
    failure_description="Value is illegal",
):
    """Validating user input by predicate.

    Parameters:
        - prompt: message displayed when prompting for user input.
        - is_valid: lambda function to check the validity of the input.
        - failure_description: message displayed when is_valid()'s condition is not met.

    If the is_valid condition fails failure_description is raised.
    Returns the value entered after validation by is_valid.
    """
    while True:
        value = input(f"{Color.INFORMATION}{prompt}{Color.END}\n")
        try:
            value = literal_eval(value)
        except:
            pass
        try:
            assert is_valid(value)
            if not input(f"{Color.INFORMATION}Is this correct: {value} ? press enter to confirm (enter any value to retry){Color.END} "):
                return value
        except:
            print(f"{Color.FAIL}<{failure_description}> was raised, try again{Color.END}\n")


def get_date_time(log=False):
    """Current date and time

    Returns the date and time in the format:
            13-02-2021 22:13:01
    """
    dt = datetime.now()
    if log:
        return f"{dt.day:02d}-{dt.month:02d}-{dt.year}_{dt.hour:02d}_{dt.minute:02d}_{dt.second:02d}"
    return f"{dt.day:02d}-{dt.month:02d}-{dt.year} {dt.hour:02d}:{dt.minute:02d}:{dt.second:02d}"


def countdown(seconds):
    for s in range(seconds, 0, -1):
        sys.stdout.write(f"\r  {Color.INFORMATION}{s // 60:02d}:{s % 60:02d}{Color.END}  ")
        time.sleep(1)