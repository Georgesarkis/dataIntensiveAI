import numpy as np
import pandas as pd
import sqlite3
from clean_up_dataset import *
from MLModel import *
from csv2sqlite import *
import os
from sklearn.preprocessing import LabelEncoder
import neptune


NEPTUNE_API_TOKEN = 'eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vdWkubmVwdHVuZS5tbCIsImFwaV91cmwiOiJodHRwczovL3VpLm5lcHR1bmUuYWkiLCJhcGlfa2V5IjoiNGYwOTRmZTgtMzZiNi00MjcyLTg3MTItN2ZjOWNmMjBhNmVkIn0='

# NEPTUNE_API_TOKEN = os.getenv('NEPTUNE_API_TOKEN')

"""
    @author @George Sarkisian
"""
def init():
    # Location of this script in the file system.
    file_location = os.path.dirname(os.path.realpath(__file__))
    neptune.init(api_token=NEPTUNE_API_TOKEN,
                 project_qualified_name='majeddalain/sandbox')
    print("init is successed now ")

    with neptune.create_experiment(name='car_prediction_model') as exp:
        print("created the exp now ")
        # cleanAndDivide(f"{file_location}/../../datasets/data.csv")
        # CleanModels()
        dp = OpenCSV()
        dp['brand'] = dp['brand'].str.upper()
        dp['model'] = dp['model'].str.upper()
        dp = InitCleaningData(dp)
        dp = InitFeatureEng(dp)
        dp = DropOutlier(dp)
        create_table("cars")
        insert(dp, "cars")

        dp = OnhotLabelEncoding(dp)
        print("done onhotlabel encoding")
        Model = MLModelTraining(dp, exp)

        saved = SaveModel(Model, f"{file_location}/../../datasets/model", exp)
        print(saved)
        return dp,Model
