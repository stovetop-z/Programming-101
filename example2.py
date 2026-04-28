import pygame
import random

# We must initialize modules before we can create a window.
pygame.init()
screen = pygame.display.set_mode((400, 600))
clock = pygame.time.Clock()

font = pygame.font.Font(None, 25)
COINS = [0]

player_position = [180, 530]
coin_position = [random.randint(0, 370), 0]
coin_speed = 7
score = 0

def the_player_and_the_coin_collide(player_position, coin_position) -> bool:
    return (player_position[1] < coin_position[1] < player_position[1] + 50) and (player_position[0] < coin_position[0] < player_position[0] + 50)

def the_coin_goes_out_of_bounds(coin_position) -> bool:
    return coin_position[1] > 600

def the_key_pressed_is_left_and_the_player_does_not_go_out_of_bounds(keys, player_position) -> bool:
    return keys[pygame.K_LEFT] and player_position[0] > 0

def the_key_pressed_is_right_and_the_player_does_not_go_out_of_bounds(keys, player_position) -> bool:
    return keys[pygame.K_RIGHT] and player_position[0] < 350

def the_player_closes_the_window(event) -> bool:
    return event.type == pygame.QUIT

# LOOPS: The 'while' loop keeps the game running.
# Without this, the program would run once and immediately close.
running = True
while running:
    screen.fill((30, 30, 30)) # Dark Grey background
    
    # CONDITIONALS: Checking for specific events or logic states.
    for event in pygame.event.get():
        if the_player_closes_the_window(event):
            running = False

    keys = pygame.key.get_pressed()
    if the_key_pressed_is_left_and_the_player_does_not_go_out_of_bounds(keys, player_position):
        if 5 + score > 14:
            player_position[0] -= 14
        else:
            player_position[0] -= 5 + score
    if the_key_pressed_is_right_and_the_player_does_not_go_out_of_bounds(keys, player_position):
        if 5 + score > 14:
            player_position[0] += 14
        else:
            player_position[0] += 5 + score

    # Update coin positionition (Sequencing: Gravity happens every frame)
    if coin_speed + score > 14:
        coin_position[1] += 14
    else:
        coin_position[1] += coin_speed + score

    # CONDITIONALS: Logic for catching the coin or missing it
    if the_coin_goes_out_of_bounds(coin_position):
        coin_position = [random.randint(0, 370), 0] # Reset coin if missed
        COINS.append(score)
        score = 0

    # Simple Collision detection
    if the_player_and_the_coin_collide(player_position, coin_position):
        score += 1
        coin_position = [random.randint(0, 370), 0]

    # Draw elements
    current_score_surface = font.render(f"Current: {score}", True, (255,255,255))
    best_score_surface = font.render(f"Best: {max(COINS)}", True, (255,255,255))
    pygame.draw.rect(screen, (0, 255, 0), (player_position[0], player_position[1], 50, 50)) # Player
    pygame.draw.circle(screen, (255, 215, 0), (coin_position[0], coin_position[1]), 15)      # Coin
    screen.blit(current_score_surface, (25,50))
    screen.blit(best_score_surface, (25,15))
    
    pygame.display.flip()
    clock.tick(60) # Limits the loop to 60 frames per second

pygame.quit()