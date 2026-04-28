import pygame
import heapq

# Color schemes
background_color = "#1F4765"
player_color = "#9E575F"
border_color = "#CBC694"
enemy_color = "#658C81"

# Width and height of the window and the player, enemies, and borders
width = 800
height = 800

TILE_SIZE = 50
PLAYER_SIZE = 25
ENEMY_SIZE = 25
BULLET_SIZE = 10

# Set player and enemy starting locations and capabilities
start_pos = [PLAYER_SIZE, TILE_SIZE * 3 + PLAYER_SIZE]
player_pos = start_pos.copy()
player_speed = 5

enemy_pos = [ENEMY_SIZE + TILE_SIZE * 3, TILE_SIZE * 14 + ENEMY_SIZE]
enemy_speed = 5 
bullet_speed = 10

# Game map
game_map = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,0,0,0,1,0,0,0,1],
    [0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1],
    [0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1],
    [0,0,0,0,0,0,0,1,0,0,0,1,0,0,0,1],
    [1,1,1,1,0,0,0,1,0,0,0,1,0,0,0,1],
    [1,0,0,1,0,0,0,1,0,0,0,1,0,0,0,1],
    [1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1],
    [1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1],
    [1,0,0,1,0,0,0,0,0,0,0,1,0,0,0,1],
    [1,0,0,1,1,1,1,1,1,1,1,1,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

# Initialize the game window
pygame.init()
screen = pygame.display.set_mode((width,height)) 
clock = pygame.time.Clock()
running = True

# Font details
font = pygame.font.Font(None, 36) 
text_surface = font.render("WINNER", True, (255,255,255))
retry = font.render("retry press 'r'", True, (255,255,255))

# --- GAME LOGIC FUNCTIONS ---

def drawMap():
    for row_index, row in enumerate(game_map):
        for col_index, tile in enumerate(row):
            x = col_index * TILE_SIZE
            y = row_index * TILE_SIZE
            color = border_color if tile == 1 else background_color
            pygame.draw.rect(screen, color, (x, y, TILE_SIZE, TILE_SIZE))
            pygame.draw.rect(screen, (0,0,0), (x, y, TILE_SIZE, TILE_SIZE), 1)

# Generate walls for collision
walls = []
for r, row in enumerate(game_map):
    for c, tile in enumerate(row):
        if tile == 1:
            walls.append(pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def restart():
    global player_pos, enemy_pos
    print("Restart method called")
    player_pos = start_pos.copy()
    enemy_pos = [ENEMY_SIZE + TILE_SIZE * 3, TILE_SIZE * 14 + ENEMY_SIZE]

# A* Pathfinding Algorithm
def get_path(start, target):
    # Convert pixels to grid coordinates (row, col)
    start_grid = (start[1] // TILE_SIZE, start[0] // TILE_SIZE)
    target_grid = (target[1] // TILE_SIZE, target[0] // TILE_SIZE)

    # Prevent crashing if target is outside map bounds
    if target_grid[0] >= len(game_map) or target_grid[1] >= len(game_map[0]) or target_grid[0] < 0 or target_grid[1] < 0:
        return []

    open_set = []
    heapq.heappush(open_set, (0, start_grid))
    
    came_from = {}
    g_score = {start_grid: 0}
    
    def heuristic(a, b):
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    while open_set:
        current = heapq.heappop(open_set)[1]

        if current == target_grid:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            return path[::-1] # Reverse the path

        for dx, dy in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            neighbor = (current[0] + dx, current[1] + dy)
            
            # Boundary and wall check
            if 0 <= neighbor[0] < len(game_map) and 0 <= neighbor[1] < len(game_map[0]):
                if game_map[neighbor[0]][neighbor[1]] == 1:
                    continue
                
                tentative_g_score = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g_score < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g_score
                    f_score = tentative_g_score + heuristic(neighbor, target_grid)
                    heapq.heappush(open_set, (f_score, neighbor))
    return []

# --- MAIN GAME LOOP ---

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    # 1. Handle Player Horizontal Movement
    new_x = player_pos[0]
    if keys[pygame.K_LEFT]:
        new_x -= player_speed
    if keys[pygame.K_RIGHT]:
        new_x += player_speed
    
    temp_rect_x = pygame.Rect(new_x, player_pos[1], PLAYER_SIZE, PLAYER_SIZE)
    if not any(temp_rect_x.colliderect(wall) for wall in walls):
        player_pos[0] = new_x

    # 2. Handle Player Vertical Movement
    new_y = player_pos[1]
    if keys[pygame.K_UP]:
        new_y -= player_speed
    if keys[pygame.K_DOWN]:
        new_y += player_speed
    
    temp_rect_y = pygame.Rect(player_pos[0], new_y, PLAYER_SIZE, PLAYER_SIZE)
    if not any(temp_rect_y.colliderect(wall) for wall in walls):
        player_pos[1] = new_y

    # 3. Handle Enemy AI (A*)
    path = get_path(enemy_pos, player_pos)
    chase_speed = 4 
    
    target_x = 0
    target_y = 0
    if path:
        # Get the first step in the path and aim for the center of that tile
        next_step = path[0]
        target_y = next_step[0] * TILE_SIZE + (TILE_SIZE // 2) - (ENEMY_SIZE // 2)
        target_x = next_step[1] * TILE_SIZE + (TILE_SIZE // 2) - (ENEMY_SIZE // 2)

    # Move enemy toward the target pixel coordinate safely
    if enemy_pos[0] < target_x:
        enemy_pos[0] = min(enemy_pos[0] + chase_speed, target_x)
    if enemy_pos[0] > target_x:
        enemy_pos[0] = max(enemy_pos[0] - chase_speed, target_x)
    if enemy_pos[1] < target_y:
        enemy_pos[1] = min(enemy_pos[1] + chase_speed, target_y)
    if enemy_pos[1] > target_y:
        enemy_pos[1] = max(enemy_pos[1] - chase_speed, target_y)


    # 4. Draw Everything
    drawMap()
    
    # Draw Player
    player = pygame.Rect(player_pos[0], player_pos[1], PLAYER_SIZE, PLAYER_SIZE)
    pygame.draw.rect(screen, player_color, player)
    
    # Draw Enemy
    enemy_rect = pygame.Rect(enemy_pos[0], enemy_pos[1], ENEMY_SIZE, ENEMY_SIZE)
    pygame.draw.rect(screen, enemy_color, enemy_rect)

    # 5. Check Game Over / Win States
    # If the enemy catches the player
    if player.colliderect(enemy_rect):
        restart() # Quick restart for hitting enemy

    # If player passes the right edge of the screen, "WINNER!!!"
    if player_pos[0] > width:
        waiting_for_restart = True
        while waiting_for_restart and running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    waiting_for_restart = False

            keys = pygame.key.get_pressed()
            if keys[pygame.K_r]:
                restart()
                waiting_for_restart = False

            drawMap()
            text_rect = text_surface.get_rect(center=(width // 2, height // 2))
            retry_rect = retry.get_rect(center=(width // 2, height // 1.5))
            screen.blit(text_surface, text_rect)
            screen.blit(retry, retry_rect)
            pygame.display.flip()
            clock.tick(60)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()