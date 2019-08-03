#!/usr/bin/python
# -*- coding: utf-8 -*-


def keras_bike_predict(bicycle, bicycle_wheel, bicycle_part, bicycle_frame, bicycle_tire, vehicle, spoke, bicycle_saddle, bicycle_fork, bicycle_drivetrain_part):
    from keras.models import load_model
    import numpy as np
    import pandas as pd
    from sklearn import preprocessing
    irisModel = load_model("bike_model.h5")
    filepath="BT3.xlsx"
    all_df = pd.read_excel(filepath)

    cols=['bicycle','bicycle_wheel','bicycle_part','bicycle_frame','bicycle_tire','vehicle','spoke','bicycle_saddle','bicycle_fork','bicycle_drivetrain_part','score']
    all_df=all_df[cols]
    
    train_df = all_df[:]


    ndarray = train_df.values
    b = np.array([[bicycle, bicycle_wheel, bicycle_part, bicycle_frame, bicycle_tire, vehicle, spoke, bicycle_saddle, bicycle_fork, bicycle_drivetrain_part]])
    Features = ndarray[:,:10]
    Features = np.concatenate((Features, b))
    leng = len(Features)

    minmax_scale = preprocessing.MinMaxScaler(feature_range=(0, 1))
    scaledFeatures=minmax_scale.fit_transform(Features)    

    train_Features=scaledFeatures

    print(train_Features[leng-1])

    
    predict_request = train_Features[leng-1]
    predict_request = np.array([predict_request])
    y_pred = irisModel.predict_classes(predict_request)
    return y_pred[0]


keras_bike_predict(bicycle = 0.9324832947, bicycle_wheel = 0.893472394793284, bicycle_part = 0.98766576777, bicycle_frame = 0.7823432948324, bicycle_tire = 0.9324832948, vehicle = 0.93942839497329, spoke = 0.9999999939499, bicycle_saddle = 0.9823483729, bicycle_fork = 0.8932473279847, bicycle_drivetrain_part = 0.932849732949328)