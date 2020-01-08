import sys
import os
import pandas as pd
from sklearn.externals import joblib
sys.path.insert(1, '../scripts')
from csv2sqlite import *
from Controller import init
from clean_up_dataset import InitCleaningData, InitFeatureEng, DropOutlier
from MLModel import *
import numpy as np
from sklearn.preprocessing import LabelEncoder
import neptune
from neptune import Session
from data_validator import validate_data_user, validate_data

# Location of this script in the file system.
file_location = os.path.dirname(os.path.realpath(__file__))
MLEvaluateValue = None
NEPTUNE_API_TOKEN = 'eyJhcGlfYWRkcmVzcyI6Imh0dHBzOi8vdWkubmVwdHVuZS5tbCIsImFwaV91cmwiOiJodHRwczovL3VpLm5lcHR1bmUuYWkiLCJhcGlfa2V5IjoiNGYwOTRmZTgtMzZiNi00MjcyLTg3MTItN2ZjOWNmMjBhNmVkIn0='

"""
    @author @George Sarkisian
"""
def changeMLEvaluateValue(dp,Model):
    global MLEvaluateValue
    MLEvaluateValue = MLEvaluate(dp,Model)
    print(MLEvaluateValue)
    return MLEvaluateValue

"""
    @author @George Sarkisian
"""
def Init(data):
    data = featureEngStringTOFloat(data)
    df = CreateDataFrame(data)

    Model = ReadModel(f"{file_location}/../../datasets/model")
    if(Model is None):
        dp, Model = init()
        changeMLEvaluateValue(dp,Model)

    df = feateEng(df,data[1])
    if validate_data_user(df) :
        df = OnhotLabelEncoding(df)
        df = CleanData(df)
        df = prepareOtherColoms(df)
        data = ['mileage', 'hp', 'type', 'geo', 'model_year', 'gear_Automat', 'gear_Manuell',
                'fuel_Bensin', 'fuel_Diesel', 'fuel_El', 'fuel_Miljöbränsle/Hybrid', 'model_code', 'brand_code']
        df = df[data]
        y = Model.predict(df)
        return y[0]
    else:
        return None

"""
    @author @George Sarkisian
"""
def validate(data):
    if(type(data[0]) is not str):
        return False
    if(type(data[1]) is not str):
        return False
    if(type(data[4]) is not str):
        return False
    if(type(data[5]) is not str):
        return False
    return True

"""
    @author @George Sarkisian
"""
def CreateDataFrame(data):
    # [[data[0],data[1],data[2],data[3],data[4],data[5],data[6],data[7],data[8]]]
    data = [[data[0], data[1], data[2], data[3], data[4], data[5]]]
    # pd.DataFrame(data, columns =['brand', 'model','model_year','mileage','gear','fuel',"hp","type", "geo"])
    df = pd.DataFrame(
        data, columns=['brand', 'model', 'model_year', 'mileage', 'gear', 'fuel'])
    return df

"""
    @author @George Sarkisian
"""
def featureEngStringTOFloat(data):
    if(type(data[2]) is str):
        data[2] = float(data[2])
    if(type(data[3]) is str):
        data[3] = float(data[3])
    # if(type(data[6]) is str):
    #    data[6] = float(data[6])

    return data

"""
    @author @George Sarkisian
"""
def feateEng(df, model):
    train_car_data = db_read_model('cars', model)
    df["geo"] = "Sweden"
    means = train_car_data.loc[:"hp"].mean()
    df['hp'] = means.hp
    df["type"] = "Sedan"
    return df

"""
    @author @George Sarkisian
"""
def CleanData(df):
    df = df.drop('brand', axis=1)
    df = df.drop('model', axis=1)
    return df

"""
    @author @George Sarkisian
"""
def prepareOtherColoms(df):
    if 'gear_Automat' not in df.columns:
        df['gear_Automat'] = 0
    if 'gear_Manuell' not in df.columns:
        df['gear_Manuell'] = 0
    if 'fuel_Bensin' not in df.columns:
        df['fuel_Bensin'] = 0
    if 'fuel_Diesel' not in df.columns:
        df['fuel_Diesel'] = 0
    if 'fuel_El' not in df.columns:
        df['fuel_El'] = 0
    if 'fuel_Miljöbränsle/Hybrid' not in df.columns:
        df['fuel_Miljöbränsle/Hybrid'] = 0
    return df

"""
    @author @George Sarkisian
"""
def AdminValidate(data):
    if 'brand' not in data.columns:
        return None
    if 'gear' not in data.columns:
        return None
    if 'model' not in data.columns:
        return None
    if 'price' not in data.columns:
        return None
    if 'fuel' not in data.columns:
        return None
    if 'mileage' not in data.columns:
        return None
    if 'hp' not in data.columns:
        return None
    if 'type' not in data.columns:
        return None
    if 'geo' not in data.columns:
        return None
    if 'model_year' not in data.columns:
        return None

    Model = ReadModel(f"{file_location}/../../datasets/model")
    if(Model is None):
        dp, Model = init()
        changeMLEvaluateValue(dp,Model)

    data = InitCleaningData(data)
    data = InitFeatureEng(data)
    data = DropOutlier(data)
    data = data.reset_index(drop=True)

    if validate_data(data):
        insert(data, "cars")
        data = OnhotLabelEncoding(data)
        return MLEvaluate(data, Model)
    else:
        return None

"""
    @author @George Sarkisian
"""
def AdminValidateoldData(data):
    global MLEvaluateValue
    print("AdminValidateoldData")
    print(MLEvaluateValue)
    return MLEvaluateValue

"""
    @author @George Sarkisian
"""
def OnhotLabelEncoding(data):
    data = pd.get_dummies(data, dummy_na = False, columns=['gear','fuel'] )

    data['brand'] = data['brand'].str.upper()
    data['model'] = data['model'].str.upper()

    print("get_dummies")
    lb_make_geo = LabelEncoder()
    lb_make_geo.classes_ = np.load(
        f"{file_location}/../../datasets/lb_make_geo.npy", allow_pickle=True)
    data["geo"] = lb_make_geo.transform(data["geo"])

    lb_make_type = LabelEncoder()
    lb_make_type.classes_ = np.load(
        f"{file_location}/../../datasets/lb_make_type.npy", allow_pickle=True)
    data["type"] = lb_make_type.transform(data["type"])

    lb_make_brand = LabelEncoder()
    lb_make_brand.classes_ = np.load(
        f"{file_location}/../../datasets/lb_make_brand.npy", allow_pickle=True)
    data["brand_code"] = lb_make_brand.transform(data["brand"])

    lb_make_model = LabelEncoder()
    lb_make_model.classes_ = np.load(
        f"{file_location}/../../datasets/lb_make_model.npy", allow_pickle=True)
    for i, item in enumerate(data['model']):
        try:
            data["model_code"] = lb_make_model.transform(data['model'])
        except:
            data = data.drop(i)

    return data

"""
    @author @George Sarkisian
"""
def NewOnhotLabelEncoding(train_car_data):
    train_car_data = pd.get_dummies(
        train_car_data, dummy_na=False, columns=['gear', 'fuel'])

    lb_make_geo = LabelEncoder()
    train_car_data["geo"] = lb_make_geo.fit_transform(train_car_data["geo"])

    lb_make_type = LabelEncoder()
    train_car_data["type"] = lb_make_type.fit_transform(train_car_data["type"])

    lb_make_model = LabelEncoder()
    train_car_data["model_code"] = lb_make_model.fit_transform(
        train_car_data["model"])

    lb_make_brand = LabelEncoder()
    train_car_data["brand_code"] = lb_make_brand.fit_transform(
        train_car_data["brand"])
    np.save(f"{file_location}/../../datasets/lb_make_geo.npy",
            lb_make_geo.classes_)
    np.save(f"{file_location}/../../datasets/lb_make_type.npy",
            lb_make_type.classes_)
    np.save(f"{file_location}/../../datasets/lb_make_model.npy",
            lb_make_model.classes_)
    np.save(f"{file_location}/../../datasets/lb_make_brand.npy",
            lb_make_brand.classes_)

    return train_car_data

"""
    @author @George Sarkisian  @Majed Dalain
"""
def RetrainModel(date1, date2):
    # this has to be improved to use Env Variables instead.
    neptune.init(api_token=NEPTUNE_API_TOKEN,
                 project_qualified_name='majeddalain/sandbox')
    print("Neptune initialization is successed")

    with neptune.create_experiment(name=    "trained on data from: " + str(date1[0]) +"/"+ str(date1[1]) +"/"+ str(date1[2]) + " to " + str(date2[0]) +"/"+ str(date2[1]) +"/"+ str(date2[2]) ) as exp:

        date1 = datetime.datetime(date1[0], date1[1], date1[2])
        date2 = datetime.datetime(date2[0], date2[1], date2[2])

        # send the two dates to the experiment
        exp.send_text('Start Date', str(date1))
        exp.send_text('End Date', str(date2))

        dp = db_read_period('cars', date1, date2)

        dp = InitCleaningData(dp)
        dp = NewOnhotLabelEncoding(dp)

        Model = MLModelTraining(dp,exp)
        saved = SaveModel(Model,f"{file_location}/../../datasets/model",exp)

        if(saved):
            return changeMLEvaluateValue(dp,Model)
        else:
            return saved

"""
    @author @Majed Dalain
"""
def getExperiments():
    session = Session.with_default_backend(api_token=NEPTUNE_API_TOKEN)
    # Get a project by it's project_qualified_name:
    my_project = session.get_project('majeddalain/sandbox')

    experiments = my_project.get_experiments(
        state=['succeeded'], owner=['majeddalain'])
    expList = {}
    print
    for i in experiments:
        expList[i.id] = {
            'name':i.name,
            'R2_train':i.get_numeric_channels_values('R2_train')['R2_train'].to_numpy()[0],
            'R2_test': i.get_numeric_channels_values('R2_test')['R2_test'].to_numpy()[0],
            'MAE_train': i.get_numeric_channels_values('MAE_train')['MAE_train'].to_numpy()[0],
            'MAE_test': i.get_numeric_channels_values('MAE_test')['MAE_test'].to_numpy()[0],
        }
    print("the list after converting:")
    print(expList)
    print(type(expList))
    return expList
