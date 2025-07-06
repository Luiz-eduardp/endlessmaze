# -*- coding: utf-8 -*-
import pygame
import os
import time
import random

TILE_SIZE = 32
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
FPS = 60

COLOR_BLACK = (15, 56, 15)
COLOR_DARK_GREEN = (48, 98, 48)
COLOR_LIGHT_GREEN = (155, 188, 15)
COLOR_WHITE = (173, 203, 173)

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Endless Maze")
clock = pygame.time.Clock()

try:
    current_dir = os.path.dirname(__file__)
except NameError:
    current_dir = os.path.dirname(os.path.abspath(__file__))
assets_dir = os.path.join(current_dir, "assets")

def load_image(path, scale=None):
    try:
        image = pygame.image.load(path).convert_alpha()
        if scale is None:
            scale = (TILE_SIZE, TILE_SIZE)
        return pygame.transform.scale(image, scale)
    except pygame.error as e:
        print(f"AVISO: Não foi possível carregar a imagem: {path}. Erro: {e}")
        surface = pygame.Surface(scale or (TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
        surface.fill((255, 0, 255, 255))
        return surface

def load_all_assets(asset_path):
    images = {}
    images['floor'] = load_image(os.path.join(asset_path, "tiles", "sprite_421.png"))
    images['wall'] = load_image(os.path.join(asset_path, "tiles", "sprite_143.png"))
    images['player'] = load_image(os.path.join(asset_path, "player", "sprite_15.png"))
    images['exit'] = load_image(os.path.join(asset_path, "tiles", "sprite_400.png"))
    images['enemy'] = load_image(os.path.join(asset_path, "player", "enemy.png"))
    return images

assets = load_all_assets(assets_dir)
floor_img = assets['floor']
wall_img = assets['wall']
player_img = assets['player']
exit_img = assets['exit']
enemy_img = assets['enemy']

def generate_maze(width, height):
    width = width if width % 2 != 0 else width + 1
    height = height if height % 2 != 0 else height + 1
    maze = [['#' for _ in range(width)] for _ in range(height)]
    
    def carve(cx, cy):
        directions = [(0, -2), (0, 2), (-2, 0), (2, 0)]
        random.shuffle(directions)
        for dx, dy in directions:
            nx, ny = cx + dx, cy + dy
            if 0 <= ny < height and 0 <= nx < width and maze[ny][nx] == '#':
                maze[ny][nx] = '.'
                maze[cy + dy // 2][cx + dx // 2] = '.'
                carve(nx, ny)

    start_x, start_y = (random.randrange(1, width, 2), random.randrange(1, height, 2))
    maze[start_y][start_x] = '.'
    carve(start_x, start_y)
    return ["".join(row) for row in maze], width, height

class Entity(pygame.sprite.Sprite):
    def __init__(self, x, y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))

    def move(self, dx, dy, walls):
        if dx != 0:
            self.rect.x += dx
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    if dx > 0: self.rect.right = wall.rect.left
                    if dx < 0: self.rect.left = wall.rect.right
        if dy != 0:
            self.rect.y += dy
            for wall in walls:
                if self.rect.colliderect(wall.rect):
                    if dy > 0: self.rect.bottom = wall.rect.top
                    if dy < 0: self.rect.top = wall.rect.bottom

class Player(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, player_img)
        self.speed = 4
        self.hitbox = self.rect.inflate(-12, -12)

    def move(self, dx, dy, walls):
        self.hitbox.x += dx
        for wall in walls:
            if self.hitbox.colliderect(wall.rect):
                if dx > 0: self.hitbox.right = wall.rect.left
                if dx < 0: self.hitbox.left = wall.rect.right

        self.hitbox.y += dy
        for wall in walls:
            if self.hitbox.colliderect(wall.rect):
                if dy > 0: self.hitbox.bottom = wall.rect.top
                if dy < 0: self.hitbox.top = wall.rect.bottom

        self.rect.center = self.hitbox.center

    def update(self, walls):
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]: dx = -self.speed
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]: dx = self.speed
        if keys[pygame.K_UP] or keys[pygame.K_w]: dy = -self.speed
        if keys[pygame.K_DOWN] or keys[pygame.K_s]: dy = self.speed
        
        self.move(dx, dy, walls)

class Enemy(Entity):
    def __init__(self, x, y):
        super().__init__(x, y, enemy_img)
        self.speed = random.randint(1, 3)
        self.direction_x, self.direction_y = random.choice([(self.speed, 0), (-self.speed, 0), (0, self.speed), (0, -self.speed)])

    def update(self, walls):
        old_pos = self.rect.topleft
        self.move(self.direction_x, self.direction_y, walls)
        if self.rect.topleft == old_pos:
            self.direction_x, self.direction_y = random.choice([(self.speed, 0), (-self.speed, 0), (0, self.speed), (0, -self.speed)])

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = wall_img
        self.rect = self.image.get_rect(topleft=(x, y))

class Exit(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = exit_img
        self.rect = self.image.get_rect(topleft=(x, y))

class Camera:
    def __init__(self, width, height):
        self.camera = pygame.Rect(0, 0, width, height)
        self.width = width
        self.height = height

    def apply(self, entity_rect):
        return entity_rect.move(self.camera.topleft)

    def update(self, target):
        x = -target.rect.centerx + int(SCREEN_WIDTH / 2)
        y = -target.rect.centery + int(SCREEN_HEIGHT / 2)
        x = min(0, x)
        y = min(0, y)
        x = max(-(self.width - SCREEN_WIDTH), x)
        y = max(-(self.height - SCREEN_HEIGHT), y)
        self.camera = pygame.Rect(x, y, self.width, self.height)

all_sprites = pygame.sprite.Group()
walls = pygame.sprite.Group()
exits = pygame.sprite.Group()
enemies = pygame.sprite.Group()

player = Player(0, 0)
camera = Camera(0, 0)
level = 1
game_active = True

def get_level_config(level):
    maze_w = 21 + ((level - 1) // 2) * 4
    maze_h = 15 + ((level - 1) // 2) * 4
    time_limit = max(20, 70 - (level - 1) * 2.5)
    num_enemies = 1 + (level - 1) // 2
    return maze_w, maze_h, time_limit, num_enemies

def setup_level(current_level):
    global maze_map, map_width, map_height, camera, player, start_time, time_limit
    
    all_sprites.empty(); walls.empty(); exits.empty(); enemies.empty()

    maze_w, maze_h, time_limit, num_enemies = get_level_config(current_level)
    maze_map, map_width, map_height = generate_maze(maze_w, maze_h)
    map_width *= TILE_SIZE
    map_height *= TILE_SIZE
    
    floor_positions = []
    for r, row in enumerate(maze_map):
        for c, tile in enumerate(row):
            if tile == '.': floor_positions.append((c, r))
    random.shuffle(floor_positions)

    player_pos = floor_positions.pop()
    player.rect.topleft = (player_pos[0] * TILE_SIZE, player_pos[1] * TILE_SIZE)
    player.hitbox.center = player.rect.center
    
    exit_pos = floor_positions.pop()
    exits.add(Exit(exit_pos[0] * TILE_SIZE, exit_pos[1] * TILE_SIZE))

    for _ in range(int(num_enemies)):
        if not floor_positions: break
        enemy_pos = floor_positions.pop()
        enemies.add(Enemy(enemy_pos[0] * TILE_SIZE, enemy_pos[1] * TILE_SIZE))
    
    for r, row in enumerate(maze_map):
        for c, tile in enumerate(row):
            if tile == '#': walls.add(Wall(c * TILE_SIZE, r * TILE_SIZE))

    all_sprites.add(player, exits, enemies, walls)
    
    camera.__init__(map_width, map_height)
    start_time = time.time()

font = pygame.font.Font(None, 40)
big_font = pygame.font.Font(None, 74)
hud_height = 40

running = True
setup_level(level)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False
            if not game_active and event.key == pygame.K_r:
                level = 1
                game_active = True
                setup_level(level)

    if game_active:
        all_sprites.update(walls)
        camera.update(player)
        
        elapsed_time = time.time() - start_time
        
        collided_exit = False
        for exit_tile in exits:
            if player.hitbox.colliderect(exit_tile.rect):
                collided_exit = True
                break
        
        if collided_exit:
            level += 1
            setup_level(level)
            continue

        collided_enemy = False
        for enemy in enemies:
            if player.hitbox.colliderect(enemy.rect):
                collided_enemy = True
                break
        
        if elapsed_time > time_limit or collided_enemy:
            game_active = False

    screen.fill(COLOR_BLACK)
    
    for r in range(map_height // TILE_SIZE):
        for c in range(map_width // TILE_SIZE):
            screen.blit(floor_img, camera.apply(pygame.Rect(c * TILE_SIZE, r * TILE_SIZE, TILE_SIZE, TILE_SIZE)))

    for sprite in all_sprites:
        screen.blit(sprite.image, camera.apply(sprite.rect))

    hud_panel = pygame.Surface((SCREEN_WIDTH, hud_height))
    hud_panel.fill(COLOR_BLACK)
    
    if game_active:
        remaining_time = time_limit - elapsed_time
        time_color = COLOR_LIGHT_GREEN if remaining_time > 10 else COLOR_WHITE
        time_text = font.render(f"Tempo: {int(remaining_time)}s", True, time_color)
    else:
        time_text = font.render("Tempo: 0s", True, COLOR_WHITE)
    
    hud_panel.blit(time_text, (10, 5))
    
    level_text = font.render(f"Nível: {level}", True, COLOR_LIGHT_GREEN)
    level_rect = level_text.get_rect(right=SCREEN_WIDTH - 10, top=5)
    hud_panel.blit(level_text, level_rect)
    screen.blit(hud_panel, (0, 0))

    if not game_active:
        overlay = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
        overlay.fill((COLOR_BLACK[0], COLOR_BLACK[1], COLOR_BLACK[2], 200))
        screen.blit(overlay, (0,0))
        
        game_over_text = big_font.render("FIM DE JOGO", True, COLOR_WHITE)
        restart_text = font.render("Pressione 'R' para reiniciar", True, COLOR_LIGHT_GREEN)
        
        screen.blit(game_over_text, game_over_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 - 30)))
        screen.blit(restart_text, restart_text.get_rect(center=(SCREEN_WIDTH/2, SCREEN_HEIGHT/2 + 30)))

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()