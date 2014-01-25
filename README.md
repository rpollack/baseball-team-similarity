Team Similarity Score Calculator (need to come up with a clever acronym!)
Script by Ryan Pollack (http://www.ryanpollack.com)
Adapted from Bill James' Similarity Scores method. 
Uses Lahman's Baseball Database (http://www.seanlahman.com/baseball-archive/statistics/)

Starts with 1000 points between each team.
For offense, we then subtract points based on the differences in certain statistics:
	1 point for every difference of 10 runs scored. The reason is that every 10 runs is roughly one win.
	1 point for every difference of one strikeout
	1 point for every difference of one walk
	1 point for every home run hit
	1 point for every one stolen base
	
For pitching/defense, we then subtract:
	1 point for every difference of 10 runs allowed. Same reason as above for the runs scored.
	1 point for every strikeout allowed
	1 point for every walk allowed
	1 point for every home run allowed
	1 point for every error

All calculations are made using a 162-game equivalent season.

The input to this script is the Teams.csv file available from the Lahman database. It is expected to be located at 'lahman/Teams.csv' relative to this script.

The output of this script is one .csv file for each team/season. Each .csv file consists of rows defining the similarity score between that team and all the others. For example, 2011 Baltimore Orioles.csv might look like this:

comparedTeam,simScore
2010 Texas Rangers, 857
2010 Washington Nationals, 365

... and so on. Currently all .csv file are stored in a "results" subdirectory which is created if it doesn't exist already.


Teams are not compared with themselves; that is, in 2012 Miami Marlins.csv, there is no line for 2012 Miami Marlins. But there is some duplication. For example, the score between the 2012 Chicago Cubs and 1978 Detroit Tigers will exist in both 2012 Chicago Cubs.csv and 1978 Detroit Tigers.csv.