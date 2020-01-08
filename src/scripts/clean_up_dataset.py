import pandas as pd
import os
import numpy as np
from sklearn.preprocessing import LabelEncoder
import collections
import json

# Location of this script in the file system.
file_location = os.path.dirname(os.path.realpath(__file__))

"""
    @author @MartinStanchev
"""
def cleanAndDivide(csvFileLocation):
    csv_file = open(csvFileLocation)
    row_count = sum(1 for row in csv_file)
    print(f"Lines in initial file: {row_count}")

    # Return back to the beginning of the file.
    csv_file.seek(0)

    # Read half of the file.
    df = pd.read_csv(csvFileLocation, sep=',', nrows=int(row_count * 0.75), low_memory=False)

    # Save the dataframe in result.csv
    try:
        df.to_csv(path_or_buf=f"{file_location}/../../datasets/result.csv", sep=",", index=False)
    except:
        print("Error with saving the result file.")
    else:
        print("Successfully cleaned up data, saving in datasets/result.csv")

    with open(f"{file_location}/../../datasets/result.csv") as result:
        row_count = sum(1 for row in result)
        print(f"Lines of the result file: {row_count}")

    df = pd.read_csv(csvFileLocation, sep=',', skiprows=int(row_count * 0.75), low_memory=False)
    df.to_csv(path_or_buf=f"{file_location}/../../datasets/restdata.csv", sep=",", index=False)

    with open(f"{file_location}/../../datasets/restdata.csv") as result:
        row_count = sum(1 for row in result)
        print(f"Rest of the data used for admin validation etc: {row_count}")

"""
    @author @George Sarkisian
"""
def OpenCSV():
    df = pd.read_csv(f"{file_location}/../../datasets/result.csv", low_memory=False)
    return df

"""
    @author @George Sarkisian
"""
def InitCleaningData(train_car_data):
    if 'regnr' in train_car_data.columns:
        train_car_data = train_car_data.drop('regnr', axis =1)
    if 'id' in train_car_data.columns:
        train_car_data = train_car_data.drop('id', axis =1)
    if 'add_date' in train_car_data.columns:
        train_car_data = train_car_data.drop('add_date', axis =1)
    if 'make_year' in train_car_data.columns:
        train_car_data = train_car_data.drop('make_year', axis =1)
    train_car_data = train_car_data[train_car_data.brand != "Övriga"]
    train_car_data = train_car_data.dropna(subset=['model', 'brand', 'price'])
    return train_car_data

"""
    @author @George Sarkisian
"""
def InitFeatureEng(train_car_data):
    train_car_data["geo"] = train_car_data["geo"].replace(np.nan, "Sweden", regex=True)
    train_car_data["geo"] = train_car_data["geo"].replace("-", "Sweden", regex=True)
    train_car_data["type"] = train_car_data["type"].replace(np.nan, "Sedan", regex=True)
    train_car_data["type"] = train_car_data["type"].replace("-", "Sedan", regex=True)
    train_car_data["gear"] = train_car_data["gear"].replace(np.nan, "Manuell", regex=True)
    train_car_data["gear"] = train_car_data["gear"].replace("-", "Manuell", regex=True)
    train_car_data["fuel"] = train_car_data["fuel"].replace(np.nan, "Bensin", regex=True)
    train_car_data["fuel"] = train_car_data["fuel"].replace("-", "Bensin", regex=True)

    train_car_data['mileage'] = train_car_data['mileage'].replace(" ", "", regex=True)
    train_car_data['mileage'] = train_car_data['mileage'].apply(lambda x: x[5:] if "Merän" in x else (x if x.find("-") == -1 else x[:x.find("-")]))
    train_car_data['mileage'] = train_car_data['mileage'].astype(float)

    train_car_data["hp"] = train_car_data["hp"].replace("0", np.nan, regex=True)
    train_car_data["hp"] = train_car_data["hp"].replace("-", np.nan, regex=True)
    train_car_data['hp'] = train_car_data['hp'].astype(float)

    train_car_data['model_year'] = train_car_data['model_year'].astype(float)

    # BRAND SHOULD BE CHANGE WITH MODEL(model) FOR BETTER ACCURECY FOR NOW THIS COUSE 5% WORST ACCURECY IN OUR MODEL
    train_car_data["hp"] = train_car_data.groupby(["brand"])["hp"].transform(lambda x: x.fillna(x.median()))
    return train_car_data

"""
    @author @George Sarkisian
"""
def DropOutlier(train_car_data):
    train_car_data = train_car_data[(train_car_data.hp > 40)]
    train_car_data = train_car_data[(train_car_data.price > 4000)]
    train_car_data = train_car_data[(train_car_data.price < 5000000)]
    train_car_data =  train_car_data[(train_car_data.mileage < 300000)]
    train_car_data = train_car_data[(train_car_data.hp < 800)]
    return train_car_data

"""
    @author @MartinStanchev
"""
def CleanModels():
    print("Cleaning models....")
    cars = json.load(open(f"{file_location}/../../datasets/makemodel.json"))

    df = OpenCSV()
    count = 0
    count_1 = 0
    for index, row in df.iterrows():
        car_make = row["brand"].upper()
        try:
            match = next(
                (s for s in cars[car_make] if s.upper().replace(" ", "") in row["model"].upper().replace(" ", "")),
                None)
            if (match is not None):
                count_1 += 1
                row['model'] = match
                df.set_value(index=index, col="model", value=match)
        except:
            count += 1
    df.to_csv(path_or_buf=f"{file_location}/../../datasets/result.csv", sep=",", index=False)
    print(f"Cleaned models, valid entries: {count_1}, non-valid: {count}")

"""
    perform onehotEncoding and LabelEncoding

    @author @George Sarkisian
"""
def OnhotLabelEncoding(train_car_data):
    train_car_data = pd.get_dummies(train_car_data, dummy_na = False, columns=['gear','fuel'] )

    lb_make_geo = LabelEncoder()
    train_car_data["geo"] = lb_make_geo.fit_transform(train_car_data["geo"])

    lb_make_type = LabelEncoder()
    train_car_data["type"] = lb_make_type.fit_transform(train_car_data["type"])

    lb_make_model = LabelEncoder()
    train_car_data["model_code"] = lb_make_model.fit_transform(train_car_data["model"])

    lb_make_brand = LabelEncoder()
    train_car_data["brand_code"] = lb_make_brand.fit_transform(train_car_data["brand"])

    np.save(f"{file_location}/../../datasets/lb_make_geo.npy",lb_make_geo.classes_ )
    np.save(f"{file_location}/../../datasets/lb_make_type.npy",lb_make_type.classes_ )
    np.save(f"{file_location}/../../datasets/lb_make_model.npy",lb_make_model.classes_ )
    np.save(f"{file_location}/../../datasets/lb_make_brand.npy",lb_make_brand.classes_ )

    return train_car_data
