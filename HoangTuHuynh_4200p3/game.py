# Import modules
import time
import random

# Define constants
BOARD_SIZE = 8
EMPTY = "-"
HUMAN = "O"
COMPUTER = "X"
WIN_LENGTH = 4
TIME_LIMIT = 5

# Define the board as a list of lists
board = [[EMPTY for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]

# Define the rows and columns as strings
rows = "ABCDEFGH"
cols = "12345678"

# Define a function to print the board
def print_board():
    # Print the column labels
    print(" ", end=" ")
    for col in cols:
        print(col, end=" ")
    print()
   
    for i in range(BOARD_SIZE):
        print(rows[i], end=" ")
        for j in range(BOARD_SIZE):
            print(board[i][j], end=" ")
        print()

# Define a function to check if the board is full
def is_full():
    # Loop through the board and return False if there is an empty space
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == EMPTY:
                return False
    
    return True

# Define a function to check if a player has won
def is_win(player):
    # Loop through the rows and check for horizontal win
    for i in range(BOARD_SIZE):
        count = 0
        for j in range(BOARD_SIZE):
            if board[i][j] == player:
                count += 1
            else:
                count = 0
            if count == WIN_LENGTH:
                return True
    # Loop through the columns and check for vertical win
    for j in range(BOARD_SIZE):
        count = 0
        for i in range(BOARD_SIZE):
            if board[i][j] == player:
                count += 1
            else:
                count = 0
            if count == WIN_LENGTH:
                return True
   
    return False

# Define a function to get the valid moves for a player
def get_moves(player):
    moves = []
    center = BOARD_SIZE // 2
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE):
            if board[i][j] == EMPTY:
                # Check for immediate win or block
                make_move(player, (i, j))
                if is_win(player):
                    priority = -100  # Highest priority for winning move
                elif is_win(HUMAN if player == COMPUTER else COMPUTER):
                    priority = -50   # Next highest for blocking opponent
                else:
                    # Prioritize center positions
                    priority = -((abs(i - center) + abs(j - center)))
                undo_move((i, j))
                moves.append(((i, j), priority))
    moves.sort(key=lambda x: x[1], reverse=True)  # Sort moves based on priority
    return [move for move, _ in moves]

# Define a function to make a move on the board
def make_move(player, move):
    # Get the row and column from the move tuple
    row, col = move
    # Update the board with the player's symbol
    board[row][col] = player

# Define a function to undo a move on the board
def undo_move(move):
    # Get the row and column from the move tuple
    row, col = move
    # Reset the board value to empty
    board[row][col] = EMPTY

# Define a function to evaluate the board for a player
def evaluate(player):
    opponent = HUMAN if player == COMPUTER else COMPUTER
    score = 0

    # Simple scoring function
    def score_line(count, opponent_count):
        if count == WIN_LENGTH - 1 and opponent_count == 0:
            return 10  # Win next move
        elif opponent_count == WIN_LENGTH - 1 and count == 0:
            return -10  # Opponent wins next move
        return 0

    # Evaluate rows and columns
    for i in range(BOARD_SIZE):
        for j in range(BOARD_SIZE - WIN_LENGTH + 1):
            # Check row
            row_count = sum(1 for k in range(WIN_LENGTH) if board[i][j + k] == player)
            row_opponent_count = sum(1 for k in range(WIN_LENGTH) if board[i][j + k] == opponent)
            score += score_line(row_count, row_opponent_count)

            # Check column
            col_count = sum(1 for k in range(WIN_LENGTH) if board[j + k][i] == player)
            col_opponent_count = sum(1 for k in range(WIN_LENGTH) if board[j + k][i] == opponent)
            score += score_line(col_count, col_opponent_count)

    return score

def iterative_deepening(player, time_limit):
    start_time = time.time()
    best_move = None
    depth = 1

    while time.time() - start_time < time_limit:
        move, _ = alpha_beta(player, -float("inf"), float("inf"), depth, start_time)
        if move is not None:
            best_move = move
        depth += 1

    return best_move
# Define a function to implement the alpha-beta pruning algorithm
def alpha_beta(player, alpha, beta, depth, start_time):
    # Check if the time limit is exceeded
    if time.time() - start_time > TIME_LIMIT:
        return None, None
    # Check if the game is over or the depth limit is reached
    if is_win(COMPUTER):
        return None, 1000
    elif is_win(HUMAN):
        return None, -1000
    elif is_full():
        return None, 0
    elif depth == 0:
        return None, evaluate(COMPUTER) - evaluate(HUMAN)
    # Initialize the best move and the best score
    best_move = None
    if player == COMPUTER:
        best_score = -float("inf")
    else:
        best_score = float("inf")
    # Loop through the possible moves
    for move in get_moves(player):
        # Make the move
        make_move(player, move)
        # Recursively call the alpha-beta function with the opposite player and the updated alpha and beta values
        if player == COMPUTER:
            next_player = HUMAN
        else:
            next_player = COMPUTER
        _, score = alpha_beta(next_player, alpha, beta, depth - 1, start_time)
        # Undo the move
        undo_move(move)
        # Check if the score is None, meaning the time limit was exceeded
        if score is None:
            return None, None
        # Update the best move and the best score
        if player == COMPUTER:
            if score > best_score:
                best_move = move
                best_score = score
            # Update the alpha value
            alpha = max(alpha, best_score)
        else:
            if score < best_score:
                best_move = move
                best_score = score
            # Update the beta value
            beta = min(beta, best_score)
        # Prune the branch if alpha is greater than or equal to beta
        if alpha >= beta:
            break
    # Return the best move and the best score
    return best_move, best_score

# Define a function to get the computer's move
def get_computer_move():
    # Get the current time
    start_time = time.time()
    # Call the alpha-beta function with the computer as the player and a large depth
    move = iterative_deepening(COMPUTER, TIME_LIMIT)
    # Check if the move is None, meaning the time limit was exceeded
    if move is None:
        # Choose a random move from the available moves
        move = random.choice(get_moves(COMPUTER))
    # Return the move
    return move

# Define a function to get the human's move
def get_human_move():
    # Loop until a valid move is entered
    while True:
        # Prompt the user to enter a move in the format of row and column, such as A1
        move = input("Enter your move: ")
        # Check if the move is valid
        if len(move) == 2 and move[0].capitalize() in rows and move[1] in cols:
            # Convert the move to a tuple of row and column indices
            row = rows.index(move[0].capitalize())
            col = cols.index(move[1])
            # Check if the board space is empty
            if board[row][col] == EMPTY:
                # Return the move
                return (row, col)
        # Otherwise, print an error message and ask the user to re-enter a valid move
        print("Invalid move. Please enter a move in the format of row and column, such as A1.")

# Define a function to play the game
def play():
    # Print a welcome message
    print("Welcome to the 4-in-a-line game!")
    print("You are O and I am X.")
    print("The board is 8x8 and the first player to get 4 in a line wins.")
    print("You can enter your move in the format of row and column, such as A1.")
    print("Here is the initial board:")
    # Print the initial board
    print_board()

    # Ask the user to choose who goes first
    turn = input("Do you want to go first? (Y/N) ")
    # Loop until the game is over
    while True:
        # Check if the board is full
        if is_full():
            # Print a draw message and break the loop
            print("The board is full. It's a draw.")
            break
        # Check if the user goes first
        if turn.upper() == "Y":
            # Get the human's move
            move = get_human_move()
            # Make the move on the board
            make_move(HUMAN, move)
            # Print the updated board
            print_board()
            # Check if the human has won
            if is_win(HUMAN):
                # Print a win message and break the loop
                print("You win! Congratulations!")
                break
            # Change the turn to the computer
            turn = "N"
        # Otherwise, the computer goes first
        else:
            # Print a message that the computer is thinking
            print("I am thinking...")
            # Get the computer's move
            move = get_computer_move()
            # Make the move on the board
            make_move(COMPUTER, move)
            # Print the updated board
            print_board()
            # Check if the computer has won
            if is_win(COMPUTER):
                # Print a win message and break the loop
                print("I win! Better luck next time.")
                break
            # Change the turn to the human
            turn = "Y"
    print("Thank you for playing the game. Have a nice day!")

if __name__ == "__main__":
    play()
    
