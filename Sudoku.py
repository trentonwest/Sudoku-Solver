import pygame
import sys
import time
import SudokuBoardGen

# Initialize Pygame
pygame.init()

sound= pygame.mixer.Sound("Sudoku/audio/001.mp3")
sound.set_volume(0.2)

# Constants
WIDTH, HEIGHT = 900,900
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRID_SIZE = 9
CELL_SIZE = WIDTH // GRID_SIZE

# Sample Sudoku puzzle (0 represents empty cells)
PUZZLE = SudokuBoardGen.generate_sudoku_board()

# Initialize the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sudoku Solver")
font = pygame.font.Font(None, 100)


# Function to draw the grid
def draw_grid():
    for i in range(GRID_SIZE):
        if i % 3 == 0:
            pygame.draw.line(window, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 2)
            pygame.draw.line(window, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 2)
        else:
            pygame.draw.line(window, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE), 1)
            pygame.draw.line(window, BLACK, (i * CELL_SIZE, 0), (i * CELL_SIZE, HEIGHT), 1)

# Function to fill the puzzle values
def fill_puzzle(grid):
    for i in range(GRID_SIZE):
        for j in range(GRID_SIZE):
            if grid[i][j] != 0:
                num = font.render(str(grid[i][j]), True, BLACK)
                window.blit(num, (j * CELL_SIZE + CELL_SIZE // 2 - num.get_width() // 2,
                                  i * CELL_SIZE + CELL_SIZE // 2 - num.get_height() // 2))

def is_valid(board, row, col, num):
    # Check if the number is not in the current row
    if num in board[row]:
        return False

    # Check if the number is not in the current column
    if num in [board[i][col] for i in range(9)]:
        return False

    # Check if the number is not in the current 3x3 grid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(start_row, start_row + 3):
        for j in range(start_col, start_col + 3):
            if board[i][j] == num:
                return False

    return True

def solve_sudoku(board):
    for row in range(9):
        for col in range(9):
            # If the current cell is empty
            if board[row][col] == 0:
                # Try filling the cell with numbers from 1 to 9
                for num in range(1, 10):
                    sound.play()
                    if is_valid(board, row, col, num):
                        #try this
                        board[row][col] = num
                        window.fill(WHITE)
                        draw_grid()
                        fill_puzzle(PUZZLE)
                        pygame.draw.rect(window, (0,255,0), (col*CELL_SIZE,row*CELL_SIZE,CELL_SIZE,CELL_SIZE),5)  # (x, y, width, height)
                        pygame.display.flip()
                        time.sleep(0.005)
                        # Recur with the updated board
                        if solve_sudoku(board):
                            return True
                        
                        # Backtrack
                        window.fill(WHITE)
                        draw_grid()
                        fill_puzzle(PUZZLE)
                        pygame.draw.rect(window, (255,0,0), (col*CELL_SIZE,row*CELL_SIZE,CELL_SIZE,CELL_SIZE),5)  # (x, y, width, height)
                        pygame.display.flip()
                        #time.sleep(0.2)
                        board[row][col] = 0
                        
                # If no number works, backtrack to the previous state
                return False
    # If all cells are filled, the Sudoku is solved
    return True


# Main game loop
while True:
    window.fill(WHITE)

    # Handle events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            x, y = pygame.mouse.get_pos()
            row, col = y // CELL_SIZE, x // CELL_SIZE
            # Check if the clicked cell is empty (contains 0)
            if PUZZLE[row][col] == 0:
                #highlioght cell
                draw_grid()
                fill_puzzle(PUZZLE)
                pygame.draw.rect(window, (0,255,190), (col*CELL_SIZE,row*CELL_SIZE,CELL_SIZE,CELL_SIZE),3)  # (x, y, width, height)
                pygame.display.flip()
                PUZZLE[row][col] = input()  # You can change this to handle input from the player
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                solve_sudoku(PUZZLE)
                time.sleep(3)
                exit(0)

    # Draw grid and puzzle
    draw_grid()
    fill_puzzle(PUZZLE)

    pygame.display.flip()
