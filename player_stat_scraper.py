# -*- coding: utf-8 -*-
"""
Author: Luke Galvan
Date: October 3rd 2022
Project: Fantasy Football Scraper
Scrape regular season player data from 9 different positions from years 2010-2020 
"""
#Import modules
import requests
import pandas as pd
from bs4 import BeautifulSoup

#Create position holder to search though different URLs
pos_holder = ['qb','rb','wr','te','k','dst']
URL = "https://www.fantasypros.com/nfl/stats/"
#Loop through positions in outer loop
#unhighlight the following line to scrape only QB data
#pos_holder=['qb']
for pos in pos_holder:
    m=0
    n=0
    for year in range(2010,2020):
        m=0
        for week_num in range(1,18):
            #Change URl for each loop, use BeautifulSoup to parse HTML
            req = requests.get(URL + str(pos) + '.php?year=' + str(year) + '&week=' + str(week_num) + '&range=week')
            soup = BeautifulSoup(req.content, 'html.parser')
            results = soup.find(id="data")
            #Find player stats
            stats_name = results.find_all("td", class_="player-label")
            stats      = results.find_all("td", class_="center")
            
            #Create lists to store player stats
            stat_holder = []
            stat_name_holder = []
            
            #convert to string before storing
            for stat in stats:
                stat_holder.append(str(stat))
            
            #strip left behind HTML syntax
            stripped_stats = [s.strip('<td class="center"></td>') for s in stat_holder]
            for name in stats_name:
                stat_name_holder.append(name.text)

            #List to hold player name
            stat_nameh = []
            for link in soup.find_all('th'):
                stat_nameh.append(link.get_text('data-column'))
                
            #List to hold player weekly rank
            stat_rank = []
            for link in soup.find_all('tr'):
                stat_rank.append(str(link.find('td')))
                
            stat_rankh = [s.strip('<td></td>') for s in stat_rank]
            #remove unrelated HTML syntax
            del stat_rankh[0:1]
            if len(stat_name_holder) != len(stat_rankh):
                del stat_rankh[0:1]
            
            df_list = []
            #Initialize Player stat Data Frame
            df = pd.DataFrame({'Player': stat_name_holder, 'Rank': stat_rankh})
            df_list.append(df)
            numcolums = len(stripped_stats) / len(stat_name_holder)
            for i in range(0,int(numcolums)):
                #Create columns from the cleaned stats list
                parse_strip = [stripped_stats[x] for x in range(0+i,len(stripped_stats),int(numcolums))]
                df1 = pd.DataFrame({'stat' + str(i): parse_strip})
                df = df.join(df1, how='right')
            
            #Remove leftover HTML syntax
            del stat_nameh[0:2]
            i=0
            #Create player name column
            for x in stat_nameh:
                df = df.rename(columns={'stat' + str(i): str(x)})
                i=i+1
            #Add remaining data including week number, year, position, and name
            yearh = [int(year) for x in range(0,len(stat_rankh))]
            weekNum = [int(week_num) for x in range(0,len(stat_rankh))]
            posi = [str(pos) for x in range(0,len(stat_rankh))]
            name_holder = ['Week Num.','Year','Pos']
            holder = [weekNum,yearh,posi]
            for i in range(0,3):
                df1 = pd.DataFrame({name_holder[i]: holder[i]})
                df = df.join(df1, how='right')
                
            #store df from first iteration
            if m == 0:
                dfc=df
            #concatenate data frame each iteration after
            if m >= 1:
                df_total = pd.concat([dfc, df], ignore_index=True)
                dfc = df_total
                statement = 'df_'+str(pos)+' = df_total'
                exec(statement)
            m=m+1
                
        print('Collected year %d for position %s' %(year,str(pos)))
        if n == 0:
            statement = 'dfy=df_'+str(pos)
            exec(statement)
        if n >= 1:
            statement = 'df=df_'+str(pos)
            exec(statement)
            df_total = pd.concat([dfy, df], ignore_index=True)
            dfy = df_total
            df_total["Player"] = df_total["Player"].str.replace(r"\(.*\)","")
            df_total["Player"] = df_total["Player"].str.rstrip()
            statement = 'df_'+str(pos)+' = df_total'
            exec(statement)
        n=n+1
print('done')

#For defense, remove all but mascot name - will help with matching up players with opponent defense.
df_dst['Player']=df_dst['Player'].str.split(n=1).str[1]
dfholder = df_dst['Player']
df_dst['Player']=df_dst['Player'].str.split(n=1).str[1]
df_dst['Player'].fillna(dfholder, inplace=True)