import random
import time

# Player stats
player_health = 100
player_inventory = []
pistol_ammo = 10  # Ammo for the pistol
rifle_ammo = 5    # Ammo for the rifle

# Monster stats
monsters = {
    "Mutant Rat": {"health": 30, "damage": 10},
    "Lab Zombie": {"health": 50, "damage": 15},
    "Viral Creature": {"health": 80, "damage": 20},
}

# Item stats
items = {
    "Health Potion": 30,  # Heals 30 health
    "Red Bull": 20    # Increases damage by 20 for 1 combat
}

# Weapon stats as items
weapon_items = {
    "Dissecting Knife": {"damage": 10, "ammo_required": 0, "infinite": True},
    "Pistol": {"damage": 25, "ammo_required": 1},
    "Rifle": {"damage": 50, "ammo_required": 1},
    "Chemical": {"damage": 75, "ammo_required": 0, "poison": True, "one_time": True},  # Chemical is one-time use
}

# Introduction
def intro():
    print("Welcome to the Abandoned Laboratory Escape Game!")
    print("A failed experiment has turned the lab into a dangerous place.")
    print("You need to navigate through random hallways, fight monsters, and escape.")
    print("Good luck!")

def print_status():
    print(f"\nYour health: {player_health}")
    print(f"Inventory: {player_inventory}")
    print(f"Pistol Ammo: {pistol_ammo}")
    print(f"Rifle Ammo: {rifle_ammo}")
    print("-" * 30)

# Combat function
def combat(monster_name, monster_health, monster_damage):
    global player_health, pistol_ammo, rifle_ammo
    
    print(f"\nYou encounter a {monster_name}!")
    print(f"It has {monster_health} health and deals {monster_damage} damage.")
    
    while monster_health > 0 and player_health > 0:
        print_status()
        print("Weapons available from inventory: Dissecting Knife, Pistol, Rifle, Chemical")
        weapon_choice = input(f"Choose your weapon: ").title()

        # Check if the player has the weapon in their inventory
        if weapon_choice in weapon_items and weapon_choice in player_inventory:
            weapon = weapon_items[weapon_choice]
            
            # Handle weapon logic
            if weapon_choice == "Pistol" and pistol_ammo <= 0:
                print("\nYou are out of pistol ammo!")
                continue
            elif weapon_choice == "Rifle" and rifle_ammo <= 0:
                print("\nYou are out of rifle ammo!")
                continue
            
            if weapon_choice == "Pistol":
                pistol_ammo -= weapon["ammo_required"]
                damage_dealt = random.randint(20, 30)
                monster_health -= damage_dealt
                print(f"You fire the pistol and deal {damage_dealt} damage to the {monster_name}!")
            elif weapon_choice == "Rifle":
                rifle_ammo -= weapon["ammo_required"]
                damage_dealt = random.randint(40, 60)
                monster_health -= damage_dealt
                print(f"You fire the rifle and deal {damage_dealt} damage to the {monster_name}!")
            elif weapon_choice == "Dissecting Knife":
                damage_dealt = random.randint(5, 15)
                monster_health -= damage_dealt
                print(f"You stab the {monster_name} with the dissecting knife and deal {damage_dealt} damage!")
            elif weapon_choice == "Chemical":
                poison_damage = 75  # Chemical now does 75 damage
                monster_health -= poison_damage
                print(f"You throw the chemical and deal {poison_damage} damage to the {monster_name}!")
                player_inventory.remove("Chemical")  # Remove the chemical from inventory after use
            
            # Monster counterattack
            if monster_health > 0:
                player_health -= monster_damage
                print(f"The {monster_name} attacks you for {monster_damage} damage!")
                
        else:
            print("Invalid weapon choice or you don't have that weapon in your inventory. Please choose a valid weapon.")
            continue

        if player_health <= 0:
            print("\nYou have been defeated. Game Over.")
            return False  # Player lost in combat, game over

    if monster_health <= 0:
        print(f"You defeated the {monster_name}!")
        return True  # Player won the combat

    return True  # Return True to keep the game running

# Random event chance for lab events
def random_event():
    # Define the chances (percentages) for each event
    chance_for_nothing = 40  # 40% chance for nothjing
    chance_for_item = 25     # 25% chance for an item
    chance_for_monster = 25  # 25% chance for a monster
    chance_for_exit = 10      # 10% chance for the exit

    # Generate a random number between 1 and 100
    random_number = random.randint(1, 100)

    # Determine which event occurs based on the random number and the probabilities
    if random_number <= chance_for_nothing:
        print("You find nothing in this hallway.")
        return "nothing"
    
    elif random_number <= chance_for_nothing + chance_for_item:
        print("You find an item!")
        return "item"
    
    elif random_number <= chance_for_nothing + chance_for_item + chance_for_monster:
        print("You encounter a monster!")
        return "monster"
    
    elif random_number <= chance_for_nothing + chance_for_item + chance_for_monster + chance_for_exit:
        print("You have found the exit!")
        return "exit"
    
    else:
        print("An unexpected event occurred.")
        return "unexpected"

# Hallway navigation: Choose left, right, or straight
def choose_direction():
    global player_health
    
    print("\nYou reach a junction in the hallway.")
    choice = input("Do you want to go [L]eft, [R]ight, or [S]traight? ").lower()

    if choice == "l":
        print("\nYou choose to go left...")
        return random_event()

    elif choice == "r":
        print("\nYou choose to go right...")
        return random_event()

    elif choice == "s":
        print("\nYou choose to go straight...")
        return random_event()

    else:
        print("Invalid choice. Please choose 'L', 'R', or 'S'.")
        return choose_direction()  # Recursively ask again

# Main game loop
def main():
    global player_health

    intro()

    # Add some starting items (weapons) to the player's inventory
    player_inventory.append("Dissecting Knife")
    player_inventory.append("Pistol")
    player_inventory.append("Rifle")
    player_inventory.append("Chemical")

    while player_health > 0:
        event_result = choose_direction()

        # If any event leads to the player dying or escaping, break the loop
        if event_result == "nothing":
            print("\nYou continue exploring the lab...\n")
        elif event_result == "item":
            item = random.choice(list(items.keys()))
            player_inventory.append(item)
            print(f"Item found: {item}")
        elif event_result == "monster":
            monster = random.choice(list(monsters.keys()))
            monster_health = monsters[monster]["health"]
            monster_damage = monsters[monster]["damage"]
            if not combat(monster, monster_health, monster_damage):
                break  # Player lost in combat
        elif event_result == "exit":
            print("\nCongratulations! You escaped the lab!")
            break  # Player escaped

        time.sleep(1)  # Simulate time passing

    print("\nGame Over. Thank you for playing!")

# Start the game
main()


