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

## Installation

### Motion Sensor
#### Wire the motion sensor to the RPi:
> - Wire the motion sensor's output pin to any of your RPi's GPIO pin.
>   - BOARD configuration is used in the program.
>   - For instance if you choose GPIO17, you'll have to enter 11 as the pin's number when running `config.py`
> Wire the anode (+) to 5Volts.
> Wire the cathode (-) to GND.

