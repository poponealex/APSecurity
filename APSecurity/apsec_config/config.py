#!usr/bin/python3
# -*-coding:utf-8 -*

import json, re, signal, sys
from pathlib import Path
from apsec_lib import *


HOSTNAME = re.compile(r"^[a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~:()\"\"\[\]]{1,}[.][a-zA-Z0-9\[\]]{1,}$")
EMAIL = re.compile(r"^[a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~:()\"\"\[\]]{1,}[@][a-zA-Z0-9.!#$%&'*+-/=?^_`:{|}~()\"\"\[\]]{1,}[.][a-zA-Z0-9\[\]]{1,}$")


def close(signum="", frame=""):
    sys.exit(0)
signal.signal(signal.SIGINT, close)


if Path.cwd().name != "apsec_config":
    print(f"\n{Color.FAIL}Run config.py from the 'apsec_config' directory -> 'APSecurity/apsec_config'.\nCurrent directory: {Path.cwd().name}.{Color.END}")

else:
    print(f"{Color.TITLE}\n\t\tLet's configurate the program!{Color.END}\n\n")
    parameters = {
        "PROGRAM_NAME": "AP EaZey sEcuRiTy",
        "MOTION_DETECTOR_PIN": input_value_satisfying_condition(
            prompt="Enter the motion sensor's pin's number:",
            is_valid=lambda value: isinstance(value, int) and value >= 1 and value <= 40,
            failure_description="Enter a number in between 1 and 40.",
        ),
        "MAIL_SERVER": input_value_satisfying_condition(
            prompt="Enter the mail server's hostname:",
            is_valid=lambda value: isinstance(value, str) and HOSTNAME.match(value),
            failure_description="Enter a server in the format: foo.bar",
        ),
        "SERVER_PORT": input_value_satisfying_condition(
            prompt="Enter the mail server's PORT number:",
            is_valid=lambda value: isinstance(value, int) and value > 0,
            failure_description="Enter a valid port number.",
        ),
        "MAIL_USER": input_value_satisfying_condition(
            prompt="Enter your username (email address):",
            is_valid=lambda value: isinstance(value, str) and EMAIL.match(value),
            failure_description="Enter an email in the format foo@bar.spam",
        ),
        "MAIL_PWD": input_value_satisfying_condition(
            prompt="Enter your password:",
            is_valid=lambda _: True,
        ),
        "SENDER_NAME": input_value_satisfying_condition(
            prompt="Enter a custom sender's name:", is_valid=lambda value: isinstance(value, str), failure_description="Enter your 'name'."
        ),
        "MAIL_RECIPIENT": input_value_satisfying_condition(
            prompt="Enter the recipient's email for the alerts:",
            is_valid=lambda value: isinstance(value, str) and EMAIL.match(value),
            failure_description="Enter an email in the format foo@bar.spam",
        ),
        "TXT_MSG_URL": input_value_satisfying_condition(
            prompt="Enter your SMS URL ending with the GET parameter for the message's content (eg: 'msg='): ",
            is_valid=lambda value: isinstance(value, str) and re.match(r".*[=]$", value),
            failure_description="Enter a valid SMS URL.",
        ),
        "MAIL_SUBJECT": "ALERT",
        "MSG": "ALERT!!! MOTION SENSOR HAS DETECTED SOMEONE at {x}!",
        "MSG_BREAK": "THE SECURITY SYSTEM IS PAUSING at {x}! It will resume in 2 hours.",
        "MSG_RESUME": "THE SECURITY SYSTEM HAS RESUMED at {x}.",
    }

    with open("config.json", "w") as f:
        json.dump(parameters, f)

    print(f"{Color.INFORMATION}\nDONE! You're all set!\n{Color.END}")

close()
