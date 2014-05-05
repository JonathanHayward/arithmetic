#!/usr/bin/env python
# -*- coding: UTF-8 -*-
'''POC for EXACT precision arithmetic that provides arbitrary precision OUTPUT.

A bit of Guido's time machine here: the decimal class provides Decimals that
act like people expect from school. This makes this implementation partly
piggy-backed on the Decimal class, but Numbers are stored with absolute
precision and given decimal place approximation are published on demand.

All of the arbitrary precision libraries I've seen, including Python's, allow
you to specify a given arbitrary but finite precision, and then work with
that precision. This method allows you to work with absolute precision for
any computable number you have the algorithm for (i.e. you can make a
generator that will yield any number of digits in a finite amount of time),
and then on-demand print a decimal approximation. Later on change your mind
and want an extra digit? No problem, just ask for one more digit. Same goes
for twice as many digits.

At present implementation of integers and decimals is obvious. But the
solution is generic to any computable number: override get_places with
something that will get the requested number of decimal places, and you have
an exact way to represent π or e as precisely as any algebraic number. You
need to furnish the algorithm, but you are able to furnish the algorithm
and work with any computable number you have the algorithm for.

This software is available to you under your choice of the GPLv2 or MIT
licenses.'''

import decimal

ADDITION = 0
SUBTRACTION = 1
MULTIPLICATION = 2
DIVISION = 3
EXPONENTIATION = 4

BUFFER_DIGITS = 2

class Number(object):
    '''A representation of a number, possibly broken down into other numbers.

    The integer value, if non-None, is a sign that the Number is simply that
    integer. If it is non-None, there are a first and second operands, each of
    which should be a Number. operation defines which arithmetic operation; at
    present the primitives do not directly parse negative numbers but -n can be
    represented as arithmetic.Number(0) - arithmetic.Number(n).

    As built in, the structure is recursive boiling to integers joined by
    algebraic operations. The class can be subclassed, and get_places()
    overridden, to create any computable number, i.e. any number for which a
    generator can be written that will yield any finite number of digits in
    some finite amount of time.'''

    integer = None
    first = None
    second = None
    operation = None

    def __init__(self, initial_value = None, first = None, second = None,
      operation = None):
        '''Takes as its first non-self argument numeric types or a string.

        In general, the expected user initialization will be with an initial
        value, and initializations provided by the class, which acts as its own
        factory, will leave the initial value as None and populate the first
        and second Number arguments and the operation between them.

        If the first argument is None, it populates a Number composed of two
        other Numbers and the operand joining them.'''

        if initial_value != None:
            as_string = str(initial_value)
            if as_string[0] == '-':
                self.first = Number(0)
                self.second = Number(as_string[1:])
                self.operation = SUBTRACTION
            elif not '.' in as_string:
                self.integer = initial_value
            else:
                integer, fraction = as_string.split('.')
                if integer == '':
                    integer = 0
                self.first = Number((int(integer) * (10 ** len(fraction)) +
                  int(fraction)))
                self.second = Number(10 ** len(fraction))
                self.operation = DIVISION
        else:
            self.first = first
            self.second = second
            self.operation = operation

    def __add__(self, other):
        '''Factory method to produce the sum of two Numbers.'''
        return Number(None, self, other, ADDITION)
    
    def __div__(self, other):
        '''Factory method to produce the quotient of two Numbers.'''
        return Number(None, self, other, DIVISION)

    def __mul__(self, other):
        '''Factory method to produce the product of two Numbers.'''
        return Number(None, self, other, MULTIPLICATION)

    def __pow__(self, other):
        '''Factory method to produce the exponentiation of two Numbers.'''
        return Number(None, self, other, EXPONENTIATION)

    def get_places(self, places):
        '''Creates string wrapping a print-on-demand n decimal place number.'''
        if self.integer != None:
            return str(self.integer) + '.' + '0' * places
        else:
            if self.operation == ADDITION:
                raw = (decimal.Decimal(self.first.get_places(places +
                  BUFFER_DIGITS)) +
                  decimal.Decimal(self.second.get_places(places +
                  BUFFER_DIGITS)))
            elif self.operation == SUBTRACTION:
                raw = (decimal.Decimal(self.first.get_places(places +
                  BUFFER_DIGITS)) -
                  decimal.Decimal(self.second.get_places(places +
                  BUFFER_DIGITS)))
            elif self.operation == MULTIPLICATION:
                raw = (decimal.Decimal(self.first.get_places(places +
                  BUFFER_DIGITS)) *
                  decimal.Decimal(self.second.get_places(places +
                  BUFFER_DIGITS)))
            elif self.operation == DIVISION:
                raw = (decimal.Decimal(self.first.get_places(places +
                  BUFFER_DIGITS)) /
                  decimal.Decimal(self.second.get_places(places +
                  BUFFER_DIGITS)))
            elif self.operation == EXPONENTIATION:
                raw = (decimal.Decimal(self.first.get_places(places +
                  BUFFER_DIGITS)) **
                  decimal.Decimal(self.second.get_places(places +
                  BUFFER_DIGITS)))
            decimal.getcontext().prec = places + BUFFER_DIGITS
            rounded = raw.quantize(decimal.Decimal(str(.1 ** places)),
              rounding=decimal.ROUND_HALF_UP)
            return str(rounded)
