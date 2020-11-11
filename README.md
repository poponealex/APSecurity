# APSecurity
Home security system running on a Raspberry Pi.

## Introduction
AP Security is a ready to go security system. It's aimed at simple utilisations such as monitoring one room. 

### Prerequisites
- Raspberry Pi running RPi OS
- Infrared Motion Sensor
    - Jumper cables to wire the sensor to the RPi.
- Python 3
- Infrared Motion Sensor
- Internet Connectivity
- Email address
    - It is highly recommended that you use a secondary email address as the sender's email.
    - It has to support SMTP and SSL.
    - Third-Party connection (less secure apps) has to be allowed if not default.
- Text Message URL
    - Many ISP and MSP provide them, for instance FREE MOBILE FRANCE does.
    - Ex.: "https://smsapi.free-mobile.fr/sendmsg?user=&pass=&msg="
    - __THE URL HAS TO BE ENTERED WITH THE GET ATTRIBUTE FOR THE MESSAGE AT THE END OF THE LINK, please refer to the previous exemple.__

## Installation
### Motion Sensor
#### Wire the motion sensor to the RPi:
> - Wire the motion sensor's output pin to any of your RPi's GPIO pin.
>   - BOARD configuration is used in the program.
>   - For instance if you choose GPIO17, you'll have to enter 11 as the pin's number when running `config.py`.
> - Wire the anode (+) to 5Volts.
> - Wire the cathode (-) to GND.

### Configuration
Run `config.py` from the `apsec_config` directory.
> Follow the instructions.
> ![APSecurity Config](/screenshots/apsec_config.png)

### Run the program
Run `APSecurity.py` from the parent directory `APSecurity`.
> Follow the instructions.
> ![APSecurity](/screenshots/apsec_run.png)

## Errors handling
### You didn't run the `config.py` script
> This error will be raised if you try to run `APSecurity.py` without running `config.py` first.
> ![APSecurity configuration error](/screenshots/err_notConfig.png)

__The obvious fix is to run `config.py` (from the `apsec_config` directory).__

### You're trying to run `config.py` from somehere else than `/APSecurity/apsec_config`
> This error will be raised if you try to run `config.py` from somehere else than `/APSecurity/apsec_config`.
> ![APSecurity wrong dir config](/screenshots/err_dir_config.png)

__The obvious fix is to run `config.py` from the `apsec_config` directory.__

### You're trying to run `APSecurity.py` from somehere else than the `APSecurity` directory
> This error will be raised if you try to run `APSecurity.py` from somehere else than `/APSecurity`.
> ![APSecurity wrong dir config](/screenshots/err_dir_apsec.png)

__The obvious fix is to run `APSecurity.py` from the `APSecurity` directory.__

## LOGS
Logs are automatically generated to the `logs` folder that will be created after the first initialisation of the program.
> An exemple of a log:

> ![APSecurity log](/screenshots/ex_log.png) 

# ENJOY

_Thanks @laowantong for the help!_
