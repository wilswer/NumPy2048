# NumPy 2048
![Tests](https://github.com/wilswer/NumPy2048/actions/workflows/tests.yml/badge.svg)
```
__/\\\\\_____/\\\____________________________________/\\\\\\\\\\\\\_________________
 _\/\\\\\\___\/\\\___________________________________\/\\\/////////\\\_______________
  _\/\\\/\\\__\/\\\___________________________________\/\\\_______\/\\\____/\\\__/\\\_
   _\/\\\//\\\_\/\\\__/\\\____/\\\____/\\\\\__/\\\\\___\/\\\\\\\\\\\\\/____\//\\\/\\\__
    _\/\\\\//\\\\/\\\_\/\\\___\/\\\__/\\\///\\\\\///\\\_\/\\\/////////_______\//\\\\\___
     _\/\\\_\//\\\/\\\_\/\\\___\/\\\_\/\\\_\//\\\__\/\\\_\/\\\_________________\//\\\____
      _\/\\\__\//\\\\\\_\/\\\___\/\\\_\/\\\__\/\\\__\/\\\_\/\\\______________/\\_/\\\_____
       _\/\\\___\//\\\\\_\//\\\\\\\\\__\/\\\__\/\\\__\/\\\_\/\\\_____________\//\\\\/______
        _\///_____\/////___\/////////___\///___\///___\///__\///_______________\////________
         __________/\\\\\\\\\_________/\\\\\\\_______________/\\\________/\\\\\\\\\__________
          ________/\\\///////\\\_____/\\\/////\\\___________/\\\\\______/\\\///////\\\________
           _______\///______\//\\\___/\\\____\//\\\________/\\\/\\\_____\/\\\_____\/\\\________
            _________________/\\\/___\/\\\_____\/\\\______/\\\/\/\\\_____\///\\\\\\\\\/_________
             ______________/\\\//_____\/\\\_____\/\\\____/\\\/__\/\\\______/\\\///////\\\________
              ___________/\\\//________\/\\\_____\/\\\__/\\\\\\\\\\\\\\\\__/\\\______\//\\\_______
               _________/\\\/___________\//\\\____/\\\__\///////////\\\//__\//\\\______/\\\________
                ________/\\\\\\\\\\\\\\\__\///\\\\\\\/_____________\/\\\_____\///\\\\\\\\\/_________
                 _______\///////////////_____\///////_______________\///________\/////////___________
```
## Intro
A terminal-based NumPy implementation of the game "2048" originally created by Gabriele Cirulli. Frontend developed using curses.

## Requirements
This software is tested on Python3.6 or higher.
Install requirements using pip or your favorite Python package manager.
These packages are required for executing the code in this repository:
- `numpy`
- For windows systems: `windows-curses`

## Installation
To install this package, run: `pip install git+https://github.com/wilswer/NumPy2048.git@main`.

## Usage
Either clone this repository and install the dependencies and then:
- Basic usage: `python main.py` launches the game in "interactive" mode.
- Additional arguments can be passed, use `python main.py --help` to view them.
or install this package according to the installation instructions, then:
- Basic usage: `cli-2048` launches the game in "interactive" mode.
- Additional arguments can be passed, use `cli-2048 --help` to view them.
