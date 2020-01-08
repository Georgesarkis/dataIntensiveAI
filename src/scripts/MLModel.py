from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
import pickle
from modelevaluate import evaluateModel
from sklearn.externals import joblib
from hashlib import sha1

# Transform and select features

"""
    @author @George Sarkisian @Majed Dalain
"""
def MLModelTraining(train_car_data, exp):
    print("inside modelTraining ")
    # train_data_features = train_car_data.drop('date', axis=1)  # drop() creates a copy and does not affect original data
    # drop() creates a copy and does not affect original data
    train_data_features = train_car_data.drop('price', axis=1)
    # drop() creates a copy and does not affect original data
    train_data_features = train_data_features.drop('brand', axis=1)
    # drop() creates a copy and does not affect original data
    train_data_features = train_data_features.drop('model', axis=1)
    train_data_target = train_car_data["price"].copy()
    train_data_target.columns = ['price']
    train_data_target.skew()

    data = ['mileage', 'hp', 'type', 'geo', 'model_year', 'gear_Automat', 'gear_Manuell',
            'fuel_Bensin', 'fuel_Diesel', 'fuel_El', 'fuel_Miljöbränsle/Hybrid', 'model_code', 'brand_code']
    train_data_features = train_data_features[data]

    model = RandomForestRegressor()

    Xtrain, Xtest, ytrain, ytest = train_test_split(
        train_data_features, train_data_target, test_size=0.2, random_state=0)
    model.fit(Xtrain, ytrain)
    ypredtest = model.predict(Xtest)
    ypredtrain = model.predict(Xtrain)
    MAETest, R2Test = evaluateModel(ytest, ypredtest)
    MAETrain, R2Train = evaluateModel(ytrain, ypredtrain)
    

    exp.send_text('Model_Algorithm', 'Random Forest Regression')

    exp.send_metric('R2_train', R2Train)
    exp.send_metric('R2_test', R2Test)
    exp.send_metric('MAE_train', MAETrain)
    exp.send_metric('MAE_test', MAETest)

    return model

"""
    @author @George Sarkisian
"""
def MLEvaluate(data, model):
    # drop() creates a copy and does not affect original data
    train_data_features = data.drop('price', axis=1)
    # drop() creates a copy and does not affect original data
    train_data_features = train_data_features.drop('brand', axis=1)
    # drop() creates a copy and does not affect original data
    train_data_features = train_data_features.drop('model', axis=1)
    train_data_target = data["price"].copy()
    train_data_target.columns = ['price']
    train_data_target.skew()

    data = ['mileage', 'hp', 'type', 'geo', 'model_year', 'gear_Automat', 'gear_Manuell',
            'fuel_Bensin', 'fuel_Diesel', 'fuel_El', 'fuel_Miljöbränsle/Hybrid', 'model_code', 'brand_code']
    train_data_features = train_data_features[data]
    ypred = model.predict(train_data_features)

    return evaluateModel(train_data_target, ypred)


"""
    save the model to disk and Neptune tool. 

    @author @George Sarkisian @Majed Dalain
"""
def SaveModel(Model, PATH, exp):
    try:
        joblib.dump(Model, PATH)
        print("Wait while saving the model")
        # you can commit this line if you do not want to wait!
        exp.send_artifact(PATH)
        print("model has been saved !")
        exp.stop()

        return True
    except:
        return False


"""
    load the model from disk
    
    @author @George Sarkisian
"""
def ReadModel(PATH):
    try:
        loaded_model = joblib.load(PATH)
        return loaded_model
    except:
        return None
