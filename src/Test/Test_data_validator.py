import unittest
from pandas.util.testing import assert_frame_equal
import numpy as np
import pandas as pd
import sys
sys.path.insert(1, '../scripts')

from data_validator import validate_data,validate_data_user

"""
    @author @name
"""
class TestData_validator(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        '''Once, before the test suite is executed'''
        pass

    @classmethod
    def tearDownClass(cls):
        '''Once, after the test suite is executed'''
        pass

    def setUp(self):
        '''Before every single test'''
        pass

    def tearDown(self):
        '''After every single test'''
        pass

    """
        @author @name
    """
    def test_validate_data_False(self):
        cars = {
                        'brand': ['Saab', 'Volvo', 'Renault'],
                        'gear': ["Manuell", "Automat", "Manuell"],
                        'model': ["9-5", "S80", "CLIO"],
                        'price': [25000, 85000, 143900],
                        'fuel': ["Diesel", "Diesel", "Bensin"],
                        'mileage': ["30 000 - 34 999","18 000","140"],
                        'hp': ["149","163","89"],
                        'type': ["Kombi","Sedan","Halvkombi"],
                        'geo': ["Simrishamn","Helsingborg","Göteborg, Hisingen"],
                        'model_year': [2006.0,2011.0,2018.0]
                        }
        df = pd.DataFrame(cars)
        self.assertFalse(validate_data(df))

    """
        @author @name
    """
    def test_validate_data_True(self):
        cars = {
                        'brand': ['Saab', 'Volvo', 'Renault'],
                        'gear': ["Manuell", "Automat", "Manuell"],
                        'model': ["9-5", "S80", "CLIO"],
                        'price': [25000, 85000, 143900],
                        'fuel': ["Diesel", "Diesel", "Bensin"],
                        'mileage': [30000.0,18000.0,140.0],
                        'hp': [149.0,163.0,89.0],
                        'type': ["Kombi","Sedan","Halvkombi"],
                        'geo': ["Simrishamn","Helsingborg","Göteborg, Hisingen"],
                        'model_year': [2006.0,2011.0,2018.0]
                        }
        df = pd.DataFrame(cars)
        self.assertTrue(validate_data(df))

    """
        @author @name
    """
    def test_validate_data_user_False(self):
        cars = {
                        'brand': ['Saab', 'Volvo', 'Renault'],
                        'gear': ["Manuell", "Automat", "Manuell"],
                        'model': ["9-5", "S80", "CLIO"],
                        'fuel': ["Diesel", "Diesel", "Bensin"],
                        'mileage': ["30 000 - 34 999","18 000","140"],
                        'hp': ["149","163","89"],
                        'type': ["Kombi","Sedan","Halvkombi"],
                        'geo': ["Simrishamn","Helsingborg","Göteborg, Hisingen"],
                        'model_year': [2006.0,2011.0,2018.0]
                        }
        df = pd.DataFrame(cars)
        self.assertFalse(validate_data_user(df))

    """
        @author @name
    """
    def test_validate_data_user_True(self):
        cars = {
                        'brand': ['Saab', 'Volvo', 'Renault'],
                        'gear': ["Manuell", "Automat", "Manuell"],
                        'model': ["9-5", "S80", "CLIO"],
                        'fuel': ["Diesel", "Diesel", "Bensin"],
                        'mileage': [30000.0,18000.0,140.0],
                        'hp': [149.0,163.0,89.0],
                        'type': ["Kombi","Sedan","Halvkombi"],
                        'geo': ["Simrishamn","Helsingborg","Göteborg, Hisingen"],
                        'model_year': [2006.0,2011.0,2018.0]
                        }
        df = pd.DataFrame(cars)
        self.assertTrue(validate_data_user(df))

if __name__ == '__main__':
    unittest.main()
