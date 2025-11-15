import pygame
import random
import sys

pygame.init()

# ====== WINDOW ======
WIDTH = 500
HEIGHT = 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Healthy Food Catcher")

clock = pygame.time.Clock()

# ====== LOAD IMAGES ======
def load_and_scale(path, scale=0.05):  # default item scale
    img = pygame.image.load(path).convert_alpha()
    w, h = img.get_size()
    img = pygame.transform.scale(img, (int(w * scale), int(h * scale)))
    return img

# Player image
player_img = load_and_scale("16.png", 0.05)
player_rect = player_img.get_rect()
player_rect.centerx = WIDTH // 2
player_rect.y = HEIGHT - 100  # dinaikkan sedikit karena ada alas hijau
player_speed = 7

# Healthy food (1–8)
healthy_images = [
    load_and_scale(f"{i}.png", 0.05)
    for i in range(1, 9)
]

# Junk food (9–15)
junk_images = [
    load_and_scale(f"{i}.png", 0.05)
    for i in range(9, 16)
]

# ====== OBJECTS ======
objects = []
fall_speed = 3  # lebih lambat

# ====== SCORE ======
score = 5   # mulai dari 5 biar tidak langsung game over
font = pygame.font.SysFont(None, 40)

# ====== SPAWN OBJECT ======
def spawn_object():
    obj_type = random.choice(["healthy", "junk"])

    if obj_type == "healthy":
        img = random.choice(healthy_images)
    else:
        img = random.choice(junk_images)

    rect = img.get_rect()
    rect.x = random.randint(10, WIDTH - rect.width - 10)
    rect.y = -50

    objects.append({
        "img": img,
        "rect": rect,
        "type": obj_type
    })


# ====== RESET GAME ======
def reset_game():
    global objects, score, player_rect
    objects = []
    score = 5
    player_rect.centerx = WIDTH // 2


# ====== MAIN LOOP ======
spawn_timer = 0
running = True
game_over = False

while running:
    screen.fill((30, 30, 30))

    # ===== ALAS HIJAU (FULL LEBA R) =====
    pygame.draw.rect(screen, (50, 200, 70), (0, HEIGHT - 60, WIDTH, 60))

    # ===== EVENT =====
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if game_over and event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r:
                game_over = False
                reset_game()

    # Jika game over, stop logic, hanya tampilkan teks
    if game_over:
        over_text = font.render("GAME OVER!", True, (255, 50, 50))
        restart_text = font.render("Press R to Try Again", True, (255, 255, 255))
        screen.blit(over_text, (150, HEIGHT // 2 - 40))
        screen.blit(restart_text, (110, HEIGHT // 2))
        pygame.display.update()
        clock.tick(60)
        continue

    # ===== PLAYER MOVE =====
    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player_rect.x > 0:
        player_rect.x -= player_speed
    if keys[pygame.K_RIGHT] and player_rect.x < WIDTH - player_rect.width:
        player_rect.x += player_speed

    # ===== SPAWN =====
    spawn_timer += 1
    if spawn_timer > 50:
        spawn_object()
        spawn_timer = 0

    # ===== UPDATE OBJECTS =====
    for obj in objects[:]:
        obj["rect"].y += fall_speed

        # collision
        if obj["rect"].colliderect(player_rect):
            if obj["type"] == "healthy":
                score += 2
            else:
                score -= 1
            objects.remove(obj)

        elif obj["rect"].y > HEIGHT:
            objects.remove(obj)

    # ===== DRAW OBJECTS =====
    for obj in objects:
        screen.blit(obj["img"], obj["rect"])

    # ===== DRAW PLAYER =====
    screen.blit(player_img, player_rect)

    # ===== SCORE =====
    score_text = font.render(f"Score: {score}", True, (255, 255, 255))
    screen.blit(score_text, (10, 10))

    # ===== GAME OVER TRIGGER =====
    if score <= 0:
        game_over = True

    pygame.display.update()
    clock.tick(60)
