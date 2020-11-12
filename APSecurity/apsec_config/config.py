#!usr/bin/python3
# -*-coding:utf-8 -*

import json, re, signal, sys
from ast import literal_eval
from pathlib import Path


def close(signum, frame):
    print(f"{Color.INFORMATION}QUITTING..{Color.END}\n")
    sys.exit(0)


signal.signal(signal.SIGINT, close)


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


def set_var_input_validation(
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
        except ValueError:
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


if Path.cwd().name != "apsec_config":
    print(
        f"\n{Color.FAIL}Run config.py from the 'apsec_config' directory -> 'APSecurity/apsec_config'.\nCurrent directory: {Path.cwd().name}.{Color.END}"
    )
    close(signal.SIGINT, 0)

print(f"{Color.TITLE}\n\t\tWELCOME to the sEcUrItY CoNfIg fIlE{Color.END}\n\n")
var = {
    "PROGRAM_NAME": "AP EaZey sEcuRiTy",
    "MOTION_DETECTOR_PIN": set_var_input_validation(
        prompt="Enter the motion sensor's pin's number:",
        is_valid=lambda value: type(value) == int and value >= 1 and value <= 40,
    ),
    "MAIL_SERVER": set_var_input_validation(
        prompt="Enter the mail server's hostname:",
        is_valid=lambda value: type(value) == str
        and re.match(
            r"^[a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~:()\"\"\[\]]{1,}[.][a-zA-Z0-9\[\]]{1,}$", value
        ),
    ),
    "SERVER_PORT": set_var_input_validation(
        prompt="Enter the mail server's PORT number:",
        is_valid=lambda value: type(value) == int,
    ),
    "MAIL_USER": set_var_input_validation(
        prompt="Enter your username (email address):",
        is_valid=lambda value: type(value) == str
        and re.match(
            r"^[a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~:()\"\"\[\]]{1,}[@][a-zA-Z0-9.!#$%&'*+-/=?^_`:{|}~()\"\"\[\]]{1,}[.][a-zA-Z0-9\[\]]{1,}$",
            value,
        ),
    ),
    "MAIL_PWD": set_var_input_validation(
        prompt="Enter your password:",
        is_valid=lambda value: type(value) == str,
    ),
    "SENDER_NAME": set_var_input_validation(
        prompt="Enter a custom sender's name:",
        is_valid=lambda value: type(value) == str,
    ),
    "MAIL_RECIPIENT": set_var_input_validation(
        prompt="Enter the recipient's email for the alerts:",
        is_valid=lambda value: type(value) == str
        and re.match(
            r"^[a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~:()\"\"\[\]]{1,}[@][a-zA-Z0-9.!#$%&'*+-/=?^_`:{|}~()\"\"\[\]]{1,}[.][a-zA-Z0-9\[\]]{1,}$",
            value,
        ),
    ),
    "TXT_MSG_URL": set_var_input_validation(
        prompt="Enter your text message URL (with quotes) ending with 'msg=':",
        is_valid=lambda value: type(value) == str and re.match(r".*[=]$", value),
    ),
    "MAIL_SUBJECT": "ALERT",
    "MSG": "ALERT!!! MOTION SENSOR HAS DETECTED SOMEONE at {x}!",
    "MSG_BREAK": "THE SECURITY SYSTEM IS PAUSING at {x}! It will resume in 2 hours.",
    "MSG_RESUME": "THE SECURITY SYSTEM HAS RESUMED at {x}.",
}

with open("config.json", "w") as f:
    json.dump(var, f)

print(f"{Color.INFORMATION}\nDONE!\n\n{Color.END}")
