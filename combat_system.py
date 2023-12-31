# Import necessary libraries
import random  # Needed for generating random numbers (used in simulating dice rolls)
import re  # Regular expressions used for parsing damage strings
import sys  # Used to interact with python runtime environment
from character_creation import Character  # Import the Character class from the character_creation module
from utils import display_healthbars, slow_type, player_input  # Import utility functions from the utils module
import items  # Import data for healing potions
from inventory import use_item  # Import inventory management functions
from colorama import init, Fore, Back, Style  # Used to print colored text in terminal
from PIL import Image  # Python Imaging Library used for image processing
from term_image.image import AutoImage  # term_image used for converting image into ASCII art
import requests  # Used for making HTTP requests to fetch images
from io import BytesIO  # Used to read binary streams
import shutil  # High-level file operations
import textwrap  # Used for wrapping text to fit the terminal window
import subprocess  # Used to execute shell commands

# Get the width of the terminal window
terminal_width, _ = shutil.get_terminal_size()

# Set the wrap length to 1/4 of the terminal width
wrap_length = int(terminal_width / 4)
config = {
    "html.format.wrapLineLength": wrap_length
}

# Function to parse the damage string and calculate the total damage
def parse_damage(damage):
    if "d" in damage:
        # Split the string into the dice expression and the modifier
        split_parts = damage.split(" ")
        dice_expression = split_parts[0]
        # Default modifier to 0 if not present
        modifier = split_parts[1] if len(split_parts) > 1 else '0'
        # Split the modifier into its sign and value using regular expressions
        match = re.match(r"([-+]?)(\d+)", modifier)
        if match:
            sign, value = match.groups()
        else:
            sign, value = "+", "0"
        # Split the dice expression into the number of dice and the type of dice
        dice_count, dice_value = map(int, dice_expression.split("d"))
        # Roll the dice and calculate the total damage
        damage_roll = sum(random.randint(1, dice_value) for _ in range(dice_count))
        # Apply the modifier to the damage roll
        damage_roll += int(sign + value)
        return damage_roll
    else:
        # If a fixed damage amount, simply convert it to an integer
        return int(damage)


# Function to crop the image to remove blank spaces
def crop_image(img: Image.Image) -> Image.Image:
    # Get the bounding box of the non-zero regions in the image
    bbox = img.getbbox()
    # Crop the image to the bounding box dimensions
    return img.crop(bbox)

# Combat function that simulates a fight between the player and a random monster
def combat(player, monsters):
    # Randomly select a monster from the list of monsters
    monster = random.choice(monsters)

    # Get the terminal width for image rendering
    terminal_width, _ = shutil.get_terminal_size()

    # Fetch the monster image from the URL
    response = requests.get(monster['tokenURL'])
    img = Image.open(BytesIO(response.content))

    # Crop the image to remove blank spaces
    img_cropped = crop_image(img)

    # Convert the cropped image to ASCII art for terminal rendering
    image = AutoImage(img_cropped, width=terminal_width // 4)
    image_str = str(image)

    # Display the monster encounter message and render the monster image
    slow_type(f"\nYou have encountered a {monster['name']}! Prepare for battle...", styles=["bold", "italic", "red", "underline"])
    slow_type("Description: " + textwrap.fill(monster['description'], wrap_length), speed=0.004)
    slow_type("\n" + image_str + "\n", speed=0.000025)

    # Calculate initiative to determine turn order
    playerd20 = random.randint(1, 20)
    monsterd20 = random.randint(1, 20)
    playerInitiative = max(playerd20 + player.modifier(player.attributes['Dexterity']), 1)
    monsterInitiative = max(monsterd20 + player.modifier(monster['dexterity']), 1)
    
    # Color code for player and monster based on initiative
    playerColor, monsterColor = (Fore.GREEN, Fore.RED) if playerInitiative > monsterInitiative else ((Fore.RED, Fore.GREEN) if playerInitiative < monsterInitiative else (Fore.YELLOW, Fore.YELLOW))
    
    # Display initiative rolls
    slow_type(f"{player.name} rolled a {playerColor}{Style.BRIGHT}{playerInitiative}{Style.RESET_ALL} \x1B[4m(D20:{playerd20} + Dex Mod:{player.modifier(player.attributes['Dexterity'])}){Style.RESET_ALL} for initiative!")
    slow_type(f"{monster['name']} rolled a {monsterColor}{Style.BRIGHT}{monsterInitiative}{Style.RESET_ALL} \x1B[4m(D20:{monsterd20} + Dex Mod:{player.modifier(monster['dexterity'])}){Style.RESET_ALL} for initiative!")

    # Initialize monster health
    monsterMaxHealth, monsterCurrentHealth = max(int(parse_damage(monster['health'])), 1), max(int(parse_damage(monster['health'])), 1)

    # Display health bars at the start of combat
    display_healthbars(player, monster, monsterMaxHealth, monsterCurrentHealth)

    # Determine who goes first based on initiative and Dexterity attribute
    player_turn = playerInitiative > monsterInitiative or (playerInitiative == monsterInitiative and player.attributes['Dexterity'] >= monster['dexterity'])

    # Main combat loop
    while player.health > 0 and monsterCurrentHealth > 0:
        # Player's turn
        if player_turn:
            # Display player's turn message
            slow_type(f"\n{player.name}'s turn!", styles=["bold", "underline", "green"])

            # Ask player for action choice using player_input function
            player_action = player_input('(Choose an action: Move, Action, Bonus Action, Inventory, Show Character Stats, Quit): ', ['move', 'action', 'bonus action', 'inventory', 'show character stats', 'quit'])

            # Handling movement
            if player_action == 'move':
                slow_type("Moving is not implemented yet.")
                continue
            
            # Handling action
            elif player_action == 'action':
                # Display available weapons
                for i, weapon in enumerate(player.weapons):
                    slow_type(f"{i + 1}. {weapon['name']} - Damage: {Fore.YELLOW}{weapon['damage']}{Fore.RESET} - Attack Bonus: {Fore.YELLOW}{weapon['attack_bonus']}{Fore.RESET}")


                # Ask player for weapon choice using player_input function
                weapon_choice = player_input("Choose a weapon (enter the corresponding number): ", range(1, len(player.weapons) + 1), is_numeric=True)
                print()

                # Simulate an attack roll
                random_roll = random.randint(1, 20)
                attack_roll = random_roll + int(player.actions[weapon_choice - 1]['attack_bonus']) # type: ignore
                slow_type(f"You rolled a {Fore.GREEN if attack_roll >= monster['ac'] else Fore.RED}{Style.BRIGHT}{attack_roll}{Fore.RESET} (D20: {random_roll} + Attack Bonus: {int(player.actions[weapon_choice - 1]['attack_bonus'])}){Style.RESET_ALL} against the {monster['name']}'s armor class of {Fore.RED if attack_roll >= monster['ac'] else Fore.GREEN}{Style.BRIGHT}{monster['ac']}{Fore.RESET}!")

                # Check if the attack hits
                if attack_roll >= monster['ac']:
                    # Calculate and apply damage
                    player_damage = parse_damage(player.weapons[weapon_choice - 1]['damage']) # type: ignore
                    monsterCurrentHealth -= player_damage

                    # Determine attack flavor text based on weapon properties
                    weapon_property = player.weapons[weapon_choice - 1]['property'] # type: ignore
                    if weapon_property is None or weapon_property == 'Versatile':
                        slow_type(f"You swing your {player.weapons[weapon_choice - 1]['name']} with might and strike the {monster['name']} for {Fore.RED}{player_damage}{Fore.RESET} damage!") # type: ignore
                    elif weapon_property == 'Thrown':
                        slow_type(f"You throw your {player.weapons[weapon_choice - 1]['name']} with pinpoint precision and land it into the {monster['name']} for {Fore.RED}{player_damage}{Fore.RESET} damage!") # type: ignore
                    elif weapon_property == 'Ranged':
                        slow_type(f"You shoot your {player.weapons[weapon_choice - 1]['name']} with great accuracy and strike the {monster['name']} for {Fore.RED}{player_damage}{Fore.RESET} damage!") # type: ignore

                    # Display health bars after player's turn
                    display_healthbars(player, monster, monsterMaxHealth, monsterCurrentHealth)
                else:
                    slow_type(f"You attempt to use your {player.weapons[weapon_choice - 1]['name']} but miss the {monster['name']}!") # type: ignore

            # Handling Bonus Action
            elif player_action == 'bonus action':
                slow_type("Bonus Actions are not yet implemented.")
                continue

            # Handling Inventory
            elif player_action == 'inventory':
                # Check if player has items in inventory
                if len(player.inventory) > 0:
                    # Display available items
                    for i, item in enumerate(player.inventory):
                        print(f"{i + 1}. {item['name']} - {item['description']}")
                    print('0. Go Back')

                    # Ask player for item choice
                    slow_type(f"Choose an item to use (enter the corresponding number): ", new_line=False, styles=["bold underline"])
                    item_choice = int(input())

                    # Handle go back choice
                    if item_choice == 0:
                        continue

                    # Use chosen item if valid
                    if 1 <= item_choice <= len(player.inventory):
                        use_item(player, item_choice - 1)
                        display_healthbars(player, monster, monsterMaxHealth, monsterCurrentHealth)
                    else:
                        slow_type("Invalid item choice!")
                else:
                    slow_type("You have no items in your inventory!")
                    continue
                
            # Handling Show Character Stats
            elif player_action == 'show character stats':
                Character.show_character_stats(player)
                continue

            # Handling Quit
            elif player_action == 'quit':
                slow_type("You took a quick glance at the monstrous beast before you and decided discretion was the better part of valor. You quickly made your escape!")
                return

            # Handle Invalid Actions
            else:
                slow_type("Invalid action!")
                continue

        # Monster's turn
        else:
            if monsterCurrentHealth > 0:
                # Display monster's turn message
                slow_type(f"\n{monster['name']}'s turn!", styles=["bold", "underline", "red"])

                # Check if monster has actions and execute them
                if 'actions' in monster and len(monster['actions']):
                    # Simulate an attack roll
                    d20_roll = random.randint(1, 20)
                    monster_attack_roll = d20_roll + int(monster['actions'][0]['attackBonus'])
                    slow_type(f"The {monster['name']} rolled a {Fore.GREEN if monster_attack_roll >= player.ac else Fore.RED}{Style.BRIGHT}{monster_attack_roll}{Style.RESET_ALL} (D20:{d20_roll} + Attack Bonus:{int(monster['actions'][0]['attackBonus'])}) against your armor class of {Fore.RED if monster_attack_roll >= player.ac else Fore.GREEN}{Style.BRIGHT}{player.ac}{Style.RESET_ALL}!")

                    # Check if the attack hits
                    if monster_attack_roll >= player.ac:
                        # Calculate and apply damage
                        player_damage = parse_damage(monster['actions'][0]['damage'])
                        player.health -= player_damage
                        slow_type(f"The {monster['name']} lunged at you, attacking you with \x1B[4m{monster['actions'][0]['name']} and dealing{Style.RESET_ALL} {Fore.RED}{player_damage}{Fore.RESET} damage!")
                        # Display health bars after monster's turn if they hit
                        display_healthbars(player, monster, monsterMaxHealth, monsterCurrentHealth)
                    else:
                        slow_type(f"The {monster['name']} attempted to attack you but missed!")
                else:
                    slow_type(f"The {monster['name']} seems to be stunned and did not retaliate!")

        # Switch turns
        player_turn = not player_turn

    # Determine the outcome of the combat
    if player.health <= 0:
        # Player is defeated
        slow_type(f"\n{player.name} has been defeated by the {monster['name']}... The world fades to black as your last breath leaves you.", styles=["red", "bold", "underline"])
        sys.exit()  # Exit the game
    else:
        # Monster is defeated
        slow_type(f"\nCongratulations, {player.name}! You have defeated the {monster['name']}!", styles=["cyan", "bold", "underline"])
        # Give player experience points for defeating the monster
        player.xp += monster['xp']
        slow_type(f"You gained {Fore.GREEN}{monster['xp']} experience points{Fore.RESET}!", styles=["bold"])

        # Check if player leveled up
        if player.xp >= player.next_level_experience():
            player.level_up()
            slow_type(f"\n{player.name} leveled up to level {Fore.YELLOW}{player.level}{Fore.RESET}!", styles=["bold", "underline"])

        # Random chance for item drop
        if random.random() < 0.5:
            potion = random.choice(items.healing_potions)
            Character.add_to_inventory(player, potion)
            # player.add_to_inventory(player, potion)
            slow_type(f"The {monster['name']} dropped a {Fore.GREEN}{potion['name']}{Fore.RESET}! It has been added to your inventory.\n", styles=["bold"])
        
        # Save the character if alive after combat
        Character.save_character(player)