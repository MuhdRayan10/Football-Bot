from easy_sqlite3 import *

def starting11(team): # for 4-3-3 formation
    team_db = Database("backend\\teams", spaces=False)

    players = team_db.select(team.replace(" ","_"), selected=("player", "rating", "position"))

    team = {pos:[] for pos in ['GK', 'LB', 'CB', 'CB', 'LM', 'CM', 'RM', 'LW', 'ST', 'RW']}

    for player in players:
        pos = player[2]
        
        if not len(team[pos]):
            team[pos].append(player)
        else:
            if team[pos][0][1] < player[1]:
                team[pos] = [player]

    team_rating = sum([p[0][1] for p in list(team.values())])/len(team)
    print(team_rating)

    return team, team_rating


        

    



