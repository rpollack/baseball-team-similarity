import csv
import pandas as pd
import math
import os

'''
Team Similarity Score Calculator (need to come up with a clever acronym)
Starts with 1000 points between each team
Subtracts:
	Offense:
	1 point for every difference of 10 runs scored
	1 point for every 1 strikeout
	1 point for every 1 walk
	1 point for every 1 home run
	
	Defense/Pitching:
	1 point for every difference of 10 runs allowed
	1 point for every 1 strikeout allowed
	1 point for every 1 walk allowed
	1 point for every 1 home run allowed

Adapted from Bill James' Similarity Scores method. 
Uses Lahman's Baseball Database (http://www.seanlahman.com/baseball-archive/statistics/)
'''

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

def getTeamInfo(years, teamNames, runsScored, runsA, SO, HR, BB, SOA, BBA, HRA, index):
    '''
    Returns team information contained in the arrays that represent the database.
    '''
    year = years[index]
    team = teamNames[index]
    runsScored = runsScored[index] # converts partial seasons to 162-game ones
    runsAllowed = runsA[index]
    if math.isnan(SO[index]): #lahman's DB doesn't have SO numbers for many years. if we don't set them to 0, they'll come up as NaN which will screw up the calculations.
        strikeouts = 0
    else:
        strikeouts = int(SO[index]) # for some reason, SOs are being read as floats. force them to ints here.
    hrHit = HR[index]
    walks = BB[index]
    strikeoutsA = SOA[index]
    walksA = BBA[index]
    hrA = HRA[index]
    return year, team, runsScored, runsAllowed, strikeouts, hrHit, walks, strikeoutsA, walksA, hrA

dataFile = "lahman/Teams.csv"
#open Teams database file
df = pd.read_csv(dataFile)
#Get teams' info
years = df.yearID
teamNames = df.name
gamesPlayed = df.G # for normalizing all stats to 162-game season 
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

numSeasons = len(years)
header = ["comparedTeam", "simscore"]
dir = "results/"

# create one CSV file for each team/season & write the standard header to it
for i in range (0, numSeasons):
    year = years[i]
    teamName = teamNames[i]
    teamName.replace('/', '-')
    teamSeasonFile = str(year) + " " + teamName + '.csv'
    resultFile = os.path.join(dir, teamSeasonFile)
    try:
        f = open(resultFile,'w')
        writer = csv.writer(f)
        writer.writerow(header)
        f.close()
    except Exception as e:
        print "Error working with %s: %s" % (resultFile, e)

# compare teams, calculate scores, and write the scores to a file    
for j in range (0, numSeasons):
        year1, team1, runsScored1, runsA1, strikeouts1, hrHit1, walks1, strikeoutsA1, walksA1, hrA1 = getTeamInfo(years, teamNames, runsScored, runsA, SO, HR, BB, SOA, BBA, HRA, j)
        id1 = str(year1) + ' ' + team1
        fileToOpen = os.path.join(dir, id1) + '.csv'
        print "Writing to %s." % fileToOpen # to track status
        try:
            f = open(fileToOpen, 'a')
            results = csv.writer(f)
            for k in range (0, numSeasons):
                year2, team2, runsScored2, runsA2, strikeouts2, hrHit2, walks2, strikeoutsA2, walksA2, hrA2 = getTeamInfo(years, teamNames, runsScored, runsA, SO, HR, BB, SOA, BBA, HRA, k)
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