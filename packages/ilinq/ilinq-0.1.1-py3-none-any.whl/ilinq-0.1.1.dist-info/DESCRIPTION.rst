ILinq
=====

.. figure:: docs/images/symbol.png
   :alt: Symbol of ILinq

   Symbol of ILinq

This project provides the module like linq of C# for Python.

How To Install
--------------

::

    $ python setup.py install

For developers, we enter

::

    $ pip install -r extra_require.txt

First Example
-------------

::

    #!/usr/bin/env python
    # -*- coding: utf-8 -*-

    from ilinq.ilinq import Linq


    def is_prime(n):
        if n < 2:
            return False

        for j in range(2, n):
            if n % j == 0:
                return False

        return True


    if __name__ == '__main__':
        print(
            Linq(range(10**4))
            .last(is_prime))
        # => 9973

LICENSE
-------

Apache 2.0


