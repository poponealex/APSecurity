from ast import literal_eval
import time


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
            if not is_valid(value):
                raise Exception(failure_description)
            if literal_eval(input(f"{Color.INFORMATION}Is this correct: {value} ? enter 1 to confirm, 0 to retry{Color.END}\n")) == 1:
                return value 
        except Exception as e:
            print(f"{Color.FAIL}<{e}> was raised, try again{Color.END}")


def get_date_time():
    """Current date and time

    Returns:
        Date and time in the format:
            Sun Nov  8 16:16:54 2020
    """
    return time.ctime(time.time())
