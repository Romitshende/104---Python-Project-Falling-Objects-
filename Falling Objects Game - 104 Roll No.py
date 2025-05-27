import pygame
import random

# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 600, 800
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Falling Object Game")

# Load background image
background_img = pygame.image.load("background.jpg")  # or "background.png"
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))

# Load Ben 10 image
ben10_img = pygame.image.load("ben10.png")
player_size = 85
ben10_img = pygame.transform.scale(ben10_img, (player_size, player_size))

# Colors
RED = (255, 0, 0)
GREEN = (0, 200, 0)
BLACK = (0, 0, 0)

# Fonts
font = pygame.font.SysFont("Arial", 30)
big_font = pygame.font.SysFont("Arial", 50)

# Player setup
player_pos = [WIDTH // 2, HEIGHT - 2 * player_size]
player_speed = 10

# Object setup
obj_size = 50
obj_speed = 5
num_objects = 7

def create_object():
    obj_type = random.choice(["enemy", "enemy", "powerup"])
    return [random.randint(0, WIDTH - obj_size), random.randint(-HEIGHT, 0), obj_type]

objects = [create_object() for _ in range(num_objects)]

score = 0
lives = 3
clock = pygame.time.Clock()
game_over = False
message = ""

def detect_collision(p_pos, o_pos):
    px, py = p_pos
    ox, oy = o_pos[0], o_pos[1]
    return (ox < px < ox + obj_size or ox < px + player_size < ox + obj_size) and \
           (oy < py < oy + obj_size or oy < py + player_size < oy + obj_size)

# Game loop
while not game_over:
    screen.blit(background_img, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_over = True

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_pos[0] > 0:
        player_pos[0] -= player_speed
    if keys[pygame.K_RIGHT] and player_pos[0] < WIDTH - player_size:
        player_pos[0] += player_speed

    for obj in objects:
        obj[1] += obj_speed

        if detect_collision(player_pos, obj):
            if obj[2] == "enemy":
                lives -= 1
                obj[:] = create_object()
                if lives <= 0:
                    game_over = True
            elif obj[2] == "powerup":
                score += 5
                obj[:] = create_object()
                continue

        if obj[1] > HEIGHT:
            obj[:] = create_object()
            if obj[2] == "enemy":
                score += 1

        color = RED if obj[2] == "enemy" else GREEN
        pygame.draw.rect(screen, color, (*obj[:2], obj_size, obj_size))

    # Draw player with Ben 10 image
    screen.blit(ben10_img, player_pos)

    # Draw score and lives
    score_text = font.render(f"Score: {score}", True, GREEN)
    lives_text = font.render(f"Lives: {lives}", True, GREEN)
    screen.blit(score_text, (10, 10))
    screen.blit(lives_text, (WIDTH - 120, 10))

    # Milestone message
    if score >= 20 and score < 25:
        message = "Great Job!"
    elif score >= 50:
        message = "Awesome!"
    else:
        message = ""

    if message:
        msg_text = big_font.render(message, True, GREEN)
        screen.blit(msg_text, (WIDTH // 2 - msg_text.get_width() // 2, HEIGHT // 2 - 100))

    pygame.display.update()
    clock.tick(30)

# Show Game Over
screen.blit(background_img, (0, 0))
over_text = big_font.render("Game Over", True, RED)
score_text = font.render(f"Your Score: {score}", True, BLACK)
lives_text = font.render(f"Lives Left: {lives}", True, BLACK)
screen.blit(over_text, (WIDTH // 2 - over_text.get_width() // 2, HEIGHT // 2 - 50))
screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 + 10))
screen.blit(lives_text, (WIDTH // 2 - lives_text.get_width() // 2, HEIGHT // 2 + 50))
pygame.display.update()
pygame.time.wait(3000)

pygame.quit()
