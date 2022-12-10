from PIL import Image, ImageDraw, ImageFont
from easy_sqlite3 import *
import difflib


def get_match(player, db):
    
    match = difflib.get_close_matches(player, [n[0] for n in db.select("players")], n=1)
    return db.select("players", where={"player":match[0] if match else '------'}, dict_format=True)

def create_card(user, player):

    ratio = (250, 250)    
    
    db = Database(f"./Data/Worlds/{user}/players")
    player = get_match(player, db)

    if not player: return None
        
    r = player['rating']
    card = "card1" if r > 89 else "card2" if r > 84 and player['age'] < 21 else \
            "card3" if r > 84 else "card4" if r > 79 else "card5" if r > 74 else \
            "card6" if r > 69 else "card7"

    card_t = card[-1] == "1" or card[-1] == "2"

    rating_coord = {"1":(90, 170), "2":(100, 170)}
    position_coord = {"1":(90, 290), "2":(100, 290)} 
    names_coord = {"1":(280, 425), "2":(280, 440)}
    
    colors = {"1":(240, 240, 240), "2":(76,54,20)}

    card_img = Image.open(f"./Data/Cards/{card}.png").resize((560, 600), Image.ANTIALIAS)
    club_img = Image.open(f"./Data/Clubs/{player['team']}.png").resize(ratio, Image.ANTIALIAS)
    
    font = ImageFont.truetype("consolas.ttf", 75)
    font2 = ImageFont.truetype("consolas.ttf", 45)

    drawer = ImageDraw.Draw(card_img)
    drawer.text(rating_coord["1" if card_t else "2"], str(r), font=font, fill=colors["1" if card_t else "2"])
    drawer.text(position_coord["1" if card_t else "2"], player["position"], font=font, fill=colors["1" if card_t else "2"])

    text_size = drawer.textsize(player["player"], font=font2)
    drawer.text((names_coord["1" if card_t else "2"][0]-text_size[0]/2, names_coord["1" if card_t else "2"][1]), player["player"], font=font2, fill=colors["1" if card_t else "2"])

    card_img.paste(club_img, (210, 150), club_img.convert("RGBA"))

    db.close()
    del drawer

    return card_img

def get_team(db, team):
    match = difflib.get_close_matches(team, list(db.get_tables().keys()), n=1)
    
    return db.select(match[0], dict_format=True) if match else None

def create_team(user, team):
    db = Database(f"./Data/Worlds/{user}/teams", spaces=True)

    info = []
    team = get_team(db, team)
    db.close()
    for i, player in enumerate(team):
        info.append(f"{i+1}. {player['player']} [{player['rating']}] - {player['age']} yrs - {player['position']} -- ${player['value']:,}")
    
    return info

def create_team_image(team, user):
    from Backend.starting11 import starting11 

    db = Database(f"./Data/Worlds/{user}/teams", spaces=True)

    team = difflib.get_close_matches(team, list(db.get_tables().keys()), n=1)
    if not team: return None

    db.close()

    team_11 = starting11(team[0], user)
    
    template = Image.open(f"./Data/Formations/433.png")
    for pos, player in team_11.items():
        positions = {'GK':(10,250), 'ST':(695, 250), 'LW':(625, 75), 'RW':(625, 425),
                'LM':(440, 125), 'RM':(440, 370), 'LB':(225,35), 'RB':(225, 450),
                'CM':(325, 250), 'CB':[(150, 170), (150, 320)]}
        
        
        for i, p in enumerate(player):
            card = create_card(user, p[0]).resize((140, 150), Image.ANTIALIAS)
            location = positions[pos][i] if pos == 'CB' else positions[pos]
            template.paste(card, location, card.convert("RGBA"))

    club = Image.open(f"./Data/Clubs/{team[0]}.png").resize((150, 150), Image.ANTIALIAS)
    template.paste(club, (810, 500), club.convert("RGBA"))
            
    return template
    


