"""This file provides tests for umist database loader.

This one not only tests code but also validates database.
"""

import unittest

from umist.reader import Reader


class Test(unittest.TestCase):
    _r_types = {'AD', 'CD', 'CE', 'CP', 'CR', 'DR', 'IN', 'MN', 'NN', 'PH',
                'RA', 'REA', 'RR'}
    _sources = {'E', 'M', 'C', 'L', 'D', ''}
    _accuracies = {'A', 'B', 'C', 'D', 'E', ''}

    def test_reader_function(self):
        try:
            reagents, reactions = Reader.read()
        except Exception as err:
            self.fail(
                "read() function raised an exception and cannot continue: %s"
                % str(err))
        self.assertTrue(reagents, msg='No reagents loaded from a file.')
        self.assertTrue(reactions, msg='No reactions loaded from a file.')
        for r in reactions:
            print('R. #%d' % r.id)
            self.assertIn(r.type, self._r_types, msg='Wrong reaction type.')
            self.assertTrue(r.reagents, msg='No reagents found.')
            self.assertTrue(r.products, msg='No products found.')
            self.assertTrue(r.fits, msg='No fits found.')
            for f in r.fits:
                self.assertIn(f.source, self._sources, msg='Wrong source type.')
                self.assertIn(f.accuracy, self._accuracies,
                              msg='Wrong accuracy flag.')
                self.assertGreater(f.t_range[0], 0.,
                                   msg='Wrong left temperature value.')
        self.assertGreater(reactions[0].get_rate(200.), -1,
                           msg='Wrong rate value')

if __name__ == "__main__":
    unittest.main()
