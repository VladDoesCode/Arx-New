# Arx.py
import json
from game_state import set_my_character
from character_creation import Character
from combat_system import combat
from utils import slow_type, get_terminal_size, wait_for_input
import keyboard

# Get terminal size
term_width, term_height = get_terminal_size()

seperator = ("\n") + ('-' * term_width) + ('\n') # Text separator

# Start the Game
# Clear the screen
print("\033c", end='')
# slow_type('Welcome to....', 0.1, center=True, styles=['bold'])
# slow_type(f"""                                           
#      _____        _____                   
#  ___|\    \   ___|\    \  _____      _____
#  /    /\    \ |    |\    \ \    \    /    / 
# |    |  |    ||    | |    | \    \  /    /  
# |    |__|    ||    |/____/   \____\/____/   
# |    .--.    ||    |\    \   /    /\    \   
# |    |  |    ||    | |    | /    /  \    \  
# |____|  |____||____| |____|/____/ /\ \____| 
# |    |  |    ||    | |    ||    |/  \|    | 
# |____|  |____||____| |____||____|    |____| 
#   \(      )/    \(     )/    \(        )/   
#    '      '      '     '      '        '    
#                                            """,0.005, center=True, styles=['red'], new_line=False)
# slow_type('A Text RPG created by Vladimir B.', center=True)
# slow_type('You will be able to create your own character, and fight monsters in turn-based combat.', center=True)
# slow_type('Notes: If your character dies, their save file will be deleted.', center=True, styles=['green'])
# slow_type('After each combat your character will be quick saved.', center=True, styles=['green'])
# slow_type('At anypoint after character creation you can type "menu" to goto the in game menu!', center=True, styles=['green'])
# print(seperator)

# create a new character
my_character = Character()

# set the my_character object in the game state
set_my_character(my_character)

my_character.generate_character() # Create a character

with open('monsters.json', 'r') as f:
    monsters = json.load(f)

# Run combat
while True:
    combat(my_character, monsters)
    wait_for_input("Press any key to continue and fight another monster, or press 'q' to quit.")
    if keyboard.read_key(suppress=True) == 'q':
        break
    separator = ('-' * term_width) + ('') # Update separator width
    print(separator)