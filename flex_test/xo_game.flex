// XO Game (Tic-Tac-Toe) in Flex Language - English Syntax
// A complete two-player XO game with input validation and win detection

def print_board(board)
    print("Current Board:")
    print("")
    for i=0 to 2
        print(board[i][0] + " | " + board[i][1] + " | " + board[i][2])
        if i < 2
            print("---------")
        end
    end
    print("")
end

def check_winner(board, mark)
    // Check rows
    for i=0 to 2
        if board[i][0] == mark and board[i][1] == mark and board[i][2] == mark
            return true
        end
    end
    
    // Check columns
    for i=0 to 2
        if board[0][i] == mark and board[1][i] == mark and board[2][i] == mark
            return true
        end
    end
    
    // Check diagonals
    if board[0][0] == mark and board[1][1] == mark and board[2][2] == mark
        return true
    end
    if board[0][2] == mark and board[1][1] == mark and board[2][0] == mark
        return true
    end
    
    return false
end

def is_draw(board)
    for i=0 to 2
        for j=0 to 2
            if board[i][j] == " "
                return false
            end
        end
    end
    return true
end

def get_valid_input(prompt_text, min_val, max_val)
    while true
        print(prompt_text)
        input_val = input()
        
        // Convert to number and validate
        if input_val >= min_val and input_val <= max_val
            return input_val
        else
            print("Invalid input! Please enter a number between " + min_val + " and " + max_val)
        end
    end
end

def main()
    // Initialize empty board
    board = [[" ", " ", " "], [" ", " ", " "], [" ", " ", " "]]
    players = ["X", "O"]
    turn = 0
    
    print("=== Welcome to XO Game (Tic-Tac-Toe) ===")
    print("Players take turns placing X and O")
    print("Enter row and column numbers (1-3)")
    print("")
    
    while true
        print_board(board)
        current_player = players[turn % 2]
        print("Player " + current_player + "'s turn")
        
        // Get row input
        row = get_valid_input("Enter row (1-3): ", 1, 3)
        
        // Get column input  
        col = get_valid_input("Enter column (1-3): ", 1, 3)
        
        // Convert to 0-based indexing
        row = row - 1
        col = col - 1
        
        // Check if cell is already taken
        if board[row][col] != " "
            print("Cell already taken! Try again.")
            print("")
            continue
        end
        
        // Place the mark
        board[row][col] = current_player
        
        // Check for winner
        if check_winner(board, current_player)
            print_board(board)
            print("🎉 Player " + current_player + " wins! Mabrouk!")
            break
        end
        
        // Check for draw
        if is_draw(board)
            print_board(board)
            print("🤝 It's a draw! Good game!")
            break
        end
        
        // Next player's turn
        turn = turn + 1
        print("")
    end
    
    print("Thanks for playing XO!")
end

// Start the game
main()
