from ast import literal_eval
import time

class Color:
    """ANSI color codes.

    Args:
        - FAIL: bold red
        - INFORMATION: bold blue
        - TITLE: bold cyan
        - END: end point of the coloration
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

    Vars:
        - prompt: message displayed when prompting for user input.
        - is_valid: lambda function to verify a condition.
        - failure_description: message displayed when is_valid()'s condition is not met.

    Returns:
        - The value entered by the user if is_valid's condition is met and after confirmation by the user.
        - If the is_valid condition fails failure_description is displayed
        - If literal_eval fails an error message containing the raised exception.
    """
    while True:
        value = input(f"{Color.INFORMATION}{prompt}{Color.END}\n")
        try:
            value = literal_eval(value)
        except Exception:
            pass
        try:
            if is_valid(value):
                a = literal_eval(
                    input(
                        f"{Color.INFORMATION}Is this correct: {value} ? enter 1 to confirm, 0 to retry{Color.END}\n"
                    )
                )
                if a == 1:
                    return value
            else:
                print(f"{Color.FAIL}{failure_description}{Color.END}")
        except Exception as e:
            print(f"{Color.FAIL}{e} was raised, try again{Color.END}")

def get_date_time():
    """Current date and time

    Returns:
        Date and time in the format:
            Sun Nov  8 16:16:54 2020
    """
    return time.ctime(time.time())
