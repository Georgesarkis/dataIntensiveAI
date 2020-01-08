import unittest
from pandas.util.testing import assert_frame_equal
import numpy as np
import pandas as pd
import sys
sys.path.insert(1, '../scripts')

from clean_up_dataset import OpenCSV,InitCleaningData,InitFeatureEng,DropOutlier

"""
    @author @name
"""
class TestClean_up_dataset(unittest.TestCase):
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

        cars = {'id': [0, 1, 2],
                     'brand': ['Saab', 'Volvo', 'Renault'],
                     'gear': ["Manuell", "Automat", "Manuell"],
                     'model': ["9-5", "S80", "CLIO"],
                     'price': [25000, 85000, 143900],
                     'fuel': ["Diesel", "Diesel", "Bensin"],
                     'mileage': ["30 000 - 34 999","18 000","140"],
                     'hp': ["149","163","89"],
                     'type': ["Kombi","Sedan","Halvkombi"],
                     'geo': ["Simrishamn","Helsingborg","Göteborg, Hisingen"],
                     'model_year': [2006,2011,2018]
                     }

        self.df = pd.DataFrame(cars)

    def tearDown(self):
        '''After every single test'''
        pass

    """
        @author @name
    """
    def test_OpenCSV(self):
        newdf = OpenCSV()
        assert_frame_equal(newdf.head(3) ,self.df, check_dtype=False, check_like=True)

    """
        @author @name
    """
    def test_InitCleaningData(self):
        cars = {'id': [0, 1, 2],
                'brand': ['Övriga', 'Volvo', 'Renault'],
                'gear': ["Manuell", "Automat", "Manuell"],
                'model': ["9-5", "S80", "CLIO"],
                'price': [25000, 85000, np.nan ],
                'fuel': ["Diesel", "Diesel", "Bensin"],
                'mileage': ["30 000 - 34 999","18 000","140"],
                'hp': ["149","163","89"],
                'type': ["Kombi","Sedan","Halvkombi"],
                'geo': ["Simrishamn","Helsingborg","Göteborg, Hisingen"],
                'model_year': [2006,2011,2018]
                }

        df = pd.DataFrame(cars)
        newdf = df.copy()
        df = df.drop('id', axis =1)
        df = df[df.brand != "Övriga"]
        df = df.dropna(subset=['model', 'brand', 'price'])
        assert_frame_equal(df ,InitCleaningData(newdf), check_dtype=False, check_like=True)

    """
        @author @name
    """
    def test_InitFeatureEng(self):
        cars = {'id': [0, 1, 2],
            'brand': ['Saab', 'Volvo', 'Renault'],
            'gear': ["Manuell", "Automat", "Manuell"],
            'model': ["9-5", "S80", "CLIO"],
            'price': [25000, 85000, 143900],
            'fuel': ["Diesel", "Diesel", "Bensin"],
            'mileage': [30000,18000,140],
            'hp': [149,163,89],
            'type': ["Kombi","Sedan","Halvkombi"],
            'geo': ["Simrishamn","Helsingborg","Göteborg, Hisingen"],
            'model_year': [2006,2011,2018]
            }

        newdf = pd.DataFrame(cars)
        assert_frame_equal(newdf ,InitFeatureEng(self.df), check_dtype=False, check_like=True)

    """
        @author @name
    """
    def test_DropOutlier(self):
        car = {'id': [1],
                    'brand': ['Volvo'],
                    'gear': ["Automat"],
                    'model': ["S80"],
                    'price': [85000],
                    'fuel': ["Diesel"],
                    'mileage': [18000],
                    'hp': [163],
                    'type': ["Sedan"],
                    'geo': ["Helsingborg"],
                    'model_year': [2011]
                    }

        ndf = pd.DataFrame(car)

        cars = {'id': [0, 1, 2],
            'brand': ['Saab', 'Volvo', 'Renault'],
            'gear': ["Manuell", "Automat", "Manuell"],
            'model': ["9-5", "S80", "CLIO"],
            'price': [6000000, 85000, 143900],
            'fuel': ["Diesel", "Diesel", "Bensin"],
            'mileage': [30000,18000,140],
            'hp': [149,163,1],
            'type': ["Kombi","Sedan","Halvkombi"],
            'geo': ["Simrishamn","Helsingborg","Göteborg, Hisingen"],
            'model_year': [2006,2011,2018]
            }
        newdf = pd.DataFrame(cars)
        nwedf = DropOutlier(newdf)
        nwedf = nwedf.reset_index(drop=True)
        assert_frame_equal(ndf ,nwedf, check_dtype=False, check_like=True)

if __name__ == '__main__':
    unittest.main()
