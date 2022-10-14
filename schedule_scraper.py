# -*- coding: utf-8 -*-
"""
Author: Luke Galvan
Date: September 27 2022
Project: Fantasy Football Scraper
Scrape schedule data from 2010-2020- will be used to determine if a player has home-field advantage during a game week.
"""
#Import modules
import requests
import pandas as pd
from bs4 import BeautifulSoup

#Original URL
#"https://www.pro-football-reference.com/years/2011/games.htm"

#Initialize m, will help concatenate data frames later 
m=0
URL = 'https://www.pro-football-reference.com/years/'
#Loop over years
for year in range(2010,2020):
    #Change URl for each loop, use BeautifulSoup to parse HTML
    Opp_URL = (URL + str(year) + '/games.htm')
    Opp_results = requests.get(Opp_URL)
    Opp_soup = BeautifulSoup(Opp_results.content, "html.parser")
    #Identify area of HTML code to look for data in
    Opp_results = Opp_soup.find(id="games")
    
    #Create lists to clean data from
    opp_matchup = []
    opp_matchup_week = []
    
    #Find and store week numbers
    for link in Opp_soup.find_all('th'):
        if link.get('data-stat') == 'week_num':
            opp_matchup_week.append(link.get_text('data-stat'))
            
    #Find and store opponent matchup data
    for link in Opp_soup.find_all('td'):
        if link.get('data-stat') == 'winner':
            opp_matchup.append(link.get_text('data-stat'))
        if link.get('data-stat') == 'game_location' and link.get_text('data-stat') != '@':
            opp_matchup.append(link.get_text('data-stat'))
        if link.get('data-stat') == 'game_location' and link.get_text('data-stat') == '@':
            opp_matchup.append(link.get_text('data-stat'))
        if link.get('data-stat') == 'loser':
            opp_matchup.append(link.get_text('data-stat'))
            
    #Clean data by removing unneeded words from lists
    for i in range(0,opp_matchup_week.count('Week')):
        opp_matchup_week.remove('Week')
    for i in range(0,opp_matchup_week.count('WildCard')):
        opp_matchup_week.remove('WildCard')
    for i in range(0,opp_matchup_week.count('Division')):
        opp_matchup_week.remove('Division')
    for i in range(0,opp_matchup_week.count('ConfChamp')):
        opp_matchup_week.remove('ConfChamp')
    opp_matchup_week.remove('SuperBowl')
    opp_matchup_week.remove('')
    
    #Remove all playoff games from origional 12-team playoff format
    del opp_matchup[len(opp_matchup) - 36:len(opp_matchup)]
    #Remove extra playoff games from new 14-team playoff format
    if year >= 2020:
        del opp_matchup[len(opp_matchup) - 6:len(opp_matchup)]
    
    #Organize data collected from opp_matchup list (format was e.g. 'Team1', '@', 'Team2', 'Team3', '','Team4'...)
    team1 = []
    team1 = [opp_matchup[x] for x in range(0,len(opp_matchup),3)]
    location = []
    location = [opp_matchup[x] for x in range(1,len(opp_matchup),3)]
    team2 = []
    team2 = [opp_matchup[x] for x in range(2,len(opp_matchup),3)]
    year = [int(year) for x in range(0,len(team1))]
    
    #Construct columns of data frame
    pd.DataFrame(team1,columns=['Team1'])
    df = pd.DataFrame({'Team1': team1})
    name_holder = ['location','Team2','Week Num.','Year']
    holder = [location,team2,opp_matchup_week,year]
    for i in range(0,4):
        df1 = pd.DataFrame({name_holder[i]: holder[i]})
        df = df.join(df1, how='right')
    
    #Locate and place home teams and away teams in separate columns
    idx = (df['location'] == '@')
    df.loc[idx,['Team1','Team2']] = df.loc[idx,['Team2','Team1']].values
    df = df.drop('location', axis=1)
    
    #Rename home team/ away team columns
    df = df.rename(columns={'Team1': 'Home Team', 'Team2': 'Away Team'})
    
    #Remove all but mascot name - will help with matching up players with home team later
    df['Home Team']=df['Home Team'].str.split(n=1).str[1]
    dfholder = df['Home Team']
    df['Home Team']=df['Home Team'].str.split(n=1).str[1]
    df['Home Team'].fillna(dfholder, inplace=True)

    df['Away Team']=df['Away Team'].str.split(n=1).str[1]
    dfholder = df['Away Team']
    df['Away Team']=df['Away Team'].str.split(n=1).str[1]
    df['Away Team'].fillna(dfholder, inplace=True)
    
    #store df from first iteration
    if m == 0:
        dfc=df
        #display(df)
        
    #concatenate data frame each iteration
    if m >= 1:
        #display(df)
        df_total_matchup = pd.concat([dfc, df], ignore_index=True)
        dfc = df_total_matchup
    m=m+1
    print('Collected year', m)
i=0
while i < len(df_total_matchup['Home Team'])-1:
    if df_total_matchup['Home Team'][i] == 'Redskins' or df_total_matchup['Home Team'][i] == 'Team':
        df_total_matchup['Home Team'][i] = 'Commanders'
    if df_total_matchup['Away Team'][i] == 'Redskins' or df_total_matchup['Away Team'][i] == 'Team':
        df_total_matchup['Away Team'][i] = 'Commanders'
    i = i + 1