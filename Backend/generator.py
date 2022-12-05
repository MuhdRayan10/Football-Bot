import random, os, math
from easy_sqlite3 import *

WEIGHTS = [i for i in range(105, 70, -3)] + [i for i in range(70, 40, -2)] + [i for i in range(40, 1, -5)]

class Player:
    def __init__(self, name, pos, rating, age=None):
        self.name = name
        self.pos = pos
        self.rating = rating
        self.age = age if age else self.gen_age()
    
    def gen_age(self):
        ages =  [i for i in range(17, 34)]
        if self.rating >= 90:
            return random.choices(ages, k=1, weights=[i for i in range(1, 5)] + [i for i in range(5, 16, 2)] + [i for i in range(16, 26, 3)] + [25, 22, 19])[0]
        elif self.rating >= 85:
            return random.choices(ages, k=1, weights=[i for i in range(5, 9)] + [i for i in range(9, 20, 2)] + [i for i in range(20, 30, 3)] + [30, 27, 24])[0]
        elif self.rating >= 75:
            return random.choice(ages)
        else:
            return random.choices(ages, k=1, weights=[i for i in range(34, 17, -1)])[0]


    def __repr__(self):
        return f"{self.name} - {self.pos} - ({self.rating}) -- {self.age} yrs"

    
def generate_player(name, pos):
    rating = random.choices([i for i in range(60, 95)], k=1, weights=WEIGHTS)[0]
    return Player(name, pos, rating)

def generate_players():
    POSITIONS = ['GK', 'LB', 'CB', 'CB', 'LM', 'CM', 'RM', 'LW', 'ST', 'RW']
    players = {}

    with open('./Data/Generation/first_names.txt', 'r') as f:
        first_names = f.readlines()

    with open('./Data/Generation/last_names.txt', 'r') as f:
        last_names = f.readlines()
    
    for _ in range(7):
        for pos in POSITIONS:
            for _ in range(3):
                name = f"{random.choice(first_names).title()} {random.choice(last_names).title()}".replace('\n', '')
                players[pos] = players.get(pos, []) + [generate_player(name, pos)]

    return players

def generate_teams():
    TEAMS = ["Liverpool", "Manchester City", "Manchester United", "Aston Villa", "Arsenal", "Tottenham"]

    players = generate_players()

    teams = {}

    for li in players.values():
        random.shuffle(li)

    for team in TEAMS:
        teams[team] = []
        for _ in range(3):
            for pos in players:
                teams[team].append(players[pos].pop())
    
    left = [p for player in players.values() for p in player]
    
    while left:
        teams[random.choice(TEAMS)].append(left.pop())

    return teams
 
def create_tables(teams, user):
    world_db = Database(f"./Data/Worlds/{user}/world", spaces=False)
    league_db = Database(f"./Data/Worlds/{user}/league")
    player_db = Database(f"./Data/Worlds/{user}/players")
    team_db = Database(f'./Data/Worlds/{user}/teams', spaces=False)

    league_db.create_table('league', {'name':TEXT, 'matches':INT, 'gd':INT, 'scored':INT, 'conceded':INT,
                    'wins':INT, 'draws':INT, 'losses':INT, 'points':INT})
    league_db.create_table('player_stats', {'player':TEXT, 'team':TEXT, 'goals':INT, 'assists':INT})

    world_db.create_table("teams", {'team':TEXT, 'coach':TEXT, 'players':INT, 'teamrating':INT, 'transferbudget':INT})

    for team in teams:
        team_db.create_table(team, {'player':TEXT, 'team':TEXT, 'position':TEXT, 'goals':INT, 'assists':INT, 'value':INT,
                    'rating':INT, 'age':INT, 'happiness':INT})


    player_db.create_table("players", {'player':TEXT, 'team':TEXT, 'position':TEXT, 'goals':INT, 'assists':INT, 'value':INT,
                    'rating':INT, 'age':INT, 'happiness':INT})

    del world_db, league_db, player_db, team_db



    mail_db = Database(f"./Data/Worlds/{user}/mail")
    mail_db.create_table('inbox', {'message':STR, 'subject':STR, 'sender':STR, 'type':STR, 'status':INT})
    mail_db.create_table('outbox', {'message':STR, 'subject':STR, 'receiver':STR, 'status':INT})

    del mail_db

def calculate_value(player):
    
    pos = {'GK':2500000, 'LB':10000000, 'CB':7500000, 'LM':15000000, 'CM':15000000,
                 'RM':15000000, 'LW':20000000, 'ST':22500000, 'RW':20000000, 'RB':10000000}

    value = int(pos[player.pos] + math.exp(player.rating/8) * 935 + random.randint(100, 500) * 250 - player.age * 100_000)

    if player.age < 20:
        return value

    if player.age < 25:
        sub = player.age * 75_000
        return value - (sub if value > sub else value//2)

    elif player.age < 30:
        sub = player.age * 200_000
        return value - (sub if value > sub else value//4)
    else:
        value = int(pos[player.pos] + math.exp(player.rating/4.5) * 0.05 + random.randint(10, 50) * 250 - player.age * 750_000)
        return  value if value > 50_000 else int(math.exp(player.rating/4.9) * 0.2 + random.randint(10, 50) * 250)


def average_rating(players):
    total = sum([p.rating for p in players])
    return int(total / len(players))

def add_players(teams, user):
    team_db = Database(f"./Data/Worlds/{user}/teams", spaces=False)
    world_db = Database(f"./Data/Worlds/{user}/world", spaces=False)
    player_db = Database(f"./Data/Worlds/{user}/players")

    for db in (team_db, world_db, player_db):
        db.initiate_transaction()

    for team, players in teams.items():
        world_db.insert("teams", (team, 'Bot', len(players), average_rating(players), 100000))
        for p in players:
            player = (p.name, team, p.pos, 0, 0, calculate_value(p), p.rating, p.age, 10)
            team_db.insert(team, player)
            player_db.insert("players", player)

    for db in (team_db, world_db, player_db):
        db.commit()

    del team_db, world_db, player_db


def generate_world(user):
    #Creating a folder
    base_path = os.getcwd()
    teams = generate_teams()
    try:
        folder_path = f"{base_path}\\Data\\Worlds\\{user}"
        os.mkdir(folder_path)

    except FileExistsError:
        pass
    
    create_tables(teams, user)
    add_players(teams, user)

def destroy_world(user):
    from shutil import rmtree
    folder_path = f"{os.getcwd()}\\Data\\Worlds\\{user}"

    rmtree(folder_path)
