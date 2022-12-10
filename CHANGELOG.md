# Change Log
#### Made by Rayan  
<br />
<br />

## Version 0.0.1
___

- Made function generates individual players

## Version 0.0.2

- Made algorithm that assigns players to teams
- Made ```register``` and ```unregister``` functions that add user's id and name to a database (or removes it)

## Version 0.0.3

- Created `create_world` function that creates a new world along with the necessary databases and commits all data (to be imported and called to create new world, and supplied userid)
- Made algorithm to calculate player value, for transfer purposes
- Connected `register` and `unregister` functions to the generator code, creating or destroying the user's world

## Version 0.0.4

- Remade `world` DB's structure for easier usage and better efficiency
- Decreased high rated player generation
- Fixed problem involving very high rated youngsters


## Version 0.0.5

- Created functions for player card image generation, which can be viewed with the command `show`, to search for a specific player's card
- Made a team's squad viewable

## Version 0.0.6

- Added a mail system for the user to be able to interact with the world
  
## Version 0.0.7

- Created logic for finding a team's starting XI
- Made team starting XI viewable using +show 11 <team> command, which gives a generated image of the starting team (best players)

### Work to be done

- [x] Register User
- [x] Generate World
- [x] Calculate player value
- [x] Make player GUI to view players
- [x] Make team GUI to view teams 
- [x] Create mail inbox
- [x] Create AI for finding Starting XI
- [x] Migrate to slash commands 
- [ ] Fix some proportions
- [ ] Generate offers for user
- [ ] League Fixture Generation
- [ ] View league standings
- [ ] Match Simulation
- [ ] Match Gameplay Logic (currently working on)