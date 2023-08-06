# amdfans

Command-line program for setting AMD GPU fan speeds

Requires root permissions

## System requirements
- Python 3
- Linux
- [AMDGPU-PRO Driver for Linux](https://support.amd.com/en-us/kb-articles/Pages/AMD-Radeon-GPU-PRO-Linux-Beta-Driver–Release-Notes.aspx)

## Installation

### Ubuntu
    sudo apt update
    sudo apt install -y python python-pip python3 python3-pip
    sudo pip3 install --upgrade amdfans

## Options
    Usage: amdfans [OPTIONS] PERCENTAGE

    Options:
      -v, --verbose  Enable verbose logging.
      -q, --quiet    Disable stdout logging.
      -h, --help     Show this message and exit.

## Example
    $ sudo amdfans 70
    card1 manual fan settings enabled
    card1 fan speed set to 70%
    card0 manual fan settings enabled
    card0 fan speed set to 70%

    Exiting.