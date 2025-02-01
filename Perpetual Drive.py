import pygame
import sys
import random

pygame.init()

SCREEN_HEIGHT = 1000
SCREEN_WIDTH = int(SCREEN_HEIGHT * (2 / 3))

BLUE = (135, 206, 250)
GRAY = (50, 50, 50)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Perpetual Drive")

clock = pygame.time.Clock()

VANISHING_POINT = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 20)

CAR_WIDTH = 50
CAR_HEIGHT = 75
car_image = pygame.image.load('car.png')
car_image = pygame.transform.scale(car_image, (CAR_WIDTH, CAR_HEIGHT))
car_x = SCREEN_WIDTH // 2 - CAR_WIDTH // 2
car_y = SCREEN_HEIGHT - CAR_HEIGHT - 20
car_speed = 10

coin_width = 50
coin_height = 50
coin_image = pygame.image.load('coin.png')
coin_image = pygame.transform.scale(coin_image, (coin_width, coin_height))
coin_x = random.randint(SCREEN_WIDTH // 4, 3 * SCREEN_WIDTH // 4 - coin_width)
coin_y = SCREEN_HEIGHT  
coin_speed = 5

obstacle_width = 50
obstacle_height = 75
obstacle_image = pygame.image.load('obstacle.png')
obstacle_image = pygame.transform.scale(obstacle_image, (obstacle_width, obstacle_height))
obstacle_x = random.randint(SCREEN_WIDTH // 4, 3 * SCREEN_WIDTH // 4 - obstacle_width)
obstacle_y = -50 
obstacle_speed = 5

score = 0
level = 1
font = pygame.font.Font(None, 36)

running = True

def reset_game():
    global car_x, car_y, car_speed, coin_y, coin_x, obstacle_y, obstacle_x, coin_speed, obstacle_speed, score, level
    car_x = SCREEN_WIDTH // 2 - CAR_WIDTH // 2
    car_y = SCREEN_HEIGHT - CAR_HEIGHT - 20
    car_speed = 5
    coin_x = random.randint(SCREEN_WIDTH // 4, 3 * SCREEN_WIDTH // 4 - coin_width)
    coin_y = SCREEN_HEIGHT
    obstacle_x = random.randint(SCREEN_WIDTH // 4, 3 * SCREEN_WIDTH // 4 - obstacle_width)
    obstacle_y = -50
    coin_speed = 5
    obstacle_speed = 5
    score = 0
    level = 1

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and car_x > SCREEN_WIDTH // 4:
        car_x -= car_speed
    if keys[pygame.K_RIGHT] and car_x < 3 * SCREEN_WIDTH // 4 - CAR_WIDTH:
        car_x += car_speed

    coin_y += coin_speed
    if coin_y > SCREEN_HEIGHT:
        coin_y = -50
        coin_x = random.randint(SCREEN_WIDTH // 4, 3 * SCREEN_WIDTH // 4 - coin_width)

    distance_from_vanishing_point_coin = SCREEN_HEIGHT - coin_y
    perspective_scale_coin = distance_from_vanishing_point_coin / SCREEN_HEIGHT
    adjusted_coin_width = max(int(coin_width * perspective_scale_coin), 5)
    adjusted_coin_height = max(int(coin_height * perspective_scale_coin), 5)
    adjusted_coin_x = VANISHING_POINT[0] + (coin_x - VANISHING_POINT[0]) * perspective_scale_coin

    obstacle_y += obstacle_speed
    if obstacle_y > SCREEN_HEIGHT:
        obstacle_y = -50
        obstacle_x = random.randint(SCREEN_WIDTH // 4, 3 * SCREEN_WIDTH // 4 - obstacle_width)

    distance_from_vanishing_point_obstacle = SCREEN_HEIGHT - obstacle_y
    perspective_scale_obstacle = 1 - (distance_from_vanishing_point_obstacle / SCREEN_HEIGHT)
    adjusted_obstacle_width = max(int(obstacle_width * perspective_scale_obstacle), 5)
    adjusted_obstacle_height = max(int(obstacle_height * perspective_scale_obstacle), 5)
    adjusted_obstacle_x = VANISHING_POINT[0] + (obstacle_x - VANISHING_POINT[0]) * perspective_scale_obstacle

    if (car_x < adjusted_coin_x + adjusted_coin_width
        and car_x + CAR_WIDTH > adjusted_coin_x
        and car_y < coin_y + adjusted_coin_height
        and car_y + CAR_HEIGHT > coin_y):
        score += 1
        coin_y = SCREEN_HEIGHT
        coin_x = random.randint(SCREEN_WIDTH // 4, 3 * SCREEN_WIDTH // 4 - coin_width)

    if (car_x < adjusted_obstacle_x + adjusted_obstacle_width
        and car_x + CAR_WIDTH > adjusted_obstacle_x
        and car_y < obstacle_y + adjusted_obstacle_height
        and car_y + CAR_HEIGHT > obstacle_y):
        game_over_text = font.render("Game Over! Press SPACE to Restart", True, (255, 0, 0))
        screen.blit(game_over_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2))
        pygame.display.flip()

        game_over = True
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    game_over = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        reset_game()
                        game_over = False
            pygame.time.delay(100)
        continue

    if score >= 5 * level:
        level += 1
        coin_speed += 1
        obstacle_speed += 1

    screen.fill(BLUE)

    pygame.draw.polygon(
        screen,
        GRAY,
        [
            (SCREEN_WIDTH // 4, SCREEN_HEIGHT),
            (3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT),
            (VANISHING_POINT[0] + 20, VANISHING_POINT[1]),
            (VANISHING_POINT[0] - 20, VANISHING_POINT[1]),
        ],)
    pygame.draw.line(screen, WHITE, (SCREEN_WIDTH // 2, SCREEN_HEIGHT), VANISHING_POINT, 3)
    screen.blit(car_image, (car_x, car_y))

    coin_perspective_image = pygame.transform.scale(coin_image, (adjusted_coin_width, adjusted_coin_height))
    screen.blit(coin_perspective_image, (adjusted_coin_x, coin_y))

    obstacle_perspective_image = pygame.transform.scale(obstacle_image, (adjusted_obstacle_width, adjusted_obstacle_height))
    screen.blit(obstacle_perspective_image, (adjusted_obstacle_x, obstacle_y))

    score_text = font.render(f"Score: {score}  Level: {level}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
