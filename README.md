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

The output of this script is one .csv file for each team/season. For example, 2011 Baltimore Orioles.csv and 2012 Baltimore Orioles.csv. Currently all .csv file are stored in a "results" subdirectory which is created if it doesn't exist already.

Each .csv file has 2714 rows defining the similarity score between that team and all the others.

For example, 2011 Baltimore Orioles.csv might look like this:
2010 Texas Rangers, 857
2010 Washing Nationals, 857

... and so on.

Teams are not compared with themselves; that is, in 2012 Miami Marlins.csv, there is no line for 2012 Miami Marlins. But there is some duplication. For example, the score between the 2012 Chicago Cubs and 1978 Detroit Tigers will exist in both 2012 Chicago Cubs.csv and 1978 Detroit Tigers.csv.