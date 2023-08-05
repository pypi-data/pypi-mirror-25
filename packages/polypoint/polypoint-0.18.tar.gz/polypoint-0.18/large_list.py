from polypoint import polypoint
import time
import numpy as np
import pickle
import os
from random import shuffle
from pprint import pprint

point_list = []
answers = []

if os.path.exists('testing/large_point_list.pickle'):
    with open('testing/large_point_list.pickle', 'rb') as f:
        point_list = pickle.load(f)
if os.path.exists('testing/answers_list.pickle'):
    with open('testing/answers_list.pickle', 'rb') as f:
        answers = pickle.load(f)

if (len(point_list) == 0):
    with open("testing/uscities.txt") as f:
        for line in f:
            words = line.split(",")
            if words[3] in abbr:
                t = (float(words[5]), float(words[6][:-1]))
                point_list.append(t)
    with open('testing/large_point_list.pickle', 'wb') as f:
        pickle.dump(point_list, f)
if(len(answers) == 0):
    with open("testing/uscities.txt") as f:
        for line in f:
            words = line.split(",")
            if words[3] in abbr:
                t = (float(words[5]), float(words[6][:-1]))
                answers.append(abbr.index(words[3]))
    with open('testing/answers_list.pickle', 'wb') as f:
        pickle.dump(answers, f)

time_list = []
classifier = polypoint.PolygonClassifier()
beg = time.time()
classifier.initialize()
end = time.time()
print("Initialized in {} seconds. ".format(str(end - beg)))

for i in range(3):
    shuffle(point_list)
    classifier.initialize()
    beg = time.time()
    test_answers = classifier.match_points_to_polygon(point_list)
    end = time.time()
    time_list.append(end - beg)

min_time = min(time_list)

print(str(len(test_answers)) + " points in " + str(min_time) + " seconds.")
print(str(len(test_answers)/(min_time)) + " points per second.")
print("Zero-index of minimum time: " + str(time_list.index(min_time)) + " in array of length " + str(len(time_list)))
pprint(time_list)
