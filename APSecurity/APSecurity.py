#!usr/bin/python3
# -*-coding:utf-8 -*

import RPi.GPIO as gpio
import sys, signal, time, json
import smtplib, ssl
from urllib.request import urlopen
from pathlib import Path
from email.message import EmailMessage
from apsec_config.apsec_lib import *

TWO_MINUTES = 120
THIRTY_MINUTES = 1800
ONE_HOUR = 3600
ONE_DAY = 86400
MAX_CONSECUTIVE_ALERTS = 15

def close(signum="", frame="", process_started=True, message=""):
    print(f"{message}\n{Color.INFORMATION}QUITTING..{Color.END}\n")
    if process_started:
        send_text_message("SECURITY SYSTEM is OFF")
        send_email(subject="SECURITY SYSTEM OFF", msg="SECURITY SYSTEM is OFF")
        log._add_event(type="end")
        gpio.cleanup()
    sys.exit(0)
signal.signal(signal.SIGINT, close)

def check_load_config_file():
    """Checking and loading the configuration file.

    Run the config.py script from the apsec_config folder.
    The config.json will be created.

    Always run 'APSecurity.py' from the APSecurity folder.
    """
    if not Path.cwd().name == "APSecurity":
        close(process_started=False, message=f"\n{Color.FAIL}Run 'APSecurity.py' from the 'APSecurity' directory.\nCurrent directory: {Path.cwd().name}.{Color.END}")

    file_path = Path.cwd() / "apsec_config" / "config.json"
    if not file_path.exists():
        close(process_started=False, message=f"\n{Color.FAIL}Run the config.py script first.{Color.END}") 

    with open(file_path, "r") as f:
        return json.load(f)


class Logging:
    """LOGGING MODULE"""

    def __init__(self):
        self.path = Path.cwd() / "logs"
        self.log = self.path / f"log_{get_date_time()}".replace(" ", "_").replace(":", "-")
        self._create_log()
        self.err_count = 0

    def _create_log(self):
        if not self.path.exists():
            self.path.mkdir()
        with open(self.log, "w") as f:
            f.write(f"\tstarted at: {get_date_time()}\n\n")

    def _add_event(self, type="", nb="", msg=""):
        with open(self.log, "a") as f:
            if type == "a":
                f.write(f"{get_date_time()}\nALERT nb: {nb}\n\n")
            elif type == "p":
                f.write(f"{get_date_time()}\nPAUSE: {nb} {msg}\n\n")
            elif type == "r":
                f.write(f"{get_date_time()}\nRESUME: {nb} {msg}\n\n")
            elif type == "end":
                f.write(f"\t{get_date_time()}\n\tPROGRAM ENDED\n\n")
            elif type == "err":
                self.err_count += 1
                f.write(f"{get_date_time()}\nERROR: {self.err_count}\n{msg}\n\n")
            elif msg:
                f.write(f"{get_date_time()}\n{msg}\n\n")
            else:
                f.write(f"{get_date_time()}\nUNKNOWN ERROR\n\n")

def send_email(subject="", msg=""):
    try:
        message = EmailMessage()
        message["From"] = var["SENDER_NAME"]
        message["To"] = var["MAIL_RECIPIENT"]
        message["Subject"] = subject
        message.set_content(msg)

        with smtplib.SMTP_SSL(var["MAIL_SERVER"], var["SERVER_PORT"], context=ssl._create_unverified_context()) as server:
            server.login(var["MAIL_USER"], var["MAIL_PWD"])
            server.send_message(msg)
    except Exception as e:
        log._add_event(type="err", msg=f"EMAIL ERROR: {e}")


def send_text_message(message):
    try:
        url = f"{var['TXT_MSG_URL']}{message.replace(' ', '%20')}"
        urlopen(url, context=ssl._create_unverified_context())
    except Exception as e:
        log._add_event(type="err", msg=f"TEXT MESSAGE ERROR: {e}")

def setup():
    """Setting up the program.

    Note that the motion sensor will send HIGH level signals for about 80secs after being wired to the RPi.
    """
    gpio.setmode(gpio.BOARD)
    gpio.setup(var["MOTION_DETECTOR_PIN"], gpio.IN)

    print(f"\n\t{Color.TITLE}WELCOME TO {var['PROGRAM_NAME']}{Color.END}\n")

    sec = input_value_satisfying_condition(
        f"{Color.INFORMATION}Delay before starting the security system (in seconds)? {Color.END}",
        is_valid=lambda value: value <= THIRTY_MINUTES,
        failure_description="should be at most 30 mn",
    )

    for a in range(sec, -1, -1):
        sys.stdout.write(f" {Color.INFORMATION}{a}{Color.END} \r")
        if sec > 0:
            time.sleep(1)

    print(f"{Color.INFORMATION}\nSTARTING at {get_date_time()}!{Color.END}\n")

def run():
    """Running the program.

    An email + a text message are sent when the motion sensor is triggered.
    There is a 2min pause in between each alert.
    There is a 1 hour pause after 10 alerts.
    """
    alerts_count = 0
    pauses_count = 0
    start_time = time.time()

    while True:
        try:
            if gpio.input(var["MOTION_DETECTOR_PIN"]) == gpio.HIGH:
                alerts_count += 1
                print(f"{Color.INFORMATION}{get_date_time()}{Color.END}")
                print(f"{Color.FAIL}ALERT nb: {alerts_count}{Color.END}\n")
                log._add_event(type="a", nb=alerts_count)
                send_text_message(var["MSG"].format(x=get_date_time()))
                send_email(subject=var["MAIL_SUBJECT"], msg=var["MSG"].format(x=get_date_time()))
                if alerts_count > MAX_CONSECUTIVE_ALERTS:
                    pauses_count += 1
                    print(f"{Color.INFORMATION}PAUSING..{Color.END}")
                    log._add_event(type="p", nb=pauses_count)
                    send_text_message(var["MSG_BREAK"].format(x=get_date_time()))
                    send_email(subject="break", msg=var["MSG_BREAK"].format(x=get_date_time()))
                    time.sleep(ONE_HOUR)
                    alerts_count = 0
                    print(f"{Color.INFORMATION}RESUMING..{Color.END}\n")
                    log._add_event(type="r", nb=pauses_count)
                    send_text_message(var["MSG_RESUME"].format(x=get_date_time()))
                    send_email(subject="resume", msg=var["MSG_RESUME"].format(x=get_date_time()))
                else:
                    print(f"{Color.INFORMATION}pausing..{Color.END}")
                    log._add_event(type="p", msg="short 2min pause")
                    time.sleep(TWO_MINUTES)
                    print(f"{Color.INFORMATION}resuming..{Color.END}\n")
                    log._add_event(type="p", msg="end of short pause")

            if time.time() - start_time > ONE_DAY:
                alerts_count = 0
                start_time = time.time()
                log._add_event(msg=f"start time and alerts' count reseted at {get_date_time()}")
        except Exception as e:
            log._add_event(type="err", msg=f"{e}")
            print(f"{Color.INFORMATION}<{e}> was raised!{Color.END}")

if __name__ == "__main__":
    log = Logging()
    var = check_load_config_file()
    setup()
    run()