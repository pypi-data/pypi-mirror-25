# -*- coding: utf-8 -*-

import unittest
from reverpf import reverpf


class TestReversePrintf(unittest.TestCase):
    """ Test Reverse printf"""

    def test_reverse_printf(self):
        fmt = '%02d%03d'
        line = '01002'
        expe = '|01|002|'

        self.assertEqual(reverpf.rever_printf(fmt, line), expe)

    def test_reverse_printf_complex(self):
        fmt = ('%8s%04d%07d%06d%06d%-17s%8s%1d%014.3f%014.3f%014.3f%05.2f%8s'
               '%1s%014.3f%014.3f%014.3f%015.4f%s')
        line = ('1017030809060003235422387102702734358/702       01891961'
                '00000002135.9700000002135.9700000000581.97000.0020170308P'
                '0000002091.0000000002091.0000000000640.9370000000000.0000')
        expe = ('|10170308|0906|0003235|422387|102702|734358/702       '
                '|01891961|0|0000002135.970|0000002135.970|0000000581.970'
                '|00.00|20170308|P|0000002091.000|0000002091.000|'
                '0000000640.937|0000000000.0000||')

        self.assertEqual(reverpf.rever_printf(fmt, line), expe)
