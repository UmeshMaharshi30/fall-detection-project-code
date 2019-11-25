# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 00:58:06 2019

@author: umesh
"""


from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
import pickle

import serial
from collections import deque
import time
from time import sleep
import numpy as np

class SensorData:
    def __init__(self, above, over, duration):
        self.activity = "random"
        self.above = above
        self.over = over
        self.duration = duration
        self.fall = 0


def get_train_data(input_file):
    print("Reading input file and generating train data")
    input_data_file = open(input_file, 'r')
    train_x = []
    train_y = []
    lines = []
    count = 0
    for line in input_data_file:
        if count == 0:
            count = count + 1
            continue
        line = line.strip()
        temp = []
        for reading in line.split(","):
            if len(reading) == 0:
                temp.append(0)
            else :
                temp.append(int(reading))
        lines.append(temp)
    for i in range(0, 80):
        x_data = []
        for j in range(0, len(lines)):
            if j >= 2500:
                continue
            x_data.append(lines[j][i])
        train_x.append(x_data)
        if i < 20:
            train_y.append(1)
        else:
            train_y.append(0)
    return train_x, train_y

def get_test_data(input_file):
    print("Reading input file and generating and test data")
    input_data_file = open(input_file, 'r')
    test_x = []
    test_y = []
    lines = []
    count = 0
    for line in input_data_file:
        if count == 0:
            count = count + 1
            continue
        line = line.strip()
        temp = []
        for reading in line.split(","):
            if len(reading) == 0:
                temp.append(0)
            else :
                temp.append(int(reading))
        lines.append(temp)
    for i in range(0, 10):
        x_data_test = []
        for j in range(0, len(lines)):
            if j >= 2500:
                continue
            x_data_test.append(lines[j][i])
        test_x.append(x_data_test)
        if i < 5:
            test_y.append(1)
        else:
            test_y.append(0)
    return test_x, test_y



def start_analysing_data(model):
    time_series = deque()
    try:
        while True:
            while len(time_series) < 2500: 
                voltage = ser.readline()
                voltage= voltage.rstrip().decode('utf-8','ignore')
                try:
                    voltage = int(voltage)
                    if voltage > 500 or voltage < 100:
                        continue
                    voltage = max(0, voltage - 164)
                    time_series.append(voltage)
                except ValueError:
                    pass
            prediction = model.predict([time_series])
            if prediction[0] == 1:
                print("Fall detected")
                time_series = deque()
                sleep(10)
            else:
                time_series.popleft()
    except KeyboardInterrupt:
        ser.close()
    finally:
        ser.close()
        pass


def start_peak_determining_algo(threshold_value):
    peaks_above_threshold = 0
    peaks_above_limit = 0
    peaks_below_threshold = 0
    duration_of_peak = 0
    possible_fall = False
    try:
        while True:
            voltage = ser.readline()
            voltage= voltage.rstrip().decode('utf-8','ignore')
            try:
                voltage = int(voltage)
                if voltage > 500 or voltage < 100:
                    continue
                if voltage > threshold_value :
                    peaks_below_threshold = 0
                    if voltage > threshold_value + 6:
                        peaks_above_limit = peaks_above_limit + 1
                    else:
                        peaks_above_threshold = peaks_above_threshold + 1
                else:
                    peaks_below_threshold = peaks_below_threshold + 1
                # if constant static reading for over certain period, check if possible fall or discard everything *
                if peaks_below_threshold > 250:  
                    if possible_fall:
                        print("Possible Fall Detected !!!")
                        possible_fall = not possible_fall
                    peaks_above_threshold = 0
                    peaks_above_limit = 0
                    duration_of_peak = 0
                    peaks_below_threshold = 0
                    continue
                if peaks_above_threshold > 0:
                    duration_of_peak = duration_of_peak + 1
                    if duration_of_peak == 600:
                        print(peaks_above_threshold)
                        print(peaks_above_limit)
                        if peaks_above_threshold > 10:
                            possible_fall = not possible_fall
                        else:
                            duration_of_peak = 0
                            peaks_above_threshold = 0
                            peaks_above_limit = 0
            except ValueError:
                pass
    except KeyboardInterrupt:
        ser.close()
    finally:
        ser.close()
            


def start_peak_determining_algo_with_duration(threshold_value):
    peaks_above_threshold = 0
    peaks_above_limit = 0
    peaks_below_threshold = 0
    start_of_peak = 0
    end_of_peak = 0
    threshold_time = 1000000000
    #data_collected = []
    classifier = pickle.load(open('neural_model.model', 'rb'))
    try:
        while True:
            voltage = ser.readline()
            voltage= voltage.rstrip().decode('utf-8','ignore')
            try:
                voltage = int(voltage)
                curr_time = time.time_ns()
                if voltage > 500 or voltage < 100:
                    continue
                if voltage > threshold_value :
                    if start_of_peak == 0:
                        start_of_peak = curr_time 
                        end_of_peak = curr_time
                    else:
                        end_of_peak = curr_time
                    peaks_below_threshold = 0
                    if voltage > threshold_value + 6:
                        peaks_above_limit = peaks_above_limit + 1
                    else:
                        peaks_above_threshold = peaks_above_threshold + 1
                else:
                    peaks_below_threshold = peaks_below_threshold + 1
                # if constant static reading for over certain period, check if possible fall or discard everything *
                if start_of_peak > 0 and curr_time - end_of_peak > threshold_time:
                    print("End of activity")
                    #data_collected.append(SensorData(peaks_above_threshold,peaks_above_limit, end_of_peak - start_of_peak ))
                    #print(str(peaks_above_threshold))
                    #print(str(peaks_above_limit))
                    #print(str(end_of_peak - start_of_peak))
                    input_list = [peaks_above_threshold, peaks_above_limit, round((end_of_peak - start_of_peak)/threshold_time, 2)]
                    input_list = np.asarray(input_list).reshape(1,3)
                    prediction = classifier.predict(input_list)
                    prediction = prediction[0][0]
                    if prediction > 0.4:
                        print("Possible fall")
                        print(prediction)
                    peaks_above_threshold = 0
                    peaks_above_limit = 0
                    peaks_below_threshold = 0
                    start_of_peak = 0
                    end_of_peak = 0
            except ValueError:
                pass
            
        file = "random_activit.csv"
        with open(file, 'w') as f:
            for item in data_collected:
                print(item.activity + ", " + str(item.above) + ", "+str(item.over) + ", " + str(item.duration) + ", 0")
                #f.write("%s\n" % item)
                f.write(item.activity + ", " + str(item.above) + ", "+str(item.over) + ", " + str(item.duration) + ", 0" + "\n")
            
    except KeyboardInterrupt:
        ser.close()
    finally:
        ser.close()

def start_peak_count_analysis(min_count, max_count, static_time, threshold):
    peak_time_map = [-1, 0, 0]
    while True:
        voltage = ser.readline()
        voltage= voltage.rstrip().decode('utf-8','ignore')
        try:
            voltage = int(voltage)
            curr_time = time.time_ns()
            if voltage > 500 or voltage < 100:
                continue
            if voltage > threshold:
                print(peak_time_map)
                if peak_time_map[0]  < 0:
                    peak_time_map[0] = time.time_ns()
                    peak_time_map[1] = 1
                    peak_time_map[2] = voltage
                else:
                    if curr_time - peak_time_map[0] > static_time:
                       peak_time_map[1] = 0 
                    peak_time_map[0] = curr_time
                    peak_time_map[1] = peak_time_map[1] + 1
                    peak_time_map[2] = voltage
            else:
                if peak_time_map[0] > 0 and curr_time - peak_time_map[0] > static_time:
                    #print("diff " + str(curr_time - peak_time_map[0]))
                    if peak_time_map[1] > min_count and peak_time_map[1] < max_count:
                        #print(peak_time_map)
                        print("Fall detected !!!")
                        sleep(5)
                    peak_time_map[0] = -1
                    peak_time_map[1] = 0
        except ValueError:
                pass

combined_data_file = "A:\CC\experiment\\fall-detection-project-code\collecting-test-data\processed\scaled_down_119.csv"

combined_test_file = "A:\\CC\\experiment\\fall-detection-project-code\\collecting-test-data\\test\\scaled_down_114.csv"

#train_x, train_y = get_train_data(combined_data_file)

#test_x, test_y = get_test_data(combined_test_file)




#clf = RandomForestClassifier(n_estimators=1000)
#print("len of train x " + str(len(train_x)))
#print("len of train y " + str(len(train_y)))
#print("len of test x " + str(len(test_x)))
#print("len of test y " + str(len(test_y)))
#clf.fit(train_x, train_y)
#print("Accuracy on training set is : {}".format(clf.score(train_x, train_y)))
#print("Accuracy on test set is : {}".format(clf.score(test_x, test_y)))
#test_y_pred = clf.predict(test_x)
#filename = "random_forest.sav"
#pickle.dump(clf, open(filename, 'wb'))

# start_analysing_data(clf)


#start_peak_determining_algo(164)

min_count = 0
max_count = 2
static_time = 40000
#threshold = 148 # for 140 base
threshold = 103

ser = serial.Serial('COM4', baudrate=115200)

try:
    start_peak_determining_algo_with_duration(threshold)
    #start_peak_determining_algo(threshold)
    #start_peak_count_analysis(min_count, max_count, static_time, threshold)
except KeyboardInterrupt:
    ser.close()
finally:
    ser.close()