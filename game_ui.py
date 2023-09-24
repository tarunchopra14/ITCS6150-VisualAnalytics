import pygame
import numpy as np

pygame.init()

# BOARD CONSTANTS
LEVELS = 4
WIDTH, HEIGHT = 750, 750
GRID_SIZE = 4
PADDING = WIDTH // 16
BASE_CELL_HEIGHT = HEIGHT // GRID_SIZE // 6
TOP_WIDTH = WIDTH // 4
BOTTOM_WIDTH = 1.5 * TOP_WIDTH
LINE_WIDTH = 1
BACKGROUND = (0, 0, 0)
LINE_COLOR = (0, 255, 0)
PLAYER_X_COLOR = (255, 0, 0)
PLAYER_O_COLOR = (0, 0, 255)

top_lefts = [(WIDTH // 1.33 - TOP_WIDTH // 2, PADDING + level * (4 * BASE_CELL_HEIGHT + PADDING)) for level in range(LEVELS)]
top_rights = [(WIDTH // 1.33 + TOP_WIDTH // 2, PADDING + level * (4 * BASE_CELL_HEIGHT + PADDING)) for level in range(LEVELS)]
bottom_lefts = [(WIDTH // 1.33 - BOTTOM_WIDTH // 2, PADDING + level * (4 * BASE_CELL_HEIGHT + PADDING) + 4 * BASE_CELL_HEIGHT) for level in range(LEVELS)]
bottom_rights = [(WIDTH // 1.33 + BOTTOM_WIDTH // 2, PADDING + level * (4 * BASE_CELL_HEIGHT + PADDING) + 4 * BASE_CELL_HEIGHT) for level in range(LEVELS)]

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("3D Tic Tac Toe")

def initialize_board():
    return [[[0 for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)] for _ in range(LEVELS)]

def draw_board(board):
    for level in range(LEVELS):
        top_left = top_lefts[level]
        top_right = top_rights[level]
        bottom_left = bottom_lefts[level]
        bottom_right = bottom_rights[level]
        
        pygame.draw.polygon(screen, LINE_COLOR, [top_left, top_right, bottom_right, bottom_left], LINE_WIDTH)
        
        # Draw rows
        for y in range(1, GRID_SIZE):
            ratio = y / GRID_SIZE
            
            start = (
                top_left[0] + ratio * (bottom_left[0] - top_left[0]),
                top_left[1] + y * BASE_CELL_HEIGHT
            )
            end = (
                top_right[0] + ratio * (bottom_right[0] - top_right[0]),
                top_right[1] + y * BASE_CELL_HEIGHT
            )
            
            pygame.draw.line(screen, LINE_COLOR, start, end, LINE_WIDTH)

        # Draw columns
        for x in range(1, GRID_SIZE):
            ratio = x / GRID_SIZE
            
            left_start = (
                top_left[0] + ratio * (top_right[0] - top_left[0]),
                top_left[1]
            )
            left_end = (
                bottom_left[0] + ratio * (bottom_right[0] - bottom_left[0]),
                bottom_left[1]
            )
            
            pygame.draw.line(screen, LINE_COLOR, left_start, left_end, LINE_WIDTH)
    
    # Now draw the existing moves
    for level in range(LEVELS):
        for row in range(GRID_SIZE):
            for col in range(GRID_SIZE):
                player = board[level][row][col]
                if player != 0:
                    draw_circle_in_cell(level, row, col, player)

def get_clicked_cell(pos):
    x, y = pos

    # Determine level
    level = y // (4 * BASE_CELL_HEIGHT + PADDING)
    if level >= LEVELS:
        return None

    # Adjust y based on the level to get row
    y -= level * (4 * BASE_CELL_HEIGHT + PADDING)

    # Determine row
    row = (y - PADDING) // BASE_CELL_HEIGHT
    if row < 0 or row >= GRID_SIZE:
        return None

    # Compute x-coordinates for the clicked row using the appropriate level's top_left and top_right
    ratio = row / GRID_SIZE
    left_x = top_lefts[level][0] + ratio * (bottom_lefts[level][0] - top_lefts[level][0])
    right_x = top_rights[level][0] + ratio * (bottom_rights[level][0] - top_rights[level][0])
    cell_width = (right_x - left_x) / GRID_SIZE

    # Determine column
    col = (x - left_x) // cell_width
    if col < 0 or col >= GRID_SIZE:
        return None

    return level, int(row), int(col)


PLAYER = 1
AI = -1

def update_board(level, row, col, player):
    if board[level][row][col] == 0:  # Check if the cell is empty
        board[level][row][col] = player
        return True  # Successfully updated
    return False  # Cell is already occupied

def draw_circle_in_cell(level, row, col, player):
    # Determine center X using interpolation between the left and right x-coordinates of the clicked row
    left_x = top_lefts[level][0] + row / GRID_SIZE * (bottom_lefts[level][0] - top_lefts[level][0])
    right_x = top_rights[level][0] + row / GRID_SIZE * (bottom_rights[level][0] - top_rights[level][0])
    center_x = left_x + (right_x - left_x) / GRID_SIZE * (col + 0.5)  # col + 0.5 ensures we're in the center of the cell

    # Determine center Y (similar logic to how it's done in get_clicked_cell)
    center_y = PADDING + level * (4 * BASE_CELL_HEIGHT + PADDING) + row * BASE_CELL_HEIGHT + BASE_CELL_HEIGHT // 2

    # Determine the color based on the player
    color = PLAYER_X_COLOR if player == PLAYER else PLAYER_O_COLOR

    # Draw the filled circle
    pygame.draw.circle(screen, color, (int(center_x), int(center_y)), 10)



# Title properties
TITLE_FONT = pygame.font.SysFont("Arial", 40)
TITLE_COLOR = (255, 255, 255)  # White color
TITLE_TEXT = "3D Tic-Tac-Toe"
title_surface = TITLE_FONT.render(TITLE_TEXT, True, TITLE_COLOR)
TITLE_POSITION = (WIDTH // 4 - title_surface.get_width() // 2, PADDING)

def draw_title():
    """Draw the game title on the screen."""
    screen.blit(title_surface, TITLE_POSITION)

# Constants for buttons
BUTTON_WIDTH, BUTTON_HEIGHT = 200, 50
BUTTON_PADDING = 50
BUTTON_COLORS = {
    "default": (200, 200, 200),
    "hover": (150, 150, 150),
}
BUTTON_FONT_COLOR = (0, 0, 0)
FONT = pygame.font.SysFont("Arial", 20)


# Define the Play button
play_button = {
    "rect": pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 2 - BUTTON_HEIGHT // 2, BUTTON_WIDTH, BUTTON_HEIGHT),
    "label": "Play"
}

# Define the buttons
buttons = {
    "easy": {
        "rect": pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 4, BUTTON_WIDTH, BUTTON_HEIGHT),
        "label": "Easy",
        "difficulty": 2
    },
    "difficult": {
        "rect": pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 4 + BUTTON_HEIGHT + BUTTON_PADDING, BUTTON_WIDTH, BUTTON_HEIGHT),
        "label": "Difficult",
        "difficulty": 4
    },
    "insane": {
        "rect": pygame.Rect(WIDTH // 2 - BUTTON_WIDTH // 2, HEIGHT // 4 + 2*(BUTTON_HEIGHT + BUTTON_PADDING), BUTTON_WIDTH, BUTTON_HEIGHT),
        "label": "Insane",
        "difficulty": 6
    }
}

def draw_play_button():
    """Draw the Play button on the screen."""
    rect = play_button["rect"]
    pygame.draw.rect(screen, BUTTON_COLORS["hover"] if rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLORS["default"], rect)
    label = FONT.render(play_button["label"], True, BUTTON_FONT_COLOR)
    screen.blit(label, (rect.x + (rect.width - label.get_width()) // 2, rect.y + (rect.height - label.get_height()) // 2))
    pygame.display.flip()

def draw_buttons():
    """Draw difficulty buttons on the screen."""
    for button_name, button in buttons.items():
        pygame.draw.rect(screen, BUTTON_COLORS["hover"] if button["rect"].collidepoint(pygame.mouse.get_pos()) else BUTTON_COLORS["default"], button["rect"])
        label = FONT.render(button["label"], True, BUTTON_FONT_COLOR)
        screen.blit(label, (button["rect"].x + (button["rect"].width - label.get_width()) // 2, button["rect"].y + (button["rect"].height - label.get_height()) // 2))
    pygame.display.flip()

def get_clicked_difficulty(pos):
    """Determine which difficulty button was clicked."""
    for button_name, button in buttons.items():
        if button["rect"].collidepoint(pos):
            return button["difficulty"]
    return None

# Define the Reset button
reset_button = {
    "rect": pygame.Rect(10, HEIGHT - BUTTON_HEIGHT - 10, BUTTON_WIDTH, BUTTON_HEIGHT),  # Bottom-left position
    "label": "Reset"
}


def draw_reset_button():
    """Draw the Reset button on the screen."""
    rect = reset_button["rect"]
    pygame.draw.rect(screen, BUTTON_COLORS["hover"] if rect.collidepoint(pygame.mouse.get_pos()) else BUTTON_COLORS["default"], rect)
    label = FONT.render(reset_button["label"], True, BUTTON_FONT_COLOR)
    screen.blit(label, (rect.x + (rect.width - label.get_width()) // 2, rect.y + (rect.height - label.get_height()) // 2))

def reset_game():
    """Reset the game state."""
    global board
    board = initialize_board()
