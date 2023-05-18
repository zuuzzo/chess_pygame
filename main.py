import pygame

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

# Function to convert screen coordinates to chessboard coordinates
def get_chessboard_pos(mouse_pos):
    col = mouse_pos[0] // SQUARE_SIZE
    row = mouse_pos[1] // SQUARE_SIZE
    return row, col

# Function to handle piece movement
def move_piece(from_pos, to_pos):
    global chessboard
    chessboard[to_pos[0]][to_pos[1]] = chessboard[from_pos[0]][from_pos[1]]
    chessboard[from_pos[0]][from_pos[1]] = None

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

            if selected_piece is None:
                # Select a piece
                if chessboard[row][col] is not None:
                    selected_piece = chessboard[row][col]
                    selected_piece_pos = (row, col)
            else:
                # Move the selected piece
                move_piece(selected_piece_pos, (row, col))
                selected_piece = None
                selected_piece_pos = None

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