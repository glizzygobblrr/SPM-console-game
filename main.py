import random


class CityBuildingGame:
    def __init__(self):
        self.main_menu()

    def main_menu(self):
        while True:
            print("\nMain Menu:")
            print("1. Start New Arcade Game")
            print("2. Start New Free Play Game")
            print("3. Load Saved Game")
            print("4. Display High Scores")
            print("5. Exit Game")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.start_arcade_game()
            elif choice == "2":
                self.start_free_play_game()
            elif choice == "3":
                self.load_saved_game()
            elif choice == "4":
                self.display_high_scores()
            elif choice == "5":
                print("Exiting game. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 5.")

    def start_arcade_game(self):
        # Initialize game state for Arcade mode
        board_size = 20
        initial_coins = 16
        current_coins = initial_coins
        current_score = 0
        turn = 1
        board = [[' '] * board_size for _ in range(board_size)]

        print("\nStarting new Arcade game.")
        print("You have", initial_coins, "coins to build your city.")

        while current_coins > 0:
            print("\nTurn:", turn)
            print("Coins left:", current_coins)
            print("Current score:", current_score)
            print("Current map:")
            self.display_board(board)

            print("\nOptions:")
            print("1. Build a Building")
            print("2. Demolish a Building")
            print("3. Save Game")
            print("4. Exit to Main Menu")
            choice = input("Enter your choice: ")

            if choice == "1":
                if turn == 1:
                    self.build_first_building(board, current_coins)
                else:
                    self.build_building(board, current_coins)
            elif choice == "2":
                self.demolish_building(board, current_coins)
            elif choice == "3":
                self.save_game(board, current_coins, current_score, turn)
            elif choice == "4":
                print("Exiting Arcade game.")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 4.")
                continue

            turn += 1

        # Calculate final score and display
        final_score = self.calculate_final_score(board)
        print("\nFinal score:", final_score)
        self.update_high_scores(final_score)

    def build_first_building(self, board, current_coins):
        # Allow the player to build any building anywhere on the board in the first turn
        print("\nAvailable buildings: R (Residential), I (Industry), C (Commercial), O (Park), * (Road)")
        building_type = input("Choose a building to construct: ").upper()
        if building_type not in ['R', 'I', 'C', 'O', '*']:
            print("Invalid building type. Please choose from R, I, C, O, *.")
            return

        row = int(input("Enter row (1-20): ")) - 1
        col = int(input("Enter column (1-20): ")) - 1

        if board[row][col] != ' ':
            print("Cannot build on an occupied space.")
            return

        board[row][col] = building_type
        current_coins -= 1

    def build_building(self, board, current_coins):
        # Allow the player to build a building adjacent to an existing building
        print("\nAvailable buildings: R (Residential), I (Industry), C (Commercial), O (Park), * (Road)")
        building_type = input("Choose a building to construct: ").upper()
        if building_type not in ['R', 'I', 'C', 'O', '*']:
            print("Invalid building type. Please choose from R, I, C, O, *.")
            return

        print("Select a location adjacent to an existing building:")
        self.display_board(board)
        while True:
            row = int(input("Enter row (1-20): ")) - 1
            col = int(input("Enter column (1-20): ")) - 1

            if self.is_adjacent_to_building(board, row, col):
                if board[row][col] == ' ':
                    board[row][col] = building_type
                    current_coins -= 1
                    break
                else:
                    print("Cannot build on an occupied space.")
            else:
                print("Selected location is not adjacent to an existing building.")

    def is_adjacent_to_building(self, board, row, col):
        # Check if the given row, col is adjacent to an existing building
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < len(board) and 0 <= nc < len(board[0]) and board[nr][nc] != ' ':
                return True
        return False

    def demolish_building(self, board, current_coins):
        # Allow the player to demolish a building for 1 coin
        print("\nSelect a building to demolish:")
        self.display_board(board)

        while True:
            row = int(input("Enter row (1-20): ")) - 1
            col = int(input("Enter column (1-20): ")) - 1

            if board[row][col] != ' ':
                board[row][col] = ' '
                current_coins -= 1
                break
            else:
                print("No building at this location.")

    def save_game(self, board, current_coins, current_score, turn):
        # Placeholder for saving the game state to a file
        filename = input("Enter file name to save game: ")
        with open(filename, 'w') as f:
            f.write(f"{current_coins}\n")
            f.write(f"{current_score}\n")
            f.write(f"{turn}\n")
            for row in board:
                f.write(" ".join(row) + "\n")
        print("\nGame saved.")

    def load_saved_game(self):
        # Placeholder for loading a saved game state from a file
        filename = input("Enter file name to load game: ")
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
                current_coins = int(lines[0].strip())
                current_score = int(lines[1].strip())
                turn = int(lines[2].strip())
                board = [line.strip().split() for line in lines[3:]]
            print("\nGame loaded successfully.")
            return board, current_coins, current_score, turn
        except FileNotFoundError:
            print("\nFile not found. Could not load game.")
            return None, None, None, None

    def display_high_scores(self):
        # Placeholder for displaying the top 10 high scores
        print("\nHigh Scores:")
        print("No high scores to display yet.")

    def display_board(self, board):
        board_size = len(board)

        # Print column indices
        print("    ", end="")
        for col in range(1, board_size + 1):
            print(f"{col:3}", end="")
        print()

        # Print top border
        print("   +" + "---+" * board_size)

        # Print board rows
        for row in range(board_size):
            # Print row number
            print(f"{row + 1:2} |", end="")

            # Print board contents
            for col in range(board_size):
                print(f" {board[row][col]} |", end="")

            print()  # End of row

            # Print horizontal border
            print("   +" + "---+" * board_size)

    def calculate_final_score(self, board):
        # Placeholder for calculating the final score based on the board state
        return 0

    def update_high_scores(self, final_score):
        # Placeholder for updating the high scores list
        print("Updating high scores with final score:", final_score)

    def start_free_play_game(self):
        # Placeholder for implementing Free Play mode
        print("\nFree Play mode not implemented yet.")


# Start the game
if __name__ == "__main__":
    game = CityBuildingGame()
