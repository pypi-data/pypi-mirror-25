=======================
 dialogue.multi-method
=======================

A small library to provide multi-methods.  All functions are in the
`dialogue.multi_method` package.

To create a multi-method, create a dispatch function, that takes the
arguments and returns a hashable value, that is used to dispatch on.
Use the `@multi` function annotation to annotate the function.

For each value of the dispatch function that you want to be handled
differently, create a method with that dispatch value.

You can define a method with no dispatch value, that becomes the
default method if no other method is defined for a dispatch value.


An example::

  @multi
  def number(x):
    return x


  @method(number, 1)
  def number_one(x):
    return 'one'


  @method(number)
  def number_other(x):
    return "not one, but "+ str(c)


  assert number(1) == 'one'
  assert number(0) == 'not one, but 0'


The dispatch function is available, e.g. for testing::

  assert dispatch_fn(number)('x') == 'x'
