import pygame
import sys
import random

def snake_game():
    pygame.init()
    width, height = 400, 400
    screen = pygame.display.set_mode((width, height))
    clock = pygame.time.Clock()
    snake = [[100, 100]]
    direction = [20, 0]
    food = [random.randrange(0, 20)*20, random.randrange(0, 20)*20]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            direction = [-20, 0]
        if keys[pygame.K_RIGHT]:
            direction = [20, 0]
        if keys[pygame.K_UP]:
            direction = [0, -20]
        if keys[pygame.K_DOWN]:
            direction = [0, 20]

        snake[0][0] += direction[0]
        snake[0][1] += direction[1]

        if snake[0] == food:
            snake.append(food)
            food = [random.randrange(0, 20)*20, random.randrange(0, 20)*20]

        screen.fill((0,0,0))
        for segment in snake:
            pygame.draw.rect(screen, (0,255,0), (*segment, 20, 20))
        pygame.draw.rect(screen, (255,0,0), (*food, 20, 20))
        pygame.display.update()
        clock.tick(10)

    pygame.quit()
    sys.exit()
    # Issue: score is not displayed
