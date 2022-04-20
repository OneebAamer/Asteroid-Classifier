import csv
import glob
import os
import math
import time
#IMPORTANT: place this file just outside of all training data files, where the training data will be kept in a file called "cartOrder"

#INPUT: csv file array converted into array.
avgUncertainty = '0.002'
start_time = time.time()
def convertInput(filename):
    asteroid = []
    with open(filename,newline = "") as csvfile:
        reader = csv.reader(csvfile, delimiter = ",", quotechar="|")
        for row in reader:
            if len(row) == 2:
                row.append(avgUncertainty)
            asteroid.append(row)
        asteroid.pop(0)
        csvfile.close()
    return asteroid
def find(asteroid,data, labels):
    category = "None"
    prevCategory = "None"
    print("Finding best fit...")
    minScore = float("inf")
    for i in range(0,len(data)):
        score = 0
        checked = False
        for j in range(0,len(data[i])):
            for k in range(0,len(asteroid)):
                try:
                    if float(asteroid[k][0]) == float(data[i][j][0]):
                        checked = True
                        score += abs(float(data[i][j][1]) - float(asteroid[k][1]))*(1+float(asteroid[k][2]) + float(data[i][j][2]))
                        if score > minScore:
                            break
                except ValueError:
                    continue
            else:
                continue
            break
        if checked == False:
            score = float("inf")
        elif score < minScore:
            minScore = score
            category = labels[i]
            if minScore < 1:
                p = abs((1-(minScore)) * 100)
            else:
                p = 0
            print(category +" "+ str(round(p,2)) +"%")
            print("Still processing...")
            if category == prevCategory:
                count += 1
                if count == 5:
                    minScore += 10
                    break
            else:
                prevCategory = category
                count = 0
            if minScore == 0:
                break
    p = abs((1-(minScore*100)) * 100)
    print("Final prediction: "+category +" "+ str(p) + "%")
    print("Program completed in: " + str(round(time.time() - start_time,2)) + "s")
    time.sleep(5)
            
#TRAIN DATA:
def train_data(folderLocation):
    values = []
    classify = []
    print("training algorithm...")

    for filename in glob.glob(folderLocation + "\*.tab"):
        classification = ""
        with open(os.path.join(os.getcwd(), filename), 'r') as f:
            text = f.read()
            text = text.split("\n")
            data = []
            for i in range(0,len(text)):
                text[i] = text[i].strip()
                text[i] = text[i].split("   ")
                if len(text[i]) == 2:
                    text[i].append(avgUncertainty)
                # Only adds useful data.
                if text[i] == ['']:
                    break
                else:
                    data.append(text[i])
            data.pop(0)
        values.append(data)
        with open(os.path.join(os.getcwd(),os.path.splitext(filename)[0]+ ".xml"),"r") as f:
            text = f.read()
            if "carbonaceous chondrite" in text.lower():
                classification = "C"
            elif "stony" in text.lower() or "silicate" in text.lower():
                classification = "S"
            else:
                classification = "X"
        classify.append(classification)
        f.close()
    print("Done")
    return values,classify
try:
    location = str(input("Enter the folder name containing the training data.\nEnsure it consists of the TAB and XML files for each meteorite: "))
    csvname = str(input("Enter the name of the csv file (no extension needed): "))
    target = convertInput(csvname + ".csv")
    spectra,classes = train_data(location)
    find(target,spectra,classes)
    print("Finished")
except FileNotFoundError:
    print("Not a valid file/folder, please make sure the file is in the same location as this script")
    time.sleep(2)
