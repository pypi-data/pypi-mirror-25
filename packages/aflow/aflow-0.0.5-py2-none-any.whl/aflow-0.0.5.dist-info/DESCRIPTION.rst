|Build Status| |Coverage Status|

``AFLOW`` Python API
====================

Python API wrapping the AFLUX API language for AFLOW library. *Note:*
This is not an official repo of the AFLOW consortium and is not
maintained by them. `API
Documentation <https://rosenbrockc.github.io/aflow/>`__

Quickstart
----------

Install ``aflow`` from the python package index:

::

    pip install aflow

Open an ipython notebook or terminal and execute the query from the
paper:

.. code:: python

    from aflow import *

    result = search(batch_size=20
            ).select(K.agl_thermal_conductivity_300K
            ).filter(K.Egap > 6).orderby(K.agl_thermal_conductivity_300K, True)

    # Now, you can just iterate over the results.
    for entry in result:
        print(entry.Egap)

``aflow`` supports lazy evaluation. This means that if you didn't ask
for a particular property during the initial query, you can just ask for
it later and the request will happen transparently in the background.

.. |Build Status| image:: https://travis-ci.org/rosenbrockc/aflow.svg?branch=master
   :target: https://travis-ci.org/rosenbrockc/aflow
.. |Coverage Status| image:: https://coveralls.io/repos/github/rosenbrockc/aflow/badge.svg?branch=master
   :target: https://coveralls.io/github/rosenbrockc/aflow?branch=master


