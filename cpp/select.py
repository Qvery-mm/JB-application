import sys
import os
import csv
from time import sleep

dir = "Clones"
try:
    print("Specify threshold:")
    threshold = float(input())
except Exception as e:
    print(e)
    exit(-1)

with open("finalClones", "w") as output:
    with open("ClonesWithDistance", "r") as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            row[8] = float(row[8])
            if row[8] <= threshold:
                totalNumber+=1
                print(','.join(row[:-1]), file=output)
        print(totalNumber)
