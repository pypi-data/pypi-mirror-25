=========
 @public
=========

This is a very simple decorator and function which populates a module's
``__all__`` and optionally the module globals.  This provides both a
pure-Python implementation and an optional C implementation.


Background
==========

``__all__`` is great.  It has both a functional and a documentation purpose.

The functional purpose is that it `directly controls`_ which module names are
imported by the ``from <module> import *`` statement.  In the absence of an
``__all__``, when this statement is executed, every name in ``<module>`` that
does not start with an underscore will be imported.  This often leads to
importing too many names into the module.  That's a good enough reason not to
use ``from <module> import *`` with modules that don't have an ``__all__``.

In the presence of an ``__all__``, only the names specified in this list are
imported by the ``from <module> import *`` statement.  This in essence gives
the ``<module>`` author a way to explicitly state which names are for public
consumption.

And that's the second purpose of ``__all__``; it serves as module
documentation, explicitly naming the public objects it wants to export.  You
can print a module's ``__all__`` and get an explicit declaration of its public
API.


The problem
===========

``__all__`` has two problems.

First, it separates the declaration of a name's public export semantics from
the implementation of that name.  Usually the ``__all__`` is put at the top of
the module, although this isn't required, and in some cases it's `actively
prohibited`_.  So when you're looking at the definition of a function or class
in a module, you have to search for the ``__all__`` definition to know whether
the function or class is intended for public consumption.

This leads to the second problem, which is that it's too easy for the
``__all__`` to get `out of sync`_ with the module's contents.  Often a
function or class is renamed, removed, or added without the ``__all__`` being
updated.  Then it's difficult to know what the module author's intent was, and
it can lead to an exception when a string appearing in ``__all__`` doesn't
match an existing name in the module.  Some tools like Sphinx_ will complain
when names appear in ``__all__`` don't appear in the module.  All of this
points to the root problem; it should be easy to keep ``__all__`` in sync!


The solution
============

This package provides a way to declare a name's *publicness* right at the
point of its declaration, and to infer the name to export from that
definition.  In this way, a module's author never explicitly sets the
``__all__`` so there's no way for it to get out of sync.

This package, and Python `issue 26632`_, propose just such a solution, in the
form of a ``public`` builtin that can be used as either a decorator, or a
callable.

You'll usually use this as a decorator, for example::

    @public
    def foo():
        pass

or::

    @public
    class Bar:
        pass

If you were to print the ``__all__`` after both of those code snippets, you'd
see::

    >>> print(__all__)
    ['foo', 'Bar']

Note that you do not need to initialize ``__all__`` in the module, since
``public`` will do it for you.  Of course, if your module *already* has an
``__all__``, it will just append new names to the existing list.

The requirements to use the ``@public`` decorator are simple: the decorated
thing must have a ``__name__`` attribute.  Since you'll overwhelmingly use it
to decorate functions and classes, this will always be the case.

There's one other common use case that isn't covered by the ``@public``
decorator.  Sometimes you want to declare simple constants or instances as
publicly available.  You can't use the ``@public`` decorator for two reasons:
constants don't have a ``__name__`` and Python's syntax doesn't allow you to
decorate such constructs.

To solve this use case, ``public`` is also a callable function accepting
keyword arguments.  An example makes this obvious::

    public(SEVEN=7)
    public(a_bar=Bar())

Now if you print the module's ``__all__`` you'll see::

    >>> print(__all__)
    ['foo', 'Bar', 'SEVEN', 'a_bar']

and as should be obvious, the module contains name bindings for these
constants::

    >>> print(SEVEN)
    7
    >>> print(a_bar)
    <__main__.Bar object at ...>

**Note:** While you can use ``public()`` with multiple keyword arguments in a
single call, the order of the resulting ``__all__`` entries is undefined in
Python versions earlier than 3.6, due to indeterminate dictionary sort order.
If order matters to you, call ``public()`` multiple times each with a single
keyword argument.


Extension module alternative
============================

This package actually provides both a pure Python implementation and an
optional C extension module.  When you do the typical import, e.g.::

    >>> from public import public

you'll get the most efficient version available.  Since the C implementation
is entirely optional (albeit moderately more efficient), you'll get that if it
was built.  If not, you'll get the pure-Python implementation.

For all intents and purposes, the two versions are identical.  You generally
won't notice the difference.  If for some reason you want to force the
pure-Python version just do::

    >>> from public import py_public as public


Making @public a built-in
=========================

It can get rather tedious if you have to add the above import in every module
where you want to use it.  What if you could put ``public`` into Python's
builtins_?  Then it would be available in all your code for free::

    >>> from public import install
    >>> install()

and now you can just use ``@public`` without having to import anything in your
other modules.

Again by default, this installs the most efficient version it can find, but if
you wanted to force install the pure-Python version, just do::

    >>> from public import py_install
    >>> py_install()


Installation
============

Use the normal ``setup.py install`` or ``pip install`` commands to install
this library.  By default, the C extension is **not** built, in order to make
it more portable to environments without a C compiler.  If you want a version
that's a little more efficient than the pure-Python implementation, set the
environment variable ``ATPUBLIC_BUILD_EXTENSION=1`` when you build/install the
module.


Caveats
=======

There are some important usage restrictions you should be aware of:

* Only use ``@public`` on top-level object.  Specifically, don't try to use
  ``@public`` on a class method name.  While the declaration won't fail,
  you will get an exception when you attempt to ``from <module> import *``
  because the name pulled from ``__all__`` won't be in the module's globals.
* If you explicitly set ``__all__`` in your module, be sure to set it to a
  list.  Some style guides require ``__all__`` to be a tuple, but since that's
  immutable, as soon as ``@public`` tries to append to it, you will get an
  exception.  Best practice is to not set ``__all__`` explicitly; let
  ``@public`` do it!
* If you still want ``__all__`` to be immutable, put the following at the
  bottom of your module::

    __all__ = tuple(__all__)


Alternatives
============

This isn't a unique approach to ``@public``.  Other_ implementations_ do
exist.  There are some subtle differences between this package and those
others.  This package:

* uses keyword arguments to map names which don't have an ``__name__``
  attribute;
* can be used to bind names and values into a module's globals;
* provides both C and Python implementations;
* can optionally put ``public`` in builtins.


Author
======

``public`` is Copyright (C) 2016-2017 Barry Warsaw

Contact Barry:

* barry@python.org
* @pumpichank on Twitter
* @warsaw on GitHub and GitLab

Licensed under the terms of the Apache License 2.0.  See LICENSE.txt for
details.


Project details
===============

* Project home: https://gitlab.com/warsaw/public
* Report bugs at: https://gitlab.com/warsaw/public/issues
* Fork the code: https://gitlab.com/warsaw/public.git
* Documentation: http://public.readthedocs.io/en/latest/
* PyPI: https://pypi.python.org/pypi/atpublic


NEWS
====

.. toctree::
   :maxdepth: 2

   NEWS



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`


.. _`issue 26632`: http://bugs.python.org/issue26632
.. _builtins: https://docs.python.org/3/library/builtins.html
.. _`directly controls`: https://docs.python.org/3/tutorial/modules.html#importing-from-a-package
.. _`actively prohibited`: http://pep8.readthedocs.io/en/latest/intro.html?highlight=e402#error-codes
.. _`out of sync`: http://bugs.python.org/issue23883
.. _Other: https://pypi.python.org/pypi/public
.. _implementations: http://bugs.python.org/issue22247#msg225637
.. _Sphinx: http://www.sphinx-doc.org/en/stable/
