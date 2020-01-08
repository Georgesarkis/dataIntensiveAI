import pandas as pd
import numpy as np
from pandas_schema import Column, Schema
from pandas_schema.validation import CustomElementValidation

HP_MIN_VALUE=40
HP_MAX_VALUE=800
MILEAGE_MAX_VALUE=300000
PRICE_MIN_VALUE=4000
PRICE_MAX_VALUE=5000000

"""
    @author @Amjad Alshihabi
"""
def is_int(value):
    return isinstance(value, int)

"""
    @author @Amjad Alshihabi
"""
def is_string(value):
    return isinstance(value, str)

"""
    @author @Amjad Alshihabi
"""
def is_float(value):
    return isinstance(value, float)

int_validation=[CustomElementValidation(lambda d: is_int(d), 'is not integer')]
string_validation=[CustomElementValidation(lambda d: is_string(d), 'is not string')]
float_validation=[CustomElementValidation(lambda d: is_float(d), 'is not float')]
null_validation=[CustomElementValidation(lambda d: pd.notnull(d), 'cannot be null')]
hp_min_validation=[CustomElementValidation(lambda d: d>HP_MIN_VALUE, 'cannot be less than 40')]
hp_max_validation=[CustomElementValidation(lambda d: d<HP_MAX_VALUE, 'cannot be greater than 800')]
mileage_max_validation=[CustomElementValidation(lambda d: d<MILEAGE_MAX_VALUE, 'cannot be less than 300000')]
price_max_validation=[CustomElementValidation(lambda d: d<PRICE_MAX_VALUE, 'cannot be greater than 5000 000')]
price_min_validation=[CustomElementValidation(lambda d: d>PRICE_MIN_VALUE, 'cannot be less than 4000')]

"""
    @author @Amjad Alshihabi
"""
def validate_data(df):
    schema = Schema([
        Column('brand', null_validation+string_validation),
        Column('gear', null_validation+string_validation),
        Column('model', null_validation+string_validation),
        Column('price', null_validation+int_validation+price_max_validation, price_min_validation),
        Column('fuel', null_validation+string_validation),
        Column('mileage', null_validation+float_validation+mileage_max_validation),
        Column('hp', null_validation+float_validation+hp_min_validation+hp_max_validation),
        Column('type', null_validation+string_validation),
        Column('geo', null_validation+string_validation),
        Column('model_year', null_validation+float_validation),
    ])
    try:
        errors = schema.validate(df)
        for e in errors:
            print(e)
    except:
        return False
    else:
        if not errors:
            return True
        else:
            return False

"""
    @author @Amjad Alshihabi
"""
def validate_data_user(df):
    schema = Schema([
        Column('brand', null_validation+string_validation),
        Column('gear', null_validation+string_validation),
        Column('model', null_validation+string_validation),
        Column('fuel', null_validation+string_validation),
        Column('mileage', null_validation+float_validation+mileage_max_validation),
        Column('hp', null_validation+float_validation+hp_min_validation+hp_max_validation),
        Column('type', null_validation+string_validation),
        Column('geo', null_validation+string_validation),
        Column('model_year', null_validation+float_validation),
    ])
    try:
        errors = schema.validate(df)
        for e in errors:
            print(e)
    except:
        return False
    else:
        if not errors:
            return True
        else:
            return False
