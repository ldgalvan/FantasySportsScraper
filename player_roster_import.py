# -*- coding: utf-8 -*-
"""
Author: Luke Galvan
Date: October 5th 2022
Project: Fantasy Football Scraper
Upload data from existing github profile, contains rosters of players with their teams that year.
Goal: Connect players with their teams each year, will be used to determine if a player has home field advantage each week. 
"""
#Import module
import pandas as pd

#Read in CSV file of roster data
df100 = pd.read_csv("https://raw.githubusercontent.com/leesharpe/nfldata/master/data/rosters.csv")
df00 = pd.read_csv("https://raw.githubusercontent.com/leesharpe/nfldata/master/data/teams.csv")

#filter by columns needed
df3 = df00[['nfl','full','season']]
df2=df100[['full_name','position','team','season']]

#drop any rows with missing data - most of this are players with very few stats.
df2=df2.dropna()

#reset index
df2.reset_index(drop=True, inplace=True)

df3['nfl'][625] = 'LAR'
teamlist = []

#Loop to connect players with full team name, the csv only has players matched with team abbreviation (e.g. Tom Brady (TB))
for i in range(0,len(df2['team'])):
    k=0
    j=0
    while k==0:
        if df2['team'][i]==df3['nfl'][j]:
            teamlist.append(df3['full'][j])
            k=1
        j=j+1
        
#construct data frame with full team ame
df10 = pd.DataFrame({'Team3': teamlist})
df20 = df2.join(df10, how='right')
display(df20)
#drop rows of years prior to 2006 (we only need data from 2010-2020)
for i in range(2006,2010):
    df20 = df20[df20['season'] != int(i)]
    
#sort data frame by name and season
df20 = df20.sort_values(['full_name','season' ],ascending=[True,True])
df20.reset_index(drop=True, inplace=True)

i=0
indtoremove = []
#loop to find indexes of duplicates in list - in particular players which switched teams midseason
while i <len(df20['full_name'])-1:
    i = i+1
    j = i-1
    if df20['season'][i] == df20['season'][j]:
        if df20['full_name'][i] == df20['full_name'][j]:
            if df20['position'][i] == df20['position'][j]:
                indtoremove.append(i)
                indtoremove.append(j)

#drop collected indexes and reset index
df20 = df20.drop(df20.index[indtoremove])
df20.reset_index(drop=True, inplace=True)

#Remove all but mascot
df20['Team3']=df20['Team3'].str.split(n=1).str[1]
dfholder = df20['Team3']
df20['Team3']=df20['Team3'].str.split(n=1).str[1]
df20['Team3'].fillna(dfholder, inplace=True)

#change washington's mascot to be consistent throughout our target years
i=0
while i < len(df20['Team3'])-1:
    if df20['Team3'][i] == 'Redskins' or df20['Team3'][i] == 'Team':
        df20['Team3'][i] = 'Commanders'
    i = i + 1
df20.reset_index(drop=True, inplace=True)
