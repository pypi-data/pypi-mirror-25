Goals
=====

A collection of curses utils for performing simple UI tasks. Currently
this includes a simple console and a menu with vi-like bindings.

Installation
============

Requires python 3.

``pip3 install curses-util`` should do the trick, or else
``python setup.py install`` from source.

Usage
=====

SimpleConsole
-------------

A dirt simple console based interface.

    ::

	from curses_util import SimpleConsole

	def oninput(console, msg):
	    if msg == '/exit':
	    console.exit()

	    console.log("Received {0} as input".format(msg))

	console = SimpleConsole(oninput)
	console.log("Welcome from the main thread.")

Menu
----

This can be used to vend a collection of items which the user may then
select one or more of. Navigation can be performed using standard vi
bindings (count operands are also supported) or via the arrow keys.
Multiple items can be selected if the user presses m over each of the
items they wish to select and then presses enter.

    ::

	import curses_util

	menu = curses_util.Menu()

	items = range(100)
	selected = menu.vend(items, display=lambda x: str(x))

	print("The following item was selected: " + selected)

	selected = menu.multi_vend(items, display=str)
	print("The following items were selected: \n")
	print("\n".join(selected), "\n")

Bugs, etc..
===========

If you bother to read the code and invariably feel the need to abuse the
person who wrote it, know that such sentiments will be happily received
at r.vaiya@gmail.com.
