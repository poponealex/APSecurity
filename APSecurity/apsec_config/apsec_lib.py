import time, sys, json, os
from ast import literal_eval
from datetime import datetime
from pathlib import Path

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
    prompt: str="",
    is_valid=lambda _: True,
    failure_description: str="Value is illegal",
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
        if not is_valid(value):
            print(f"{Color.FAIL}{failure_description}{Color.END}\n")
        elif not input(f"{Color.INFORMATION}Is this correct: {value} ? press enter to confirm (enter any value to retry){Color.END} "):
            return value
            

def check_load_config_file() -> dict:
    """Checking and loading the configuration file.

    Run the config.py script from the apsec_config folder.
    The config.json will be created.

    Always run 'APSecurity.py' from the APSecurity folder.
    """
    if not Path.cwd().name == "APSecurity":
        raise FileNotFoundError(
            f"\n{Color.FAIL}Run 'APSecurity.py' from the 'APSecurity' directory.\nCurrent directory: {Path.cwd().name}.{Color.END}"
        )
    file_path = Path("apsec_config/config.json")
    if not file_path.exists():
        os.chdir("apsec_config")
        os.system("python3 config.py")
    return json.loads(file_path.read_text())


def get_date_time(log: bool=False) -> str:
    """Current date and time

    Returns the date and time in the format:
            13-02-2021 22:13:01
    """
    dt = datetime.now()
    if log:
        return f"{dt.day:02d}-{dt.month:02d}-{dt.year}_{dt.hour:02d}_{dt.minute:02d}_{dt.second:02d}"
    return f"{dt.day:02d}-{dt.month:02d}-{dt.year} {dt.hour:02d}:{dt.minute:02d}:{dt.second:02d}"


def countdown(seconds: int):
    for s in range(seconds, 0, -1):
        sys.stdout.write(f"\r  {Color.INFORMATION}{s // 60:02d}:{s % 60:02d}{Color.END}  ")
        time.sleep(1)