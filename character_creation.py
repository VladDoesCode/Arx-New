from rich.console import Console
import time
import random
import json
import os
from utils import slow_type, wait_for_input, player_input
from items import healing_potions, armors
from tabulate import tabulate

console = Console()
seperator = '\n' + '-' * console.width + '\n'  # Text separator
character_folder = "characters"  # New folder name

class Character:
    """A class to represent a character in the game."""

    # Initialize the character
    def __init__(self):
        self.name = ""
        self.race = ""
        self.character_class = ""
        self.attributes = {}
        self.ac = 0
        self.health = 0
        self.max_health = 0
        self.weapons = []
        self.actions = []
        self.inventory = []
        self.xp = 0
        self.level = 1

    def modifier(self, attribute_value):
        """Calculate the modifier for an attribute value."""
        return (attribute_value - 10) // 2

    # Show the character's stats
    def show_character_stats(self):
        # Define color codes
        HEADER_COLOR = "\033[95m"
        NAME_COLOR = "\033[92m"
        RACE_COLOR = "\033[93m"
        CLASS_COLOR = "\033[94m"
        RESET_COLOR = "\033[0m"

        # Define header
        header = ["Name", "Race", "Class", "Attributes", "Action", "Attack Bonus", "Damage", "Damage Type"]

        # Populate the Attributes column
        attributes_string = '\n'.join([f"{attr}: {value} (Mod: {self.modifier(value)})" for attr, value in self.attributes.items()])

        # Populate the table with the character information
        rows = []
        for action in self.actions:
            row = [
                f"{NAME_COLOR}{self.name}{RESET_COLOR}" if self.name and not rows else "",
                f"{RACE_COLOR}{self.race}{RESET_COLOR}" if self.race and not rows else "",
                f"{CLASS_COLOR}{self.character_class}{RESET_COLOR}" if self.character_class and not rows else "",
                attributes_string if attributes_string and not rows else "",
                action["name"],
                action["attackBonus"],
                action["damage"],
                action["damagetype"]
            ]
            rows.append(row)

        # Create the table string
        table_string = tabulate(rows, headers=header, tablefmt="grid")

        # Colorize the header
        for h in header:
            table_string = table_string.replace(h, f"{HEADER_COLOR}{h}{RESET_COLOR}")

        # Display the table
        slow_type(table_string, 0.001, styles=["bold"], center=True)

        # Wait for user input before continuing
        wait_for_input()

    # Helps make list choosing easier
    def choose_from_list(self, choice_list, prompt, go_back=False, speed=0.013, style=None, center=False):
        """Helper function to choose an item from a list"""
        while True:
            for i, item in enumerate(choice_list):
                slow_type(f"{i + 1}. {item}", speed, center=center)
            if go_back:
                slow_type("0. Go Back", speed, center=center)
            slow_type(prompt, new_line=False, styles=style, center=center)
            choice = input()
            if choice.isdigit():
                if go_back and int(choice) == 0:
                    print('\n')
                    return None
                elif 1 <= int(choice) <= len(choice_list):
                    print('\n')
                    return choice_list[int(choice) - 1]
            slow_type('Invalid choice!\n', speed, styles=["bold", "Red"], center=center)

    # Load a character from a file
    def choose_character(self):
        """Look for character files in the character folder."""
        character_files = [file for file in os.listdir(character_folder) if file.endswith(".json")]
        if len(character_files) == 0:
            return None
        slow_type("Character Files:", center=True)
        character_files.append("Create new character")
        choice = player_input("Choose a character file to load (enter the corresponding number), or choose 'Create new character': ", character_files, is_list=True, center=True)
        # choice = self.choose_from_list(character_files, "Choose a character file to load (enter the corresponding number), or choose 'Create new character': ", style=["bold", "underline"], center=True)
        if choice == "Create new character":
            return None
        else:
            player = self.load_character(choice)
            slow_type(f"Character '{choice}' loaded successfully!\n", styles=["bold", "Green"], center=True)
            time.sleep(.5)
            return player

    # Choose character name
    def choose_name(self):
        """Choose a name for the character."""
        while True:
            slow_type((f'Please enter your character\'s name: '), new_line=False, styles=["bold"])
            self.name = input()
            if os.path.exists(f"{self.name}.json"):
                slow_type("A character file with that name already exists. Please choose a different name.")
            else:
                slow_type(f"Welcome, {self.name}!")
                print(seperator)  # Separator
                slow_type('Character Creation]', styles=["bold"])
                break

    # Choose character race
    def choose_race(self):
        """Choose a race for the character."""
        # Race selection
        races = {
            'Player\'s Handbook / Basic Rules (9 Races)': ['Dragonborn', 'Dwarf', 'Elf', 'Gnome', 'Half-Elf', 'Halfling', 'Half-Orc', 'Human', 'Tiefling'],
            'Mordenkainen Presents: Monsters of the Multiverse (33 Races)': ['Aarakocra', 'Aasimar', 'Air Genasi', 'Bugbear', 'Centaur', 'Changeling', 'Deep Gnome', 'Duergar', 'Earth Genasi', 'Eladrin', 'Fairy', 'Firbolg', 'Fire Genasi', 'Githyanki', 'Githzerai', 'Goblin', 'Goliath', 'Harengon', 'Hobgoblin', 'Kenku', 'Kobold', 'Lizardfolk', 'Minotaur', 'Orc', 'Satyr', 'Sea Elf', 'Shadar-kai', 'Shifter', 'Tabaxi', 'Tortle', 'Triton', 'Water Genasi', 'Yuan-ti'],
            'Dragonlance: Shadow of the Dragon Queen (1 Race)': ['Kender'],
            'Spelljammer: Adventures in Space (6 Races)': ['Astral Elf', 'Autognome', 'Giff', 'Hadozee', 'Plasmoid', 'Thri-kreen'],
            'Strixhaven: A Curriculum of Chaos (1 Race)': ['Owlin'],
            'Mythic Odysseys of Theros (2 Races)': ['Leonin', 'Satyr'],
            'Eberron: Rising from the Last War (3 Races)': ['Kalashtar', 'Shifter', 'Warforged'],
            'Acquisitions Incorporated (1 Race)': ['Verdan'],
            'Guildmasters\' Guide to Ravnica (3 Races)': ['Loxodon', 'Simic Hybrid', 'Vedalken'],
            'Sword Coast Adventurer\'s Guide (1 Race)': ['Feral Tiefling'],
            'The Tortle Package (1 Race)': ['Tortle'],
            'Locathah Rising (1 Race)': ['Locathah'],
            'One Grung Above (1 Race)': ['Grung']
        }
        while True:
            selected_race_category = self.choose_from_list(list(races.keys()), 'Choose a category of races (enter the corresponding number): ', speed=0, style=["bold", "underline"])
            if selected_race_category is not None:
                race_list = races[selected_race_category]
                chosen_race = self.choose_from_list(race_list, 'Choose a race (enter the corresponding number): ', go_back=True, speed=0, style=["bold", "underline"])
                if chosen_race is not None:
                    self.race = chosen_race
                    break

    # Choose character class
    def choose_class(self):
        """Choose a class for the character."""
        # Class selection
        classes = {
            'Player\'s Handbook / Basic Rules (12 Classes)': ['Barbarian', 'Bard', 'Cleric', 'Druid', 'Fighter', 'Monk', 'Paladin', 'Ranger', 'Rogue', 'Sorcerer', 'Warlock', 'Wizard'],
            'Tasha\'s Cauldron of Everything (1 Class)': ['Artificer'],
            'Critical Role (1 Class)': ['Blood Hunter']
        }
        print(seperator)  # Separator
        while True:
            selected_class_category = self.choose_from_list(list(classes.keys()), 'Choose a category of classes (enter the corresponding number): ', speed=0, style=["bold", "underline"])
            if selected_class_category is not None:
                class_list = classes[selected_class_category]
                chosen_class = self.choose_from_list(class_list, 'Choose a class (enter the corresponding number): ', go_back=True, speed=0, style=["bold", "underline"])
                if chosen_class is not None:
                    self.character_class = chosen_class
                    break

    # Choose character attributes and Assign AC and Health
    def choose_attributes(self):
        """Roll and assign attribute values."""
        # Attribute roll and allocation
        attributes = ['Strength', 'Dexterity', 'Constitution', 'Intelligence', 'Wisdom', 'Charisma']
        # Roll for attributes
        slow_type('Attribute Allocation', styles=["bold"])
        rolls = [self.roll_dice(4, 6, drop_lowest=True) for _ in range(6)]
        rolls.sort(reverse=True)

        for attr in attributes:
            slow_type(f"Available rolls: {rolls}")
            slow_type((f"Choose a value for {attr} (enter the corresponding number): "), new_line=False, styles=["bold", "underline"])
            attr_roll = int(input())

            while attr_roll not in rolls:
                slow_type("Invalid selection. Please choose a value from the available rolls.")
                slow_type((f"Choose a value for {attr} (enter the corresponding number): "), new_line=False, styles=["bold", "underline"])
                attr_roll = int(input())

            self.attributes[attr] = attr_roll
            rolls.remove(attr_roll)

        # Calculate AC and health
        armor_ac_values = [armor['ac'] for armor in self.inventory if armor.get('ac')]
        if armor_ac_values:
            max_armor_ac = max(armor_ac_values)
            self.ac = max(max_armor_ac, 10 + self.modifier(self.attributes['Dexterity']))
        else:
            self.ac = 10 + self.modifier(self.attributes['Dexterity'])

        hit_dice = {
            'Barbarian': 12, 'Fighter': 10, 'Paladin': 10, 'Ranger': 10,
            'Bard': 8, 'Cleric': 8, 'Druid': 8, 'Monk': 8, 'Rogue': 8, 'Warlock': 8,
            'Sorcerer': 6, 'Wizard': 6, 'Artificer': 8, 'Blood Hunter': 10
        }
        self.health = hit_dice[self.character_class] + self.modifier(self.attributes['Constitution'])
        self.max_health = self.health

    def choose_weapons(self):
        """Choose weapons for the character."""
        weapons = [
            {'name': 'Short Sword', 'damage': '1d6', 'type': 'piercing', 'property': 'Finesse'},
            {'name': 'Long Sword', 'damage': '1d8', 'type': 'slashing', 'property': None},
            {'name': 'Dagger', 'damage': '1d4', 'type': 'piercing', 'property': 'Finesse'},
            {'name': 'Battleaxe', 'damage': '1d8', 'type': 'slashing', 'property': None},
            {'name': 'Handaxe', 'damage': '1d6', 'type': 'slashing', 'property': None},
            {'name': 'Javelin', 'damage': '1d6', 'type': 'piercing', 'property': 'Thrown'},
            {'name': 'Mace', 'damage': '1d6', 'type': 'bludgeoning', 'property': None},
            {'name': 'Quarterstaff', 'damage': '1d6', 'type': 'bludgeoning', 'property': 'Versatile'},
            {'name': 'Spear', 'damage': '1d6', 'type': 'piercing', 'property': 'Thrown'},
            {'name': 'Light Crossbow', 'damage': '1d8', 'type': 'piercing', 'property': 'Ranged'},
            {'name': 'Shortbow', 'damage': '1d6', 'type': 'piercing', 'property': 'Ranged'},
        ]

        chosen_weapons = []

        while len(chosen_weapons) < 2:
            # Display weapons
            console.print(('[bold]Weapon Selection[/bold]'))
            for i, weapon in enumerate(weapons):
                if weapon not in chosen_weapons:  # Check if the weapon has already been chosen
                    # Determine appropriate attribute for attack bonus
                    if weapon['property'] == 'Finesse':
                        attack_bonus = max(self.modifier(self.attributes['Strength']), self.modifier(self.attributes['Dexterity']))
                    elif weapon['property'] == 'Ranged':
                        attack_bonus = self.modifier(self.attributes['Dexterity'])
                    else:
                        attack_bonus = self.modifier(self.attributes['Strength'])

                    # Add + symbol for positive bonuses
                    attack_bonus = f"+{attack_bonus}" if attack_bonus >= 0 else attack_bonus

                    console.print(f'{i + 1}. {weapon["name"]} - Damage: {weapon["damage"]} {weapon["type"].title()} - Attack Bonus: {attack_bonus}')

            slow_type('Choose a weapon (enter the corresponding number), you get to pick 2: ', new_line=False, styles=["bold", "underline"])
            weapon_choice = input()
            if weapon_choice.isdigit() and 1 <= int(weapon_choice) <= len(weapons):
                chosen_weapon = weapons[int(weapon_choice) - 1]
                if chosen_weapon in chosen_weapons:
                    print(f"You've already chosen the {chosen_weapon['name']}!")
                else:
                    chosen_weapons.append(chosen_weapon)
                    print(f"You've chosen the {chosen_weapon['name']}!")
                    weapons.remove(chosen_weapon)  # Remove the chosen weapon from the list
            else:
                print('Invalid choice!')

        self.weapons = chosen_weapons

    def generate_actions(self):
        """Generate actions for each weapon."""
        player_actions = []
        for weapon in self.weapons:
            if weapon['property'] == 'Finesse':
                attack_bonus = max(self.modifier(self.attributes['Strength']), self.modifier(self.attributes['Dexterity']))
            elif weapon['property'] == 'Ranged':
                attack_bonus = self.modifier(self.attributes['Dexterity'])
            else:
                attack_bonus = self.modifier(self.attributes['Strength'])

            action = {
                'name': 'Attack with ' + weapon['name'],
                'description': f"{weapon['name']} {weapon['type'].title()} Attack",
                'attackBonus': f"+{attack_bonus}",
                'damage': weapon['damage'],
                'damagetype': weapon['type']
            }
            player_actions.append(action)

        self.actions = player_actions

    def generate_inventory(self):
        """Generate the initial inventory for the character."""
        self.inventory.append(healing_potions[0])  # Add a Minor Healing Potion to the inventory
        self.inventory.append(armors[0])  # Add Padded Armor to the inventory

    def generate_character(self):
        """Function to go through the steps of character creation."""
        if self.choose_character() is None:
            slow_type('First, you must create your character...')
            self.choose_name()
            self.choose_race()
            self.choose_class()
            print(seperator)
            self.choose_attributes()
            self.choose_weapons()
            self.generate_actions()
            self.generate_inventory()
            self.save_character()
        self.show_character_stats()

    def save_character(self, quicksave=False):
        """Save character to a .json file."""
        filename = os.path.join(character_folder, f"{self.name}.json")
        with open(filename, 'w') as f:
            json.dump(self.__dict__, f)
        if quicksave:
            slow_type(f"Character saved as {filename}")

    def load_character(self, filename):
        """Load character from a .json file."""
        with open(os.path.join(character_folder, filename), 'r') as f:
            data = json.load(f)
        for key, value in data.items():
            setattr(self, key, value)
        return self
    
    def delete_character(self):
        """Delete the character file from the character folder."""
        filename = os.path.join(character_folder, f"{self.name}.json")
        if os.path.exists(filename):
            os.remove(filename)
            print(f"Character '{self.name}' deleted successfully.")
            wait_for_input()
        else:
            print(f"Character '{self.name}' does not exist.")
        

    # Dice rolling function
    def roll_dice(self, number, sides, drop_lowest=False):
        """Helper function to roll a set of dice."""
        rolls = [random.randint(1, sides) for _ in range(number)]
        if drop_lowest:
            return sum(sorted(rolls)[1:])
        else:
            return sum(rolls)
        
    def next_level_experience(self):
        """Return the experience points needed for the next level."""
        
        # Table for experience points needed for each level
        level_xp_table = [
            0, 300, 900, 2700, 6500, 14000, 23000, 34000, 48000, 64000,
            85000, 100000, 120000, 140000, 165000, 195000, 225000, 265000, 305000, 355000
        ]
        
        # Find the current level based on XP
        current_level = self.level
        for i, xp_needed in enumerate(level_xp_table):
            if self.xp >= xp_needed:
                current_level = i + 1
            else:
                break
        
        # Return the experience points needed for the next level
        if current_level < 20:
            return level_xp_table[current_level] - self.xp
        else:
            return 0  # At level 20, no more levels can be gained


# while True:
#     character = Character()
#     character.generate_character()
