# bprint

Beautiful print for Python.

## Why?

[Python's `pprint`](https://docs.python.org/3/library/pprint.html) is
supposed to be a "Data pretty printer" and claims the following:

> provides a capability to "pretty-print" arbitrary Python data structures

This is simply not true, because it will choke on "arbitrary Python data".

It's not even good at pretty-printing, since the indentation often goes
way too far to the right, and in general makes things unreadable.

`bprint` aims at solving both of these issues.

## How?

Thanks to Python's dynamic nature, we can query the attributes of *any*
object, and thus beautifully print them, even if they don't define
[`__str__`](https://docs.python.org/3/reference/datamodel.html#object.__str__)
(which is in fact not queried at all for custom classes).

Installation is done with `pip install beauty-print`.

## What?

`bprint` will help you beautifully print your objects, and is also easily
customizable, with a lot of freedom.

The `pip` package is called
[`beauty-print`](https://pypi.org/project/beauty-print/) because `bprint`
was already taken, unfortunately.

## When?

During one of the many moments when I'm procrastinating. You can install
it any time you want though!

## Where?

In Python 3.6 and above, and PyPi as
[`beauty-print`](https://pypi.org/project/beauty-print/).

## How much?

Free, as in beer and freedom!

## Who?

[Lonami](https://lonami.dev) is the primary author and thanks also
to [udf](https://github.com/udf), but more contributors are welcome!
