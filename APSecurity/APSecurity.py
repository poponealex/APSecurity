#!usr/bin/python3
# -*-coding:utf-8 -*

import RPi.GPIO as gpio
import sys, os, signal, time, json, logging
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
LOGGING_FORMAT = "%(asctime)s\n%(levelname)s: %(message)s\n"
LOGGING_DATE_FORMAT = "%d/%m/%Y - %I:%M:%S %p"

def close(signum="", frame="", process_started=True, message=""):
    print(f"{message}\n{Color.INFORMATION}QUITTING..{Color.END}\n")
    if process_started:
        send_text_message("SECURITY SYSTEM IS OFF")
        send_email(subject="SECURITY SYSTEM OFF", msg="SECURITY SYSTEM IS OFF")
        gpio.cleanup()
    logging.warning("SECURITY SYSTEM IS OFF")
    sys.exit(0)
signal.signal(signal.SIGINT, close)

def enable_logging():
    path = Path.cwd() / "logs"
    log_name = f"log_{get_date_time(log=True)}.log"
    if not path.exists():
        path.mkdir()
    logging.basicConfig(filename=f"{path / log_name}", encoding="utf-8", level=logging.DEBUG, format=LOGGING_FORMAT, datefmt=LOGGING_DATE_FORMAT)
    logging.info("Logging has started.")

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
        os.chdir("apsec_config")
        os.system("python3 config.py")
        logging.info("config file created")

    with open(file_path, "r") as f:
        return json.load(f)

def send_email(subject="", msg=""):
    try:
        message = EmailMessage()
        message["From"] = var["SENDER_NAME"]
        message["To"] = var["MAIL_RECIPIENT"]
        message["Subject"] = subject
        message.set_content(msg)

        with smtplib.SMTP_SSL(var["MAIL_SERVER"], var["SERVER_PORT"], context=ssl._create_unverified_context()) as server:
            server.login(var["MAIL_USER"], var["MAIL_PWD"])
            server.send_message(message)
    except Exception as e:
        logging.critical(f"EMAIL ERROR: {e}")
        return print(f"{Color.FAIL}An error occurred while sending an email.{Color.END}")


def send_text_message(message):
    try:
        url = f"{var['TXT_MSG_URL']}{message.replace(' ', '%20')}"
        urlopen(url, context=ssl._create_unverified_context())
    except Exception as e:
        logging.critical(f"TEXT MESSAGE ERROR: {e}")
        return print(f"{Color.FAIL}An error occurred while sending a text message.{Color.END}")

def run():
    """Setting up and running the program.

    Note that the motion sensor will send HIGH level signals for about 80secs after being wired to the RPi.
    An email + a text message are sent when the motion sensor is triggered.
    There is a 2min pause in between each alert.
    There is a 1 hour pause after 10 alerts.
    """
    
    gpio.setmode(gpio.BOARD)
    gpio.setup(var["MOTION_DETECTOR_PIN"], gpio.IN)

    print(f"\n\t{Color.TITLE}WELCOME TO {var['PROGRAM_NAME']}{Color.END}\n")
    countdown(
        input_value_satisfying_condition(
        f"{Color.INFORMATION}Delay before starting the security system (in seconds)? {Color.END}",
        is_valid=lambda value: 0 <= value <= THIRTY_MINUTES,
        failure_description="should be at most 30 mn",
    ))

    print(f"{Color.INFORMATION}\nSTARTING at {get_date_time()}!{Color.END}\n")
    start_time = time.time()

    alerts_count = 0
    pauses_count = 0
    
    while True:
        try:
            if gpio.input(var["MOTION_DETECTOR_PIN"]) == gpio.HIGH:
                alerts_count += 1
                print(f"{Color.INFORMATION}{get_date_time()}{Color.END}")
                print(f"{Color.FAIL}ALERT nb: {alerts_count}{Color.END}\n")
                logging.critical(f"ALERT [{alerts_count}]: MOTION SENSOR WAS TRIGGERED")
                send_text_message(var["MSG"].format(x=get_date_time()))
                send_email(subject=var["MAIL_SUBJECT"], msg=var["MSG"].format(x=get_date_time()))
                if alerts_count > MAX_CONSECUTIVE_ALERTS:
                    pauses_count += 1
                    print(f"{Color.INFORMATION}PAUSING..{Color.END}")
                    logging.info(f"PAUSING [{pauses_count}]")
                    send_text_message(var["MSG_BREAK"].format(x=get_date_time()))
                    send_email(subject="break", msg=var["MSG_BREAK"].format(x=get_date_time()))
                    time.sleep(ONE_HOUR)
                    alerts_count = 0
                    print(f"{Color.INFORMATION}RESUMING..{Color.END}\n")
                    logging.info("RESUMING")
                    send_text_message(var["MSG_RESUME"].format(x=get_date_time()))
                    send_email(subject="resume", msg=var["MSG_RESUME"].format(x=get_date_time()))
                else:
                    print(f"{Color.INFORMATION}pausing..{Color.END}")
                    logging.info("SHORT 2MN PAUSE")
                    time.sleep(TWO_MINUTES)
                    print(f"{Color.INFORMATION}resuming..{Color.END}\n")
                    logging.info("RESUMING")

            if time.time() - start_time > ONE_DAY:
                alerts_count = 0
                start_time = time.time()
                logging.info("Start time and alerts' count have been reseted.")
        except Exception as e:
            logging.error(e)
            print(f"{Color.FAIL}<{e}> was raised!{Color.END}")

if __name__ == "__main__":
    enable_logging()
    var = check_load_config_file()
    run()