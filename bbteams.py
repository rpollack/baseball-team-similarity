import csv
import pandas as pd
import sys
import math
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

#open Teams database file
df = pd.read_csv('lahman/Teams.csv')

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
numCompares = numSeasons * (numSeasons -1) #the total number of comparisons we do, comparing each team against every other team but itself

comparedTeams = [] # initialize the list that holds team comparisons to prevent duplicate comparisons

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

def needToCompare(yearA, teamA, yearB, teamB, comparedTeams):
    '''
    Given teams A and B, returns True if we have already compared team B to team A or if Team A == Team B.
    '''
    doCompare = True # by default assume we need to compare the teams
    seasonA = str(yearA) + teamA 
    seasonB = str(yearB) + teamB
    
    if seasonA == seasonB: # prevent comparing a team-year against itself
        doCompare = False
    else:
        # teams are unique, but see if we've already compared them
        for c in comparedTeams:
            if seasonA == c[0]:
                if seasonB == c[1]:
                     doCompare = False
            elif seasonA == c[1]:
                if seasonB == c[0]:
                     doCompare = False
    if doCompare:
        print "Comparing %s and %s." % (seasonA, seasonB)
    else:
        print "Skipping unnecessary comparison."
    return doCompare        

def calcSimilarity(runsScored1, runsScored2, runsA1, runsA2, strikeouts1, strikeouts2, hrHit1, hrHit2, walks1, walks2, strikeoutsA1, strikeoutsA2, walksA1, walksA2, hrA1, hrA2):
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

#open file that will contain the results
resultFile = "similarityscores.csv"
f = open(resultFile,'w')
header = ["year1", "team1", "year2", "team2", "R1", "R2", "RA1", "RA2", "BB1", "BB2", "SO1", "SO2", "HR1", "HR2", "BBA1", "BBA2", "SOA1", "SOA2", "HRA1", "HRA2", "simscore"]
writer = csv.writer(f)
writer.writerow(header)

for i in range (0, numSeasons):    
    year1, team1, runsScored1, runsA1, strikeouts1, hrHit1, walks1, strikeoutsA1, walksA1, hrA1 = getTeamInfo(years, teamNames, runsScored, runsA, SO, HR, BB, SOA, BBA, HRA, i)
    for j in range (0, numSeasons):
        #get the info to find out whether we need to compare the teams
        team2 = teamNames[j]
        year2 = years[j]
        if needToCompare(year1, team1, year2, team2, comparedTeams):
            # get all data for Team 2
            year2, team2, runsScored2, runsA2, strikeouts2, hrHit2, walks2, strikeoutsA2, walksA2, hrA2 = getTeamInfo(years, teamNames, runsScored, runsA, SO, HR, BB, SOA, BBA, HRA, j)
            similarityScore = calcSimilarity(runsScored1, runsScored2, runsA1, runsA2, strikeouts1, strikeouts2, hrHit1, hrHit2, walks1, walks2, strikeoutsA1, strikeoutsA2, walksA1, walksA2, hrA1, hrA2)  
            similarityData = [year1, team1, year2, team2, runsScored1, runsScored2, runsA1, runsA2, walks1, walks2, strikeouts1, strikeouts2, hrHit1, hrHit2, walksA1, walksA2, strikeoutsA1, strikeoutsA2, hrA1, hrA2, similarityScore]
            writer.writerow(similarityData)
            
            # store year1/team1 and year2/team2 in a list of already-compared teams
            justCompared = [str(year1) + team1, str(year2) + team2]
            comparedTeams.append(justCompared)
print "Complete."
f.close()
            
#account for different-length seasons & convert to 162-game seasons (linear regression?)
#for each team, find the top 10 most similar teams and display the data that went into it