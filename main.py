import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
FPS = 60
PLAYER_SIZE = 50
BLOCK_SIZE = 50
GRAVITY = 0.5
JUMP_HEIGHT = -15
MOVE_SPEED = 5
MAX_JUMP_COUNT = 2  # Allowing double jumps

# Colors
PASTEL_COLORS = [
    (205, 230, 208),  # pastel green
    (232, 209, 209),  # pastel red
    (209, 226, 232),  # pastel blue
    (234, 209, 232),  # pastel purple
    (255, 244, 209)   # pastel yellow
]

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Block Jumper')

# Clock
clock = pygame.time.Clock()

# Font setup for scoring
font = pygame.font.Font(None, 36)

def create_block():
    # Blocks spawn at varying heights
    return pygame.Rect(random.randint(0, SCREEN_WIDTH - BLOCK_SIZE),
                       random.randint(SCREEN_HEIGHT // 2, SCREEN_HEIGHT - BLOCK_SIZE - 120),
                       BLOCK_SIZE, BLOCK_SIZE)

# Player setup
player = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 150, PLAYER_SIZE, PLAYER_SIZE)
velocity_y = 0
velocity_x = 0
on_ground = False
jump_count = 0
score = 0

# Blocks
blocks = [create_block() for _ in range(5)]

# Game loop
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if jump_count < MAX_JUMP_COUNT:
                    velocity_y = JUMP_HEIGHT
                    jump_count += 1
            if event.key in (pygame.K_LEFT, pygame.K_a):
                velocity_x = -MOVE_SPEED
            if event.key in (pygame.K_RIGHT, pygame.K_d):
                velocity_x = MOVE_SPEED
        if event.type == pygame.KEYUP:
            if event.key in (pygame.K_LEFT, pygame.K_a) and velocity_x < 0:
                velocity_x = 0
            if event.key in (pygame.K_RIGHT, pygame.K_d) and velocity_x > 0:
                velocity_x = 0

    # Physics
    player.y += velocity_y
    velocity_y += GRAVITY

    # Horizontal movement
    player.x += velocity_x
    if player.left < 0:
        player.left = 0
    elif player.right > SCREEN_WIDTH:
        player.right = SCREEN_WIDTH

    on_ground = False

    # Collision with the ground
    if player.bottom >= SCREEN_HEIGHT:
        player.bottom = SCREEN_HEIGHT
        velocity_y = 0
        on_ground = True
        jump_count = 0

    # Collision with blocks
    hit_block = None
    for block in blocks:
        if player.colliderect(block) and velocity_y > 0 and player.bottom <= block.top + 10:
            player.bottom = block.top
            velocity_y = 0
            on_ground = True
            jump_count = 0
            hit_block = block
            break

    if hit_block:
        blocks.remove(hit_block)
        blocks.append(create_block())
        score += 1

    # Drawing
    screen.fill((250, 250, 250))  # Clear screen with white
    for block in blocks:
        pygame.draw.rect(screen, random.choice(PASTEL_COLORS), block)  # Draw blocks with random pastel color
    pygame.draw.rect(screen, (0, 0, 0), player)  # Draw player as black

    # Score display
    score_text = font.render(f'Score: {score}', True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)
