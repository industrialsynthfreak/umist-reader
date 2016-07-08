"""This file provides parser and loader functions.
"""

import logging
import os
import sys
import urllib.request as request

from urllib.error import *

from reaction import Reaction, Reagent, Fit


__version__ = '1.0'

_link = 'http://udfa.ajmarkwick.net/downloads/RATE12.dist.txt'
_path = 'sample.txt'


def read(ignore_exceptions=True):
    """Reads and returns a class based representation of UMIST database.

    ..note:: If _link cannot be reached it will try to parse sample.txt file
        with UMIST 2012 data which should be present in the module dir.

    :param ignore_exceptions: default is True, if True then exceptions will
        be omitted
    :type ignore_exceptions: bool
    :return: list of reactions and list of reagents
    :rtype: tuple of ([Reaction,..,Reaction], [Reagent,..,Reagent])
    """

    def setup_logger():
        logging.basicConfig(filename='umistloader.log')
        l = logging.getLogger()
        l.setLevel(logging.DEBUG)
        return l

    def get_size_of(data):
        size = sum((sys.getsizeof(r) for r in data))
        return size

    def parse_reagent(reagent):
        r = REAGENTS.get(reagent)
        if not r:
            r = Reagent(name=reagent.decode())
            REAGENTS[reagent] = r
        return r

    def parse_reaction(r_data):
        # reaction_no.:r_type:R1:R2:P1:P2:P3:P4:NE:[a : b : c:Tl:Tu:ST:ACC:REF]
        r_data = r_data.split(b':')

        reaction = Reaction()
        reaction.id = int(r_data[0])
        reaction.type = r_data[1].decode()

        for reagent in r_data[2:4]:
            if not reagent:
                continue
            reaction.reagents.append(parse_reagent(reagent))

        for product in r_data[4:8]:
            if not product:
                continue
            reaction.products.append(parse_reagent(product))

        fits = int(r_data[8])
        for f in range(fits):
            i = f * 8
            a = float(r_data[9 + i])
            b = float(r_data[10 + i])
            c = float(r_data[11 + i])
            t0 = float(r_data[12 + i])
            t1 = float(r_data[13 + i])
            st = r_data[14 + i].decode()
            acc = r_data[15 + i].decode()
            # reference = r_data[16 + i]
            f = Fit((t0, t1), a, b, c, st, acc)
            reaction.fits.append(f)
        REACTIONS.append(reaction)

    REACTIONS = list()
    REAGENTS = dict()
    logger = setup_logger()
    try:
        logger.debug('Opening URL: %s' % _link)
        data = request.urlopen(_link)
    except URLError:
        logger.debug('Cannot open URL, using a local db.')
        path = os.path.join(os.getcwd(), _path)
        data = open(path, 'rb')
    for line in data:
        try:
            parse_reaction(line)
        except Exception as err:
            if not ignore_exceptions:
                raise err
    data.close()
    REAGENTS = list(REAGENTS.values())
    logger.debug('Reactions: %d records loaded, %d KB'
                 % (len(REACTIONS), get_size_of(REACTIONS) // 1000))
    logger.debug('Reagents: %d records loaded, %d KB'
                 % (len(REAGENTS), get_size_of(REAGENTS) // 1000))
    return REAGENTS, REACTIONS


if __name__ == "__main__":
    reagents, reactions = read()
