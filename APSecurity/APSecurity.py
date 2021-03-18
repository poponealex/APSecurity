import RPi.GPIO as gpio
import sys, os, signal, time, logging
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
VAR = check_load_config_file()


def close(signum="", frame=""):
    print(f"{Color.INFORMATION}QUITTING..{Color.END}\n")
    send_text_message("SECURITY SYSTEM IS OFF")
    send_email("SECURITY SYSTEM OFF", "SECURITY SYSTEM IS OFF")
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


def send_email(subject: str, msg: str) -> None:
    try:
        message = EmailMessage()
        message["From"] = VAR["SENDER_NAME"]
        message["To"] = VAR["MAIL_RECIPIENT"]
        message["Subject"] = subject
        message.set_content(msg)

        with smtplib.SMTP_SSL(VAR["MAIL_SERVER"], VAR["SERVER_PORT"], context=ssl._create_unverified_context()) as server:
            server.login(VAR["MAIL_USER"], VAR["MAIL_PWD"])
            server.send_message(message)
    except Exception as e:
        logging.critical(f"EMAIL ERROR: {e}")
        return print(f"{Color.FAIL}An error occurred while sending an email.{Color.END}")


def send_text_message(message: str) -> None:
    try:
        url = f"{VAR['TXT_MSG_URL']}{message.replace(' ', '%20')}"
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
    gpio.setup(VAR["MOTION_DETECTOR_PIN"], gpio.IN)

    print(f"\n\t{Color.TITLE}WELCOME TO {VAR['PROGRAM_NAME']}{Color.END}\n")
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
            if gpio.input(VAR["MOTION_DETECTOR_PIN"]) == gpio.HIGH:
                alerts_count += 1
                print(f"{Color.INFORMATION}{get_date_time()}{Color.END}")
                print(f"{Color.FAIL}ALERT nb: {alerts_count}{Color.END}\n")
                logging.critical(f"ALERT [{alerts_count}]: MOTION SENSOR WAS TRIGGERED")
                send_text_message(VAR["MSG"].format(x=get_date_time()))
                send_email(VAR["MAIL_SUBJECT"], VAR["MSG"].format(x=get_date_time()))
                if alerts_count > MAX_CONSECUTIVE_ALERTS:
                    pauses_count += 1
                    print(f"{Color.INFORMATION}PAUSING..{Color.END}")
                    logging.info(f"PAUSING [{pauses_count}]")
                    send_text_message(VAR["MSG_BREAK"].format(x=get_date_time()))
                    send_email("break", VAR["MSG_BREAK"].format(x=get_date_time()))
                    time.sleep(ONE_HOUR)
                    alerts_count = 0
                    print(f"{Color.INFORMATION}RESUMING..{Color.END}\n")
                    logging.info("RESUMING")
                    send_text_message(VAR["MSG_RESUME"].format(x=get_date_time()))
                    send_email("resume", VAR["MSG_RESUME"].format(x=get_date_time()))
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
    try:
        enable_logging()
        run()
    except Exception as e:
        print(f"{Color.FAIL}{e}{Color.END}")
    close()