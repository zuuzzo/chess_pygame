import pygame
import sys
# Initialize Pygame
pygame.init()

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
SELECTED_COLOR = (0, 255, 0)

# Set the dimensions of the window
WINDOW_SIZE = (800, 800)
WIDTH, HEIGHT = WINDOW_SIZE

# Set the size of each square on the chessboard
SQUARE_SIZE = WIDTH // 8

# Set up the display
screen = pygame.display.set_mode(WINDOW_SIZE)
pygame.display.set_caption("Chess Game")

# Load chess piece images
pieces = {
    "bR": pygame.image.load("images/black_rook.png").convert_alpha(),
    "bN": pygame.image.load("images/black_knight.png").convert_alpha(),
    "bB": pygame.image.load("images/black_bishop.png").convert_alpha(),
    "bQ": pygame.image.load("images/black_queen.png").convert_alpha(),
    "bK": pygame.image.load("images/black_king.png").convert_alpha(),
    "bp": pygame.image.load("images/black_pawn.png").convert_alpha(),
    "wR": pygame.image.load("images/white_rook.png").convert_alpha(),
    "wN": pygame.image.load("images/white_knight.png").convert_alpha(),
    "wB": pygame.image.load("images/white_bishop.png").convert_alpha(),
    "wQ": pygame.image.load("images/white_queen.png").convert_alpha(),
    "wK": pygame.image.load("images/white_king.png").convert_alpha(),
    "wp": pygame.image.load("images/white_pawn.png").convert_alpha()
}

# Create the chessboard
chessboard = [[None] * 8 for _ in range(8)]
chessboard[0] = ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"]
chessboard[1] = ["bp"] * 8
chessboard[6] = ["wp"] * 8
chessboard[7] = ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]

# Game state variables
selected_piece = None
selected_piece_pos = None
current_turn = "w"

# Function to convert screen coordinates to chessboard coordinates
def get_chessboard_pos(mouse_pos):
    col = mouse_pos[0] // SQUARE_SIZE
    row = mouse_pos[1] // SQUARE_SIZE
    return row, col

# Function to handle piece movement
def move_piece(from_pos, to_pos):
    global chessboard, current_turn
    piece = chessboard[from_pos[0]][from_pos[1]]
    target_piece = chessboard[to_pos[0]][to_pos[1]]
    
    if is_valid_move(piece[1], from_pos, to_pos):
        # Make a temporary move and check if the current player's king is in check
        temp_board = [row[:] for row in chessboard]  # Create a copy of the chessboard
        temp_board[to_pos[0]][to_pos[1]] = piece
        temp_board[from_pos[0]][from_pos[1]] = None

        if not is_in_check(current_turn, temp_board):
            # Move the piece if it doesn't result in the king being in check
            chessboard[to_pos[0]][to_pos[1]] = piece
            chessboard[from_pos[0]][from_pos[1]] = None

            # Check for checkmate
            if is_in_check(current_turn, chessboard):
                print("Check!")

            # Check for stalemate
            if is_stalemate(current_turn):
                print("Stalemate!")

            # Switch the turn
            current_turn = "b" if current_turn == "w" else "w"

# Function to check if the king of the current player is in check
def is_in_check(player, board):
    # Find the king's position
    king_pos = None
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece is not None and piece[0] == player and piece[1] == "K":
                king_pos = (row, col)
                break
        if king_pos is not None:
            break

    # Check if any opponent piece can attack the king
    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece is not None and piece[0] != player:
                if is_valid_move(piece[1], (row, col), king_pos):
                    return True

    return False

# Function to check if the game is in a stalemate position
def is_stalemate(player):
    # Check if the player has any valid move
    for row1 in range(8):
        for col1 in range(8):
            piece = chessboard[row1][col1]
            if piece is not None and piece[0] == player:
                for row2 in range(8):
                    for col2 in range(8):
                        if is_valid_move(piece[1], (row1, col1), (row2, col2)):
                            # Make a temporary move and check if the opponent's king is in check
                            temp_board = [row[:] for row in chessboard]  # Create a copy of the chessboard
                            temp_board[row2][col2] = temp_board[row1][col1]
                            temp_board[row1][col1] = None

                            if not is_in_check("w" if player == "b" else "b", temp_board):
                                return False

    return True

# Function to check if the move is valid for a pawn
def is_valid_pawn_move(from_pos, to_pos):
    row1, col1 = from_pos
    row2, col2 = to_pos
    piece = chessboard[row1][col1]
    if piece == "wp":
        # White pawn
        if row1 - row2 == 1 and abs(col1 - col2) == 1:
            # Diagonal capture
            return chessboard[row2][col2] is not None and chessboard[row2][col2][0] == "b"
        elif row1 - row2 == 1 and col1 == col2 and chessboard[row2][col2] is None:
            # Forward move
            return chessboard[row2][col2] is None
        elif row1 == 6 and row1 - row2 == 2 and col1 == col2 and chessboard[row2][col2] is None and chessboard[row2 + 1][col2] is None:
            # Initial two-square move
            return chessboard[row2][col2] is None and chessboard[row2 + 1][col2] is None
    else:
        # Black pawn
        if row2 - row1 == 1 and abs(col2 - col1) == 1:
            # Diagonal capture
            return chessboard[row2][col2] is not None and chessboard[row2][col2][0] == "w"
        elif row2 - row1 == 1 and col1 == col2 and chessboard[row2][col2] is None:
            # Forward move
            return chessboard[row2][col2] is None
        elif row1 == 1 and row2 - row1 == 2 and col1 == col2 and chessboard[row2][col2] is None and chessboard[row2 - 1][col2] is None:
            # Initial two-square move
            return chessboard[row2][col2] is None and chessboard[row2 - 1][col2] is None
    return False

def is_valid_rook_move(from_pos, to_pos):
    if from_pos == to_pos:
        return False

    piece = chessboard[from_pos[0]][from_pos[1]]
    target_piece = chessboard[to_pos[0]][to_pos[1]]

    if from_pos[0] == to_pos[0] or from_pos[1] == to_pos[1]:
        # Check if the move is horizontal or vertical
        row_step = 1 if to_pos[0] > from_pos[0] else -1 if to_pos[0] < from_pos[0] else 0
        col_step = 1 if to_pos[1] > from_pos[1] else -1 if to_pos[1] < from_pos[1] else 0

        current_pos = (from_pos[0] + row_step, from_pos[1] + col_step)
        while current_pos != to_pos:
            if chessboard[current_pos[0]][current_pos[1]] is not None:
                return False  # Piece blocking the path
            current_pos = (current_pos[0] + row_step, current_pos[1] + col_step)

        return target_piece is None or target_piece[0] != piece[0]  # Check for capturing opponent's piece

    return False

# Function to check if the move is valid for a knight
def is_valid_knight_move(from_pos, to_pos):
    if to_pos is None:
        return False
    
    row1, col1 = from_pos
    row2, col2 = to_pos
    piece = chessboard[row1][col1]
    target_piece = chessboard[row2][col2]
    if abs(row1 - row2) == 2 and abs(col1 - col2) == 1:
        return target_piece is None or target_piece[0] != piece[0] # Check for capturing opponent's piece
    elif abs(row1 - row2) == 1 and abs(col1 - col2) == 2:
        return target_piece is None or target_piece[0] != piece[0] # Check for capturing opponent's piece
    return False

# Function to check if the move is valid for a bishop
def is_valid_bishop_move(from_pos, to_pos):
    if from_pos == to_pos:
        return False

    piece = chessboard[from_pos[0]][from_pos[1]]
    target_piece = chessboard[to_pos[0]][to_pos[1]]

    if abs(from_pos[0] - to_pos[0]) == abs(from_pos[1] - to_pos[1]):
        # Check if the move is diagonal
        row_step = 1 if to_pos[0] > from_pos[0] else -1 if to_pos[0] < from_pos[0] else 0
        col_step = 1 if to_pos[1] > from_pos[1] else -1 if to_pos[1] < from_pos[1] else 0

        current_pos = (from_pos[0] + row_step, from_pos[1] + col_step)
        while current_pos != to_pos:
            if chessboard[current_pos[0]][current_pos[1]] is not None:
                return False  # Piece blocking the path
            current_pos = (current_pos[0] + row_step, current_pos[1] + col_step)

        return target_piece is None or target_piece[0] != piece[0]  # Check for capturing opponent's piece

    return False

# Function to check if the move is valid for a queen
def is_valid_queen_move(from_pos, to_pos):
    if from_pos == to_pos:
        return False

    piece = chessboard[from_pos[0]][from_pos[1]]
    target_piece = chessboard[to_pos[0]][to_pos[1]]

    # Check if the move is diagonal or horizontal/vertical
    if abs(from_pos[0] - to_pos[0]) == abs(from_pos[1] - to_pos[1]) or \
       from_pos[0] == to_pos[0] or from_pos[1] == to_pos[1]:
        
        # Determine the row and column steps for movement
        row_step = 1 if to_pos[0] > from_pos[0] else -1 if to_pos[0] < from_pos[0] else 0
        col_step = 1 if to_pos[1] > from_pos[1] else -1 if to_pos[1] < from_pos[1] else 0

        current_pos = (from_pos[0] + row_step, from_pos[1] + col_step)
        while current_pos != to_pos:
            if chessboard[current_pos[0]][current_pos[1]] is not None:
                return False  # Piece blocking the path
            current_pos = (current_pos[0] + row_step, current_pos[1] + col_step)

        return target_piece is None or target_piece[0] != piece[0]  # Check for capturing opponent's piece

    return False

# Function to check if the move is valid for a king
def is_valid_king_move(from_pos, to_pos):
    row1, col1 = from_pos
    row2, col2 = to_pos
    piece = chessboard[row1][col1]
    target_piece = chessboard[row2][col2]
    if abs(row1 - row2) <= 1 and abs(col1 - col2) <= 1:
        return target_piece is None or target_piece[0] != piece[0] # Check for capturing opponent's piece
    return False

# Function to check if the move is valid based on the piece type
def is_valid_move(piece_type, from_pos, to_pos):
    if piece_type == "p":
        return is_valid_pawn_move(from_pos, to_pos)
    elif piece_type == "R":
        return is_valid_rook_move(from_pos, to_pos)
    elif piece_type == "N":
        return is_valid_knight_move(from_pos, to_pos)
    elif piece_type == "B":
        return is_valid_bishop_move(from_pos, to_pos)
    elif piece_type == "Q":
        return is_valid_queen_move(from_pos, to_pos)
    elif piece_type == "K":
        return is_valid_king_move(from_pos, to_pos)
    return False

def show_winner_popup(winner):
    popup_width = 400
    popup_height = 200

    popup_pos_x = (WIDTH - popup_width) // 2
    popup_pos_y = (HEIGHT - popup_height) // 2

    popup_screen = pygame.display.set_mode((popup_width, popup_height))
    pygame.display.set_caption("Game Over")

    font = pygame.font.Font(None, 36)
    text = font.render(f"{winner.capitalize()} wins!", True, WHITE)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        popup_screen.fill(BLACK)
        popup_screen.blit(text, ((popup_width - text.get_width()) // 2, (popup_height - text.get_height()) // 2))

        pygame.display.update()


# Game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            # Handle mouse click events
            mouse_pos = pygame.mouse.get_pos()
            row, col = get_chessboard_pos(mouse_pos)

            if selected_piece is None and chessboard[row][col] is not None and chessboard[row][col][0] == current_turn:
                # Select a piece
                selected_piece = chessboard[row][col]
                selected_piece_pos = (row, col)
            elif selected_piece is not None:
                # Move the selected piece
                from_pos = selected_piece_pos
                to_pos = (row, col)
                if is_valid_move(selected_piece[1], from_pos, to_pos):
                    move_piece(from_pos, to_pos)
                selected_piece = None
                selected_piece_pos = None

        if is_stalemate("b"):
            show_winner_popup("white")
            running = False
        elif is_stalemate("w"):
            show_winner_popup("black")
            running = False

    # Clear the screen
    screen.fill(BLACK)

    # Draw the chessboard
    for row in range(8):
        for col in range(8):
            square_color = WHITE if (row + col) % 2 == 0 else BLACK
            pygame.draw.rect(screen, square_color, (col * SQUARE_SIZE, row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

            # Draw the chess pieces
            piece = chessboard[row][col]
            if piece is not None:
                piece_image = pieces[piece]
                piece_image = pygame.transform.scale(piece_image, (SQUARE_SIZE, SQUARE_SIZE))
                screen.blit(piece_image, (col * SQUARE_SIZE, row * SQUARE_SIZE))

    # Highlight the selected piece
    if selected_piece is not None:
        selected_row, selected_col = selected_piece_pos
        pygame.draw.rect(screen, SELECTED_COLOR, (selected_col * SQUARE_SIZE, selected_row * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 4)

    # Update the display
    pygame.display.update()

# Quit the game
pygame.quit()
sys.exit()

#ENDED ON IF CHECK 