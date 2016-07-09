"""Reader for the UMIST chem. reactions database.

:Authors: Violet Red
:Version: 1.0 2016/07/08

The module provides a simple class model for the 2012 edition of the
*UMIST Database for Astrochemistry*.

**Example:**
::

    from umist.reader import read
    reagents, reactions = read()
    print(reactions[0].get_rate(300))

.. note:: The data is loaded directly into memory. At the time it weights
          approximately 400 KB.

**Basic Info:**

    The UMIST db is a set of reactions of formation and destruction of common
    chemical elements in the interstellar medium, such as molecular clouds.
    It contains temperatures and coefficients for the reaction rate equation.

**Source data format description:**

    Line format:
    `reaction no.:r_type:R1:R2:P1:P2:P3:P4:NE:[a : b : c:Tl:Tu:ST:ACC:REF]`

.. _Main link: http://udfa.ajmarkwick.net/
.. _Download link: http://udfa.ajmarkwick.net/downloads/RATE12.dist.txt
.. _Full description: http://arxiv.org/pdf/1212.6362v1.pdf
.. _List of species: http://udfa.ajmarkwick.net/index.php?mode=species
"""

__version__ = '1.0'

import umist.reaction as reaction
import umist.reader as reader
