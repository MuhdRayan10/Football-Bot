import random
import json
import time

team1 = {'GK': [('Denis Ambrose', 84, 'GK')], 'LB': [('Taylor Jerry', 88, 'LB')], 'CB': [('Thomas Carlo', 78, 'CB'), ('Ed Charlie', 83, 'CB')],
 'RB': [('Kareem Genaro', 76, 'RB')], 'LM': [('Roscoe Justin', 65, 'LM')], 'CM': [('Rickie Marlon', 74, 'CM')], 'RM': [('Odis Lamont', 72, 'RM')],
 'LW': [('Harrison Junior', 73, 'LW')], 'ST': [('Allan Karl', 80, 'ST')],'RW': [('Marcel Rubin', 77, 'RW')]}

team2 = {'GK': [('Alexis Frederic', 89, 'GK')], 'LB': [('Berry Ronald', 91, 'LB')], 'CB': [('Buford Lloyd', 66, 'CB'), ('Kristofer Dario', 77, 'CB')],
 'RB': [('Alton Deon', 80, 'RB')], 'LM': [('Monte Charlie', 80, 'LM')], 'CM': [('Eugenio Dillon', 71, 'CM')], 'RM': [('Stacey Douglass', 76, 'RM')],
 'LW': [('Alfredo Tommy', 83, 'LW')], 'ST': [('Boris Thomas', 84, 'ST')], 'RW': [('Ward Trevor', 89, 'RW')]}

class Player:
    def __init__(self, name, rating, position, team):
        self.name = name
        self.rating = rating
        self.position = position
        self.team = team

        #stats
        self.goals = 0
        self.assists = 0
        
        #cards
        self.yellow = 0
        self.red = 0

class Team:
    def __init__(self, name, starting11, playing_style):
        self.name = name
        self.s11 = starting11

        self.style = playing_style

        self.assign_players()

    def assign_players(self):
        for pos, players in self.s11.items():
            p = []
            for player in players:
                p.append(Player(player[0], player[1], player[2], self.name))
            
            exec(f"self.{pos} = {p}")


class Chance:
    def __init__(self, team1, team2, weight, linked=False, prev_chance=None, action=None):
        
        if linked:
            self.position = random.choice(["defense", "midfield", "attack"])    

            self.team1_chance = random.choices([True, False], weights=weight)
            
            self.team1 = team1
            self.team2 = team2

            with open("./Data/gameplay.json", "r") as f:
                self.gameplay_data = json.load(f)

            self.chance("offense") if self.team1_chance else self.chance("defense") 
        else:
            pass


    def chance(self, mode):
        self.gameplay_data = self.gameplay_data[mode][self.position]
        self.chance_type = random.choice(list(self.gameplay_data.keys()))

        self.options = list(self.gameplay_data[self.chance_type]["options"].keys())
        print(self.chance_type, self.position, self.options)

    def craft_chance(self, chance, action):
        pass


class Match:
    def __init__(self, team1, team2):
        self.team1 = team1
        self.team2 = team2

        self.time = 0
        self.extra_time = random.randint(0, 8)
        self.score = (0, 0)

    def start_match(self):

        chance_weights = {'oo': (50, 50), 'om': (60, 40), 'od': (75, 25),
                        'mm': (50, 50), 'md': (60, 40), 'dd': (50, 50),
                        'mo': (40, 60), 'do':(75, 25), 'dm':(40, 60)}
        
        self.weight = chance_weights[f"{self.team1.style}{self.team2.style}"]

        while self.time > 90 + self.extra_time:
            chance = Chance(self.team1, self.team2, self.weight)
            self.execute_chance(chance)
            
            self.time += random.randint(2, 10)

            time.sleep(3)
    
    def execute_chance(self, chance):
        # for now, randomly choose action
        option = random.choice(chance.options)

        new_chance = Chance(self.team1, self.team2, self.weight, linked=True, prev_chance=chance, action=option)
        self.execute_chance(new_chance)
            




            





    
