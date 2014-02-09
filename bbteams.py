import csv
import pandas as pd
from math import isnan
import os
from sys import exit
import numpy as np

'''
offense, add:

hits
doubles
triples
slugging %
avg
(calc OBP?)

pitching, add:
hits allowed
shutouts
CG
'''


def calcRelativeStats(team, average):
    '''
    For a stat, calculates a team's performance relative to the average for that year.
    
    For example, the 2008 Red Sox struck out 1068 times. The average team in 2008 struck out 1099 times. Therefore the Red Sox's relative stat is (100*(1068/1099)) or 97, meaning they struck out 97% as often as the average team. Put another way, the Red Sox struck out 3% less often than the average team.
    '''
    return int(100*(float(team) / float(average)))

def compareTeams(runsScored1, runsScored2, runsA1, runsA2, strikeouts1, strikeouts2, hrHit1, hrHit2, walks1, walks2, strikeoutsA1, strikeoutsA2, walksA1, walksA2, hrA1, hrA2, sb1, sb2, e1, e2, hits1, hits2, doubles1, doubles2, triples1, triples2):
    '''
    Compares the stats of two teams and calculates how similar the teams are.
    '''
    startingScore = 1000

    pointsOffRunsScored = int(abs(runsScored1 - runsScored2))
    pointsOffRunsA = int(abs(runsA1 - runsA2))
    pointsOffSO = abs(strikeouts1-strikeouts2)
    pointsOffHR = abs(hrHit1-hrHit2)
    pointsOffBB = abs(walks1-walks2)
    pointsOffSOA = abs(strikeoutsA1 - strikeoutsA2)
    pointsOffBBA = abs(walksA1 - walksA2)
    pointsOffHRA = abs(hrA1 - hrA2) 
    pointsOffSB = abs(sb1 - sb2)
    pointsOffE = abs(e1 - e2)
    pointsOffHits = abs(hits1-hits2)
    pointsOffDoubles = abs(doubles1-doubles2)
    pointsOffTriples = abs(triples1-triples2)
    totalPointsOff = pointsOffRunsScored + pointsOffRunsA + pointsOffSO + pointsOffHR + pointsOffBB + pointsOffSOA + pointsOffBBA + pointsOffHRA + pointsOffSB + pointsOffE + pointsOffHits + pointsOffDoubles + pointsOffTriples
    similarityScore = startingScore - totalPointsOff 
    return similarityScore


def getTeamInfo(years, teamNames, runsScored, H, doubles, triples, runsA, SO, HR, BB, SOA, BBA, HRA, SB, E, avg, index):
    '''
    Returns team's stats relative to the average team of that year. This methodology allows us to fairly compare teams across years by accounting for game-wide changes in offense and defense.
    This method does not take into account the strength of the AL vs. the NL. It just compares each team to all other teams in MLB that year.
    '''
    year = years[index]
    team = teamNames[index]
    
    hits = H[index]
    avgHits = int(avg.get_value(year, 'H'))
    hitsPlus = calcRelativeStats(hits, avgHits)
    
    twoBaggers = doubles[index]
    avgDoubles = int(avg.get_value(year, 'D'))
    doublesPlus = calcRelativeStats(twoBaggers, avgDoubles)
  
    threeBaggers = triples[index]
    avgTriples = int(avg.get_value(year, 'Trip'))
    triplesPlus = calcRelativeStats(threeBaggers, avgTriples)
    
    runsScored = runsScored[index]
    avgRunsScored = int(avg.get_value(year, 'R'))
    runsScoredPlus = calcRelativeStats(runsScored, avgRunsScored)
    
    runsAllowed = int(runsA[index])
    avgRunsAllowed = int(avg.get_value(year, 'RA'))
    runsAllowedPlus = calcRelativeStats(runsAllowed, avgRunsAllowed)
    
    errors = int(E[index])
    avgErrors = int(avg.get_value(year, 'E'))
    errorsPlus = calcRelativeStats(errors, avgErrors)
    
    if isnan(SO[index]): #lahman's DB doesn't have SO numbers for many years. if we don't set them to 0, they'll come up as NaN which will screw up the calculations.
        strikeoutsPlus = 0
    else:
        strikeouts = int(SO[index])
        avgStrikeouts = int(avg.get_value(year, 'SO'))
        strikeoutsPlus = calcRelativeStats(strikeouts, avgStrikeouts)
        
    if isnan(SB[index]):
        sbPlus = 0
    else:
        sb = int(SB[index])
        avgSB = int(avg.get_value(year, 'SB'))
        sbPlus = calcRelativeStats(sb, avgSB)

    hrHit = int(HR[index])
    avgHRHit = int(avg.get_value(year, 'HR'))
    hrHitPlus = calcRelativeStats(hrHit, avgHRHit)
    
    walks = int(BB[index])
    avgWalks = int(avg.get_value(year, 'BB'))
    walksPlus = calcRelativeStats(walks, avgWalks)
    
    strikeoutsA = int(SOA[index])
    avgSOA = int(avg.get_value(year, 'SOA'))
    SOAPlus = calcRelativeStats(strikeoutsA, avgSOA)
    
    walksA = int(BBA[index])
    avgWalksA = int(avg.get_value(year, 'BBA'))
    walksAPlus = calcRelativeStats(walksA, avgWalksA)
    
    hrA = int(HRA[index])
    avgHRA = int(avg.get_value(year, 'HRA'))
    HRAPlus = calcRelativeStats(hrA, avgHRA)
    
    return year, team, runsScoredPlus, hitsPlus, doublesPlus, triplesPlus, runsAllowedPlus, strikeoutsPlus, hrHitPlus, walksPlus, SOAPlus, walksAPlus, HRAPlus, sbPlus, errorsPlus

def readDatabase(datafile):
    '''
    Read data from the Lahman database file.
    
    Note that I had to rename the 2B and 3B columns to D and T, respectively. Python doesn't like identifiers that start with numbers.
    '''
    try:
        df = pd.read_csv(dataFile)
        #Get teams' info
        years = df.yearID
        numSeasons = len(years)
        teamNames = df.name
        #Get pythagorean stats
        runsScored = df.R
        runsA = df.RA
        #Get stats for offense
        H = df.H
        doubles = df.D
        #print doubles.dtypes
        triples = df.Trip
        '''
        #reading as series but I want it as a data frame!?
        #print "BLAH"
        #print triples.dtypes
        #triples = triples.astype(int, copy=False)
        #print "TRIPLES:::"
        ##print triples
        #raw_input()
        '''
        BB = df.BB # walks by offense
        SO = df.SO # strikeouts by offense
        HR = df.HR # home runs by offense
        #Get FIP stats for pitchers
        BBA = df.BBA # walks allowed by pitchers
        SOA = df.SOA # strikeouts by pitchers
        HRA = df.HRA # home runs allowed by pitchers
        #Get stolen bases
        SB = df.SB
        #Get errors
        E = df.E
        
        #Compute annual averages for all the stats we care about
        grouped = df.groupby('yearID')
        avg = grouped.agg({'BB': np.mean, 'SO': np.mean, 'R':np.mean, 'RA': np.mean, 'HR': np.mean, 'BBA': np.mean, 'SOA': np.mean, 'HRA': np.mean, 'SB':np.mean, 'E':np.mean, 'D':np.mean, 'Trip':np.mean, 'H':np.mean})
        
        return years, numSeasons, teamNames, runsScored, runsA, H, doubles, triples, BB, SO, HR, BBA, SOA, HRA, SB, E, avg
    except Exception as e:
        exit("Error reading from %s: %s" % (dataFile, e))

def createOutputFiles(years, teamNames, numSeasons):
    '''
    Creates the .csv files that will hold the results of comparing each team to the rest.
    '''
    for i in range (0, numSeasons):
        year = years[i]
        teamName = teamNames[i]
        if teamName == "Chicago/Pittsburgh (Union League)":
            # the / causes an error because the computer thinks it's a dir separator 
            teamName = "Chicago Pittsburgh (Union League)"
            teamNames.loc[i] = teamName
        teamSeasonFile = str(year) + " " + teamName + '.csv'
        resultFile = os.path.join(dir, teamSeasonFile)
        try:
            f = open(resultFile,'w')
            writer = csv.writer(f)
            writer.writerow(header)
            f.close()
        except Exception as e:
            print "Error creating %s: %s" % (resultFile, e)

dataFile = "lahman/Teams.csv"
years, numSeasons, teamNames, runsScored, runsA, H, doubles, triples, BB, SO, HR, BBA, SOA, HRA, SB, E, avg = readDatabase(dataFile)
header = ["comparedTeam", "simscore"]
dir = "results/"
if not os.path.exists(dir): # create results directory if it doesn't exist already 
    os.makedirs(dir)
createOutputFiles(years, teamNames, numSeasons)

# compare teams, calculate scores, and write the scores to a file    
for j in range (0, numSeasons):
        year1, team1, runsScored1, hits1, doubles1, triples1, runsA1, strikeouts1, hrHit1, walks1, strikeoutsA1, walksA1, hrA1, sb1, e1 = getTeamInfo(years, teamNames, runsScored, H, doubles, triples, runsA, SO, HR, BB, SOA, BBA, HRA, SB, E, avg, j)
        id1 = str(year1) + ' ' + team1
        print "Comparison team: %s" %id1
        fileToOpen = os.path.join(dir, id1) + '.csv'
        try:
            # Open Team J's results file for writing
            f = open(fileToOpen, 'a')
            results = csv.writer(f)
            for k in range (0, numSeasons):
                year2, team2, runsScored2, hits2, doubles2, triples2, runsA2, strikeouts2, hrHit2, walks2, strikeoutsA2, walksA2, hrA2, sb2, e2 = getTeamInfo(years, teamNames, runsScored, H, doubles, triples, runsA, SO, HR, BB, SOA, BBA, HRA, SB, E, avg, k)
                id2 = str(year2) + ' ' + team2                
                if (id1 != id2): # prevent comparing a team to itself
                    print "\tto %s" %id2
                    row = [] # start a blank row for a new comparison
                    row.append(id2) #add the comparison team as the first column
                    simScore = compareTeams(runsScored1, runsScored2, runsA1, runsA2, strikeouts1, strikeouts2, hrHit1, hrHit2, walks1, walks2, strikeoutsA1, strikeoutsA2, walksA1, walksA2, hrA1, hrA2, sb1, sb2, e1, e2, hits1, hits2, doubles1, doubles2, triples1, triples2)
                    row.append(simScore)
                    results.writerow(row)
        except Exception as e:
            print "Error opening %s: %s" % (fileToOpen, e) 
        f.close() #we are done with team J's CSV file.       
