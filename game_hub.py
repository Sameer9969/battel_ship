import random
import os

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header(title):
    clear_screen()
    print("=" * 60)
    print(f"    {title.center(50)}")
    print("=" * 60)
    print()

# ==================== BATTLESHIP ====================
BOARD_SIZE = 5
SHIPS = [3, 2]

def create_board():
    return [['.' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

def print_board(board, hide_ships=False, title=""):
    print(f"\n{title}")
    print("   " + " ".join([chr(65+i) for i in range(BOARD_SIZE)]))
    for i in range(BOARD_SIZE):
        row = [board[i][j] if not (hide_ships and board[i][j] == 'S') else '.' for j in range(BOARD_SIZE)]
        print(f"{i+1:2} {' '.join(row)}")

def place_ship(board, size, is_player=True):
    while True:
        if is_player:
            print(f"\nPlacing ship of size {size}")
            try:
                row = int(input("Enter row (1-5): ")) - 1
                col = ord(input("Enter column (A-E): ").upper()) - ord('A')
                direction = input("Direction (H/V): ").upper()
            except:
                print("Invalid input! Try again.")
                continue
        else:
            row = random.randint(0, BOARD_SIZE-1)
            col = random.randint(0, BOARD_SIZE-1)
            direction = random.choice(['H', 'V'])

        if direction == 'H':
            if col + size > BOARD_SIZE: continue
            positions = [(row, col + i) for i in range(size)]
        else:
            if row + size > BOARD_SIZE: continue
            positions = [(row + i, col) for i in range(size)]

        if all(0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE and board[r][c] == '.' for r, c in positions):
            for r, c in positions:
                board[r][c] = 'S'
            return True
        elif is_player:
            print("Invalid placement, try again.")

def get_player_ships(board):
    print("\n=== Place Your Ships ===")
    for size in SHIPS:
        place_ship(board, size, True)

def get_computer_ships(board):
    for size in SHIPS:
        place_ship(board, size, False)

def make_guess(board, row, col):
    if board[row][col] == 'S':
        board[row][col] = 'X'
        return True
    elif board[row][col] == '.':
        board[row][col] = 'O'
        return False
    return None

def is_game_over(board):
    return all(cell != 'S' for row in board for cell in row)

def player_turn(computer_board):
    while True:
        try:
            col = ord(input("\nEnter column (A-E): ").upper()) - ord('A')
            row = int(input("Enter row (1-5): ")) - 1
            if 0 <= row < BOARD_SIZE and 0 <= col < BOARD_SIZE:
                result = make_guess(computer_board, row, col)
                if result is None:
                    print("Already guessed!")
                    continue
                print("🎯 HIT!" if result else "💦 MISS!")
                return
            print("Invalid position!")
        except:
            print("Invalid input!")

def computer_turn(player_board):
    while True:
        row = random.randint(0, BOARD_SIZE-1)
        col = random.randint(0, BOARD_SIZE-1)
        if player_board[row][col] in ['.', 'S']:
            result = make_guess(player_board, row, col)
            print(f"Computer {chr(65+col)}{row+1} → {'HIT!' if result else 'MISS!'}")
            return

def play_battleship():
    print_header("BATTLESHIP")
    player_board = create_board()
    computer_board = create_board()

    print("Computer ships placing...")
    get_computer_ships(computer_board)
    get_player_ships(player_board)

    print("\n=== GAME START ===\n")

    while True:
        print_board(player_board, False, "YOUR BOARD")
        print_board(computer_board, True, "ENEMY BOARD")

        player_turn(computer_board)
        if is_game_over(computer_board):
            print("\n🎉 YOU WIN!")
            break

        computer_turn(player_board)
        if is_game_over(player_board):
            print("\n💥 COMPUTER WINS!")
            break

    print_board(player_board, False, "YOUR FINAL BOARD")
    print_board(computer_board, False, "ENEMY FINAL BOARD")

# ==================== OTHER GAMES ====================
def number_guessing_game():
    print_header("NUMBER GUESSING")
    number = random.randint(1, 100)
    attempts = 0
    print("Guess number 1 to 100")
    while True:
        try:
            guess = int(input("\nGuess: "))
            attempts += 1
            if guess < number: print("Too Low!")
            elif guess > number: print("Too High!")
            else:
                print(f"Correct in {attempts} attempts!")
                break
        except:
            print("Enter number only!")

# ==================== MAIN MENU ====================
def main_menu():
    games = {
        1: ("Number Guessing", number_guessing_game),
        2: ("Battleship", play_battleship),
        3: ("Quit", None)
    }

    while True:
        print_header("TERMINAL GAME ARENA")
        for num, (name, _) in games.items():
            print(f"{num}. {name}")
        
        try:
            choice = int(input("\nEnter choice: "))
            if choice == 3:
                print("Goodbye!")
                break
            if choice in games and games[choice][1]:
                games[choice][1]()
                input("\nPress Enter to go back to menu...")
        except:
            print("Invalid choice!")

if __name__ == "__main__":
    main_menu()