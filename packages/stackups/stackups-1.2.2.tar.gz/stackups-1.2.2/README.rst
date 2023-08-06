Info about stackups.py
======================

.. contents::
   :local:
   
Introduction
------------

This program's purpose is to allow engineers and designers to verify clearances
between moving or stationary parts within a machine.  This check becomes more
critical when one recognizes that all the features of machined parts are
machined according to an allowable tolerance range.  These accumulated
tolerances can close operating gaps and thus result in malfunctioning
machinery.

It should be obvious that all the features of all the parts will not be at the
maximum of their tolerance range, nor at their minimum.  This program, in
addition to calculating gaps based on max/min tolerances, will also calculate
clearances based on the probability of features being at some median size.
This probability calculation is used by a majority of the major manufacturers
today (six sigma).

Cost
----

This program is "donationware", meaning your good grace is needed to support
this project.  Recommended cost: $25 per seat.  You may pay for this program
per the link set up on the website `<http://newconceptzdesign.com/>`_.
(See the license agreement for more information.)


How it works
------------

This program works within a Python [2] command prompt window (or more 
preferably, in an ipython command prompt window).  This program works very 
similarly to Python's standard "list" command, which is a basic, fundamental
feature of Python.  Therefore this program is easy to learn.  YOU DO NOT HAVE
TO KNOW THE PYTHON LANGUAGE TO USE THIS PROGRAM!

The fundamental element used in this program is an obect called a "Stackunit".
A Stackunit is composed of a dimension, a tolerance, the name assigned to that
dimension (e.g., END TO SHOULDER), and the part no. to which that dimension
pertains.  A group of Stackunit objects form a "Stack" object.  The Stack 
object not only contains Stackunit objects, but also has wrapped within it
computer code which carries out analysis and summation of the encompassed
Stackunit objects.  Finally, a group of Stack objects can be grouped together
in what's called a "Stacks" object.  If a dimenion or tolerance changes for one
Stackunit, then if that same Stackunit is used in other Stack objects, it will 
be automatically updated in all the Stack objects.

During the course of building stacks, editing is very common.  Editing involves
updating dimensions, inserting new dimensions, rearranging dimensions, etc.
This program is designed to facilitate that editing.

Tutorial
--------

If you have never done a stackup (i.e., by hand), no problem.  A tutorial has
been created to show you how to do this, along with showing you how to use this
program.  It can be found at `<http://newconceptzdesign.com/>`_.


---------------------------------------------------------------------

.. rubric:: Footnotes

.. [1] Recommended Python engine on which to run this program (it's free):
    `Anaconda <http://www.continuum.io/downloads/>`_

.. [2] What is Python?  2 min 50 secs to 4 min 10 secs of this video from
    Google describes Python: `<http://www.youtube.com/watch?v=tKTZoB2Vjuk>`_
    (An old version of Python, version 2.4, was used in this class.  As 
    concerns beginners, only two main differences exists between version 2.4
    and the newer 3.x version: 1. for division in 2.4, make sure that you use a
    decimal point in at least one of the numbers.  For example, in 2.4, 
    3/2 = 1, and 3/2.0 = 1.5.  That is, in 2.4, 3/2 is an integer division.  
    2. In version 3.x, a parenthesis is needed for the print command.  That is,
    `print('something to print')` instead of `print 'something to print'`.)