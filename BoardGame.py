# dice_game.py

import random
import json
import os

SAVE_FILE = "game_state.json"
MAX_TILE = 24

def roll_dice():
    return random.randint(1, 6)

def save_game(players, current_player_index):
    try:
        with open(SAVE_FILE, 'w') as f:
            json.dump({
                "players": players,
                "current_player_index": current_player_index
            }, f)
        print("✅ Game saved successfully.\n")
    except Exception as e:
        print(f"❌ Error saving game: {e}")

def load_game():
    if os.path.exists(SAVE_FILE):
        try:
            with open(SAVE_FILE, 'r') as f:
                data = json.load(f)
                return data["players"], data["current_player_index"]
        except Exception as e:
            print(f"❌ Error loading saved game: {e}")
    return None, 0

def initialize_players(num_players):
    return [{"name": f"Player {i+1}", "position": 0} for i in range(num_players)]

def display_positions(players):
    print("\n🎯 Current Positions:")
    for player in players:
        print(f"   {player['name']}: Tile {player['position']}")
    print()

def play_turn(player):
    input(f"🎲 {player['name']}, press Enter to roll the dice...")
    roll = roll_dice()
    print(f"   You rolled a {roll}!")

    current_pos = player["position"]
    if current_pos + roll > MAX_TILE:
        print(f"   ❌ You can't move past tile {MAX_TILE}. Staying at tile {current_pos}.\n")
    else:
        player["position"] += roll
        print(f"   ✅ Moved to tile {player['position']}.\n")

    if player["position"] == MAX_TILE:
        print(f"🎉 {player['name']} wins the game by reaching tile {MAX_TILE}!\n")
        return True
    return False

def main():
    print("🎮 Welcome to the Dice Game!")

    load_choice = input("Do you want to load a saved game? (y/n): ").strip().lower()
    if load_choice == 'y':
        players, current_player_index = load_game()
        if not players:
            print("⚠️ No saved game found. Starting a new game.")
            players = None
    else:
        players = None

    if not players:
        while True:
            try:
                num_players = int(input("Enter number of players (1–3): "))
                if 1 <= num_players <= 3:
                    break
                else:
                    print("Please enter a number between 1 and 3.")
            except ValueError:
                print("Invalid input. Enter a number.")

        players = initialize_players(num_players)
        current_player_index = 0

    game_over = False

    while not game_over:
        display_positions(players)

        current_player = players[current_player_index]
        game_over = play_turn(current_player)

        if game_over:
            if os.path.exists(SAVE_FILE):
                os.remove(SAVE_FILE)
            break

        current_player_index = (current_player_index + 1) % len(players)

        # Ask if user wants to save and quit
        next_action = input("Press Enter to continue or type 's' to save and exit: ").strip().lower()
        if next_action == 's':
            save_game(players, current_player_index)
            print("Game saved. See you next time!")
            break

if __name__ == "__main__":
    main()


   