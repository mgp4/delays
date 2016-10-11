from sklearn import svm
from sklearn import preprocessing
from . import models
import random
import datetime
import numpy as np
from sklearn.externals import joblib


enc = preprocessing.OneHotEncoder() # might be used to transform categorical features (airport codes, locations, carriers, ...)
clf = svm.SVC(gamma='auto', C=1.2)


def minute_of_day(dt):
    time = datetime.datetime.time(dt)
    return time.hour * 60 + time.minute


def map_to_int(s):
    # simple hash from str to numeric value for mining inputs
    # TODO: use something better, maybe OneHotEncoder?
    return abs(hash(s)) % (10 ** 6)


def extract_features(flight):
    return [
            minute_of_day(flight.scheduled_departure),
            map_to_int(flight.carrier),
            # simple_int(flight.departure_airport),
            flight.src_airport.latitude,
            flight.src_airport.longitude
           ]


def train_from_db(limit_sample=10000):
    sample = models.Flight.query.limit(limit_sample).all()
    data, target = zip(*[(extract_features(f), f.delay_mins) for f in sample])
    clf.fit(data, target)
    

def test_prediction_db(tests=100, offset=5000000):
    test_flights = models.Flight.query.offset(offset).limit(tests).all()
    score = 0
    for f in test_flights:
        r = clf.predict(np.array(extract_features(f)).reshape((1, -1)))
        error = abs(r[0] - f.delay_mins)
        score += error
        print(r, f.delay_mins, error)
    print("sum errors: %s" % score)


def store_classifier_model(filename="model.dat"):
    joblib.dump(clf, filename)


def restore_classifier_model(filename="model.dat"):
    global clf
    clf = joblib.load(filename)
