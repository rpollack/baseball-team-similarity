import csv
import pandas as pd
from math import isnan
import os
from sys import exit

def compareTeams(runsScored1, runsScored2, runsA1, runsA2, strikeouts1, strikeouts2, hrHit1, hrHit2, walks1, walks2, strikeoutsA1, strikeoutsA2, walksA1, walksA2, hrA1, hrA2):
    '''
    Compares the stats of two teams and calculates how similar the teams are.
    '''
    startingScore = 1000
    runsScoredDivisor = 10 # the differential in runs scored that causes a one-point drop in similarity score between two teams
    runsADivisor = 10
    pointsOffRunsScored = int(abs(runsScored1 - runsScored2)/runsScoredDivisor)
    pointsOffRunsA = int(abs(runsA1 - runsA2)/runsADivisor)
    pointsOffSO = abs(strikeouts1-strikeouts2)
    pointsOffHR = abs(hrHit1-hrHit2)
    pointsOffBB = abs(walks1-walks2)
    pointsOffSOA = abs(strikeoutsA1 - strikeoutsA2)
    pointsOffBBA = abs(walksA1 - walksA2)
    pointsOffHRA = abs(hrA1 - hrA2) 
    totalPointsOff = pointsOffRunsScored + pointsOffRunsA + pointsOffSO + pointsOffHR + pointsOffBB + pointsOffSOA + pointsOffBBA + pointsOffHRA
    similarityScore = startingScore - totalPointsOff 
    return similarityScore

def getTeamInfo(years, teamNames, runsScored, runsA, SO, HR, BB, SOA, BBA, HRA, G, index):
    '''
    Returns team information contained in the arrays that represent the database. All stats are proportioned to a 162-game season.
    '''
    fullSeason = 162 # number of games in a full season
    year = years[index]
    team = teamNames[index]
    gamesPlayed = G[index]
    gamesRatio = float(fullSeason)/float(gamesPlayed)
    runsScored = int(runsScored[index] * gamesRatio) # converts partial seasons to 162-game ones
    runsAllowed = int(runsA[index] * gamesRatio)
    if isnan(SO[index]): #lahman's DB doesn't have SO numbers for many years. if we don't set them to 0, they'll come up as NaN which will screw up the calculations.
        strikeouts = 0
    else:
        strikeouts = int(SO[index] * gamesRatio)
    hrHit = int(HR[index] * gamesRatio)
    walks = int(BB[index] * gamesRatio)
    strikeoutsA = int(SOA[index] * gamesRatio)
    walksA = int(BBA[index] * gamesRatio)
    hrA = int(HRA[index] * gamesRatio)
    return year, team, runsScored, runsAllowed, strikeouts, hrHit, walks, strikeoutsA, walksA, hrA

def readDatabase(datafile):
    '''
    Read data from the Lahman database file.
    '''
    try:
        df = pd.read_csv(dataFile)
        #Get teams' info
        years = df.yearID
        numSeasons = len(years)
        teamNames = df.name
        G = df.G # number of games played that season
        #Get pythagorean stats
        runsScored = df.R
        runsA = df.RA
        #Get FIP stats for offense
        BB = df.BB # walks by offense
        SO = df.SO # strikeouts by offense
        HR = df.HR # home runs by offense
        #Get FIP stats for pitchers
        BBA = df.BBA # walks allowed by pitchers
        SOA = df.SOA # strikeouts by pitchers
        HRA = df.HRA # home runs allowed by pitchers
        return years, numSeasons, teamNames, G, runsScored, runsA, BB, SO, HR, BBA, SOA, HRA
    except Exception as e:
        exit("Error reading from %s: %s" % (dataFile, e))

def createOutputFiles(years, teamNames, numSeasons):
    '''
    Creates the .csv files that will hold the results of comparing each team to the rest.
    '''
    for i in range (0, numSeasons):
        year = years[i]
        teamName = teamNames[i]
        teamName = teamName.replace('/', '-')
        # deal with filename "1884 Chicago/Pittsburgh (Union League).csv"
        teamSeasonFile = str(year) + " " + teamName + '.csv'
        resultFile = os.path.join(dir, teamSeasonFile)
        try:
            f = open(resultFile,'w')
            writer = csv.writer(f)
            writer.writerow(header)
            f.close()
        except Exception as e:
            print "Error working with %s: %s" % (resultFile, e)

dataFile = "lahman/Teams.csv"
years, numSeasons, teamNames, G, runsScored, runsA, BB, SO, HR, BBA, SOA, HRA = readDatabase(dataFile)

header = ["comparedTeam", "simscore"]
dir = "results/"
if not os.path.exists(dir): # create results directory if it doesn't exist already 
    os.makedirs(dir)

createOutputFiles(years, teamNames, numSeasons)

# compare teams, calculate scores, and write the scores to a file    
for j in range (0, numSeasons):
        year1, team1, runsScored1, runsA1, strikeouts1, hrHit1, walks1, strikeoutsA1, walksA1, hrA1 = getTeamInfo(years, teamNames, runsScored, runsA, SO, HR, BB, SOA, BBA, HRA, G, j)
        id1 = str(year1) + ' ' + team1
        
        fileToOpen = os.path.join(dir, id1) + '.csv'
        print "Writing to %s." % fileToOpen # to track status
        try:
            f = open(fileToOpen, 'a')
            results = csv.writer(f)
            for k in range (0, numSeasons):
                year2, team2, runsScored2, runsA2, strikeouts2, hrHit2, walks2, strikeoutsA2, walksA2, hrA2 = getTeamInfo(years, teamNames, runsScored, runsA, SO, HR, BB, SOA, BBA, HRA, G, k)
                id2 = str(year2) + ' ' + team2                
                if (id1 != id2): # prevent comparing a team to itself
                    row = [] # start a blank row for a new comparison
                    row.append(id2) #add the comparison's team as the first column
                    simScore = compareTeams(runsScored1, runsScored2, runsA1, runsA2, strikeouts1, strikeouts2, hrHit1, hrHit2, walks1, walks2, strikeoutsA1, strikeoutsA2, walksA1, walksA2, hrA1, hrA2)
                    row.append(simScore)
                    results.writerow(row)
        except Exception as e:
            print "Error working with %s: %s" % (fileToOpen, e) 
        f.close() #we are done with team J's CSV file.       
