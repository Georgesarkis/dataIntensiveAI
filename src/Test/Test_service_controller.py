import unittest
from pandas.util.testing import assert_frame_equal
import numpy as np
import pandas as pd

import sys

sys.path.insert(1, '../service')

from ServiceController import validate,CreateDataFrame,featureEngStringTOFloat

"""
    @author @name
"""
class Test_model_evaluate(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        '''Once, before the test suite is executed'''
        pass

    @classmethod
    def tearDownClass(cls):
        '''Once, after the test suite is executed'''
        pass

    """
        @author @name
    """
    def setUp(self):
        '''Before every single test'''

        self.data = ["Fiat","TALENTO",2016,560,"Manuell","Diesel"]

        cars = {'brand': ['Fiat'],
                'model': ["TALENTO"],
                'model_year': [2016],
                "mileage" : [560],
                'gear': ["Manuell"],
                'fuel': ["Diesel"]
                }

        self.df = pd.DataFrame(cars)
        pass

    def tearDown(self):
        '''After every single test'''
        pass

    """
        @author @name
    """
    def test_validate_True(self):
        data1 = ["Fiat","TALENTO",2016,560,"Manuell","Diesel"]
        self.assertTrue(validate(data1))

    """
        @author @name
    """
    def test_validate_False(self):
        data1 = ["TALENTO",2016,560,"Manuell","Diesel"]
        self.assertFalse(validate(data1))

    """
        @author @name
    """
    def test_CreateDataFrame(self):
        datafreme = CreateDataFrame(self.data)
        assert_frame_equal(datafreme, self.df, check_dtype=False, check_like=True)

    """
        @author @name
    """
    def test_featureEngStringTOFloat(self):
        data1 = ["Fiat","TALENTO","2016","560","Manuell","Diesel"]
        data1 = featureEngStringTOFloat(data1)
        self.assertEqual(data1,self.data)

if __name__ == '__main__':
    unittest.main()
