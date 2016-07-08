"""Reader for the UMIST chem. reactions database.

The module provides a simple class model for the 2012 edition of
"The UMIST Database for Astrochemistry".

**example**
    >> from umist.reader import read
    >> reagents_list, reactions_list = read()
    >>

..note:: The data is loaded directly into memory. At the time it weights
    approximately 400kb.

**classes**
    - Reagent - simple reagent class with no methods
    - Reaction - simple reaction type, containing reagents, products and fits
        provides a single method get_rate() to determine a reaction rate
    - Fit - aux. class containing fit coefficients for Reaction

**scientific info**

    The UMIST db is a set of reactions of formation and destruction of common
    interstellar chemical elements and contains temperatures and coefficients
    for the reaction rate equation.

**UMIST db file description**

    line format:
    reaction no.:r_type:R1:R2:P1:P2:P3:P4:NE:[a : b : c:Tl:Tu:ST:ACC:REF]

Link: http://udfa.ajmarkwick.net/
Link for download: http://udfa.ajmarkwick.net/downloads/RATE12.dist.txt
Full description: http://arxiv.org/pdf/1212.6362v1.pdf
List of species: http://udfa.ajmarkwick.net/index.php?mode=species
"""
