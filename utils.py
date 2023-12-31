# utils.py
import sys
import time
import keyboard
from colorama import init, Fore, Back, Style
import shutil
import re
import os
from game_state import get_my_character
import inspect

init()  # Initialize colorama

def slow_type(text, speed=0.013, new_line=True, styles=None, link=None, center=False):
    """Print out text with a typewriter effect."""
    TextStyle = f""

    if link is not None:
        colored_text = f"{Fore.BLUE}{text}{Style.RESET_ALL}"
        text = f"\033]8;;{link}\033\\{colored_text}\033]8;;\033\\"

    if styles is not None:
        for style in styles:
            if style.lower() == "bold":
                # Add {Style.BRIGHT} to TextStyle
                TextStyle += f"{Style.BRIGHT}"

            elif style.lower() == "italic":
                # Add Italic Stylizing to TextStyle
                TextStyle += f"\x1B[3m"

            elif style.lower() == "reverse":
                # Add Reverse Stylizing to TextStyle
                TextStyle += f"\x1B[7m"

            elif style.lower() == "underline":
                # Add Underline Stylizing to TextStyle
                TextStyle += f"\x1B[4m"
            
            elif style.lower() == "blink":
                # Add Blink Stylizing to TextStyle
                TextStyle += f"\x1B[5m"
            
            elif style.lower() in ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]:
                # Add Color Stylizing to TextStyle
                TextStyle += f"{getattr(Fore, style.upper())}"
            
            elif style.lower() in ["back_black", "back_red", "back_green", "back_yellow", "back_blue", "back_magenta", "back_cyan", "back_white"]:
                # Add Background Color Stylizing to TextStyle
                TextStyle += f"{getattr(Back, style[5:].upper())}"

        text = f"{TextStyle}{text}{Style.RESET_ALL}"
    
    # Center the text if center is True
    if center:
        # Get the width of the terminal window
        terminal_width = shutil.get_terminal_size().columns
        # Split the text into lines
        lines = text.splitlines(True)
        for line in lines:
            # Calculate the number of spaces to add before the line
            unstyled_len = len(re.sub(r'\x1B\[\d+m', '', line))
            num_spaces = (terminal_width - unstyled_len) // 2
            # Create a string of spaces with the desired length
            spaces = " " * num_spaces
            # Print the spaces before the line
            print(spaces, end="")
            # Slowtype the line
            for char in line:
                # Print the character, flush to force the stdout buffer to print immediately
                sys.stdout.write(char)
                sys.stdout.flush()
                # Wait until the desired delay has passed
                start_time = time.perf_counter()
                while time.perf_counter() - start_time < speed:
                    pass
            # Print a newline after the line
            if "\n" in line:
                new_line = True
                continue
    else:
        # Slowtype the text
        for char in text:
            # Print the character, flush to force the stdout buffer to print immediately
            sys.stdout.write(char)
            sys.stdout.flush()
            # Wait until the desired delay has passed
            start_time = time.perf_counter()
            while time.perf_counter() - start_time < speed:
                pass

    if new_line:
        print("")


def display_healthbars(player, monster, monsterMaxHealth, MonsterCurrentHealth):
    """Display the health bars for the player and monster at the specified x, y coordinate. Put both health bars on the same line."""
    player_health_percentage = player.health / player.max_health
    player_health_bar = "#" * max(int(player_health_percentage * 10), 1 if player.health > 0 else 0)
    monster_health_percentage = MonsterCurrentHealth / monsterMaxHealth
    monster_health_bar = "#" * max(int(monster_health_percentage * 10), 1 if MonsterCurrentHealth > 0 else 0)
    if player_health_percentage >= 0.75:
        color_code = Fore.GREEN  # Green
    elif player_health_percentage >= 0.3:
        color_code = Fore.YELLOW  # Yellow
    else:
        color_code = Fore.RED  # Red
    slow_type(f"{player.name}: {color_code}[{player_health_bar:<10}]{Fore.RESET} {player.health}/{player.max_health}", new_line=False)

    if monster_health_percentage >= 0.75:
        color_code = Fore.GREEN  # Green
    elif monster_health_percentage >= 0.3:
        color_code = Fore.YELLOW  # Yellow
    else:
        color_code = Fore.RED  # Red
    if MonsterCurrentHealth < 0:
        MonsterCurrentHealth = 0
    slow_type(f" - {monster['name']}: {color_code}[{monster_health_bar:<10}]{Fore.RESET} {MonsterCurrentHealth}/{monsterMaxHealth}")

def wait_for_input(text="Press any key to continue..."):
    # Wait for any key press
    slow_type(text, center=True, new_line=False, styles=["bold"])
    keyboard.read_key(suppress=True)
    print("")

def scroll_text(text, delay, center_text=False, rise_from_bottom=False):
    lines = text.split('\n')
    height = len(lines)
    
    # Get terminal size
    term_width, term_height = get_terminal_size()
    
    for i in range(height):
        # Clear the screen
        print("\033c", end='')
        
        # Calculate the vertical position based on the rise_from_bottom flag
        if rise_from_bottom:
            vertical_position = height - i
        else:
            vertical_position = i + 1
        
        # Set the cursor position
        if center_text:
            # Calculate the horizontal position to center the text
            line_width = len(lines[i])
            horizontal_position = max((term_width - line_width) // 2, 0)
            print(f"\033[{vertical_position};{horizontal_position}H", end='')
        else:
            print(f"\033[{vertical_position};1H", end='')
        
        # Print the lines from the current position to the end
        for j in range(i, height):
            print(lines[j])
        
        time.sleep(delay)

def get_terminal_size():
    """Get the size of the terminal window."""
    try:
        size = os.get_terminal_size()
        return size.columns, size.lines
    except OSError:
        return 80, 24  # Default size if getting terminal size fails
    
def show_game_menu(player):
    """
    Display the game menu to the player. 
    player: The Player object representing the player's character.
    """
    while True:
        # Print the menu options
        slow_type("\n=== Game Menu ===", center=True, styles=["bold"])
        slow_type("1. View Inventory", center=True)
        slow_type("2. View XP Progression", center=True)
        slow_type("3. [Other options can be added here]", center=True)
        slow_type("0. Return to Game", center=True, styles=["underline"])
        
        # Get the player's choice
        slow_type("Enter your choice: ", new_line=False, center=True)
        choice = input()
        
        # Handle the player's choice
        if choice == '1':
            # View Inventory
            if player.inventory:
                slow_type("\nInventory:")
                for item in player.inventory:
                    if 'description' in item:
                        slow_type(f"- {item['name']}: {item['description']}")
                    else:
                        slow_type(f"- {item['name']}")
            else:
                slow_type("\nYour inventory is empty.")
        
        elif choice == '2':
            # View XP Progression
            xp_percentage = player.xp / player.next_level_experience()
            xp_bar = "#" * max(int(xp_percentage * 10), 1 if player.health > 0 else 0)
            slow_type(f"\nXP Progression: {xp_bar} {player.xp}/{player.next_level_experience()}")
            slow_type(f"Current Level: {player.level}")
        
        elif choice == '0':
            # Return to Game
            slow_type("Returning to game...\n")
            break
        
        else:
            # Invalid choice
            slow_type("\nInvalid choice. Please try again.")

def player_input(prompt, valid_options, is_numeric=False, is_list=False, go_back=False, speed=0.013, styles=None, center=False, new_line=False):
    while True:
        # Display the valid options
        if is_list:
            for i, item in enumerate(valid_options, start=1):
                slow_type(f"{i}. {item}", speed=speed, center=center)
            if go_back:
                slow_type("0. Go Back", speed=speed, center=center)

        # Ask the player for input
        slow_type(prompt, new_line=False, styles=styles, center=center, speed=speed)
        response = input().lower().strip()
        if new_line:
            print()

        # Handle 'menu' command
        if response == 'menu':
            # Display menu or perform other menu-related actions here
            show_game_menu(get_my_character())
            continue

        # Check if the response is valid
        if is_numeric:
            try:
                choice = int(response)
                if choice in valid_options:
                    return choice
            except ValueError:
                pass
        elif is_list:
            if go_back and response == '0':
                return None
            elif response.isdigit() and 1 <= int(response) <= len(valid_options):
                return valid_options[int(response) - 1]
            else:
                # Check if the response matches any valid option (shortened or full)
                matching_options = [option for option in valid_options if response in str(option).lower()]
                if matching_options:
                    return matching_options[0]
        else:
            valid_responses = [option[0] if isinstance(option, tuple) else option for option in valid_options]
            # Check if the response matches any valid option (shortened or full)
            matching_responses = [valid_response for valid_response in valid_responses if response in valid_response.lower()]
            if matching_responses:
                return matching_responses[0]

        # If input is invalid, ask again
        slow_type("Invalid input, please try again.\n", styles=["bold", "red"], center=center)


def seperator(first_line=True, last_line=True):
    # Get terminal size
    term_width, term_height = get_terminal_size()

    if first_line and last_line:
        seperator = ("\n") + ('-' * term_width) + ('\n') # Text separator
    elif first_line == True and last_line == False:
        seperator = ("\n") + ('-' * term_width)
    elif last_line == True and first_line == False:
        seperator = ('-' * term_width) + ('\n')
    slow_type(seperator, speed=0.001, styles=["bold"])

def move_cursor_up(lines=1):
    # Get the current line number
    current_line = inspect.currentframe().f_back.f_lineno - 1

    # Calculate the new line number
    new_line = max(current_line - lines, 0)

    # Move the cursor to the new line
    for i in range(current_line - new_line):
        print("\033[F", end="")
    print("\033[E", end="")

# slow_type("Google", link = "https://google.com")  # Link style
# slow_type("Bold text", styles=["bold"])  # Bold style
# slow_type("Google Link but Bold", styles=["bold"], link="https://google.com") 
# slow_type("Italic text", styles=["italic"])  # Italic style
# slow_type("Italic text", styles=["italic", "bold"])  # Italic style
# slow_type("Reversed text", styles=["reverse"])  # Reverse style
# slow_type("Reversed text", styles=["reverse", "bold", "italic"])  # Reverse style
# slow_type("Underlined text", styles=["underline"])  # Underline style
# slow_type("Blinking text", styles=["blink"])  # Blink style
# slow_type("Black text", styles=["black"])  # Black style
# slow_type("Red text", styles=["red"])  # Red style
# slow_type("Green text", styles=["green"])  # Green style
# slow_type("Yellow text", styles=["yellow"])  # Yellow style
# slow_type("Blue text", styles=["blue"])  # Blue style
# slow_type("Magenta text", styles=["magenta"])  # Magenta style
# slow_type("Cyan text", styles=["cyan"])  # Cyan style
# slow_type("White text", styles=["white"])  # White style
# slow_type("Black background", styles=["back_black"])  # Black background style
# slow_type("Red background", styles=["back_red"])  # Red background style
# slow_type("Green background", styles=["back_green"])  # Green background style
# slow_type("Yellow background", styles=["back_yellow"])  # Yellow background style
# slow_type("Blue background", styles=["back_blue"])  # Blue background style
# slow_type("Magenta background", styles=["back_magenta"])  # Magenta background style
# slow_type("Cyan background", styles=["back_cyan"])  # Cyan background style
# slow_type("White background", styles=["back_white"])  # White background style
# slow_type("Danger, Will Robinson!", styles=["bold", "red", "underline", "blink", "back_white"])

# monster = {
#     'name': 'Dragon',
#     'attack_roll': 20
# }
# player = {
#     'ac': 15
# }

# slow_type(f"The {monster['name']} rolled a {Fore.RED}{monster['attack_roll']}{Style.RESET_ALL} against your armor class of {Fore.BLUE}{player['ac']}{Style.RESET_ALL}!")