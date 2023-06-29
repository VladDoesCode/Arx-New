import random
import json
import os
from utils import slow_type, wait_for_input, player_input, seperator, move_cursor_up
from items import item_dict
from colorama import init, Fore, Back, Style
import json
import items

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
        self.equipped_items = []  # Add an equipped_items attribute
        self.xp = 0
        self.level = 1
        self.currencies = []
    
    def add_to_inventory(self, item, quantity=1):
        """Add an item to the character's inventory."""
        item['quantity'] = quantity  # Add the 'quantity' key to the item dictionary
        self.inventory.append(item)  # Append the item to the inventory

    def equip_item(self, item):
        """Equip an item."""
        self.equipped_items.append(item)

    def unequip_item(self, item):
        """Unequip an item."""
        self.equipped_items.remove(item)

    def modifier(self, attribute_value):
        """Calculate the modifier for an attribute value."""
        return (attribute_value - 10) // 2

    # Show the character's stats
    def show_character_stats(self):
        # Define header
        header = ["Name", "Race", "Class", "Attributes", "Actions", "Inventory", "Health", "Level", "XP", "Currencies", "Equipped Items"]

        # Populate the Attributes column
        attributes_string = '\n'.join([f"{attr}: {value} ({self.modifier(value)})" for attr, value in self.attributes.items()])

        # Populate the Actions column
        actions_string = '\n'.join([f"{action['name']} (Attack Bonus: {action['attack_bonus']}, Damage: {action['damage']}, Damage Type: {action['type']})" for action in self.actions])

        # Populate the Inventory column
        inventory_string = '\n'.join([f"{item['name']} ({item['quantity']})" for item in self.inventory])

        # Populate the Currencies column
        currencies_string = '\n'.join([f"{currency['name']}: {currency['amount']}" for currency in self.currencies])

        # Populate the Equipped Items column
        equipped_items_string = '\n'.join([f"{item['name']} ({', '.join([f'{stat}: {value}' for stat, value in item['stats'].items()])})" for item in self.equipped_items])

        # Create the table rows
        rows = [
            [
                self.name,
                self.race,
                self.character_class,
                attributes_string,
                actions_string,
                inventory_string,
                f"{self.health}/{self.max_health} {'█' * int(self.health / self.max_health * 10)}{'-' * (10 - int(self.health / self.max_health * 10))}",
                f"{self.level} {'█' * int(self.xp / self.next_level_experience() * 10)}{'-' * (10 - int(self.xp / self.next_level_experience() * 10))} {self.next_level_experience()}",
                currencies_string,
                equipped_items_string
            ]
        ]

        # Create the table string
        table_string = ""
        for row in rows:
            for i, cell in enumerate(row):
                table_string += f"{cell:<20}" if i != len(row) - 1 else f"{cell}\n"

        # Display the table
        print(table_string)

        # Wait for user input before continuing
        wait_for_input()

    # Load a character from a file
    def choose_character(self):
        """Look for character files in the character folder."""
        character_files = [file for file in os.listdir(character_folder) if file.endswith(".json")]
        if len(character_files) == 0:
            return None
        slow_type("Character Files:", center=True)
        character_files.append("Create new character")
        choice = player_input("Choose a character file to load (enter the corresponding number), or choose 'Create new character': ", character_files, is_list=True, center=True)
        if choice == "Create new character":
            seperator()  # Separator
            return None
        else:
            player = self.load_character(choice)
            slow_type(f"Character '{choice}' loaded successfully!\n", styles=["bold", "Green"], center=True)
            # Clear the screen
            print("\033c", end='')
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
                seperator()  # Separator
                slow_type('Character Creation', styles=["bold"])
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
            selected_race_category = player_input('Choose a category of race (enter the corresponding number): ', list(races.keys()), is_list=True, speed=0, styles=["bold", "underline"], new_line=True)
            # selected_race_category = self.choose_from_list(list(races.keys()), 'Choose a category of races (enter the corresponding number): ', speed=0, style=["bold", "underline"])
            if selected_race_category is not None:
                race_list = races[selected_race_category]
                chosen_race = player_input('Choose a race (enter the corresponding number): ', race_list, is_list=True, go_back=True, speed=0, styles=["bold", "underline"])
                # chosen_race = self.choose_from_list(race_list, 'Choose a race (enter the corresponding number): ', go_back=True, speed=0, style=["bold", "underline"], new_line=False)
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
        seperator()  # Separator
        while True:
            selected_class_category = player_input('Choose a category of class (enter the corresponding number): ', list(classes.keys()), is_list=True, speed=0, styles=["bold", "underline"], new_line=True)
            # selected_class_category = self.choose_from_list(list(classes.keys()), 'Choose a category of classes (enter the corresponding number): ', speed=0, style=["bold", "underline"])
            if selected_class_category is not None:
                class_list = classes[selected_class_category]
                chosen_class = player_input('Choose a class (enter the corresponding number): ', class_list, is_list=True, go_back=True, speed=0, styles=["bold", "underline"])
                # chosen_class = self.choose_from_list(class_list, 'Choose a class (enter the corresponding number): ', go_back=True, speed=0, style=["bold", "underline"])
                if chosen_class is not None:
                    self.character_class = chosen_class
                    break

        seperator()  # Separator

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
            slow_type(f"Available rolls: {Fore.GREEN}{rolls}{Fore.RESET}", speed=0.008)
            attr_roll = player_input(f"Choose a value for {attr} (enter the corresponding number): ", rolls, styles=["bold", "underline"], speed=0.008, is_numeric=True)
            # do something for every attr in atrributes except for the last one:
            if attr != attributes[-1]:
                print("")
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
        move_cursor_up(1)  # Move cursor up 1 line
        seperator()  # Separator

    def choose_weapons(self):
        """Choose weapons for the character."""
        weapons = [
            {'name': 'Short Sword', 'damage': '1d6', 'type': 'piercing', 'property': 'Finesse', 'attack_bonus': max(self.modifier(self.attributes['Strength']), self.modifier(self.attributes['Dexterity']))},
            {'name': 'Long Sword', 'damage': '1d8', 'type': 'slashing', 'property': None, 'attack_bonus': self.modifier(self.attributes['Strength'])},
            {'name': 'Dagger', 'damage': '1d4', 'type': 'piercing', 'property': 'Finesse', 'attack_bonus': max(self.modifier(self.attributes['Strength']), self.modifier(self.attributes['Dexterity']))},
            {'name': 'Battleaxe', 'damage': '1d8', 'type': 'slashing', 'property': None, 'attack_bonus': self.modifier(self.attributes['Strength'])},
            {'name': 'Handaxe', 'damage': '1d6', 'type': 'slashing', 'property': None, 'attack_bonus': self.modifier(self.attributes['Strength'])},
            {'name': 'Javelin', 'damage': '1d6', 'type': 'piercing', 'property': 'Thrown', 'attack_bonus': self.modifier(self.attributes['Strength'])},
            {'name': 'Mace', 'damage': '1d6', 'type': 'bludgeoning', 'property': None, 'attack_bonus': self.modifier(self.attributes['Strength'])},
            {'name': 'Quarterstaff', 'damage': '1d6', 'type': 'bludgeoning', 'property': 'Versatile', 'attack_bonus': self.modifier(self.attributes['Strength'])},
            {'name': 'Spear', 'damage': '1d6', 'type': 'piercing', 'property': 'Thrown', 'attack_bonus': self.modifier(self.attributes['Strength'])},
            {'name': 'Light Crossbow', 'damage': '1d8', 'type': 'piercing', 'property': 'Ranged', 'attack_bonus': self.modifier(self.attributes['Dexterity'])},
            {'name': 'Shortbow', 'damage': '1d6', 'type': 'piercing', 'property': 'Ranged', 'attack_bonus': self.modifier(self.attributes['Dexterity'])},
        ]

        chosen_weapons = []

        while len(chosen_weapons) < 2:
            # Display weapons
            slow_type('Weapon Selection', styles=["bold"], speed=0)
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

                    slow_type(f'{i + 1}. {weapon["name"]} - Damage: {Fore.RED}{weapon["damage"]} {weapon["type"].title()}{Fore.RESET} - Attack Bonus: {Fore.GREEN}{attack_bonus}{Fore.RESET}', speed=0)

            # Choose weapon
            weapon_choice = player_input('Choose a weapon (enter the corresponding number), you get to pick 2: ', valid_options=[i+1 for i in range(len(weapons))], styles=["bold", "underline"], speed=0, is_numeric=True)
            # weapon_choice = player_input('Choose a weapon (enter the corresponding number), you get to pick 2: ', valid_options=[str(i+1) for i in range(len(weapons))], styles=["bold", "underline"], speed=0, is_numeric=True)
            if isinstance(weapon_choice, int) and 1 <= weapon_choice <= len(weapons):
                chosen_weapon = weapons[int(weapon_choice) - 1]
                if chosen_weapon in chosen_weapons:
                    print(f"You've already chosen the {chosen_weapon['name']}!")
                else:
                    chosen_weapons.append(chosen_weapon)
                    slow_type(f"\nYou've chosen the {chosen_weapon['name']}!\n", speed=0, new_line=True, styles=["bold", "yellow"])
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

            # Add + symbol for positive bonuses
            attack_bonus = f"+{attack_bonus}" if attack_bonus >= 0 else attack_bonus

            # Create action dictionary
            action = {
                'name': weapon['name'],
                'damage': weapon['damage'],
                'type': weapon['type'],
                'attack_bonus': attack_bonus
            }

            player_actions.append(action)

        self.actions = player_actions

    def generate_inventory(self):
        """Generate the initial inventory for the character."""
        self.add_to_inventory(item_dict['Backpack']) # Add a backpack to the inventory
        self.add_to_inventory(item_dict['Rations'], 10) # Add 10 days of rations to the inventory
        self.add_to_inventory(item_dict['Torch'], 10) # Add 10 torches to the inventory
        self.add_to_inventory(item_dict['Minor Healing Potion']) # Add a Minor Healing Potion to the inventory
        self.add_to_inventory(item_dict['Padded Armor']) # Add Padded Armor to the inventory

    def generate_character(self):
        """Function to go through the steps of character creation."""
        if self.choose_character() is None:
            slow_type('First, you must create your character...')
            self.choose_name()
            self.choose_race()
            self.choose_class()
            self.choose_attributes()
            self.choose_weapons()
            self.generate_actions()
            self.generate_inventory()
            self.save_character()
            # Clear the screen
            print("\033c", end='')
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
