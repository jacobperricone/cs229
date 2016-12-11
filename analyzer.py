import pandas as pd
import os
import numpy as np
import sklearn
import sqlalchemy as s


def return_engine(database):
    engine = s.create_engine('mysql+pymysql://root:Redstring01!1@127.0.0.1:3306/' + database,
                           echo=False)
    return engine


databases = ['Reg_Master', 'Playoff_Master']
file_types = ['aggregatematchups','gamelist', 'matchups','playbyplay', 'players2', 'playerstats2', 'playerstatsbyteam','teamstats']
key_indices = {file_types[i]:i for i in range(len(file_types))}

engine = return_engine('Reg_Master')
conn = engine.connect()
game_list = pd.read_sql('select * from gamelist', con=conn)
players = pd.read_sql_query('select * from players2', con=conn)
player_stats = pd.read_sql_query('select * from playerstats2', con=conn)
player_stats_team = pd.read_sql_query('select * from playerstatsbyteam', con=conn)
team_stats = pd.read_sql_query('select * from teamstats', con=conn)

#'2006-2007':0, '2007-2008':1,
date_dict = {'2006-2007':0, '2007-2008':1,'2008-2009':2, '2009-2010':3, '2010-2011': 4,'2011-2012': 5}



def add_final_outcome(conn):
    # make a query
    #$query = s.text("select g.GameID from gamelist as g left outer join (select DISTINCT(m.GameID) from matchups as m) as s on g.GameID= s.GameID)")
    query = s.text("select s.GameID, s.EndScoreHome, s.EndScoreAway,s.Differential from gamelist as g left outer join (select IND,GameID, EndTime, EndScoreHome, EndScoreAway, Differential from matchups where EndTime ='00:00:00') as s on g.GameID= s.GameID")

    game_data = {row[0]: (row[1], row[2], row[3]) for row in conn.execute(query)}


    query=s.text("select GameID from gamelist as g")
    game_list = [row[0] for row in conn.execute(query)]

    disjoint_games = [x for x in game_list if x not in game_data.keys()]

    for game, values in game_data.iteritems():
        query = s.text("Update gamelist set EndScoreHome =:eh, EndScoreAway=:ea, Differential=:d where GameID=:g")
        conn.execute(query, eh=values[0], ea=values[1],d=values[2], g=game )


def players_on_team(year, team):
    player_ids = players['PlayerID'].ix[(players['TeamName3'] == team) & players['Year'].str.contains(year)]
    player_ids = list(player_ids.value_counts().index)
    return player_ids

def players_statsbyteam(team, year):
    player_ids = players['PlayerID'].ix[(players['TeamName3'] == team) & players['Year'].str.contains(year)]
    player_ids = list(player_ids.value_counts().index)
    index = {}
    for id in player_ids:
        tmp = players['Year'].ix[(players['TeamName3'] == team) & (players['PlayerID'] == id)].value_counts()
        years_played = sorted(list(tmp.index), key=lambda x: date_dict[x])
        index[str(id)] = years_played.index(year)

    pstats = player_stats[player_stats['PlayerID'].isin(player_ids) & (player_stats['PlayerTeams'] == team)]

    player_stats_final = pd.DataFrame()

    for id, ind in index.iteritems():
        print int(id)
        tmp = player_stats[player_stats['PlayerID']==int(id)].iloc[ind]
        tmp = pd.DataFrame([list(tmp.values)], columns=list(tmp.index))
        player_stats_final = player_stats_final.append(tmp, ignore_index=True)

    return player_stats_final


# def playerstats_agg(team, year):
#     player_ids = players['PlayerID'].ix[(players['TeamName3'] == team) & players['Year'].str.contains(year)]
#     player_ids = list(player_ids.value_counts().index)
#     index = {};
#     for id in player_ids:
#         tmp = players['Year'].ix[(players['TeamName3'] == team) & (players['PlayerID'] == id)].value_counts()
#
#         years_played =  sorted(list(tmp.index), key=lambda x: date_dict[x])
#         index[str(id)] = years_played.index(year)
#
#
#     pstats = player_stats[player_stats['PlayerID'].isin(player_ids) & player_stats['PlayerTeams'].str.contains(team)]
#
#     # tstats = player_stats_team[player_stats_team['PlayerID'].isin(player_ids) & player_stats_team['Team'].str.contains(team)]
#     player_stats_final = pd.DataFrame()
#
#     for id, ind in index.iteritems():
#         tmp = pstats[pstats['PlayerID']==int(id)].iloc[ind]
#         tmp = pd.DataFrame([list(tmp.values)], columns=list(tmp.index))
#         # tmp2 = tstats[tstats['PlayerID'] == int(id)].iloc[ind-1]
#         #tmp2 = pd.DataFrame([list(tmp2.values)], columns=list(tmp2.index))
#         player_stats_final = player_stats_final.append(pd.concat([tmp,tmp2], 1), ignore_index=True)
#
#     return player_stats_final

def main():
    #add_final_outcome(conn)

    distinct_teams = list(team_stats['Team'].value_counts().index)
    prev_year = date_dict.keys()[1]
    curr_year = data_dict.keys()[2]
    players_prev = players_on_team(prev_year, distinct_teams[0])
    players_curr = players_on_team(curr_year, distinct_teams[0])
    new_players = [x for x in players_curr if x not in players_prev]












if __name__ == '__main__':
    main()


