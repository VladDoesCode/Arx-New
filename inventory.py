# inventory.py
from utils import slow_type
from colorama import init, Fore, Back, Style

def use_item(player, item_index):
    """Use the selected item from the player's inventory."""
    item = player.inventory[item_index]

    # Handle the specific logic for the item
    if 'Healing Potion' in item['name']:
        player.health += int(item['healing_amount'])
        if player.health > player.max_health:
            player.health = player.max_health
        slow_type(f"You used a {Fore.YELLOW}{item['name']}{Fore.RESET} and restored {Fore.GREEN}{Style.BRIGHT}{item['healing_amount']}{Style.RESET_ALL} health points!")
        # Remove the used item from the player's inventory
        player.inventory.pop(item_index)
