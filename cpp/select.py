import sys
import os
import csv
from time import sleep

dir = "Clones"
thereshold = 1.0
with open("finalClones" + str(thereshold), "w") as output:
    with open("ClonesWithDistance", "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            row[8] = float(row[8])
            if row[8] < thereshold:
                totalNumber+=1
                print(','.join(row[:-1]), file=output)
        print(totalNumber)
