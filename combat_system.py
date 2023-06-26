import random
import time
import re
import sys
from character_creation import Character
from utils import display_healthbars, slow_type
from items import healing_potions
from inventory import add_item_to_inventory, use_item
from colorama import init, Fore, Back, Style
from term_image.image import from_url
from PIL import Image
from term_image.image import AutoImage
import requests
from io import BytesIO
import shutil


def parse_damage(damage_string):
    if "d" in damage_string:  # handle dice expressions
        split_parts = re.split("\+|-", damage_string)
        dice_part = split_parts[0]
        # If there is no modifier, default it to 0
        modifier_part = split_parts[1] if len(split_parts) > 1 else '0'
        dice_count, dice_value = map(int, dice_part.split("d"))
        modifier = int(modifier_part)
        modifier = -modifier if "-" in damage_string else modifier
        return sum(random.randint(1, dice_value) for _ in range(dice_count)) + modifier
    else:  # handle fixed damage amounts
        return int(damage_string)

def crop_image(img: Image.Image) -> Image.Image:
    bbox = img.getbbox()  # Get bounding box of the non-zero regions in the image
    img_cropped = img.crop(bbox)  # Crop the image to the bounding box dimensions
    return img_cropped

def combat(player, monsters):
    monster = random.choice(monsters)

    # Get the terminal width
    terminal_width, _ = shutil.get_terminal_size()

    # Fetch the image from the URL
    response = requests.get(monster['tokenURL'])
    img = Image.open(BytesIO(response.content))

    # Crop the image to remove blank spaces
    img_cropped = crop_image(img)

    # Convert the cropped image to a term-image instance
    image = AutoImage(img_cropped, width=terminal_width // 4)

    # Render the image as a string
    image_str = str(image)

    slow_type(f"\nYou have encountered a {monster['name']}! Prepare for battle...", styles=["bold", "italic", "red", "underline"])
    slow_type("\n" + image_str + "\n", speed=0.00005)

    playerInitiative = random.randint(1, 20) + player.modifier(player.attributes['Dexterity'])
    monsterInitiative = random.randint(1, 20) + player.modifier(monster['dexterity'])
    playerColor, monsterColor = (Fore.GREEN, Fore.RED) if playerInitiative > monsterInitiative else ((Fore.RED, Fore.GREEN) if playerInitiative < monsterInitiative else (Fore.YELLOW, Fore.YELLOW))
    slow_type(f"{player.name} rolled a {playerColor}{Style.BRIGHT}{playerInitiative}{Fore.RESET} for initiative!")
    slow_type(f"{monster['name']} rolled a {monsterColor}{Style.BRIGHT}{monsterInitiative}{Fore.RESET} for initiative!")

    monsterMaxHealth = int(parse_damage(monster['health'])) 
    monsterCurrentHealth = monsterMaxHealth
    display_healthbars(player, monster, monsterMaxHealth, monsterCurrentHealth)

    if playerInitiative > monsterInitiative or (playerInitiative == monsterInitiative and player.attributes['Dexterity'] >= monster['dexterity']):
        player_turn = True
    else:
        player_turn = False

    while player.health > 0 and monsterCurrentHealth > 0:
        if player_turn:
            slow_type(f"\n{player.name}'s turn!", styles=["bold", "underline", "green"])
            choices = 'Attack, Run'
            if len(player.inventory) > 0:
                choices += ', Inventory'

            slow_type(f'(Choose an action: {choices}): ', new_line=False, styles=["bold underline"])
            player_action = input()
            player_action = player_action.lower().strip()

            if player_action.lower() in ['attack', 'a']:
                for i, weapon in enumerate(player.weapons):
                    slow_type(f"{i + 1}. {weapon['name']} - Damage: {weapon['damage']}")

                slow_type(f"Choose a weapon (enter the corresponding number): ", new_line=False, styles=["bold underline"])
                weapon_choice = int(input())

                random_roll = random.randint(1, 20)
                attack_roll = random_roll + int(player.actions[weapon_choice - 1]['attackBonus'])
                slow_type(f"You rolled a {Fore.GREEN if attack_roll >= monster['ac'] else Fore.RED}{Style.BRIGHT}{attack_roll}{Fore.RESET} against the {monster['name']}'s armor class of {Fore.RED if attack_roll >= monster['ac'] else Fore.GREEN}{Style.BRIGHT}{monster['ac']}{Fore.RESET}!")

                if attack_roll >= monster['ac']:
                    player_damage = parse_damage(player.weapons[weapon_choice - 1]['damage'])
                    monsterCurrentHealth -= player_damage

                    weapon_property = player.weapons[weapon_choice - 1]['property']
                    if weapon_property is None or weapon_property == 'Versatile':
                        slow_type(f"You swing your {player.weapons[weapon_choice - 1]['name']} with might and strike the {monster['name']} for {Fore.RED}{player_damage}{Fore.RESET} damage!", styles=["bold"])
                    elif weapon_property == 'Thrown':
                        slow_type(f"You throw your {player.weapons[weapon_choice - 1]['name']} with pinpoint precision and land it into the {monster['name']} for {Fore.RED}{player_damage}{Fore.RESET} damage!", styles=["bold"])
                    elif weapon_property == 'Ranged':
                        slow_type(f"You shoot your {player.weapons[weapon_choice - 1]['name']} with great accuracy and strike the {monster['name']} for {Fore.RED}{player_damage}{Fore.RESET} damage!", styles=["bold"])

                    # Display monster health bar after player's turn
                    display_healthbars(player, monster, monsterMaxHealth, monsterCurrentHealth)
                else:
                    slow_type(f"You attempt to use your {player.weapons[weapon_choice - 1]['name']} but miss the {monster['name']}!")

            elif player_action.lower() in ['run', 'r']:
                slow_type("You took a quick glance at the monstrous beast before you and decided discretion was the better part of valor. You quickly made your escape!")
                return

            elif player_action.lower() in ['inventory', 'inv', 'i']:
                # Check if the player has items in their inventory
                if len(player.inventory) > 0:
                    # Display available items
                    for i, item in enumerate(player.inventory):
                        print(f"{i + 1}. {item['name']} - {item['description']}")

                    print('0. Go Back')

                    slow_type(f"Choose an item to use (enter the corresponding number): ", new_line=False, styles=["bold underline"])
                    item_choice = int(input())

                    if item_choice == 0:
                        continue  # Go back to the player's turn

                    if 1 <= item_choice <= len(player.inventory):
                        # Use the chosen item
                        use_item(player, item_choice - 1)
                        # Display player health bar after using the item
                        display_healthbars(player, monster, monsterMaxHealth, monsterCurrentHealth)
                    else:
                        slow_type("Invalid item choice!")
                else:
                    slow_type("You have no items in your inventory!")
                    continue
            else:
                slow_type("Invalid action!")
                continue


        else:
            # Monster's turn
            if monsterCurrentHealth > 0:
                slow_type(f"\n{monster['name']}'s turn!", styles=["bold", "underline", "red"])

                if 'actions' in monster and len(monster['actions']):  # Check if 'actions' exists and is not empty
                    # Roll for Attack (d20 + attack_bonus of monster's action >= player's AC)
                    monster_attack_roll = random.randint(1, 20) + int(monster['actions'][0]['attackBonus'])
                    slow_type(f"The {monster['name']} rolled a {Fore.GREEN if monster_attack_roll >= player.ac else Fore.RED}{Style.BRIGHT}{monster_attack_roll}{Style.RESET_ALL} against your armor class of {Fore.RED if monster_attack_roll >= player.ac else Fore.GREEN}{Style.BRIGHT}{player.ac}{Style.RESET_ALL}!")
                    if monster_attack_roll >= player.ac:
                        player_damage = parse_damage(monster['actions'][0]['damage'])
                        player.health -= player_damage
                        slow_type(f"The {monster['name']} lunged at you, landing a heavy blow and dealing {Fore.RED}{player_damage}{Fore.RESET} damage!")
                        time.sleep(1)
                        # Display player health bar after monster's turn if they hit
                        display_healthbars(player, monster, monsterMaxHealth, monsterCurrentHealth)
                    else:
                        slow_type(f"The {monster['name']} attempted to attack you but missed!")
                else:
                    slow_type(f"The {monster['name']} seems to be stunned and did not retaliate!")     

        # Switch turns
        player_turn = not player_turn

    # Check who won the fight
    if player.health <= 0:
        slow_type("With a heavy heart, your vision blurred, the last thing you saw was the menacing figure of the monster looming over you... You have been defeated...")
        # Delete the character if defeated in combat
        Character.delete_character(player)
        sys.exit()
    else:
        slow_type(f"\nWith a final strike, you slayed the {monster['name']}! {Fore.YELLOW}{Style.BRIGHT}Victory is yours!{Style.RESET_ALL}")

        # Add monster's loot to player's inventory
        # Check if the monster drops a healing potion
        if random.random() < 0.6:  # Adjust the probability as desired
            potion_type = random.choices(
                healing_potions,
                weights=[1 if p['rarity'] == 'common' else 0.5 for p in healing_potions]
            )[0]

            # Add the healing potion to the player's inventory
            add_item_to_inventory(player, potion_type)
            slow_type(f"The {monster['name']} dropped a {potion_type['name']}!")

        # Save the character if alive after combat
        Character.save_character(player)