#!/usr/bin/env python

"""
  Author:  Yeison Cardona --<yeisoneng@gmail.com>
  Purpose:
  Created: 09/19/2017
"""

import time

import RPi.GPIO as GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)

#OUT = 23, 17, 27, 24
OUT = 23, 24, 17, 27
#OUT = 17, 27, 23, 24
#OUT = 23, 27, 24, 17
#OUT = 23, 17, 27, 3

[GPIO.setup(pin, GPIO.OUT, initial=GPIO.HIGH) for pin in OUT]



steps = (
    [False, True, True, False],
    [False, True, False, True],
    [True, False, False, True],
    [True, False, True, False],
)

STEP = 0

#----------------------------------------------------------------------
def step(s):
    """"""
    global STEP
    STEP += s

    if STEP > len(steps) - 1:
        STEP = 0
    elif STEP < 0:
        STEP = len(steps) - 1

    #print(STEP, steps[STEP])
    [GPIO.output(*out) for out in zip(OUT, steps[STEP])]
    time.sleep(10/1000)
    [GPIO.output(*out) for out in zip(OUT, [False, False, False, False])]


#----------------------------------------------------------------------
def cw():
    """"""
    step(1)


#----------------------------------------------------------------------
def ccw():
    """"""
    step(-1)





while True:
    cw()
    #time.sleep(10/1000)
