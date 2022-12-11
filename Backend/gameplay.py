from random import choice

team1 = {'GK': [('Denis Ambrose', 84, 'GK')], 'LB': [('Taylor Jerry', 88, 'LB')], 'CB': [('Thomas Carlo', 78, 'CB'), ('Ed Charlie', 83, 'CB')],
 'RB': [('Kareem Genaro', 76, 'RB')], 'LM': [('Roscoe Justin', 65, 'LM')], 'CM': [('Rickie Marlon', 74, 'CM')], 'RM': [('Odis Lamont', 72, 'RM')],
 'LW': [('Harrison Junior', 73, 'LW')], 'ST': [('Allan Karl', 80, 'ST')],'RW': [('Marcel Rubin', 77, 'RW')]}

team2 = {{'GK': [('Alexis Frederic', 89, 'GK')], 'LB': [('Berry Ronald', 91, 'LB')], 'CB': [('Buford Lloyd', 66, 'CB'), ('Kristofer Dario', 77, 'CB')],
 'RB': [('Alton Deon', 80, 'RB')], 'LM': [('Monte Charlie', 80, 'LM')], 'CM': [('Eugenio Dillon', 71, 'CM')], 'RM': [('Stacey Douglass', 76, 'RM')],
 'LW': [('Alfredo Tommy', 83, 'LW')], 'ST': [('Boris Thomas', 84, 'ST')], 'RW': [('Ward Trevor', 89, 'RW')]}}

def create_chance():
    team1_chance = choice([0,1])

    ball_position = ["defense", "midfield", "attack"]
    chance = choice(ball_position)
    
    if chance == "defense":
        defense_types = ["press", "buildup"]
        chance_type = choice(defense_types)




    
