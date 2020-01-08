from flask import Flask, render_template
from flask import request, jsonify
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from ServiceController import validate, Init, AdminValidateoldData , AdminValidate,RetrainModel,getExperiments
import json
import sys
sys.path.insert(1, '../scripts')
from csv2sqlite import db_read, db_read_model
import base64

app = Flask(__name__)

# ROUTES

"""
    @author @MartinStanchev
"""
@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

"""
    @author @MartinStanchev
"""
@app.route("/admin", methods=["GET"])
def admin():
    return render_template("admin.html")

"""
    @author @George Sarkisian
"""
@app.route("/api/predict", methods=["GET"])
def predictePrice():
    try:
        #data = request.get_json(force=True)
        carBrand = request.args['carBrand']
        modelName = request.args['modelName'].upper()
        modelYear = request.args['modelYear']
        mileage = request.args['mileage']
        transmission = request.args['transmission']
        fuelType = request.args['fuelType']
        """
        hp = data["hp"]
        _type = data['type']
        geo = data["geo"]
        print("read the data")
        """
        valid = validate([carBrand, modelName, modelYear,
                          mileage, transmission, fuelType])
        if(valid):
            # Init([carBrand,modelName,modelYear,mileage,transmission,fuelType,hp,_type,geo])
            y = Init([carBrand, modelName, modelYear,
                      mileage, transmission, fuelType])
            return jsonify({
                "statusCode": 200,
                "status": "Prediction made",
                "result": str(y)
            })
        else:
            return jsonify({
                "statusCode": 500,
                "status": "Could not make prediction",
                "error": "Data is not valid"
            })
    except Exception as error:
        return jsonify({
            "statusCode": 500,
            "status": "Could not make prediction",
            "error": str(error)
        })

"""
    @author @George Sarkisian @Amjad Alshihabi
"""
@app.route("/api/validate", methods=["POST"])
def adminValidate():
    try:
        print("STARTED")
        file = request.files['file']
        data = pd.read_csv(file)
        oldData = db_read('cars')
        print("before adminvalidate for data")
        MAE, R2 = AdminValidate(data)
        print("before adminvalidate for old data")
        oldMAE, oldR2 = AdminValidateoldData(oldData)

        R2_array = ['oldR2', 'R2']

        R2_values = [oldR2, R2]
        R2_xpos = np.arange(len(R2_array))
        plt.bar(R2_xpos, R2_values)
        plt.xticks(R2_xpos, R2_array)
        plt.ylabel("Difference in R2 metric")
        plt.savefig("../../datasets/R2_chart.png")

        R2_img = open("../../datasets/R2_chart.png", 'rb')
        R2_img_read = R2_img.read()
        R2_img_enc = base64.encodebytes(R2_img_read)

        MAE_array = ['oldMAE', 'MAE']
        MAE_values = [oldMAE, MAE]
        MAE_xpos = np.arange(len(MAE_array))
        plt.bar(MAE_xpos, MAE_values)
        plt.xticks(MAE_xpos, MAE_array)
        plt.ylabel('Difference in MAE metric')
        plt.savefig("../../datasets/MAE_chart.png")

        MAE_img = open("../../datasets/MAE_chart.png", 'rb')
        MAE_img_read = MAE_img.read()
        MAE_img_enc = base64.encodebytes(MAE_img_read)
        if MAE and R2 is not None:
            return jsonify({
                "statusCode": 200,
                "status": "validation made",
                "result": str(adminValidate),
                "R2_chart_img": R2_img_enc,
                "MAE_chart_img": MAE_img_enc
##
 #       print(file)
  #      data = pd.read_csv(file)
   #     print(data)
    #    print("read_csv")
    #    adminValidate = AdminValidate(data)
    #    print(adminValidate[0])
    #    print("second item is :")
    #    print(adminValidate[1])

     #   if adminValidate is not None:
      #      return jsonify({
       #         "statusCode": 200,
        #        "status": "validation made",
         #       "result": adminValidate
            })
        else:
            return jsonify({
                "statusCode": 500,
                "status": "Could not make prediction",
                "error": "Data is not valid"
            })
    except Exception as error:
        return jsonify({
            "statusCode": 500,
            "status": "Could not make prediction",
            "error": str(error)
        })

"""
    @author @George Sarkisian @Majed Dalain 
"""
@app.route("/api/retrain", methods=["POST"])
def retrainModel():
    try:
        data = request.get_json(force=True)
        startDate = data['startDate']
        endDate = data['endDate']

        saved = RetrainModel(startDate, endDate)
        if saved is not None:
            return jsonify({
                "statusCode": 200,
                "status": "validation made",
                "result": saved
                })
        else:
            return jsonify({
                "statusCode": 500,
                "status": "Could not train the model",
                "error": "Model is not saved"
            })
    except Exception as error:
        return jsonify({
            "statusCode": 500,
            "status": "Could not retrain the model",
            "error": str(error)
        })

"""
    @author @Majed Dalain
"""
@app.route("/api/experiments", methods=["GET"])
def getAllExperiments():
    try:
        experimentsList = getExperiments()
        if experimentsList is not None:
            return jsonify({
                "statusCode": 200,
                "status": "Fetch All experiments",
                "result": experimentsList
            })
        else:
            return jsonify({
                "statusCode": 500,
                "status": "Could not make prediction",
                "error": "Data is not valid"
            })
    except Exception as error:
        return jsonify({
            "statusCode": 500,
            "status": "Could not make prediction",
            "error": str(error)
        })


# START FLASK
if __name__ == "__main__":
    app.run()
