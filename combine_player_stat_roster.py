# -*- coding: utf-8 -*-
"""
Author: Luke Galvan
Date: October 9th 2022
Project: Fantasy Football Scraper
Goal: Clean QB data, match QBs with their team's mascot name, determine if a player had homefield advantage during a game week.
Idea: We now have 3 data frames to work with.
This script uses our player stats data frame (player_stat_scraper.py), uploaded roster data (player_roster_import.py)
and schedule data (schedule_scraper.py)
"""
#import module
import pandas as pd

#filter roster data by qb position
df20_qb=df20[df20["position"] == 'QB']
df20_qb.reset_index(drop=True, inplace=True)

#remove percent symbol off roster %
df_qb['ROST']=df_qb['ROST'].str.strip('%')

#crucial step in speeding up the main loop where weekly player stats are matched with their team that year
df_qb = df_qb.sort_values(by=['Player','Year'], ascending = [True,True])
df_qb.reset_index(drop=True, inplace=True)

#remove extra characters from certain players to avoid errors in matching with teams
df_qb.loc[ df_qb['Player'] == 'Patrick Mahomes II','Player'] = 'Patrick Mahomes'
df_qb.loc[ df_qb['Player'] == 'Robert Griffin III','Player'] = 'Robert Griffin'

#find and remove QBs who played less than 16 career games - helps with discrepancies between scraped data and imported roster data
name_hold = df_qb['Player']
name_toremove=[]
for n in name_hold:
    if df_qb['Player'][df_qb['Player'] == n].count() < 16:
        name_toremove.append(n)

for n in name_toremove:
    df_qb = df_qb[df_qb['Player'] != n]
    df20_qb = df20_qb[df20_qb['full_name'] != n]

#check and remove any missing players between data frames
checkname = list(set(df_qb['Player']))
checkname20 = list(set(df20_qb['full_name']))
z = list(set(checkname) - set(checkname20))

#display(df_qb)
for n in z:
    df20_qb = df20_qb[df20_qb['full_name'] != n]
    df_qb = df_qb[df_qb['Player'] != n]
    
checkname = list(set(df_qb['Player']))
checkname20 = list(set(df20_qb['full_name']))
z2 = list(set(checkname20) - set(checkname))

for n in z2:
    df20_qb = df20_qb[df20_qb['full_name'] != n]
    df_qb = df_qb[df_qb['Player'] != n]

df_qb.reset_index(drop=True, inplace=True)
df20_qb.reset_index(drop=True, inplace=True)

#Begin first loop
#remove players for which we dont have both weekly fantasy stats and roster (namely their associated team) data for
df_qbind = []
i=0
j_ind = 0
for name in df20_qb['full_name']:
    k=0
    j=0
    while j < df_qb['Player'][df_qb['Player'] == name].count():
        if i > 0:
            if df20_qb['full_name'][i] == df20_qb['full_name'][i-1] and k ==0:
                j_ind = j_ind - df_qb['Player'][df_qb['Player'] == name].count()
                k=k+1
                j=j+1
        if df20_qb['full_name'][i] == df_qb['Player'][j + j_ind] and df20_qb['season'][i] == df_qb['Year'][j + j_ind]:
            df_qbind.append(j + j_ind)
        j=j+1
    j_ind = j_ind + j
    i=i+1
dfqb = df_qb.loc[df_qbind]
dfqb.reset_index(drop=True, inplace=True)
print('Done removing player roster/stat differences')

#Begin second loop, join a player's team into their weekly statistics in an efficient manner.
#The scheme only needs to loop over necessary weeks/years. We find the number of times a player's name appears, and end the loop once this is finished.
#This reduces the QB data frame joining from roughly 5000*500 (via brute force) to ~ 35000 computations
j_ind = 0
i=0
teamlist = []
for name in df20_qb['full_name']:
    k=0
    j=0
    while j < dfqb['Player'][dfqb['Player'] == name].count(): #and k < 20:\
        if i > 0:
            if df20_qb['full_name'][i] == df20_qb['full_name'][i-1] and k ==0:
                j_ind = j_ind - dfqb['Player'][dfqb['Player'] == name].count()
                k=k+1
                j=j+1
        if df20_qb['full_name'][i] == dfqb['Player'][j + j_ind] and df20_qb['season'][i] == dfqb['Year'][j + j_ind]:
            teamlist.append(df20_qb['Team3'][i])
        j=j+1
    j_ind = j_ind + j
    i=i+1

df = pd.DataFrame({'Team': teamlist})
dfqb = dfqb.join(df, how='right')
dfqb=dfqb.sort_values(by=['Year','Week Num.'])
dfqb.reset_index(drop=True, inplace=True)
print('Done matching player stats with team')

#Begin last loop, create a final column indicaating 1 for home field advantage or 0 for non-homefield advantage that fantasy week
i=0
j=0
j_ind=0
i_ind=0
k=0
home_team_ind=list(0 for i in range(0,len(dfqb['Player'])))
for year_ind in range(2010,2020):
    print('Determined homefield advantage for %d regular seaason' %(year_ind))
    for week_ind in range(1,18):
        if k > 0:
            j_ind=j_ind+df_total_matchup['Year'][(df_total_matchup['Week Num.']==str(week_ind)) & (df_total_matchup['Year']==year_ind)].count()
            i_ind=i_ind+dfqb['Player'][(dfqb['Week Num.']==week_ind) & (dfqb['Year']==year_ind)].count()
        k=1
        i=0
        while i < dfqb['Player'][(dfqb['Week Num.']==week_ind) & (dfqb['Year']==year_ind)].count():
            j=0
            while j < df_total_matchup['Year'][(df_total_matchup['Week Num.']==str(week_ind)) & (df_total_matchup['Year']==year_ind)].count():
                if df_total_matchup['Home Team'][j+j_ind] == dfqb['Team'][i+i_ind]:
                    home_team_ind[i+i_ind]=1
                j=j+1
            i=i+1
df = pd.DataFrame({'HomeTeam=1,AwayTeam=0': home_team_ind})
dfqb = dfqb.join(df, how='right')
dfqb=dfqb.sort_values(by=['Year','Week Num.'])
dfqb.reset_index(drop=True, inplace=True)
print('Done')  