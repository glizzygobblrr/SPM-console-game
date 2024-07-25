import ast;
class CityBuildingGame:
    def __init__(self):
        self.main_menu()

    # to implement load and save game (start from where the grid left of: grid,column filled,current score of user, and number of coins)
    def main_menu(self):
        userScores = [];
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
                self.gameMode = "arcade"
                self.start_arcade_game(userScores)
            elif choice == "2":
                self.gameMode = "freeplay"
                self.start_free_play_game(userScores)
            elif choice == "3":
                self.load_saved_game()
            elif choice == "4":
                self.display_high_scores(userScores);
            elif choice == "5":
                print("Exiting game. Goodbye!")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 5.")

    def start_arcade_game(self,userScores):
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
            print("\nCurrent turn:", self.turn)
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
                self.save_game();
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
        # Push the final scores to userScores
        userScores.append(final_score);

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

    def start_free_play_game(self,userScores):
        self.board_size = 5  # Initial size of the city grid
        self.current_coins = 0  # Unlimited coins in Free Play mode
        self.current_score = 0
        self.current_profit = 0
        self.current_upkeep = 0
        self.turn = 1
        self.board = [[' '] * self.board_size for _ in range(self.board_size)]

        print("\nStarting new Free Play game.")
        print("You have unlimited coins to build your city.")

        while self.current_profit >= -20:  # End game if the city is making a loss for 20 turns
            print("\nCurrent turn:", self.turn)
            print("Current score:", self.current_score)
            print("Current profit:", self.current_profit)
            print("Current upkeep:", self.current_upkeep)
            print("Current map:")
            self.display_board(self.board)

            print("\nOptions:")
            print("1. Build a Building")
            print("2. Demolish a Building")
            print("3. Save Game")
            print("4. Exit to Main Menu")
            choice = input("Enter your choice: ")

            if choice == "1":
                self.build_building_free_play()
                self.update_score_and_coins_free_play()
            elif choice == "2":
                self.demolish_building()
                self.update_score_and_coins_free_play()
            elif choice == "3":
                self.save_game()
            elif choice == "4":
                print("Exiting Free Play game.")
                break
            else:
                print("Invalid choice. Please enter a number from 1 to 4.")
                continue

            self.turn += 1

        # Calculate final score and display
        final_score = self.calculate_final_score()
        
        print("\nFinal score:", final_score)
        self.update_high_scores(final_score)
        userScores.append(final_score);
        

    def build_building_free_play(self):
        print("\nAvailable buildings: R (Residential), I (Industry), C (Commercial), O (Park), * (Road)")
        building_type = input("Choose a building to construct: ").upper()
        if building_type not in ['R', 'I', 'C', 'O', '*']:
            print("Invalid building type. Please choose from R, I, C, O, *.")
            return

        row = int(input(f"Enter row (1-{self.board_size}): ")) - 1
        col = int(input(f"Enter column (1-{self.board_size}): ")) - 1

        if not self.is_valid_location(row, col):
            print("Invalid location. Building must be placed on an empty cell or border.")
            return

        # Expand city grid if building is placed on the border
        if self.is_on_border(row, col):
            self.expand_city_grid()

        self.board[row][col] = building_type
        self.current_coins -= 1

    def is_valid_location(self, row, col):
        if 0 <= row < self.board_size and 0 <= col < self.board_size:
            return self.board[row][col] == ' '
        return False

    def is_on_border(self, row, col):
        return row == 0 or col == 0 or row == self.board_size - 1 or col == self.board_size - 1

    def expand_city_grid(self):
        new_board_size = self.board_size + 5  # Expand by 5 rows and columns on each side
        new_board = [[' '] * new_board_size for _ in range(new_board_size)]

        # Copy existing board to new expanded board
        for r in range(self.board_size):
            for c in range(self.board_size):
                new_board[r + 5][c + 5] = self.board[r][c]

        self.board = new_board
        self.board_size = new_board_size

    def update_score_and_coins_free_play(self):
        self.current_score = self.calculate_final_score()
        self.generate_coins_free_play()

    def generate_coins_free_play(self):
        coins = 0
        upkeep_cost = 0

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

        self.current_profit = coins - upkeep_cost
        self.current_coins += self.current_profit


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

    def resume_aracade_mode(self,userScores):
        # Initialize game state for Arcade mode
        self.board_size = 20;
        board = self.board;
        current_coins = int(self.current_coins);
        current_score = int(self.current_score);
        turn = int(self.turn);

        print("\nResuming arcade mode")
        print("")

        while current_coins > 0:
            print("\nCurrent turn:", turn)
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
                if self.turn == 1:
                    self.build_first_building()
                else:
                    self.build_building()
                self.update_score_and_coins()
            elif choice == "2":
                self.demolish_building()
                self.update_score_and_coins()
            elif choice == "3":
                self.save_game();
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
        # Push the final scores to userScores
        userScores.append(final_score);

    def save_game(self):
        gameMode = self.gameMode
        board = self.board;
        current_coins = self.current_coins;
        current_score = self.current_score;
        current_turn = self.turn;
        print(current_turn)
        filename = input("Enter the file name: ")
        def write_board(board):
            result = "["
            for rows in board:
                row = "[" + ",".join(map(str, rows)) + "]"
                result += row + ","  # Add a comma after each row
            result = result.rstrip(', ') + ']'  # Remove the trailing comma and space, and close with a square bracket
            return result

        arrayString = write_board(board)
        try:
            with open(filename, 'w') as file:  # Use a with statement to ensure the file is properly closed
                file.write(f"{gameMode}\n{current_turn}\n{current_coins}\n{current_score}\n{arrayString}")
        except FileNotFoundError:
            print("\nFile not found. Could not load game.")
            return None


    def load_saved_game(self):
        # Load a saved game state from a file
        data = []
        filename = input("Enter file name to load game: ")
        try:
            with open(filename, 'r') as file:
                # Read all lines from the file
                lines = file.readlines()

                # Process each line
                for line in lines:
                    linedata = line.strip().split('\n')
                    data.append(linedata)

        except FileNotFoundError:
            print("\nFile not found. Could not load game.")
            return None
        
        if data != None:
            try:
                self.gameMode = data[0][0]
                self.turn = data[1][0];
                self.current_coins = data[2][0];
                self.current_score = data[3][0];
                boardString = data[4][0]
                def stringToArray(boardString):

                    input_string = boardString.strip("'");
                    # Split the string into rows
                    rows = input_string.split("],");
                    # End array (Outer list)
                    result = []
                    # intiailize a new array for each subarray in the board
                    for row in rows:
                        # Remove any remaining brackets if have
                        row = row.strip("[]")
                        
                        # Split the row into elements (retirve all the indexed elements in the row)
                        elements = row.split(",")
                        
                        # Process each element
                        processed_row = []
                        for element in elements:
                            processed_row.append(element)
                        
                        result.append(processed_row)
                        # append each row array to the outerList
    
                    return result
                self.board = stringToArray(boardString)
                if self.gameMode == 'arcade':
                    # Run the resume arcade mode
                    userScores = []
                    self.resume_aracade_mode(userScores);
                    print("Resuming Arcade Mode")
                elif self.gameMode == 'freeplay':
                    userScores = []
                    # Run the resume freeplay mode
                    print("Resuming Freeplay Mode");
                else:
                    # Handle the case where gameMode is neither 'arcade' nor 'freeplay'
                    print("Unknown game mode")

            except IndexError:
                print("Index defined is out of range")
        else:
            print("Data is null Goodbye")

        
       
        
        
        


    def display_high_scores(self,userScore):
        if len(userScore) != 0:
            highScore = max(userScore);
            print(f"User's Highest Score is: {highScore}");
        else:
            print("User has not started playing please select a game mode");
        

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

        net_coins = coins - upkeep_cost
        if self.current_coins + net_coins < 0:
            print("\nNot enough coins to cover upkeep costs. Game Over.")
            self.current_coins = 0
        else:
            self.current_coins += net_coins

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
        print("Updating high scores with final score:", final_score)  # may be static as not fully implemented

# Start the game
if __name__ == "__main__":
    game = CityBuildingGame()
