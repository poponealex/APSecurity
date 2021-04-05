![Logo](/misc/logo.png)
Motion detection program triggering alerts. Built to run on a Raspberry Pi.

## Introduction
AP Security is a ready to go "security system" aimed for trivial usages such as monitoring one room.

### Prerequisites
- Python 3.6+
- Raspberry Pi running RPi OS
- Infrared Motion Sensor
- Email address
    - It is highly recommended that you use a secondary email address as the sender's email.
    - It has to support SMTP and SSL.
    - Third-Party connection (less secure apps) has to be allowed if not default.
- Text Message (SMS) URL Gateway
    - Many ISP and MSP provide them, for instance FREE MOBILE FRANCE does.
    - Ex.: "https://smsapi.free-mobile.fr/sendmsg?user=&pass=&msg="

## Installation
### Motion Sensor
#### Wire the motion sensor to the RPi:
> - Wire the motion sensor's output pin to any of your RPi's GPIO pin.
>   - BOARD configuration is used in the program.
>   - For instance if you choose GPIO17, you'll have to enter 11 as the pin's number when configuring the program.
> - Wire the anode (+) to 5Volts.
> - Wire the cathode (-) to GND.

### Run the program
Run `APSecurity.py` from the parent directory `APSecurity`.
> Follow the instructions.
> ![APSecurity Config](/misc/apsec_config.png)
> ![APSecurity](/misc/apsec_run.png)

## Errors handling
### You're trying to run `APSecurity.py` from elsewhere than the `APSecurity` directory
> This error will be raised if you try to run `APSecurity.py` from somehere else than `/APSecurity`.
> ![APSecurity wrong dir config](/misc/err_dir_apsec.png)
