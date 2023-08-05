==============================
 Using :mod:`zope.exceptions`
==============================

This module extends the standard library's :mod:`traceback` module, allowing
application code to add additional information to the formatted tracebacks
using specially-named variables in the scope of a given frame.

We will use examples of a rendering function that's meant to produce
some output given a template and a set of options. But this rendering
function is quite broken and produces a useless exception, so when we
call it we'd like to be able to provide some more contextual information.

.. doctest::

   >>> import sys
   >>> def render(source, options):
   ...    raise Exception("Failed to render")

Annotating Application Code
===========================

:py:data:`__traceback_info__`
-----------------------------

This variable can only be defined at local scope.  It will be converted to a
string when added to the formatted traceback.

.. doctest::

   >>> def render_w_info(template_file, options):
   ...     with open(template_file) as f:
   ...         source = f.read()
   ...     __traceback_info__ = '%s\n\n%s' % (template_file, source)
   ...     render(source, options)


This is convenient for quickly adding context information in an
unstructured way, especially if you already have a string, or an
object with a custom ``__str__`` or ``__repr__`` that provides the
information you need (tuples of multiple such items also work well).
However, if you need to format a string to produce readable
information, as in the example above, this may have an undesirable
runtime cost because it is calculated even when no traceback is
formatted. For such cases, ``__traceback_supplement__`` may be helpful.

:py:data:`__traceback_supplement__`
-----------------------------------

This variable can be defined either at either local or global (module)
scope. Unlike ``__traceback__info__`` this is structured data. It must
consist of a sequence containing a function and the arguments to pass
to that function. At runtime, only if a traceback needs to be
formatted will the function be called, with the arguments, to produce
a *supplement object*. Because the construction of the object is
delayed until needed, this can be a less expensive way to produce
lots of useful information with minimal runtime overhead.

The formatting functions treat the resulting supplement object as if
it supports the
:py:class:`~zope.exceptions.interfaces.ITracebackSupplement`
interface. The various attributes (all optional) of that interface
will be used to add structured information to the formatted traceback.

For example, assuming your code renders a template:

.. doctest::

   >>> import os
   >>> class Supplement(object):
   ...     def __init__(self, template_file, options):
   ...         self.source_url = 'file://%s' % os.path.abspath(template_file)
   ...         self.options = options
   ...         self.expression = 'an expression'
   ...     def getInfo(self):
   ...         return "Options: " + str(self.options)
   >>> def render_w_supplement(template_file, options):
   ...     with open(template_file) as f:
   ...         source = f.read()
   ...     __traceback_supplement__ = Supplement, template_file, options
   ...     render(source, options)

Here, the filename and options of the template will be rendered as part of
the traceback.

.. note:: If there is an exception calling the constructor function,
          no supplement will be formatted, and (by default) the
          exception will be printed on ``sys.stderr``.


API Functions
=============
Three API functions support these features when formatting Python
exceptions and their associated tracebacks:

:py:func:`~zope.exceptions.exceptionformatter.format_exception`
---------------------------------------------------------------

Use this API to format an exception and traceback as a list of strings, using
the special annotations.  E.g.:

.. doctest::


   >>> from zope.exceptions import format_exception
   >>> try:
   ...     render_w_info('docs/narr.rst', {})
   ... except:
   ...     t, v, tb = sys.exc_info()
   ...     report = format_exception(t, v, tb)
   ...     del tb # avoid a leak
   ...     # Now do something with report, e.g., send e-mail.
   >>> print('\n'.join(report))
   Traceback (most recent call last):
   <BLANKLINE>
     Module <doctest default[1]>, line 2, in <module>
       render_w_info('docs/narr.rst', {})
   <BLANKLINE>
     Module <doctest default[0]>, line 5, in render_w_info
      - __traceback_info__: docs/narr.rst
   ...


:py:func:`~zope.exceptions.exceptionformatter.print_exception`
--------------------------------------------------------------

Use this API to write the formated exception and traceback to a file-like
object, using the special annotations.  E.g.:

.. doctest::

   >>> from zope.exceptions import print_exception
   >>> try:
   ...     render_w_supplement('docs/narr.rst', {})
   ... except:
   ...     t, v, tb = sys.exc_info()
   ...     print_exception(t, v, tb, file=sys.stdout)
   ...     del tb # avoid a leak
   Traceback (most recent call last):
     File "<doctest default[1]>", line 2, in <module>
       render_w_supplement('docs/narr.rst', {})
     File "<doctest default[2]>", line 5, in render_w_supplement
      - file:///...
      - Expression: an expression
   Options: {}
     File "<doctest default[1]>", line 2, in render
       render_w_supplement('docs/narr.rst', {})
   Exception: Failed to render

:py:func:`~zope.exceptions.exceptionformatter.extract_stack`
------------------------------------------------------------

Use this API to format just the traceback as a list of string,s using the
special annotations.  E.g.:

.. doctest::

   >>> import sys
   >>> from zope.exceptions import extract_stack
   >>> try:
   ...     raise ValueError('demo')
   ... except:
   ...     for line in extract_stack(sys.exc_info()[2].tb_frame):
   ...         pass # do something with each line
