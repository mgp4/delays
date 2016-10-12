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
    #       better solution might be assigning numeric ids based on list of categories by avg delay 
    #       but could we be then sure we won't get unknown airport/airline?
    return abs(hash(s)) % (10 ** 6)


def extract_features(flight):
    """
    creates feature vector for training and prediction inputs
    """
    return [
            minute_of_day(flight.scheduled_departure),
            map_to_int(flight.carrier),
            flight.src_airport.latitude,
            flight.src_airport.longitude,
            map_to_int(flight.arrival_airport),
            int(flight.flight_number) # we might use just len() of flight number
           ]


def train_from_db(limit_sample=50000):
    """
    get a sample from db and train calssifier
    """
    # TODO: use some more representative sample than just first n of db records
    # NOTE: SVM training complexity is O(n^2), we cannot use whole dataset for training, 
    #       is tehre a better solution?
    sample = models.Flight.query.limit(limit_sample).all()
    data, target = zip(*[(extract_features(f), f.delay_mins) for f in sample])
    clf.fit(data, target)
    

def test_prediction_db(tests=1000, offset=200000):
    """
    test our classifier's prediction (in)accuracy
    """
    test_flights = models.Flight.query.offset(offset).limit(tests).all()
    score = 0
    print("{:>6} {:>6} {:>7}".format("pred.", "actual", "error"))
    print("-" * 21)
    for f in test_flights:
        r = clf.predict(np.array(extract_features(f)).reshape((1, -1)))
        error = (r[0] - f.delay_mins)
        score += abs(error)
        print("{:>6} {:>6} {:>7}".format(r[0], f.delay_mins, error))
    print("-" * 21)
    print("sum errors: %s" % score)
    print("average error: %s" % (score/tests))
    print("-" * 21)


def store_classifier_model(filename="model.dat"):
    joblib.dump(clf, filename)


def restore_classifier_model(filename="model.dat"):
    global clf
    clf = joblib.load(filename)

