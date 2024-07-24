import random

class CityBuildingGame:
    def __init__(self):
        self.main_menu()

    def main_menu(self):
        while True:
            print("\nWelcome to Ngee Ann City!")
            print("Main Menu:")
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
        self.board_size = 20
        self.initial_coins = 16
        self.current_coins = self.initial_coins
        self.current_score = 0
        self.turn = 1
        self.board = [[' '] * self.board_size for _ in range(self.board_size)]

        print("\nStarting new Arcade game.")
        print("You have", self.initial_coins, "coins to build your city.")

        while self.current_coins > 0:
            print("\nTurn:", self.turn)
            print("Coins left:", self.current_coins)
            print("Current score:", self.current_score)
            print("Current map:")
            self.display_board(self.board)

            print("\nOptions:")
            print("1. Build a Building")
            print("2. Demolish a Building")
            print("3. Save Game")
            print("4. Exit to Main Menu")
            choice = input("Enter your choice: ")

            if choice == "1":
                if self.turn == 1:
                    self.build_first_building()
                else:
                    self.build_building()
                self.update_score_and_coins()
            elif choice == "2":
                self.demolish_building()
                self.update_score_and_coins()
            elif choice == "3":
                self.save_game()
            elif choice == "4":
                print("Exiting Arcade game.")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 4.")
                continue

            self.turn += 1

        # Calculate final score and display
        final_score = self.calculate_final_score()
        print("\nFinal score:", final_score)
        self.update_high_scores(final_score)

    def build_first_building(self):
        # Allow the player to build any building anywhere on the board in the first turn
        print("\nAvailable buildings: R (Residential), I (Industry), C (Commercial), O (Park), * (Road)")
        building_type = input("Choose a building to construct: ").upper()
        if building_type not in ['R', 'I', 'C', 'O', '*']:
            print("Invalid building type. Please choose from R, I, C, O, *.")
            return

        row = int(input("Enter row (1-20): ")) - 1
        col = int(input("Enter column (1-20): ")) - 1

        if self.board[row][col] != ' ':
            print("Cannot build on an occupied space.")
            return

        self.board[row][col] = building_type
        self.current_coins -= 1

    def build_building(self):
        # Allow the player to build a building adjacent to an existing building
        print("\nAvailable buildings: R (Residential), I (Industry), C (Commercial), O (Park), * (Road)")
        building_type = input("Choose a building to construct: ").upper()
        if building_type not in ['R', 'I', 'C', 'O', '*']:
            print("Invalid building type. Please choose from R, I, C, O, *.")
            return

        print("Select a location adjacent to an existing building:")
        self.display_board(self.board)
        while True:
            row = int(input("Enter row (1-20): ")) - 1
            col = int(input("Enter column (1-20): ")) - 1

            if self.is_adjacent_to_building(row, col):
                if self.board[row][col] == ' ':
                    self.board[row][col] = building_type
                    self.current_coins -= 1
                    break
                else:
                    print("Cannot build on an occupied space.")
            else:
                print("Selected location is not adjacent to an existing building.")

    def is_adjacent_to_building(self, row, col):
        # Check if the given row, col is adjacent to an existing building
        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for dr, dc in directions:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.board_size and 0 <= nc < self.board_size and self.board[nr][nc] != ' ':
                return True
        return False

    def demolish_building(self):
        # Allow the player to demolish a building for 1 coin
        print("\nSelect a building to demolish:")
        self.display_board(self.board)

        while True:
            row = int(input("Enter row (1-20): ")) - 1
            col = int(input("Enter column (1-20): ")) - 1

            if self.board[row][col] != ' ':
                self.board[row][col] = ' '
                self.current_coins += 1
                break
            else:
                print("No building at this location.")

    def save_game(self):
        # Save the game state to a file
        filename = input("Enter file name to save game: ")
        with open(filename, 'w') as f:
            f.write(f"{self.current_coins}\n")
            f.write(f"{self.current_score}\n")
            f.write(f"{self.turn}\n")
            for row in self.board:
                f.write(" ".join(row) + "\n")
        print("\nGame saved.")

    def load_saved_game(self):
        # Load a saved game state from a file
        filename = input("Enter file name to load game: ")
        try:
            with open(filename, 'r') as f:
                lines = f.readlines()
                self.current_coins = int(lines[0].strip())
                self.current_score = int(lines[1].strip())
                self.turn = int(lines[2].strip())
                self.board = [line.strip().split() for line in lines[3:]]
            print("\nGame loaded successfully.")
            return self.board, self.current_coins, self.current_score, self.turn
        except FileNotFoundError:
            print("\nFile not found. Could not load game.")
            return None, None, None, None

    def display_high_scores(self):
        # Display the top 10 high scores
        print("\nHigh Scores:")
        print("No high scores to display yet.")

    def display_board(self, board):
        board_size = len(board)

        # Print column indices
        print("    ", end="")
        for col in range(1, board_size + 1):
            print(f"{col:^3}", end=" ")
        print()

        # Print top border
        print("   +" + "---+" * board_size)

        # Print board rows
        for row in range(board_size):
            # Print row number
            print(f"{row + 1:2d} |", end="")

            # Print board contents
            for col in range(board_size):
                print(f" {board[row][col]} |", end="")

            print()  # End of row

            # Print horizontal border
            print("   +" + "---+" * board_size)

    def calculate_final_score(self):
        score = 0
        for row in range(self.board_size):
            for col in range(self.board_size):
                building_type = self.board[row][col]
                if building_type == 'R':
                    score += self.calculate_residential_score(row, col)
                elif building_type == 'I':
                    score += self.calculate_industry_score(row, col)
                elif building_type == 'C':
                    score += self.calculate_commercial_score(row, col)
                elif building_type == 'O':
                    score += self.calculate_park_score(row, col)
        score += self.calculate_road_score()  # Calculate road score separately
        return score

    def calculate_residential_score(self, row, col):
        score = 0
        adjacent_buildings = {'R': 0, 'C': 0, 'O': 0, 'I': 0}
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.board_size and 0 <= nc < self.board_size:
                adjacent_building = self.board[nr][nc]
                if adjacent_building in adjacent_buildings:
                    adjacent_buildings[adjacent_building] += 1

        # If adjacent to any industry, score 1 point only
        if adjacent_buildings['I'] > 0:
            score += 1
        else:
            # Score 1 point for each adjacent residential or commercial
            score += adjacent_buildings['R'] + adjacent_buildings['C']
            # Score 2 points for each adjacent park
            score += 2 * adjacent_buildings['O']

        return score

    def calculate_industry_score(self, row, col):
        return 1

    def calculate_commercial_score(self, row, col):
        score = 0
        adjacent_commercials = 0
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.board_size and 0 <= nc < self.board_size:
                if self.board[nr][nc] == 'C':
                    adjacent_commercials += 1
        score += adjacent_commercials
        return score

    def calculate_park_score(self, row, col):
        score = 0
        adjacent_parks = 0
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.board_size and 0 <= nc < self.board_size:
                if self.board[nr][nc] == 'O':
                    adjacent_parks += 1
        score += adjacent_parks
        return score

    def calculate_road_score(self):
        score = 0
        visited = [[False] * self.board_size for _ in range(self.board_size)]

        def dfs(row, col):
            stack = [(row, col)]
            count = 0
            while stack:
                r, c = stack.pop()
                if visited[r][c]:
                    continue
                visited[r][c] = True
                count += 1

                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.board_size and 0 <= nc < self.board_size and \
                            not visited[nr][nc] and self.board[nr][nc] == '*':
                        stack.append((nr, nc))
            return count

        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == '*' and not visited[row][col]:
                    road_length = dfs(row, col)
                    if road_length > 1:
                        score += road_length

        return score

    def update_score_and_coins(self):
        self.current_score = self.calculate_final_score()
        self.generate_coins()
        # Update coin generation
        for row in range(self.board_size):
            for col in range(self.board_size):
                building_type = self.board[row][col]
                if building_type == 'I':
                    self.current_coins += sum(
                        1 for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                        if 0 <= row + dr < self.board_size and 0 <= col + dc < self.board_size
                        and self.board[row + dr][col + dc] == 'R'
                    )
                elif building_type == 'C':
                    self.current_coins += sum(
                        1 for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]
                        if 0 <= row + dr < self.board_size and 0 <= col + dc < self.board_size
                        and self.board[row + dr][col + dc] == 'R'
                    )

    def generate_coins(self):
        coins = 0
        upkeep_cost = 0
        residential_clusters = self.find_residential_clusters()

        for row in range(self.board_size):
            for col in range(self.board_size):
                building = self.board[row][col]
                if building == 'R':
                    coins += 1
                elif building == 'I':
                    coins += 2
                    upkeep_cost += 1
                elif building == 'C':
                    coins += 3
                    upkeep_cost += 2
                elif building == 'O':
                    upkeep_cost += 1
                elif building == '*':
                    if not self.is_connected_road(row, col):
                        upkeep_cost += 1

            # Upkeep cost for residential clusters
            for cluster in residential_clusters:
                if len(cluster) > 1:  # Only clusters (more than 1 connected) require upkeep
                    upkeep_cost += 1

        self.current_coins += coins - upkeep_cost

    def find_residential_clusters(self):
        visited = [[False] * self.board_size for _ in range(self.board_size)]
        clusters = []

        def dfs(row, col):
            stack = [(row, col)]
            cluster = []

            while stack:
                r, c = stack.pop()
                if visited[r][c]:
                    continue
                visited[r][c] = True
                cluster.append((r, c))

                for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.board_size and 0 <= nc < self.board_size and not visited[nr][nc] and \
                            self.board[nr][nc] == 'R':
                        stack.append((nr, nc))

            return cluster

        for row in range(self.board_size):
            for col in range(self.board_size):
                if self.board[row][col] == 'R' and not visited[row][col]:
                    clusters.append(dfs(row, col))

        return clusters

    def is_connected_road(self, row, col):
        for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            nr, nc = row + dr, col + dc
            if 0 <= nr < self.board_size and 0 <= nc < self.board_size and self.board[nr][nc] == '*':
                return True
        return False

    def update_high_scores(self, final_score):
        # Placeholder for updating the high scores list
        print("Updating high scores with final score:", final_score)

    def start_free_play_game(self):
        # Placeholder for implementing Free Play mode
        print("\nFree Play mode not implemented yet.")

# Start the game
if __name__ == "__main__":
    game = CityBuildingGame()


