from sklearn import svm
from sklearn import preprocessing
from flights import models
import random
import datetime
import numpy as np


enc = preprocessing.OneHotEncoder() # might be used to transform categorical features (airport codes, locations, carriers, ...)
clf = svm.SVC(gamma=0.001, C=1000.)



def minute_of_day(dt):
    time = datetime.datetime.time(dt)
    return time.hour * 60 + time.minute

def simple_int(s):
    # simple hash from str to numeric value for mining inputs
    # TODO: use something better, maybe OneHotEncoder?
    return abs(hash(s)) % (10 ** 6)


def extract_features(flight):
    return [
        minute_of_day(flight.scheduled_departure),
        simple_int(flight.carrier),
        simple_int(flight.departure_airport)
        ]


def learn_from_db(limit_sample=10000):
    #for n in range(limit_sample):

    sample = models.Flight.query.limit(limit_sample).all()
    data, target = zip(*[(extract_features(f), f.delay_mins) for f in sample])
    clf.fit(data, target)
    

def test_prediction_db(tests=100, offset=1000000):
    test_flights = models.Flight.query.offset(offset).limit(tests).all()
    for f in test_flights:
        r = clf.predict(np.array(extract_features(f)).reshape((1, -1)))
        print(r, f.delay_mins)
