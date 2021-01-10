#!usr/bin/python3
# -*-coding:utf-8 -*

import json, re, signal, sys
from pathlib import Path
from apsec_lib import *


def close(signum="", frame=""):
    print(f"{Color.INFORMATION}QUITTING..{Color.END}\n")
    sys.exit(0)
signal.signal(signal.SIGINT, close)


if Path.cwd().name != "apsec_config":
    print(
        f"\n{Color.FAIL}Run config.py from the 'apsec_config' directory -> 'APSecurity/apsec_config'.\nCurrent directory: {Path.cwd().name}.{Color.END}"
    )

else:
    print(f"{Color.TITLE}\n\t\tWELCOME to the sEcUrItY CoNfIg fIlE{Color.END}\n\n")
    var = {
        "PROGRAM_NAME": "AP EaZey sEcuRiTy",
        "MOTION_DETECTOR_PIN": input_value_satisfying_condition(
            prompt="Enter the motion sensor's pin's number:",
            is_valid=lambda value: type(value) == int and value >= 1 and value <= 40,
        ),
        "MAIL_SERVER": input_value_satisfying_condition(
            prompt="Enter the mail server's hostname:",
            is_valid=lambda value: type(value) == str
            and re.match(
                r"^[a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~:()\"\"\[\]]{1,}[.][a-zA-Z0-9\[\]]{1,}$", value
            ),
        ),
        "SERVER_PORT": input_value_satisfying_condition(
            prompt="Enter the mail server's PORT number:",
            is_valid=lambda value: type(value) == int,
        ),
        "MAIL_USER": input_value_satisfying_condition(
            prompt="Enter your username (email address):",
            is_valid=lambda value: type(value) == str
            and re.match(
                r"^[a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~:()\"\"\[\]]{1,}[@][a-zA-Z0-9.!#$%&'*+-/=?^_`:{|}~()\"\"\[\]]{1,}[.][a-zA-Z0-9\[\]]{1,}$",
                value,
            ),
        ),
        "MAIL_PWD": input_value_satisfying_condition(
            prompt="Enter your password:",
            is_valid=lambda value: type(value) == str,
        ),
        "SENDER_NAME": input_value_satisfying_condition(
            prompt="Enter a custom sender's name:",
            is_valid=lambda value: type(value) == str,
        ),
        "MAIL_RECIPIENT": input_value_satisfying_condition(
            prompt="Enter the recipient's email for the alerts:",
            is_valid=lambda value: type(value) == str
            and re.match(
                r"^[a-zA-Z0-9.!#$%&'*+-/=?^_`{|}~:()\"\"\[\]]{1,}[@][a-zA-Z0-9.!#$%&'*+-/=?^_`:{|}~()\"\"\[\]]{1,}[.][a-zA-Z0-9\[\]]{1,}$",
                value,
            ),
        ),
        "TXT_MSG_URL": input_value_satisfying_condition(
            prompt="Enter your text message URL ending with the GET attribute 'msg=':",
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
close()