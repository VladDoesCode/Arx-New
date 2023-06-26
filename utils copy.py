# utils.py
import sys
import time
import keyboard
from colorama import init, Fore, Back, Style
import shutil
import os

init()  # Initialize colorama

def slow_type(text, speed=0.013, new_line=True, styles=None, link=None):
    """Print out text with a typewriter effect."""
    TextStyle = f""

    if link is not None:
        colored_text = f"{Fore.BLUE}{text}{Style.RESET_ALL}"
        text = f"\033]8;;{link}\033\\{colored_text}\033]8;;\033\\"

    if styles is not None:
        for style in styles:
            if style == "bold":
                # Add {Style.BRIGHT} to TextStyle
                TextStyle += f"{Style.BRIGHT}"

            elif style == "italic":
                # Add Italic Stylizing to TextStyle
                TextStyle += f"\x1B[3m"

            elif style == "reverse":
                # Add Reverse Stylizing to TextStyle
                TextStyle += f"\x1B[7m"

            elif style == "underline":
                # Add Underline Stylizing to TextStyle
                TextStyle += f"\x1B[4m"
            
            elif style == "blink":
                # Add Blink Stylizing to TextStyle
                TextStyle += f"\x1B[5m"
            
            elif style in ["black", "red", "green", "yellow", "blue", "magenta", "cyan", "white"]:
                # Add Color Stylizing to TextStyle
                TextStyle += f"{getattr(Fore, style.upper())}"
            
            elif style in ["back_black", "back_red", "back_green", "back_yellow", "back_blue", "back_magenta", "back_cyan", "back_white"]:
                # Add Background Color Stylizing to TextStyle
                TextStyle += f"{getattr(Back, style[5:].upper())}"

        text = f"{TextStyle}{text}{Style.RESET_ALL}"

    # Iterate through each character
    for char in text:
        # Print the character, flush to force the stdout buffer to print immediately
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(speed)

    if new_line:
        print("")


def display_healthbars(player, monster, monsterMaxHealth, MonsterCurrentHealth):
    """Display the health bars for the player and monster at the specified x, y coordinate. Put both health bars on the same line."""
    player_health_percentage = player.health / player.max_health
    player_health_bar = "#" * int(player_health_percentage * 10)
    monster_health_percentage = MonsterCurrentHealth / monsterMaxHealth
    monster_health_bar = "#" * int(monster_health_percentage * 10)
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

def wait_for_input():
    # Wait for any key press
    slow_type("Press any key to continue...", new_line=False)
    keyboard.read_key(suppress=True)
    print("")

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