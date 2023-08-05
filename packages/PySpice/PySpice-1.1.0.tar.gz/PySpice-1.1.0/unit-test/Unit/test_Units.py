####################################################################################################
#
# PySpice - A Spice Package for Python
# Copyright (C) 2014 Fabrice Salvaire
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
####################################################################################################

####################################################################################################

import math
import unittest

import numpy as np
from numpy import testing as np_test

####################################################################################################

from PySpice.Unit import *
from PySpice.Unit.SiUnits import *
from PySpice.Unit.Unit import *

import PySpice.Unit.Unit as _Unit

####################################################################################################

class TestUnits(unittest.TestCase):

    ##############################################

    def __init__(self, method_name):

        super().__init__(method_name)

    ##############################################

    # @unittest.skip('')
    def test_unit_prefix(self):

        # for unit_prefix in UnitPrefixMetaclass.prefix_iter():
        #     print(repr(unit_prefix))
        for power in range(-24, 25, 3):
            self.assertEqual(UnitPrefixMetaclass.get(power).power, power)
        self.assertEqual(UnitPrefixMetaclass.get(3).prefix, 'k')
        self.assertEqual(_Unit._zero_power.power, 0)

    ##############################################

    # @unittest.skip('')
    def test_unit_prefix_shortcut(self):

        self.assertEqual(micro(1).power.power, -6)

    ##############################################

    # @unittest.skip('')
    def test_si_derived_unit(self):

        self.assertEqual(SiDerivedUnit().is_anonymous(), True)
        self.assertEqual(bool(SiDerivedUnit()), False)

        si_power1 = SiDerivedUnit('m')
        si_power2 = SiDerivedUnit('s')

        self.assertEqual(bool(si_power1), True)

        self.assertEqual(si_power1, SiDerivedUnit(powers={'m': 1}))
        self.assertEqual(si_power2, SiDerivedUnit(powers={'s': 1}))

        self.assertEqual(si_power1.is_base_unit(), True)
        self.assertEqual((si_power1 * si_power2).is_base_unit(), False)

        self.assertEqual(si_power1.inverse(), SiDerivedUnit(powers={'m': -1}))
        self.assertEqual(si_power1 * si_power2, SiDerivedUnit(powers={'m': 1, 's': 1}))
        self.assertEqual(si_power1 / si_power2, SiDerivedUnit(powers={'m': 1, 's': -1}))

        self.assertEqual(si_power1 * si_power2, SiDerivedUnit('m*s'))
        self.assertEqual(si_power1 / si_power2, SiDerivedUnit('m*s^-1'))

        self.assertEqual(str(si_power1 / si_power2), 'm*s^-1')

    ##############################################

    # @unittest.skip('')
    def test_units(self):

        self.assertEqual(float(kilo(1)), 1000.)
        self.assertEqual(kilo(1), 1000.)

        self.assertTrue(kilo(1))
        self.assertFalse(kilo(0))

        self.assertEqual(kilo(1), kilo(1))
        self.assertNotEqual(kilo(1), kilo(2))

        self.assertEqual(+kilo(1), kilo(1))
        self.assertEqual(-kilo(1), kilo(-1))
        self.assertEqual(kilo(1) + kilo(2), kilo(3))
        self.assertEqual(kilo(2) - kilo(1), kilo(1))
        self.assertEqual(kilo(1) + unit_value(2), kilo(1.002))
        self.assertEqual(kilo(1) + milli(2000), kilo(1.002))

        self.assertEqual(kilo(2) * kilo(3), mega(6))
        self.assertEqual(kilo(2) * 3, kilo(6))
        self.assertEqual(kilo(6) / kilo(3), unit_value(2))
        self.assertEqual(kilo(6) / 3, kilo(2))
        self.assertEqual(3 * kilo(2), kilo(6))

        self.assertEqual(kilo(2)**3, kilo(8))

        self.assertTrue(kilo(1) < kilo(2))
        self.assertTrue(kilo(1) <= kilo(1))
        self.assertTrue(kilo(2) > kilo(1))
        self.assertTrue(kilo(1) >= kilo(1))

        self.assertEqual(kilo(2).inverse(), 1/2000.)

    ##############################################

    # @unittest.skip('')
    def test_float_cast(self):

        self.assertEqual(kilo(1) + 2, 1002.)
        self.assertEqual(2 + kilo(1), 1002.)
        self.assertEqual(kilo(1) - 2, 998.)
        self.assertEqual(2 - kilo(1), -998.)

        self.assertEqual(math.sqrt(kilo(10)), 100)

        array1 = np.array([1., 2., 3.])
        np_test.assert_almost_equal(kilo(1) * array1, array1 * 1000.)
        np_test.assert_almost_equal(array1 * kilo(1), array1 * 1000.)
        np_test.assert_almost_equal(kilo(1) / array1, 1000. / array1)
        np_test.assert_almost_equal(kilo(1) // array1, 1000. // array1)
        np_test.assert_almost_equal(array1 / kilo(1), array1 / 1000.)
        np_test.assert_almost_equal(array1 // kilo(1), array1 // 1000.)

    ##############################################

    # @unittest.skip('')
    def test_unit_str(self):

        self.assertEqual(str(u_kHz(123.4)), '123.4 kHz')
        self.assertEqual(str(u_MHz(123.4)), '123.4 MHz')

        self.assertEqual(kilo(1).str_spice(), '1k')
        self.assertEqual(u_MHz(123.4).str_spice(), '123.4MegHz')

    ##############################################

    def _test_canonise(self, unit, string):

        self.assertEqual(unit.canonise().str_spice(), string)

    ##############################################

    # @unittest.skip('')
    def test_canonisation(self):

        self._test_canonise(unit_value(-.0009), '-900.0u')
        self._test_canonise(unit_value(-.001), '-1.0m')
        self._test_canonise(unit_value(.0009999), '999.9u')
        self._test_canonise(unit_value(.001), '1.0m')
        self._test_canonise(unit_value(.010), '10.0m')
        self._test_canonise(unit_value(.100), '100.0m')
        self._test_canonise(unit_value(.999), '999.0m')
        self._test_canonise(kilo(.0001), '100.0m')
        self._test_canonise(kilo(.001), '1.0')
        self._test_canonise(kilo(.100), '100.0')
        self._test_canonise(kilo(.999), '999.0')
        self._test_canonise(kilo(1), '1k') # Fixme: .0
        self._test_canonise(kilo(1000), '1.0Meg')

    ##############################################

    # @unittest.skip('')
    def test_unit_conversion(self):

        # for units in UnitMetaclass.__hash_map__.values():
        #     print(units, [x for x in units if x.is_default_unit()])

        self.assertEqual(u_V(10) / u_A(2), u_Ω(5))
        self.assertEqual(u_Ω(5) * u_A(2), u_V(10))

        self.assertEqual(u_ms(20).inverse(), u_Hz(50))
        self.assertEqual(u_Hz(50).inverse(), u_ms(20))
        self.assertEqual(u_Hz(50).inverse(), u_ms(20))

    ##############################################

    # @unittest.skip('')
    def test_validation(self):

        self.assertEqual(as_Hz(50), u_Hz(50))
        self.assertEqual(as_Hz(u_kHz(100)), u_kHz(100))
        self.assertEqual(as_Hz(u_kHz(100)).unit_power.power.power, 3) # Fixme: API ...
        with self.assertRaises(UnitError):
            as_Hz(u_A(1))

    ##############################################

    # @unittest.skip('')
    def test_frequency_mixin(self):

        self.assertEqual(Frequency(50).period, u_s(1/50.))
        self.assertEqual(u_Hz(50).period, u_s(1/50.))
        self.assertEqual(Frequency(50).pulsation, 2*math.pi*50)
        self.assertEqual(Period(1/50.).frequency, u_Hz(50.))
        self.assertEqual(u_s(1/50.).frequency, u_Hz(50.))
        self.assertEqual(Period(1/50.).pulsation, 2*math.pi*50)

    ##############################################

    # @unittest.skip('')
    def test_list_ctor(self):

        self.assertEqual(u_mV((1, 2)), [u_mV(x) for x in range(1, 3)])
        self.assertEqual(u_mV([1, 2]), [u_mV(x) for x in range(1, 3)])
        self.assertEqual(u_mV(range(3)), [u_mV(x) for x in range(3)])

    ##############################################

    # @unittest.skip('')
    def test_matmul_syntax(self):

        self.assertEqual(1@u_kΩ, 1000.)
        self.assertEqual(1 @u_kΩ, 1000.)
        self.assertEqual(1 @ u_kΩ, 1000.)
        self.assertEqual((1, 2)@u_mV, u_mV((1, 2)))

####################################################################################################

if __name__ == '__main__':

    unittest.main()
