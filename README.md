arithmetic
==========

## ABSOLUTE Precision Arithmetic With Arbitrary Precision OUTPUT

Arbitrary precision arithmetic libraries are old hat. *But this is
different.*

This is a proof of concept, and only a proof of concept, for an approach
that will allow *exact* precision arithmetic for any computable
number. Want the square root of three to three decimal places? Realize later-on
that the user wants twenty decimal places instead, or that the number of
decimal places is dynamic? No need to refactor the original calculation; just
ask the stored square root of three for twenty, or a user-supplied number, of
decimal places. Have algorithms to calculate *e* and π? Add
*e* and π together, and don't worry until later about how many
decimal places you want for *e* + π. Numbers are stored with exact
precision and decimal approximations are print-on-demand.
