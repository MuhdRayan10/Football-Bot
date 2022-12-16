# FootballBot
A Football Simulation Bot that lets you play in your own world with your own team and manage it as a coach! You will be able to play in tournaments, buy players, sell players, and much more!

This README will be updated along with the commits, explaining the code's intended functions.

## Player Generation
The code for player generation resides in `./Backend/generation.py`, while the text files with data reside in `./Data/Generation/` which is used to randomly create the player names. The code generates a player name, assigns it a rating and an age along with its position of play. 

The generation script is to be activated when a user creates a new world, thus needing new players. It returns a list of Player class objects which have attributes that can be accessed. (The class can be printed as well to display relevant information)

Each player is assigned to a team, and all the relevant databases are created for the world. The data is then passed into the database and saved. All of this is done when the user types `/register` after which a new world is created (only the user can play in it, although multiplayer will be developed in the future). To unregister, just type `/unregister` and all the data that was saved will be removed (IRREVERSIBLE).

## Player Value Calculation

The calculation of the player's value (transfer value) is done based on which age category the player's age falls into:

1. Under 20
2. Under 25
3. Under 30
4. Above 30

This is to deal with complex stuff like potential, since a higher rated young player is worth more than an older one because the player has more time to improve and increase their rating. The value also depends on the player's position, since a GK is generally less worth than a ST in real life.

## Player card generation

For showcasing different aspects such as position and rating of a particular player, the `/view <field> <name>` command can be used to view a digitally created card like the one that follows:

![image](https://user-images.githubusercontent.com/75207653/201659866-978d9b20-e5ec-44b9-976f-e077977196ed.png)

NOTE: `<field>` basically has to be either `team` or `player` for now, as this is the same command that is used to obtain the squad of any particular team.

## Mail System

The Mail System is a way for the user to receive messages about the events of their world, for example a note from the team board. Note that it can also be used by teams to send contracts to users which can be accepted or rejected by the user in the interface itself.


A mail is divided based on its type: 

1. Message
2. Offer

## Starting XI 

The logic for finding a team's starting XI is simple: Find the best players for each position. For now, this is the maximum complexity. the `starting11` function returns a dictionary with all the starting players included. A team's starting XI can be viewed with the command `/view 11 <team>` (NOTE: Proportions will be fixed later)

![image](https://user-images.githubusercontent.com/119870649/206257976-d61168d7-1ad8-477f-b75f-e40266c3a210.png)

## Currently Working On

Game play logic (without weights) and interaction with user with chance generation and more.
