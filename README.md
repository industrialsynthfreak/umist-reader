# umist-reader
Provides a simple class model for UMIST 2012 chemical reactions database.

#Basic Description

The module provides a simple class model for the 2012 edition of "The UMIST Database for Astrochemistry".

###Example
    >> from umist.reader import read
    >> reagents_list, reactions_list = read()
    >>

The data is loaded directly into memory. At the time it weights approximately 400kb.

###Classes
    - Reagent - simple reagent class with no methods
    - Reaction - simple reaction type, containing reagents, products and fits
        provides a single method get_rate(temperature, arg=0.5) to determine a reaction rate coefficient
    - Fit - aux. class containing fit coefficients for Reaction

###Scientific info

    The UMIST db is a set of reactions of formation and destruction of common
    interstellar chemical elements and contains temperatures and coefficients
    for the reaction rate equation.

###UMIST db file description

    line format:
    reaction no.:r_type:R1:R2:P1:P2:P3:P4:NE:[a : b : c:Tl:Tu:ST:ACC:REF]

- [Main db link](http://udfa.ajmarkwick.net/)
- [Link for download](http://udfa.ajmarkwick.net/downloads/RATE12.dist.txt)
- [Full database description](http://arxiv.org/pdf/1212.6362v1.pdf)
- [List of species](http://udfa.ajmarkwick.net/index.php?mode=species)

See docstrings for more detailed info about available classes and methods.
