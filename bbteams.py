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
teamName = df.name
gamesPlayed = df.G # for normalizing all stats to 162-game season 
#Get pythagorean stats
runsScored = df.R
runsAllowed = df.RA
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

comparedTeams = [] # the list that holds team comparisons to prevent duplicate comparisons
noCompares = 0 # count the number of comparisons we DON'T make for whatever reason
compares = 0# count the number of comparisons we DO make


def getTeamInfo(years, teamName, runsScored, runsAllowed, SO, HR, BB, SOA, BBA, HRA, index):
    '''
    Returns team information contained in the arrays that represent the database.
    '''
    year = years[index]
    team = teamName[index]
    runsScored = runsScored[index] # converts partial seasons to 162-game ones
    runsAllowed = runsAllowed[index]
    if math.isnan(SO[index]): #lahman's DB doesn't have SO numbers for many years. if we don't set them to 0, they'll come up as NaN which will screw up the calculations.
        strikeouts = 0
    else:
        strikeouts = int(SO[index]) # for some reason, SOs are being read as floats. force them to ints here.
    hrHit = HR[index]
    walks = BB[index]
    strikeoutsAllowed = SOA[index]
    walksAllowed = BBA[index]
    hrAllowed = HRA[index]
    return year, team, runsScored, runsAllowed, strikeouts, hrHit, walks, strikeoutsAllowed, walksAllowed, hrAllowed

def needToCompare(year1, team1, year2, team2, comparedTeams):
    '''
    Given teams A and B, returns True if we have already compared team B to team A or if Team A == Team B.
    '''
    doCompare = True # by default assume we need to compare the teams
    if (year1 == year2) and (team1 == team2): # prevent comparing a team against itself
        doCompare = False
    else:
        # teams are unique, but see if we've already compared them
        for c in comparedTeams:
            if (year1 == c[0] and team1 == c[1]) or (year1 == c[2] and team1 == c[3]):
                # print "%s %s was found." % (year1, team1)
                # team1 was found in the list.
                if (year2 == c[0] and team2 == c[1]) or (year2 == c[2] and team2 == c[3]):
                    #team 2 was also found in the list. We've already made this comparison.
                    # don't need to compare
                    doCompare = False
    return doCompare        

def calcSimilarity(runsScored1, runsScored2, runsAllowed1, runsAllowed2, strikeouts1, strikeouts2, hrHit1, hrHit2, walks1, walks2, strikeoutsAllowed1, strikeoutsAllowed2, walksAllowed1, walksAllowed2, hrAllowed1, hrAllowed2):
    startingScore = 1000
    runsScoredDivisor = 10 # the differential in runs scored that causes a one-point drop in similarity score between two teams
    runsAllowedDivisor = 10
    pointsOffRunsScored = int(abs(runsScored1 - runsScored2)/runsScoredDivisor)
    pointsOffRunsAllowed = int(abs(runsAllowed1 - runsAllowed2)/runsAllowedDivisor)
    pointsOffSO = abs(strikeouts1-strikeouts2)
    pointsOffHR = abs(hrHit1-hrHit2)
    pointsOffBB = abs(walks1-walks2)
    pointsOffSOAllowed = abs(strikeoutsAllowed1 - strikeoutsAllowed2)
    pointsOffBBAllowed = abs(walksAllowed1 - walksAllowed2)
    pointsOffHRAllowed = abs(hrAllowed1 - hrAllowed2) 
    totalPointsOff = pointsOffRunsScored + pointsOffRunsAllowed + pointsOffSO + pointsOffHR + pointsOffBB + pointsOffSOAllowed + pointsOffBBAllowed + pointsOffHRAllowed
    similarityScore = startingScore - totalPointsOff
    return similarityScore

#open file that will contain the results
resultFile = "similarityscores.csv"
f = open(resultFile,'w')
header = ["year1", "team1", "year2", "team2", "R1", "R2", "RA1", "RA2", "BB1", "BB2", "SO1", "SO2", "HR1", "HR2", "BBA1", "BBA2", "SOA1", "SOA2", "HRA1", "HRA2", "simscore"]
writer = csv.writer(f)
writer.writerow(header)

for i in range (0, numSeasons):    
    # get the data for the first team
    year1, team1, runsScored1, runsAllowed1, strikeouts1, hrHit1, walks1, strikeoutsAllowed1, walksAllowed1, hrAllowed1 = getTeamInfo(years, teamName, runsScored, runsAllowed, SO, HR, BB, SOA, BBA, HRA, i)

    for j in range (0, numSeasons):
        #get the info to find out whether we need to compare the teams
        team2 = teamName[j]
        year2 = years[j]
        
        if needToCompare(year1, team1, year2, team2, comparedTeams):
                # get rest of data for Team 2
            year2, team2, runsScored2, runsAllowed2, strikeouts2, hrHit2, walks2, strikeoutsAllowed2, walksAllowed2, hrAllowed2 = getTeamInfo(years, teamName, runsScored, runsAllowed, SO, HR, BB, SOA, BBA, HRA, j)

            similarityScore = calcSimilarity(runsScored1, runsScored2, runsAllowed1, runsAllowed2, strikeouts1, strikeouts2, hrHit1, hrHit2, walks1, walks2, strikeoutsAllowed1, strikeoutsAllowed2, walksAllowed1, walksAllowed2, hrAllowed1, hrAllowed2)
                
            similarityData = [year1, team1, year2, team2, runsScored1, runsScored2, runsAllowed1, runsAllowed2, walks1, walks2, strikeouts1, strikeouts2, hrHit1, hrHit2, walksAllowed1, walksAllowed2, strikeoutsAllowed1, strikeoutsAllowed2, hrAllowed1, hrAllowed2, similarityScore]
            writer.writerow(similarityData)
            
            #store year1/team1 and year2/team2 in a list of already-compared teams
            justCompared = [year1, team1, year2, team2]
            comparedTeams.append(justCompared)
            compares += 1
        else:
            noCompares += 1

print "\nComplete. %s comparisons and % skipped." % (compares, noCompares)
f.close()
            
#account for different-length seasons & convert to 162-game seasons (linear regression?)
#for each team, find the top 10 most similar teams and display the data that went into it