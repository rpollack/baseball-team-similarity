Team Similarity Score Calculator (need to come up with a clever acronym!)
Script by Ryan Pollack (http://www.ryanpollack.com)
- Adapted from Bill James' Similarity Scores method.
- "unusually/truly/basically/vaguely similar" language adapted from The Politics of Glory by Bill James (1994, p. 93) 
- Uses a modified version of Lahman's Baseball Database (http://www.seanlahman.com/baseball-archive/statistics/)

This script compares teams throughout history based on how much better/worse they were than that year's average for several statistics:
- Runs scored by the offense
- Strikeouts by batters
- Hits by batters
- Doubles by batters
- Triples by batters
- Home runs by batters
- Walks by batters
- Stolen bases by runners
- Runs allowed by pitching/defense
- Strikeouts by pitchers
- Hits allowed by pitchers
- Walks by pitchers
- Home runs allowed by pitchers
- Complete games by pitchers
- Shutouts by pitchers
- Errors committed by fielders

The result of each scoring is a number relative to 100, where 100 is the average team's performance *for that year*. Starting with a score of 1000 between each team, the algorithm subtracts 1 point for each point of difference between two teams. The number remaining is the similarity score between the two teams.

For example, if the 2008 Red Sox were 5% above average at something relative to 2008 and the 1963 Yankees were 10% above average at that same stat relative to 1963, the algorithm would compute abs(5-10) or 5 points to subtract from 1000 when it compared these two teams.  

The output of the scoring is a number of .csv files in the /results/ directory for each team-season. The script 'top10.py', also available in this repo, will go through each CSV file and pull out the top 10 scores. 

The input to this script is the Teams.csv file available from the Lahman database. It is expected to be located at 'lahman/Teams.csv' relative to this script. It's modified in a couple ways:
- The '2B' column is named 'D'. Python doesn't like variables that start with numbers.
- The '3B' column is named 'Trip'. Apparently python doesn't like the column to be named 'T'.
- The data is only available for the 1913 season and later. That's the first season for which the database has all the statistics (that the script uses) for all the teams.

Notes:
- Teams are not compared with themselves.
- The comparisons on Complete Games and Shutouts may need some tweaking. The differences can be huge. For example the 2011 Angels had 12 complete games vs. the MLB average of 6. This produces a score of (12/6)=200 for the complete game stat. Any team that threw an average number of complete games will end up with a score of 100; that team will have a 100-point difference from the 2011 Angels. That's probably too many points for just six complete games.  