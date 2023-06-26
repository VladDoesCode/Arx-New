# items.py

# Healing Potions
healing_potions = [
    {
        "name": "Minor Healing Potion",
        "description": "Restores 10 health points.",
        "healing_amount": 10,
        "rarity": "common"
    },
    {
        "name": "Standard Healing Potion",
        "description": "Restores 20 health points.",
        "healing_amount": 20,
        "rarity": "common"
    },
    {
        "name": "Greater Healing Potion",
        "description": "Restores 30 health points.",
        "healing_amount": 30,
        "rarity": "uncommon"
    },
    {
        "name": "Superior Healing Potion",
        "description": "Restores 40 health points.",
        "healing_amount": 40,
        "rarity": "rare"
    }
    # Add more potions with different healing amounts and rarities
]

# Armors
armors = [
    {
        "name": "Padded Armor",
        "type": "Light armor",
        "cost": "5 gp",
        "weight": "8 lb.",
        "ac": "11 + DexMod",
        "description": "Padded armor consists of quilted layers of cloth and batting. The wearer has disadvantage on DexModterity (Stealth) checks."
    },
    {
        "name": "Leather Armor",
        "type": "Light armor",
        "cost": "10 gp",
        "weight": "10 lb.",
        "ac": "11 + DexMod",
        "description": "The breastplate and shoulder protectors of this armor are made of leather that has been stiffened by being boiled in oil. The rest of the armor is made of softer and more flexible materials."
    },
    {
        "name": "Ring Mail",
        "type": "Heavy armor",
        "cost": "30 gp",
        "weight": "40 lb.",
        "ac": "14",
        "description": "This armor is leather armor with heavy rings sewn into it. The rings help reinforce the armor against blows from swords and axes. Ring mail is inferior to chain mail, and it's usually worn only by those who can't afford better armor. The wearer has disadvantage on DexModterity (Stealth) checks."
    },
    {
        "name": "Studded Leather Armor",
        "type": "Light armor",
        "cost": "45 gp",
        "weight": "13 lb.",
        "ac": "12 + DexMod",
        "description": "Made from tough but flexible leather, studded leather is reinforced with close-set rivets or spikes."
    },
    {
        "name": "Chain Mail",
        "type": "Heavy armor",
        "cost": "75 gp",
        "weight": "55 lb.",
        "ac": "16",
        "strength_req": 13,
        "description": "Made of interlocking metal rings, chain mail includes a layer of quilted fabric worn underneath the mail to prevent chafing and to cushion the impact of blows. The suit includes gauntlets. The wearer has disadvantage on DexModterity (Stealth) checks. If the wearer has a Strength score lower than 13, they cannot use this armor."
    },
    {
        "name": "Splint Armor",
        "type": "Heavy armor",
        "cost": "200 gp",
        "weight": "60 lb.",
        "ac": "17",
        "strength_req": 15,
        "description": "This armor is made of narrow vertical strips of metal riveted to a backing of leather that is worn over cloth padding. Flexible chain mail protects the joints. The wearer has disadvantage on DexModterity (Stealth) checks. If the wearer has a Strength score lower than 15, they cannot use this armor."
    },
    {
        "name": "Plate Armor",
        "type": "Heavy armor",
        "cost": "1,500 gp",
        "weight": "65 lb.",
        "ac": "18",
        "strength_req": 15,
        "description": "Plate consists of shaped, interlocking metal plates to cover the entire body. A suit of plate includes gauntlets, heavy leather boots, a visored helmet, and thick layers of padding underneath the armor. Buckles and straps distribute the weight over the body. The wearer has disadvantage on DexModterity (Stealth) checks. If the wearer has a Strength score lower than 15, they cannot use this armor."
    }
    # Add more armors
]
