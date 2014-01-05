Team Similarity Score Calculator (need to come up with a clever acronym!)
Script by Ryan Pollack (http://www.ryanpollack.com)
Adapted from Bill James' Similarity Scores method. 
Uses Lahman's Baseball Database (http://www.seanlahman.com/baseball-archive/statistics/)

Starts with 1000 points between each team
For offense, we then subtract:
	1 point for every difference of 10 runs scored. The reason is that every 10 runs is roughly one win.
	1 point for every 1 strikeout
	1 point for every 1 walk
	1 point for every 1 home run
	
For defense, we then subtract:
	1 point for every difference of 10 runs allowed. Same reason as above for the runs scored.
	1 point for every 1 strikeout allowed
	1 point for every 1 walk allowed
	1 point for every 1 home run allowed

The output of this script is one .csv file for each team/season. For example, 2011 Baltimore Orioles.csv and 2012 Baltimore Orioles.csv.

Each .csv file has 2714 rows defining the similarity score between that team and all the others.

For example, 2011 Baltimore Orioles.csv might look like this:
2010 Texas Rangers, 857
2010 Washing Nationals, 857

... and so on.