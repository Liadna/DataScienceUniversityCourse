import os
import csv
import string

chars = string.printable
punc = string.punctuation
letters = string.letters
digits = string.digits

speeches = {"obama": [], "bush": [], "clinton": []}

# Function receives a path to the folder containing 3 folders, one for each president
def create_csv(path):
    # Presidents folders
    presidents = {"obama" : "Obama_Speeches", "bush" : "Bush_Speeches", "clinton" : "Clinton_Speeches"}
    for key, value in presidents.iteritems():
        l = []
        # Create list of the speeches for each president
        for file_name in os.listdir(path + "\\" + value):
            with open(path + "\\" + value + "\\" + file_name) as f:
                # Remove extra spaces, tabs, newlines
                speech = " ".join(f.read().strip().split(" "))
                speech_clean = ""

                # Clear unwanted symbols, leave only letters/numbers and punctuation
                for c in speech:
                    if c in digits or c in letters or c in punc or c == ' ':
                        speech_clean += c
                l.append(speech_clean)
        speeches[key] = l

    # write data to csv file
    with open(path + "\data.csv", "wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=",")
        writer.writerow(["speech", "class"])
        for key, value in speeches.iteritems():
            for row in value:
                writer.writerow([row, key])




path = "D:\Programs\PythonWorkspace\DataScienceProject\PoliticalSpeeches"
create_csv(path)

