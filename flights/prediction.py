from sklearn import svm
from sklearn import preprocessing
from . import models
from . import settings
import random
from datetime import datetime, timedelta
import numpy as np
from sklearn.externals import joblib
from tempfile import NamedTemporaryFile
import shutil
import csv


enc = preprocessing.OneHotEncoder() # might be used to transform categorical features (airport codes, locations, carriers, ...)
clf = svm.SVC(gamma='auto', C=1.2)


def minute_of_day(dt):
    time = datetime.time(dt)
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
    try:
        return [
                minute_of_day(flight.scheduled_departure),
                map_to_int(flight.carrier),
                flight.src_airport.latitude,
                flight.src_airport.longitude,
                map_to_int(flight.arrival_airport),
                int(flight.flight_number) # we might use just len() of flight number
               ]
    except (ValueError, AttributeError):
        # hot fis for missing airport record and characters in flight_number
        return [0, 0, 0, 0, 0, 0]


def train_from_db(limit_sample=50000, skip=None):
    """
    get a sample from db and train calssifier
    """
    # TODO: use some more representative sample than just first n of db records
    # NOTE: SVM training complexity is O(n^2), we cannot use whole dataset for training, 
    #       is tehre a better solution?
    sample = models.Flight.query
    if skip:
        sample = sample.filter(models.Flight.id % (skip) == 0)
    sample = sample.limit(limit_sample).all()
    data, target = zip(*[(extract_features(f), f.delay_mins) for f in sample])
    clf.fit(data, target)
    

def test_prediction_db(tests=1000, offset=200000, skip=None):
    """
    test our classifier's prediction (in)accuracy
    """
    test_flights = models.Flight.query
    if skip:
        test_flights = test_flights.filter(models.Flight.id % (skip) == 0)
    test_flights = test_flights.offset(offset).limit(tests).all()
    score = 0
    matched = 0
    print("{:>6} {:>6} {:>7}".format("pred.", "actual", "error"))
    print("-" * 21)
    for f in test_flights:
        r = clf.predict(np.array(extract_features(f)).reshape((1, -1)))
        error = (r[0] - f.delay_mins)
        score += abs(error)
        print("{:>6} {:>6} {:>7}".format(r[0], f.delay_mins, error))
        if error == 0:
            matched += 1
    print("-" * 21)
    print("sum errors: %s" % score)
    print("average error: %s" % (score / tests))
    print("matched delays: %s (%s%%)" % (matched, matched / tests * 100))
    print("-" * 21)


def predict_csv(filename="delays.csv"):
    """
    read flights from csv file, predict actual_departure_time and write into output file,
    original file then gets replaced with output as required in the task assignment
    """
    #tempfile = NamedTemporaryFile(delete=False, mode="w")
    temp_filename = ".%s_original"
    shutil.move(filename, temp_filename)
    #print("Using tempfile %s" % tempfile.name)
    fields = ["carrier", "flight_number", "dep_apt", "arr_apt", "scheduled_date", "scheduled_departure", "actual_departure"]
    cnt = 0
    with open(temp_filename, 'r') as input_file, open(filename, 'w') as output_file:
        reader = csv.DictReader(input_file)
        writer = csv.DictWriter(output_file, fieldnames=fields, extrasaction='ignore')
        writer.writeheader()

        for row in reader:
            try:
                src_airport = models.Airport.query.filter(models.Airport.code == row['dep_apt']).one()
            except:
                src_airport = {
                'latitude': 0,
                'longitude': 0
            }
            flight = {
                'carrier': row['carrier'],
                'flight_number': row['flight_number'],
                'departure_airport': row['dep_apt'],
                'arrival_airport': row['arr_apt'],
                'scheduled_departure':
                    datetime.strptime(row['scheduled_departure'],
                                      settings.DATETIME_FORMAT),
                'actual_departure': None,
                'src_airport': src_airport,
                'scheduled_date': row['scheduled_date']
            }
            delay_mins = clf.predict(np.array(extract_features(flight)).reshape((1, -1)))[0]
            flight['actual_departure'] = flight['scheduled_departure'] + timedelta(minutes=int(delay_mins))

            # convert datetimes
            # flight['scheduled_departure'] = datetime.strftime(flight['scheduled_departure'], settings.DATETIME_FORMAT)
            flight['scheduled_departure'] = row['scheduled_departure']
            flight['actual_departure'] = datetime.strftime(flight['actual_departure'], settings.DATETIME_FORMAT)
            flight['dep_apt'] = flight.pop('departure_airport')
            flight['arr_apt'] = flight.pop('arrival_airport')
            # print(flight)
            writer.writerow(flight)
            if cnt % 20 == 0:
                output_file.flush()
            cnt += 1


def store_classifier_model(filename="model.dat"):
    joblib.dump(clf, filename)


def restore_classifier_model(filename="model.dat"):
    global clf
    clf = joblib.load(filename)

