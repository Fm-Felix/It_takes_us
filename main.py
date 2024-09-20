import pygame
import sys
import random
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Pygame
pygame.init()

# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("It takes us<3")

# Define colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (100, 100, 100)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)

# Player properties
PLAYER_SIZE = 50
player1 = pygame.Rect(100, HEIGHT - PLAYER_SIZE - 10, PLAYER_SIZE, PLAYER_SIZE)
player2 = pygame.Rect(WIDTH - 100 - PLAYER_SIZE, HEIGHT - PLAYER_SIZE - 10, PLAYER_SIZE, PLAYER_SIZE)

# Button properties
button_width, button_height = 200, 50
start_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 - button_height, button_width, button_height)
exit_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + button_height, button_width, button_height)
return_button = pygame.Rect(WIDTH // 2 - button_width // 2, HEIGHT // 2 + 50, button_width, button_height)

# Game states
HOME = 0
PLAYING = 1
FINISHED = 2
game_state = HOME

# Stage properties
current_stage = 1
MAX_STAGES = 3

# Font
font = pygame.font.Font(None, 36)

# Stage 2 properties
buttons = []
correct_sequence = []
player_sequence = []
displaying_sequence = False
sequence_display_time = 0
SEQUENCE_DISPLAY_DURATION = 2000  # 2 seconds

# Stage 3 properties
keys = []
door = pygame.Rect(WIDTH - 60, HEIGHT // 2 - 30, 60, 60)

def create_buttons():
    """Create colored buttons for Stage 2 and generate a random sequence."""
    global buttons, correct_sequence
    buttons = []
    colors = [RED, BLUE, GREEN, YELLOW]
    for i in range(4):
        button = pygame.Rect(50 + i * 200, HEIGHT // 2 - 25, 150, 50)
        buttons.append((button, colors[i]))
    correct_sequence = [random.randint(0, 3) for _ in range(4)]
    logging.info(f"Stage 2: Created buttons and generated sequence: {correct_sequence}")

def create_keys():
    """Create random positions for keys in Stage 3."""
    global keys
    keys = []
    for _ in range(5):
        x = random.randint(50, WIDTH - 100)
        y = random.randint(50, HEIGHT - 100)
        keys.append(pygame.Rect(x, y, 30, 30))
    logging.info(f"Stage 3: Created keys at positions: {[(key.x, key.y) for key in keys]}")

def draw_button(button, text):
    """Draw a button with text on the screen."""
    pygame.draw.rect(screen, GREY, button)
    text_surf = font.render(text, True, WHITE)
    text_rect = text_surf.get_rect(center=button.center)
    screen.blit(text_surf, text_rect)

def draw_home_screen():
    """Draw the home screen with start and exit buttons."""
    screen.fill(WHITE)
    draw_button(start_button, "Start Game")
    draw_button(exit_button, "Exit")

def draw_game_screen():
    """Draw the game screen based on the current stage."""
    
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, player1)
    pygame.draw.rect(screen, BLUE, player2)
    
    stage_text = font.render(f"Stage {current_stage}", True, GREY)
    screen.blit(stage_text, (10, 10))
    
    if current_stage == 2:
        for button, color in buttons:
            pygame.draw.rect(screen, color, button)
        
        # Display the correct sequence for a short time
        if displaying_sequence:
            sequence_text = " ".join(str(num) for num in correct_sequence)
            text = font.render(f"Remember this sequence: {sequence_text}", True, GREY)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50))
        else:
            # Display the player's current input
            sequence_text = " ".join(str(num) for num in player_sequence)
            text = font.render(f"Your input: {sequence_text}", True, GREY)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50))

    elif current_stage == 3:
        for key in keys:
            pygame.draw.rect(screen, YELLOW, key)
        pygame.draw.rect(screen, GREEN, door)

def draw_finished_screen():
    """Draw the finished screen for each stage or game completion."""
    screen.fill(WHITE)
    if current_stage < MAX_STAGES:
        text = font.render(f"Stage {current_stage} Completed!", True, GREY)
    else:
        text = font.render("Jag älskar dig Josefin<3", True, RED)
    text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(text, text_rect)
    draw_button(return_button, "Continue" if current_stage < MAX_STAGES else "Home")

def check_win_condition():
    """Check if the current stage's win condition is met."""
    if current_stage == 1:
        win = player1.colliderect(player2)
    elif current_stage == 2:
        win = len(player_sequence) == 4 and player_sequence == correct_sequence
    elif current_stage == 3:
        win = len(keys) == 0 and (player1.colliderect(door) and player2.colliderect(door))
    
    if win:
        logging.info(f"Stage {current_stage} completed!")
    return win

def reset_game():
    """Reset the game state for a new game or stage."""
    global player1, player2, current_stage, player_sequence, displaying_sequence, sequence_display_time
    player1 = pygame.Rect(100, HEIGHT - PLAYER_SIZE - 10, PLAYER_SIZE, PLAYER_SIZE)
    player2 = pygame.Rect(WIDTH - 100 - PLAYER_SIZE, HEIGHT - PLAYER_SIZE - 10, PLAYER_SIZE, PLAYER_SIZE)
    current_stage = 1
    player_sequence = []
    displaying_sequence = True
    sequence_display_time = pygame.time.get_ticks()
    create_buttons()
    create_keys()
    logging.info("Game reset. Starting from Stage 1.")

# Main game loop
clock = pygame.time.Clock()
running = True

reset_game()

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == HOME:
                if start_button.collidepoint(event.pos):
                    game_state = PLAYING
                    reset_game()
                    logging.info("Game started from Home screen.")
                elif exit_button.collidepoint(event.pos):
                    running = False
                    logging.info("Game exited from Home screen.")
            elif game_state == FINISHED:
                if return_button.collidepoint(event.pos):
                    if current_stage < MAX_STAGES:
                        current_stage += 1
                        player_sequence = []
                        displaying_sequence = True
                        sequence_display_time = pygame.time.get_ticks()
                        if current_stage == 3:
                            create_keys()
                        game_state = PLAYING
                        logging.info(f"Moving to Stage {current_stage}")
                    else:
                        game_state = HOME
                        logging.info("All stages completed. Returned to Home screen.")
            elif game_state == PLAYING and current_stage == 2 and not displaying_sequence:
                for i, (button, _) in enumerate(buttons):
                    if button.collidepoint(event.pos):
                        player_sequence.append(i)
                        logging.info(f"Stage 2: Player clicked button {i}. Current sequence: {player_sequence}")
                        if check_win_condition():
                            game_state = FINISHED
                        elif len(player_sequence) == 4:
                            # Reset sequence if incorrect
                            logging.info("Stage 2: Incorrect sequence. Resetting player input.")
                            player_sequence = []

    if game_state == PLAYING:
        keys_pressed = pygame.key.get_pressed()
        
        # Player 1 controls (WASD)
        if keys_pressed[pygame.K_a] and player1.left > 0:
            player1.x -= 5
        if keys_pressed[pygame.K_d] and player1.right < WIDTH:
            player1.x += 5
        if keys_pressed[pygame.K_w] and player1.top > 0:
            player1.y -= 5
        if keys_pressed[pygame.K_s] and player1.bottom < HEIGHT:
            player1.y += 5

        # Player 2 controls (Arrow keys)
        if keys_pressed[pygame.K_LEFT] and player2.left > 0:
            player2.x -= 5
        if keys_pressed[pygame.K_RIGHT] and player2.right < WIDTH:
            player2.x += 5
        if keys_pressed[pygame.K_UP] and player2.top > 0:
            player2.y -= 5
        if keys_pressed[pygame.K_DOWN] and player2.bottom < HEIGHT:
            player2.y += 5

        # Stage 2: Check if sequence display time is over
        if current_stage == 2 and displaying_sequence:
            if pygame.time.get_ticks() - sequence_display_time > SEQUENCE_DISPLAY_DURATION:
                displaying_sequence = False
                logging.info("Stage 2: Sequence display time over. Players can now input sequence.")

        # Stage 3: Check for key collection
        if current_stage == 3:
            keys_to_remove = []
            for key in keys:
                if player1.colliderect(key) or player2.colliderect(key):
                    keys_to_remove.append(key)
            for key in keys_to_remove:
                keys.remove(key)
                logging.info(f"Stage 3: Key collected. Remaining keys: {len(keys)}")

        if check_win_condition():
            game_state = FINISHED

    # Draw the appropriate screen based on the game state
    if game_state == HOME:
        draw_home_screen()
    elif game_state == PLAYING:
        draw_game_screen()
    elif game_state == FINISHED:
        draw_finished_screen()

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()