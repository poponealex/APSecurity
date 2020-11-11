#!usr/bin/python3
# -*-coding:utf-8 -*

import RPi.GPIO as gpio
import sys, signal, time, json
import smtplib, ssl
from urllib.request import urlopen
from pathlib import Path
from ast import literal_eval
from email.message import EmailMessage


def check_load_config_file():
    """Checking and loading the configuration file.

    Run the config.py script from the apsec_config folder.
    The config.json will be created.

    Always run 'APSecurity.py' from the APSecurity folder.

    'var' (global variable) will store the object contained in the config.json as type(dict).
    """
    if Path.cwd().name != "APSecurity":
        print(
            f"\n{Color.FAIL}Run 'APSecurity.py' from the 'APSecurity' directory.\nCurrent directory: {Path.cwd().name}.{Color.END}"
        )
        close(signal.SIGINT, 0, config=False)

    file = Path.cwd() / "apsec_config" / "config.json"

    if not file.exists():
        print(f"\n{Color.FAIL}Run the config.py script first.{Color.END}")
        close(signal.SIGINT, 0, config=False)
    else:
        global var
        with open(file, "r") as f:
            var = json.load(f)


def get_date_time():
    """Current date and time

    Returns:
        Date and time in the format:
            Sun Nov  8 16:16:54 2020
    """
    return time.ctime(time.time())


def input_value_satisfying_condition(
    prompt, predicate=lambda _: True, failure_description="Value is illegal"
):
    """Validating user input by predicate.

    Vars:
        - prompt: message displayed when prompting for user input
        - predicate: lambda function to verify a condition
        - failure_description: message displayed when predicate's condition is not met.

    Returns:
        - The value entered by the user if predicate's condition is met.
        - If the predicate fails failure_description is displayed
        - If literal_eval fails an error message containing the raised exception."""
    while True:
        try:
            value = literal_eval(input(prompt))
            if predicate(value):
                return value
            print(f"{Color.FAIL} {failure_description}, try again. {Color.END}")
        except Exception as e:
            print(f"{Color.FAIL}'{e}' raised, try again.{Color.END}")


class Color:
    """ANSI color codes used throughout the program.

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


class Alerts:
    """Alerts object is the security module that handles notifications and logs.

    Public functions:
        - send_email
        - send_text_message

    Private functions:
         - _create_log
         - _add_event_log
    """

    def __init__(self):
        self._create_log()
        self.err_count = 0

    def __repr__(self):
        print("'Alerts' Security module")

    def _create_log(self):
        """Create the log's file and folder."""

        self.log_name = f"log_{get_date_time()}".replace(" ", "_").replace(":", "-")

        path = f"{Path.cwd()}/logs"
        p = Path(path)
        if not p.exists():
            p.mkdir()

        file = Path.cwd() / "logs" / self.log_name
        with open(file, "w") as f:
            f.write(f"\tstarted at: {get_date_time()}\n\n")

    def _add_event_log(self, type="", nb=0, **msg):
        """Add a log entry.

        Args:
            - type: A string that contains the log entry's type to create.
            - *nb: The associated event's number.
        """

        t = get_date_time()
        if type == "a":
            self.content = f"{t}\nALERT nb: {nb}\n\n"
        elif type == "p":
            self.content = f"{t}\nPAUSE: {nb}\n\n"
        elif type == "r":
            self.content = f"{t}\nRESUME: {nb}\n\n"
        elif type == "end":
            self.content = f"\t{t}\n\tPROGRAM ENDED\n\n"
        elif type == "err":
            self.err_count += 1
            self.content = f"\t{t}\n\tERROR: {self.err_count}\n\n"
        else:
            if msg:
                self.content = f"\t{t}\n\t{msg}\n\n"
            else:
                self.content = f"\t{t}\n\tENTRY NOT SPECIFIED\n\n"

        file = Path.cwd() / "logs" / self.log_name
        with open(file, "a") as f:
            f.write(self.content)

    def send_email(self, server, port, user, pwd, sender_name, recipient, subject, msg):

        self.server, self.port, self.user, self.pwd = server, port, user, pwd
        self.msg = EmailMessage()
        self.msg["From"] = sender_name
        self.msg["To"] = recipient
        self.msg["Subject"] = subject
        self.msg.set_content(msg)

        with smtplib.SMTP_SSL(
            self.server, self.port, context=ssl._create_unverified_context()
        ) as server:
            try:
                server.login(self.user, self.pwd)
                server.send_message(self.msg)
            except:
                self._add_event_log(type="err")

    def send_text_message(self, msg):

        self.msg = msg.replace(" ", "%20")
        self.u = f"{var['TXT_MSG_URL']}{self.msg}"
        try:
            urlopen(self.u, context=ssl._create_unverified_context())
        except:
            self._add_event_log(type="err")


def setup():
    """Setting up the program.

    It is important to note that the motion sensor will send HIGH level signals for about 80secs after being wired to the RPi.
    """
    gpio.setmode(gpio.BOARD)
    gpio.setup(var["MOTION_DETECTOR_PIN"], gpio.IN)

    print(f"\n\t{Color.TITLE}WELCOME TO {var['PROGRAM_NAME']}{Color.END}\n")

    sec = input_value_satisfying_condition(
        f"{Color.INFORMATION}Delay before starting the security system (in seconds)? {Color.END}",
        predicate=lambda value: value <= 1800,
        failure_description="should be at most 30 mn",
    )

    for a in range(sec, -1, -1):
        sys.stdout.write(f"\r{Color.INFORMATION}{a}{Color.END}")
        sys.stdout.flush()
        if sec > 0:
            time.sleep(1)

    print(f"{Color.INFORMATION}\nSTARTING at {get_date_time()}!{Color.END}\n")


def run():
    """Running the program.

    An email + a text message are sent when the motion sensor is triggered.
    There is a 2min pause in between each alert.
    There is a 1 hour pause after 10 alerts.
    """

    count_alerts = 0
    count_pauses = 0
    start_time = time.time()

    while True:
        if gpio.input(var["MOTION_DETECTOR_PIN"]) == gpio.HIGH:
            t = get_date_time()
            count_alerts += 1
            print(f"{Color.INFORMATION}{t}{Color.END}")
            print(f"{Color.FAIL}ALERT nb: {count_alerts}{Color.END}\n")
            alert._add_event_log(type="a", nb=count_alerts)
            alert.send_text_message(var["MSG"].format(x=get_date_time()))
            alert.send_email(
                var["MAIL_SERVER"],
                var["SERVER_PORT"],
                var["MAIL_USER"],
                var["MAIL_PWD"],
                var["SENDER_NAME"],
                var["MAIL_RECIPIENT"],
                var["MAIL_SUBJECT"],
                var["MSG"].format(x=get_date_time()),
            )
            if count_alerts > 10:
                count_pauses += 1
                print(f"{Color.INFORMATION}PAUSING..{Color.END}")
                alert._add_event_log(type="p", nb=count_pauses)
                alert.send_text_message(var["MSG_BREAK"].format(x=get_date_time()))
                alert.send_email(
                    var["MAIL_SERVER"],
                    var["SERVER_PORT"],
                    var["MAIL_USER"],
                    var["MAIL_PWD"],
                    var["SENDER_NAME"],
                    var["MAIL_RECIPIENT"],
                    "break",
                    var["MSG_BREAK"].format(x=get_date_time()),
                )
                time.sleep(3600)
                count_alerts = 0
                print(f"{Color.INFORMATION}RESUMING..{Color.END}\n")
                alert._add_event_log(type="r", nb=count_pauses)
                alert.send_text_message(var["MSG_RESUME"].format(x=get_date_time()))
                alert.send_email(
                    var["MAIL_SERVER"],
                    var["SERVER_PORT"],
                    var["MAIL_USER"],
                    var["MAIL_PWD"],
                    var["SENDER_NAME"],
                    var["MAIL_RECIPIENT"],
                    "resume",
                    var["MSG_RESUME"].format(x=get_date_time()),
                )
            else:
                print(f"{Color.INFORMATION}pausing..{Color.END}")
                time.sleep(120)
                print(f"{Color.INFORMATION}resuming..{Color.END}\n")

        if time.time() - start_time > 14400:
            count_alerts = 0
            start_time = time.time()
            _add_event_log(msg=f"start time + alerts' count reseted at {get_date_time()}")


def close(signum, frame, config=True):
    print(f"{Color.INFORMATION}QUITTING..{Color.END}\n")
    if config == True:
        alert.send_text_message("SECURITY SYSTEM is OFF")
        alert._add_event_log(type="end")
        gpio.cleanup()
    sys.exit(0)


signal.signal(signal.SIGINT, close)

if __name__ == "__main__":
    check_load_config_file()
    alert = Alerts()
    while True:
        setup()
        run()
