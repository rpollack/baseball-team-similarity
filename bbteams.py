import csv
import pandas as pd
from math import isnan
import os
from sys import exit
import numpy as np

def compareTeams(runsScored1, runsScored2, runsA1, runsA2, strikeouts1, strikeouts2, hrHit1, hrHit2, walks1, walks2, strikeoutsA1, strikeoutsA2, walksA1, walksA2, hrA1, hrA2, sb1, sb2, e1, e2):
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
    pointsOffSB = abs(sb1 - sb2)
    pointsOffE = abs(e1 - e2)
    totalPointsOff = pointsOffRunsScored + pointsOffRunsA + pointsOffSO + pointsOffHR + pointsOffBB + pointsOffSOA + pointsOffBBA + pointsOffHRA + pointsOffSB + pointsOffE
    similarityScore = startingScore - totalPointsOff 
    return similarityScore

def calcRelativeStats(team, average):
    '''
    For a stat, calculates a team's performance relative to the average for that year.
    '''
    return int(100*(float(team) / float(average)))

def getTeamInfo(years, teamNames, runsScored, runsA, SO, HR, BB, SOA, BBA, HRA, G, SB, E, avg, index):
    '''
    Returns team's stats relative to the average team of that year. This methodology allows us to fairly compare teams across years by accounting for changes in talent level, approach to the game, run scoring environment, and so on.
    
    For example, the 2008 Red Sox struck out 1068 times. The average team in 2008 struck out 1099 times. Therefore the Red Sox's relative stat is (100*(1068/1099)) or 97, meaning they struck out 97% as often as the average team. Put another way, the Red Sox struck out 3% less often than the average team.
    
    That's an example where fewer is better. For stats where more is better, you subtract 100 from the result instead of subtracting the result from 100. An example of where more is better is runs scored. The 2008 Red Sox scored 845 runs, whereas the average team scored 751. 100*(845/751) is 112, meaning they scored 112-100 or 12% more runs than the average team that year.
    
    This method does not take into account the strength of the AL vs. the NL. It just compares each team to all other teams in MLB.
    '''
    
    year = years[index]
    team = teamNames[index]
    
    runsScored = runsScored[index]
    runsScoredPlus = int(100*(float(runsScored)/ avg.get_value(year, 'R')))
    
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
    sbPlus = calcRelativeStats(hrHit, avgHRHit)
    
    walks = int(BB[index])
    avgWalks = int(avg.get_value(year, 'BB'))
    walksPlus = calcRelativeStats(walks, avgWalks)
    
    strikeoutsA = int(SOA[index])
    avgSOA = int(avg.get_value(year, 'SOA'))
    SOAPlus = calcRelativeStats(SOA, avgSOA)
    
    walksA = int(BBA[index])
    avgWalksA = int(avg.get_value(year, 'BBA'))
    walksAPlus = calcRelativeStats(walksA, walksAPlus)
    
    hrA = int(HRA[index])
    avgHRA = int(avg.get_value(year, 'HRA'))
    HRAPlus = calcRelativeStats(hrA, avgHRA)
    
    return year, team, runsScoredPlus, runsAllowedPlis, strikeoutsPlus, hrHitPlus, walksPlus, strikeoutsAPlus, walksAPlus, HRAPlus, sbPlus, errorsPlus

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
        #Get stolen bases
        SB = df.SB
        #Get errors
        E = df.E
        
        #Compute annual averages for all the stats we care about
        grouped = df.groupby('yearID')
        avg = grouped.agg({'BB': np.mean, 'SO': np.mean, 'R':np.mean, 'RA': np.mean, 'HR': np.mean, 'BBA': np.mean, 'SOA': np.mean, 'HRA': np.mean, 'SB':np.mean, 'E':np.mean})
        
        return years, numSeasons, teamNames, G, runsScored, runsA, BB, SO, HR, BBA, SOA, HRA, SB, E, avg
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
years, numSeasons, teamNames, G, runsScored, runsA, BB, SO, HR, BBA, SOA, HRA, SB, E, avg = readDatabase(dataFile)

header = ["comparedTeam", "simscore"]
dir = "results/"
if not os.path.exists(dir): # create results directory if it doesn't exist already 
    os.makedirs(dir)

createOutputFiles(years, teamNames, numSeasons)

# compare teams, calculate scores, and write the scores to a file    
for j in range (0, numSeasons):
        year1, team1, runsScored1, runsA1, strikeouts1, hrHit1, walks1, strikeoutsA1, walksA1, hrA1, sb1, e1 = getTeamInfo(years, teamNames, runsScored, runsA, SO, HR, BB, SOA, BBA, HRA, G, SB, E, avg, j)
        id1 = str(year1) + ' ' + team1
        fileToOpen = os.path.join(dir, id1) + '.csv'
        try:
            # Open Team J's results file for writing
            f = open(fileToOpen, 'a')
            results = csv.writer(f)
            for k in range (0, numSeasons):
                year2, team2, runsScored2, runsA2, strikeouts2, hrHit2, walks2, strikeoutsA2, walksA2, hrA2, sb2, e2 = getTeamInfo(years, teamNames, runsScored, runsA, SO, HR, BB, SOA, BBA, HRA, G, SB, E, k)
                id2 = str(year2) + ' ' + team2                
                if (id1 != id2): # prevent comparing a team to itself
                    row = [] # start a blank row for a new comparison
                    row.append(id2) #add the comparison team as the first column
                    simScore = compareTeams(runsScored1, runsScored2, runsA1, runsA2, strikeouts1, strikeouts2, hrHit1, hrHit2, walks1, walks2, strikeoutsA1, strikeoutsA2, walksA1, walksA2, hrA1, hrA2, sb1, sb2, e1, e2)
                    row.append(simScore)
                    results.writerow(row)
        except Exception as e:
            print "Error working with %s: %s" % (fileToOpen, e) 
        f.close() #we are done with team J's CSV file.       
