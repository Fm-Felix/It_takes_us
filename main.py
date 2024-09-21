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
HOME, PLAYING, FINISHED = range(3)
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
    global buttons, correct_sequence
    buttons = [
        (pygame.Rect(50 + i * 200, HEIGHT // 2 - 25, 150, 50), color)
        for i, color in enumerate([RED, BLUE, GREEN, YELLOW])
    ]
    correct_sequence = [random.randint(0, 3) for _ in range(4)]
    logging.info(f"Stage 2: Created buttons and generated sequence: {correct_sequence}")

def create_keys():
    global keys
    keys = [pygame.Rect(random.randint(50, WIDTH - 100), random.randint(50, HEIGHT - 100), 30, 30) for _ in range(5)]
    logging.info(f"Stage 3: Created keys at positions: {[(key.x, key.y) for key in keys]}")

def draw_button(button, text):
    pygame.draw.rect(screen, GREY, button)
    text_surf = font.render(text, True, WHITE)
    screen.blit(text_surf, text_surf.get_rect(center=button.center))

def draw_home_screen():
    screen.fill(WHITE)
    draw_button(start_button, "Start Game")
    draw_button(exit_button, "Exit")

def draw_game_screen():
    screen.fill(WHITE)
    pygame.draw.rect(screen, RED, player1)
    pygame.draw.rect(screen, BLUE, player2)
    
    screen.blit(font.render(f"Stage {current_stage}", True, GREY), (10, 10))
    
    if current_stage == 2:
        for button, color in buttons:
            pygame.draw.rect(screen, color, button)
        
        if displaying_sequence:
            sequence_text = " ".join(map(str, correct_sequence))
            text = font.render(f"Remember this sequence: {sequence_text}", True, GREY)
        else:
            sequence_text = " ".join(map(str, player_sequence))
            text = font.render(f"Your input: {sequence_text}", True, GREY)
        screen.blit(text, (WIDTH // 2 - text.get_width() // 2, 50))

    elif current_stage == 3:
        for key in keys:
            pygame.draw.rect(screen, YELLOW, key)
        pygame.draw.rect(screen, GREEN, door)

def draw_finished_screen():
    screen.fill(WHITE)
    if current_stage < MAX_STAGES:
        text = font.render(f"Stage {current_stage} Completed!", True, GREY)
    else:
        text = font.render("Completed all stages!", True, BLACK)
    screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50)))
    
    if current_stage == MAX_STAGES:
        text = font.render("I love you Josefin<3", True, RED)
        screen.blit(text, text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 25)))
    
    draw_button(return_button, "Continue" if current_stage < MAX_STAGES else "Home")

def check_win_condition():
    if current_stage == 1:
        return player1.colliderect(player2)
    elif current_stage == 2:
        return len(player_sequence) == 4 and player_sequence == correct_sequence
    elif current_stage == 3:
        return len(keys) == 0 and (player1.colliderect(door) and player2.colliderect(door))

def reset_game():
    global player1, player2, current_stage, player_sequence, displaying_sequence, sequence_display_time
    player1.topleft = (100, HEIGHT - PLAYER_SIZE - 10)
    player2.topleft = (WIDTH - 100 - PLAYER_SIZE, HEIGHT - PLAYER_SIZE - 10)
    current_stage = 1
    player_sequence = []
    displaying_sequence = True
    sequence_display_time = pygame.time.get_ticks()
    create_buttons()
    create_keys()
    logging.info("Game reset. Starting from Stage 1.")

# Main game loop
clock = pygame.time.Clock()
reset_game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if game_state == HOME:
                if start_button.collidepoint(event.pos):
                    game_state = PLAYING
                    reset_game()
                elif exit_button.collidepoint(event.pos):
                    pygame.quit()
                    sys.exit()
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
                    else:
                        game_state = HOME
            elif game_state == PLAYING and current_stage == 2 and not displaying_sequence:
                for i, (button, _) in enumerate(buttons):
                    if button.collidepoint(event.pos):
                        player_sequence.append(i)
                        if check_win_condition():
                            game_state = FINISHED
                        elif len(player_sequence) == 4:
                            player_sequence = []

    if game_state == PLAYING:
        keys_pressed = pygame.key.get_pressed()
        
        # Player movements
        player1.x += (keys_pressed[pygame.K_d] - keys_pressed[pygame.K_a]) * 5
        player1.y += (keys_pressed[pygame.K_s] - keys_pressed[pygame.K_w]) * 5
        player2.x += (keys_pressed[pygame.K_RIGHT] - keys_pressed[pygame.K_LEFT]) * 5
        player2.y += (keys_pressed[pygame.K_DOWN] - keys_pressed[pygame.K_UP]) * 5
        
        # Keep players within screen bounds
        player1.clamp_ip(screen.get_rect())
        player2.clamp_ip(screen.get_rect())

        if current_stage == 2 and displaying_sequence:
            if pygame.time.get_ticks() - sequence_display_time > SEQUENCE_DISPLAY_DURATION:
                displaying_sequence = False

        if current_stage == 3:
            keys = [key for key in keys if not (player1.colliderect(key) or player2.colliderect(key))]

        if check_win_condition():
            game_state = FINISHED

    if game_state == HOME:
        draw_home_screen()
    elif game_state == PLAYING:
        draw_game_screen()
    else:
        draw_finished_screen()

    pygame.display.flip()
    clock.tick(60)