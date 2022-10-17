# FantasySportsScraper
Credit to leesharpe (Github) for his scraped NFL roster data used in this scraping/cleaning project.
This a prototype which constructs data frames for NFL QBs from 2010 through 2019 regular seasons.
The last file combine_player_stat_roster.py be easily modified to clean/build data frames for the remaining positions that were scraped.

scraping/upload
=============================
schedule_scraper.py,
player_stat_scraper.py,
player_roster_import.py

combining data frames from scraped/imported data
=============================
combine_player_stat_roster.py

The dataframe 'dfqb' contains the player's name, stats by week (2010-2019), and a 1 or 0 in the last column indicating whether they had home field advantage.
