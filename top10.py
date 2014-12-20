import csv
import pandas as pd
from os import listdir, path, makedirs
from os.path import exists, join, isfile
import argparse

parser = argparse.ArgumentParser(description='For each team, finds the top 10 most similar teams by sorting the list of results from bbteams.py.')
parser.add_argument('-v', '--verbose', dest='verbose', action='store_true',
                   default=False,
                   help='Enable verbose mode.')
args = parser.parse_args()

header = ["comparedTeam, simScore"] #for writing to the top 10 scores file

dir = "results"
files = [ f for f in listdir(dir) if isfile(join(dir,f)) ] # gets list of only files in /results/

top10dir = "top10"
newDir = path.join(dir, top10dir) # create /results/top10 which will hold the highscore files.

if not path.exists(newDir): # create /results/top10 directory if it doesn't exist already 
    makedirs(newDir)

for file in files:
    completePath = path.join(dir, file)
    df = pd.read_csv(completePath)
    teamName, sep, after = file.partition(".") # get the name of the team from the .csv filename
    scores = df.simscore
    teams = df.comparedTeam
    newList = []
    for i in range (0, 10):  
        m = scores.max() #find the maximum similarity score in the list
        maxIdx = scores.idxmax() # get the position of the maximum score
        team = teams[maxIdx] # find the team associated with the max score we just found
        maxVals = [team, m] # combine team name, similarity score
        if args.verbose:
            if m >= 950:
               print "%s and %s are unusually similar: %s" % (teamName, team, m)
            elif m >= 900:
                print "%s and %s are truly similar: %s" % (teamName, team, m)
            elif m >= 850:
                print "%s and %s are basically similar: %s" % (teamName, team, m)
            elif m >= 800:
                print "%s and %s are somewhat similar: %s" % (teamName, team, m)
            elif m >= 750:
                print "%s and %s are vaguely similar: %s" % (teamName, team, m)
        newList.append(maxVals) # add team name, similarity score to the list of the top 5 scores
        #remove previously-found value from lists so they won't be found again
        scores = scores.drop([maxIdx])
        teams = teams.drop([maxIdx])
    
    #write the highest teams/scores to a file
    top10File = teamName + "_top10.csv" # ex: 2010 Baltimore Orioles_top10.csv
    newPath = path.join(newDir, top10File)
    f = open(newPath,'w')
    writer = csv.writer(f)
    writer.writerow(header)
    for row in newList:
        writer.writerow(row)
    f.close()

#if the max we just found was equal to the max found before that, we will have to dig deeper in the list to get five scores (because there are some ties in the list)