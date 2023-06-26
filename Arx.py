# main_script.py
import blessed
import time
import json
from character_creation import Character
from combat_system import combat
from utils import slow_type

# Initialize Blessed
term = blessed.Terminal()

seperator = ('-' * term.width) + ('') # Text separator

# Start the Game
with term.fullscreen():
    # Introductory text
    slow_type('Welcome to....', 0.1, center=True, styles=['bold'])
    slow_type(f"""\033[31m                                           
      _____        _____                   
  ___|\    \   ___|\    \  _____      _____
 /    /\    \ |    |\    \ \    \    /    /
|    |  |    ||    | |    | \    \  /    / 
|    |__|    ||    |/____/   \____\/____/  
|    .--.    ||    |\    \   /    /\    \  
|    |  |    ||    | |    | /    /  \    \ 
|____|  |____||____| |____|/____/ /\ \____|
|    |  |    ||    | |    ||    |/  \|    |
|____|  |____||____| |____||____|    |____|
  \(      )/    \(     )/    \(        )/  
   '      '      '     '      '        '   
                                           \033[0m""",0.005, center=True)
    slow_type('A Text RPG created by Vladimir B.', center=True)
    slow_type('You will be able to create your own character, and fight monsters in turn-based combat.', center=True)
    slow_type('Note: If your character dies, their save file will be deleted.', center=True, styles=['green'])
    slow_type('After each combat your character will be quick saved.', center=True, styles=['green'])
    print(seperator)

    my_character = Character()
    my_character.generate_character() # Create a character

    with open('monsters.json', 'r') as f:
        monsters = json.load(f)

    # Run combat
    while True:
        combat(my_character, monsters)
        with term.cbreak(), term.hidden_cursor():  # Hide cursor and react to key presses instantly
            slow_type("Press any key to continue and fight another monster, or press 'q' to quit.")
            key = term.inkey()  # Wait for user input
            if key.lower() == 'q':
                break
