import random
import json

team1 = {'GK': [('Denis Ambrose', 84, 'GK')], 'LB': [('Taylor Jerry', 88, 'LB')], 'CB': [('Thomas Carlo', 78, 'CB'), ('Ed Charlie', 83, 'CB')],
 'RB': [('Kareem Genaro', 76, 'RB')], 'LM': [('Roscoe Justin', 65, 'LM')], 'CM': [('Rickie Marlon', 74, 'CM')], 'RM': [('Odis Lamont', 72, 'RM')],
 'LW': [('Harrison Junior', 73, 'LW')], 'ST': [('Allan Karl', 80, 'ST')],'RW': [('Marcel Rubin', 77, 'RW')]}

team2 = {'GK': [('Alexis Frederic', 89, 'GK')], 'LB': [('Berry Ronald', 91, 'LB')], 'CB': [('Buford Lloyd', 66, 'CB'), ('Kristofer Dario', 77, 'CB')],
 'RB': [('Alton Deon', 80, 'RB')], 'LM': [('Monte Charlie', 80, 'LM')], 'CM': [('Eugenio Dillon', 71, 'CM')], 'RM': [('Stacey Douglass', 76, 'RM')],
 'LW': [('Alfredo Tommy', 83, 'LW')], 'ST': [('Boris Thomas', 84, 'ST')], 'RW': [('Ward Trevor', 89, 'RW')]}

class Chance:
    def __init__(self, team1, team2):
        self.position = random.choice(["defense", "midfield", "attack"])    

        self.team1_chance = random.choice([True, False])
        
        self.team1 = team1
        self.team2 = team2

        with open("./Data/gameplay.json", "r") as f:
            self.gameplay_data = json.load(f)

        self.offense() if self.team1_chance else self.defense()

    def offense(self):
        self.gameplay_data = self.gameplay_data["offense"][self.position]
        self.chance_type = random.choice(list(self.gameplay_data.keys()))

        self.options = list(self.gameplay_data[self.chance_type]["options"].keys())
        print(self.chance_type, self.position, self.options)

    def defense(self):
        self.gameplay_data = self.gameplay_data["defense"][self.position]
        self.chance_type = random.choice(list(self.gameplay_data.keys()))

        self.options = list(self.gameplay_data[self.chance_type]["options"].keys())
        print(self.chance_type, self.position, self.options)

Chance(team1, team2)



    
