Team Similarity Score Calculator
================================

Script by Ryan Pollack (http://www.ryanpollack.com)
- Adapted from Bill James' Similarity Scores method.
- "unusually/truly/basically/somewhat/vaguely similar" language and scoring adapted from *The Politics of Glory by Bill James* (1994, p. 93) 
- Uses a modified version of Lahman's Baseball Database (http://www.seanlahman.com/baseball-archive/statistics/)

Requirements
------------

- Python
- numpy
- pandas
- The CSV version of the Lahman DB, located at "lahman/Teams.csv" relative to this script, with some modifications:
    - The '2B' column is named 'D'. Python doesn't like variables that start with numbers.
    - The '3B' column is named 'Trip'. Apparently python doesn't like the column to be named 'T'.
    - Trimmed to 1913 and later. 1913 is the first season for which the database has all the statistics (that the script uses) for all the teams. The script should account for missing information by setting them to 0.



Overview
--------
This script compares teams throughout history based on how much better/worse they were than that year's average for several statistics:

Offense

- Runs scored by the offense
- Strikeouts by batters
- Singles by batters
- Doubles by batters
- Triples by batters
- Home runs by batters
- Walks by batters
- Stolen bases by runners

Pitching/Defense:

- Runs allowed by pitching/defense
- Strikeouts by pitchers
- Hits allowed by pitchers
- Walks allowed by pitchers
- Home runs allowed by pitchers
- Complete games by pitchers
- Shutouts by pitchers
- Errors committed by fielders

The result of each scoring is a number relative to 100, where 100 is the average team's performance *for that year*. Starting with a score of 1000 between each team, the algorithm subtracts 1 point for each point of difference between two teams. (Exception: it's every 2 points of difference for complete games.) The number remaining is the similarity score between the two teams.

Example
-------

For example, say the 2008 Red Sox compiled 5% more walks than the average team in 2008 and the 1963 Yankees compiled 20% fewer walks than the average team in 1963. The Red Sox's initial score would be 105 and the Yankees' score at that same stat would be 80.

In this situation, the algorithm would compute a difference of 25, which is 105-80. That's how far apart the 2008 Red Sox and 1963 Yankees are from each other on walks, based on how far apart they were from the average team in their own season. If each team were both 5% above average compared to their own year, the computed difference would be 0.

In this way, teams who outperform their year's average stats compare favorably with other teams who outperform their own year's averages. The net effect is to account for changes in how the game is played, how many games are in a season, and so on.

(Remember that for complete games, 1 point is taken off for every 2 points of difference.) 

Output
------
The script outputs a number of .csv files in the "results" directory (relative to the script). Each .csv file contains that team's comparison to all the other teams in the database. 

Finding the Most Similar Teams
------------------------------
The script 'top10.py', also available in this repo, goes through each CSV file and pulls out the top 10 scores for each team-season. This file stores its results in "results/top10" relative to the script. 

Notes
-----
- Run scripts with -v or --verbose to see printed status.
- Teams are not compared with themselves.
- The comparisons on Complete Games and Shutouts may need some tweaking. The differences can be huge. For example the 2011 Angels had 12 complete games vs. the MLB average of 6. This produces a score of (12/6)=200 for the complete game stat. Any team that threw an average number of complete games will end up with a score of 100; that team will have a 100-point difference from the 2011 Angels. That's probably too many points for just six complete games.  