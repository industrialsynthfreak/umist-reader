"""This file provides classes for UMIST chemical database.
"""

from math import exp


class Reagent:
    """This class provides instances for chemical reagents.

    .. py:attribute:: name

        Name of a molecule/atom/particle.

    """
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name


class Fit:
    """Set of reaction rate coefficients and other parameters for a
    certain temperature band.

    :param t_range: temperature range in K
    :type t_range: tuple of (float, float)
    :param a:
    :type a: float
    :param b:
    :type b: float
    :param c: fit coefficients
    :type c: float
    :param source: source type.
    :type source: str

    *Values:*
        - E - estimated
        - M - measured
        - C - calculated
        - L - from literature

    :param accuracy: fit error.
    :type accuracy: str

    *Values:*
        - A - < 25% error
        - B - < 50% error
        - C - within a factor 2
        - D - within an order of magnitude
        - E - highly uncertain
    """
    def __init__(self, t_range, a, b, c, source, accuracy):
        self.t_range = t_range
        self.a = a
        self.b = b
        self.c = c
        self.source = source
        self.accuracy = accuracy

    def __str__(self):
        return '%.0f--%.0fK' % self.t_range


class Reaction:
    """This class provides instances for chemical reactions.

    .. py:attribute:: id

    Reaction identifier (from the table).

    .. py:attribute:: type

    Reaction type identifier.
            *Values:*
                - AD - Associative Detachment
                - CD - Collisional Dissociation
                - CE - Charge Exchange
                - CP - Cosmic-Ray Proton (CRP)
                - CR - Cosmic-Ray Photon (CRPHOT)
                - DR - Dissociative Recombination
                - IN - Ion-Neutral
                - MN - Mutual Neutralisation
                - NN - Neutral-Neutral
                - PH - Photoprocess
                - RA - Radiative Association
                - REA - Radiative Electron Attachment
                - RR - Radiative Recombination

    .. py:attribute:: reagents

    List of reagents (instances of Reagent).

    .. py:attribute:: products

    List of products (instances of Reagent).

    .. py:attribute:: fits

    List of fit bands with coefficients (instances of Fit).
    """

    def __init__(self):
        self.id = int()
        self.type = str()
        self.reagents = []
        self.products = []
        self.fits = []

    def __str__(self):
        reag = ' + '.join(map(str, self.reagents))
        prod = ' + '.join(map(str, self.products))
        fits = ', '.join(map(str, self.fits))
        s = '%s reaction %s -> %s, Range: %s' % (self.type, reag, prod, fits)
        return s

    def get_rate(self, t, arg=0.5):
        """Returns a reaction rate coefficient (k).

        Common formula:

        .. math::

            k = a * {(T/300)}^b * e^{-c/T} [cm^3 * s^{-1}],

        where a, b, c - coefficients, T - temperature in K.
        For direct ionization (type = CP):

        .. math::

            k = a [s^{-1}],

        For cosmic-ray photoreactions (type = CR):

        .. math::

            k = a * {(T/300)}^b * c/(1 - w) [s^{-1}],

        where a - cosmic-ray ionizaton rate, c - efficiency of the cosmic-ray
        ionization event, w - dust-grain albedo in FUV range (~0.4 - 0.6 at
        150nm).

        For photoprocesses (type = PH):

        .. math::

            k = a * e^{-c/Av} [s^{-1}],

        where a - rate coefficient in the UV radiation field, Av - dust
        extinction at VIS wavelengths, c - scale parameter for VIS -> UV.

        :param t: temperature of medium
        :type t: float
        :param arg: default is 0.5, dust-grain albedo (w) if reaction type
            equals 'CR', dust extinction (Av) if reaction type is 'PH',
            otherwise not used
        :type arg: float

        :return: reaction rate in 1/s for CR, CP, PH types and cm3/s for
            everyone else, returns 0.0f if no available fit data found
        :rtype: float
        """
        fit = next((f for f in self.fits if f.t_range[0] < t < f.t_range[1]))
        if not fit:
            return 0.
        if self.type == 'CP':
            k = fit.a
        elif self.type == 'CR':
            k = fit.a * (t / 300.)**fit.b * fit.c / (1 - arg)
        elif self.type == 'PH':
            k = fit.a * exp(-fit.c / arg)
        else:
            k = fit.a * (t / 300.)**fit.b * exp(-fit.c / t)
        return k
