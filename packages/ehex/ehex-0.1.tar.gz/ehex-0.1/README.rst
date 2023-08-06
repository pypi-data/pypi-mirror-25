Traveller eHex
==============

This module implements a Python class for Traveller eHex digits. Traveller (and open-source works such as Cepheus Engine) use a pseudo-hexadecimal notation as a shorthand for expressing numbers and values. These "eHex" numbers are expressed either as ordinary digits or as capital letters. Ranges are:

0-9 (numerical values 0-9)
A-F (numerical values 10-15)
G-H (numerical values 16-17)
J-N (numerical values 18-22)
P-Z (numerical values 23-33)

Requirements
------------

* Python 2.6, 2.7, 3.5, 3.6

Status
------

.. image:: https://travis-ci.org/makhidkarun/ehex.svg?branch=master
    :target: https://travis-ci.org/makhidkarun/ehex

The project code is hosted on GitHub_ as part of the Makhidkarun collection. 

.. _GitHub: https://github.com/makhidkarun/ehex


Usage
-----

ehex() supports the following operations:

* Create
* Comparison
* Addition
* Subtraction

>>> from ehex.ehex import ehex
>>> x = ehex()      # Creates ehex variable, value 0/'0'
>>> x = ehex(1)     # Creates ehex variable, value 1/'1'
>>> x = ehex('D')   # Creates ehex variable, value 13/'D'
>>> x
D
>>> int(x)
13
>>> str(x)
'D'
>>> x == 13
True
>>> x == 'D'
True
>>> x > 9
True
>>> x < 'F'
True
>>> x + 'A'
P
>>> int(x + 'A')
23
>>> x - 2
B
>>> x - '2'
B
>>> x - 35
Traceback (most recent call last):
  File "<input>", line 1, in <module>
    x - 35
  File "ehex.py", line 146, in __sub__
    return ehex(self._value - other)
  File "ehex.py", line 31, in __init__
    raise ValueError('Invalid value {}'.format(value))
ValueError: Invalid value -22
