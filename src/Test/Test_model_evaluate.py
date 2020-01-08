import unittest
from pandas.util.testing import assert_frame_equal
import numpy as np
import pandas as pd
import sys
sys.path.insert(1, '../scripts')

from modelevaluate import evaluateModel

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

    def setUp(self):
        '''Before every single test'''
        pass

    def tearDown(self):
        '''After every single test'''
        pass

    """
        @author @name
    """
    def test_evaluateModel_100(self):
        y1 = {
                "y" : [500,400 ,200 ]
                }
        y = pd.DataFrame(y1)
        y2 = {
                'y': [500, 400, 200]
                }
        ypredicted = pd.DataFrame(y2)
        self.assertEqual(evaluateModel(y,ypredicted)[1], 100)

    """
        @author @name
    """
    def test_evaluateModel_50(self):
        y1 = {
                "y" : [500,450 ,230 ]
                }
        y = pd.DataFrame(y1)
        y2 = {
                'y': [500, 400, 200]
                }
        ypredicted = pd.DataFrame(y2)
        self.assertEqual(evaluateModel(y,ypredicted)[1].round(2), 91.76)

if __name__ == '__main__':
    unittest.main()
