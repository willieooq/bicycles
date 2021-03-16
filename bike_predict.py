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


keras_bike_predict(0,10,10,0,10,10,10,10,0,10)