import pandas as pd
import numpy as np
import goldsberry
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.feature_selection import SelectFromModel
import numpy as np
from sklearn.utils.validation import check_random_state
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.neighbors import KNeighborsRegressor
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import RidgeCV




Seasons = ['2012-13', '2013-14', '2014-15', '2015-16']
Game_Data = {}
gameids = goldsberry.GameIDs()
for i in range(len(Seasons)):
    gameids.get_new_data(Season=Seasons[i])
    Game_Data[Seasons[i]] = pd.DataFrame(gameids.game_list())

team_ids =  list(Game_Data[Seasons[0]]['TEAM_ID'].value_counts().index)
WL_dict = {'W':1, 'L': -1}


def stats_per_season(season_index):
    goldsberry.apiparams.p_team_season['Season'] = Seasons[season_index]
    data = [goldsberry.team.season_stats(team).overall()[0] for team in team_ids]
    season_data = pd.DataFrame(data)
    season_data = season_data.set_index(['TEAM_ID'])
    return season_data


Stats_Data = {}

for i in range(len(Seasons)):
    Stats_Data[Seasons[i]] = stats_per_season(i)




def create_X(season_index):
    df = Game_Data[Seasons[season_index]]
    unique_game_ids = list(df['GAME_ID'].value_counts().index)
    if season_index != 0:
        prev_season = season_index - 1
        avg_season_data = Stats_Data[Seasons[prev_season]]
    else:
        print("We Need Prev Data For Stats")
        return

    X = pd.DataFrame()
    Y = []
    for i,game in enumerate(unique_game_ids):
        print "Number %s out of %s" % (i, len(unique_game_ids))
        rows = df[['WL', 'TEAM_ID']].ix[df['GAME_ID'] == game]
        stat_columns =[x for x in list(avg_season_data.columns) if 'TEAM_NAME' not in x and 'GROUP_SET' not in x and 'GROUP_VALUE' not in x and 'GP' not in x]
        tmp = goldsberry.game.boxscore_summary(game).game_summary()[0]
        home_team_data = avg_season_data.ix[tmp['HOME_TEAM_ID'] ][stat_columns]
        away_team_data = avg_season_data.ix[tmp['VISITOR_TEAM_ID']][stat_columns]
        away_team_data = pd.DataFrame([list(away_team_data.values)], index = [game], columns = [x + '_AWAY' for x in list(away_team_data.index)])
        home_team_data = pd.DataFrame([list(home_team_data.values)], index = [game], columns = [x + '_HOME' for x in list(home_team_data.index)])
        data = pd.concat([home_team_data,away_team_data],1)
        X = X.append(data)
        if rows['WL'].ix[rows['TEAM_ID'] == tmp['HOME_TEAM_ID']] == 'W':
            Y.append(1)
        else:
            Y.append(0)


    return X,Y



def normalize_data(X):
    X_norm = (X - X.mean()) / (X.max() - X.min())

    return  X_norm



def predict_it(X_train, y_train, X_test, Y_test):
    ESTIMATORS = {
        "Extra trees": ExtraTreesRegressor(n_estimators=10, max_features=32,
                                           random_state=0),
        "K-nn": KNeighborsRegressor(),
        "Linear regression": LinearRegression(),
        "Ridge": RidgeCV(),
    }
    y_test_predict = dict()
    for name, estimator in ESTIMATORS.items():
        estimator.fit(X_train, y_train)
        y_test_predict[name] = estimator.predict(X_test)



def TreeRegressor(X, y):
    df_norm = (X - X.mean()) / (X.max() - X.min())
    forest = ExtraTreesRegressor()
    clf = forest.fit(X, y)
    clf.feature_importances_
    X_new = clf.transform(X)

   # model = SelectFromModel(clf, prefit=True)
    Yhat = clf.predict(X)











def main():
    X, y = create_X(1)



