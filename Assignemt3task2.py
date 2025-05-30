import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "1"

import pygame
import random
import math
# Initialize Pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 1000, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animal Hero Side Scroller")

# Clock and FPS
clock = pygame.time.Clock()
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)
GRAY = (128, 128, 128)
DARK_RED = (139, 0, 0)
SKY_BLUE = (135, 206, 235)
DARK_GREEN = (0, 100, 0)

# Game constants
GRAVITY = 0.8
PLAYER_SPEED = 6
JUMP_POWER = 16
PROJECTILE_SPEED = 12
GROUND_Y = HEIGHT - 100

# Load fonts
font_small = pygame.font.SysFont("Arial", 20)
font_medium = pygame.font.SysFont("Arial", 28)
font_large = pygame.font.SysFont("Arial", 36)

class Player(pygame.sprite.Sprite):
    """Player character with movement, jumping, shooting, health and lives"""

    def __init__(self):
        super().__init__()
        sprite_width, sprite_height = 40, 50

        self.original_image_right = pygame.Surface((sprite_width, sprite_height), pygame.SRCALPHA)
        self.original_image_right.fill((0,0,0,0))
        pygame.draw.rect(self.original_image_right, (50, 50, 200), (10, 15, 20, 35)) # Main body
        pygame.draw.circle(self.original_image_right, (100, 100, 255), (20, 10), 8) # Head
        pygame.draw.circle(self.original_image_right, WHITE, (23, 8), 2) # Eye
        pygame.draw.line(self.original_image_right, GRAY, (20, 25), (38, 25), 4) # Gun

        self.original_image_left = pygame.transform.flip(self.original_image_right, True, False)

        self.image = self.original_image_right
        self.rect = self.image.get_rect()
        self.rect.x = 100
        self.rect.bottom = GROUND_Y

        self.vel_y = 0
        self.on_ground = True
        self.speed = PLAYER_SPEED
        self.facing_right = True

        self.max_health = 100
        self.health = self.max_health
        self.lives = 3
        self.score = 0
        self.invulnerable = False
        self.invulnerable_timer = 0

    def update(self):
        keys = pygame.key.get_pressed()
        dx = 0

        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= self.speed
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += self.speed
            self.facing_right = True

        self.rect.x += dx

        if self.facing_right:
            self.image = self.original_image_right
        else:
            self.image = self.original_image_left

        if (keys[pygame.K_SPACE] or keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.jump()

        self.apply_gravity()
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))

        if self.invulnerable:
            self.invulnerable_timer -= 1
            if self.invulnerable_timer <= 0:
                self.invulnerable = False

    def jump(self):
        if self.on_ground:
            self.vel_y = -JUMP_POWER
            self.on_ground = False

    def apply_gravity(self):
        self.vel_y += GRAVITY
        self.rect.y += self.vel_y
        if self.rect.bottom >= GROUND_Y:
            self.rect.bottom = GROUND_Y
            self.vel_y = 0
            self.on_ground = True

    def shoot(self):
        if self.facing_right:
            projectile = Projectile(self.rect.right - 5, self.rect.centery -2, 1) # Adjust spawn point
        else:
            projectile = Projectile(self.rect.left + 5, self.rect.centery -2, -1) # Adjust spawn point
        return projectile

    def take_damage(self, damage):
        if not self.invulnerable:
            self.health -= damage
            self.invulnerable = True
            self.invulnerable_timer = 90 # 1.5 seconds invulnerability
            if self.health <= 0:
                self.lose_life()

    def lose_life(self):
        self.lives -= 1
        if self.lives > 0: # Only reset health if player has lives left
            self.health = self.max_health
        else:
            self.health = 0 # Ensure health is 0 if no lives left

    def heal(self, amount):
        self.health = min(self.max_health, self.health + amount)

    def add_life(self):
        self.lives += 1

    def add_score(self, points):
        self.score += points

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((15, 7), pygame.SRCALPHA)
        self.image.fill((0,0,0,0))
        pygame.draw.ellipse(self.image, YELLOW, self.image.get_rect())
        pygame.draw.ellipse(self.image, ORANGE, self.image.get_rect().inflate(-4,-2))
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction
        self.speed = PROJECTILE_SPEED * self.direction
        self.damage = 20

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0 or self.rect.left > WIDTH:
            self.kill()

class Enemy(pygame.sprite.Sprite):
    def __init__(self, x, enemy_type="basic"):
        super().__init__()
        self.enemy_type = enemy_type

        if enemy_type == "basic":
            self.image = pygame.Surface((35, 35), pygame.SRCALPHA)
            self.image.fill((0,0,0,0))
            pygame.draw.polygon(self.image, RED, [(17, 2), (33, 33), (2, 33)])
            self.max_health = 20; self.speed = 2; self.damage = 15; self.points = 10
        elif enemy_type == "fast":
            self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
            self.image.fill((0,0,0,0))
            pygame.draw.polygon(self.image, ORANGE, [(15,0), (30,15), (15,30), (0,15)])
            self.max_health = 15; self.speed = 4; self.damage = 10; self.points = 15
        elif enemy_type == "tank":
            self.image = pygame.Surface((45, 45), pygame.SRCALPHA)
            self.image.fill((0,0,0,0))
            pygame.draw.rect(self.image, DARK_RED, (0,0,45,45), border_radius=8)
            pygame.draw.rect(self.image, GRAY, (5,5,35,35), border_radius=5)
            self.max_health = 50; self.speed = 1; self.damage = 25; self.points = 25

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = GROUND_Y
        self.health = self.max_health

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0:
            self.kill()

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill()
            return True
        return False

class Boss(pygame.sprite.Sprite):
    def __init__(self, x):
        super().__init__()
        self.image = pygame.Surface((80, 80), pygame.SRCALPHA)
        self.image.fill((0,0,0,0))
        pygame.draw.ellipse(self.image, PURPLE, (0, 10, 80, 70))
        pygame.draw.circle(self.image, YELLOW, (40, 45), 12)
        pygame.draw.circle(self.image, RED, (40, 45), 7)
        pygame.draw.polygon(self.image, DARK_RED, [(20,10), (10,0), (30,20)])
        pygame.draw.polygon(self.image, DARK_RED, [(60,10), (70,0), (50,20)])
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = GROUND_Y
        self.max_health = 150; self.health = self.max_health
        self.speed = 1.5; self.damage = 30; self.points = 100
        self.direction = -1; self.shoot_timer = 0; self.move_timer = 0

    def update(self):
        self.move_timer += 1
        if self.move_timer > 120:
            self.direction *= -1; self.move_timer = 0
        self.rect.x += self.speed * self.direction
        if self.rect.left < WIDTH // 2: self.rect.left = WIDTH // 2; self.direction = 1
        elif self.rect.right > WIDTH: self.rect.right = WIDTH; self.direction = -1
        self.shoot_timer += 1
        if self.shoot_timer > 90:
            self.shoot_timer = 0
            return self.shoot()
        return None

    def shoot(self):
        return EnemyProjectile(self.rect.centerx, self.rect.centery)

    def take_damage(self, damage):
        self.health -= damage
        if self.health <= 0:
            self.kill(); return True
        return False

class EnemyProjectile(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((12, 12), pygame.SRCALPHA)
        self.image.fill((0,0,0,0))
        pygame.draw.circle(self.image, DARK_RED, (6,6), 6)
        pygame.draw.line(self.image, PURPLE, (6,0), (6,12), 2)
        pygame.draw.line(self.image, PURPLE, (0,6), (12,6), 2)
        pygame.draw.line(self.image, PURPLE, (2,2), (10,10), 2)
        pygame.draw.line(self.image, PURPLE, (2,10), (10,2), 2)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = -8; self.damage = 20

    def update(self):
        self.rect.x += self.speed
        if self.rect.right < 0: self.kill()

class Collectible(pygame.sprite.Sprite):
    def __init__(self, x, collectible_type):
        super().__init__()
        self.collectible_type = collectible_type
        item_y_offset = 20

        if collectible_type == "health":
            self.image = pygame.Surface((25, 25), pygame.SRCALPHA); self.image.fill((0,0,0,0))
            pygame.draw.circle(self.image, GREEN, (8, 9), 7)
            pygame.draw.circle(self.image, GREEN, (17, 9), 7)
            pygame.draw.polygon(self.image, GREEN, [(1, 10), (24, 10), (12.5, 24)])
            self.value = 30; self.points = 5
        elif collectible_type == "life":
            self.image = pygame.Surface((25, 25), pygame.SRCALPHA); self.image.fill((0,0,0,0))
            cx, cy, o_rad, i_rad, n_pts = 12.5, 12.5, 12, 5, 5; pts = []
            for i in range(n_pts * 2):
                rad = o_rad if i % 2 == 0 else i_rad
                ang = (i / (n_pts * 2)) * (2 * math.pi) - math.pi / 2
                pts.append((cx + rad * math.cos(ang), cy + rad * math.sin(ang)))
            pygame.draw.polygon(self.image, BLUE, pts)
            self.value = 1; self.points = 20
        elif collectible_type == "points":
            self.image = pygame.Surface((20, 20), pygame.SRCALPHA); self.image.fill((0,0,0,0))
            pygame.draw.circle(self.image, YELLOW, (10, 10), 10)
            pygame.draw.circle(self.image, ORANGE, (10, 10), 7)
            p_font = pygame.font.SysFont("Arial", 12, bold=True)
            txt = p_font.render("$", True, BLACK)
            self.image.blit(txt, (10 - txt.get_width()//2, 10 - txt.get_height()//2))
            self.value = 50; self.points = 0

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.bottom = GROUND_Y - item_y_offset
        self.speed = 2 # Collectibles scroll left

    def update(self):
        self.rect.x -= self.speed
        if self.rect.right < 0: self.kill()

class Game:
    def __init__(self):
        self.reset_game()

    def reset_game(self):
        self.all_sprites = pygame.sprite.Group()
        self.enemies = pygame.sprite.Group()
        self.projectiles = pygame.sprite.Group()
        self.enemy_projectiles = pygame.sprite.Group()
        self.collectibles = pygame.sprite.Group()
        self.bosses = pygame.sprite.Group()

        self.player = Player()
        self.all_sprites.add(self.player)

        self.level = 1
        self.max_level = 3
        self.level_complete = False # This flag is important
        self.game_over_active = False # To prevent multiple game over screens

        self.start_level() # This will also set spawn timers etc.

    def start_level(self):
        self.spawn_timer = 0
        self.enemies_spawned = 0
        self.level_complete = False # Reset for the new level
        self.boss_spawned = False

        # Clear only relevant groups, player persists
        for group in [self.enemies, self.projectiles, self.enemy_projectiles, self.collectibles, self.bosses]:
            for sprite in group:
                sprite.kill()

        self.player.rect.x = 100
        self.player.rect.bottom = GROUND_Y
        if self.player.lives > 0 : # Only restore health if player is alive (not after game over restart)
             self.player.health = self.player.max_health
        self.player.vel_y = 0
        self.player.on_ground = True
        self.player.invulnerable = False # Reset invulnerability

        self.spawn_collectibles()
        if self.level > 1 or (self.level == 1 and self.player.score == 0): # Avoid transition for initial game start
            self.show_level_transition_screen(f"Level {self.level}")


    def spawn_enemies(self):
        if self.level == 3 and self.boss_spawned: return
        if self.enemies_spawned >= [15, 25, 20][self.level - 1]: return

        self.spawn_timer += 1
        spawn_rate = max(90 - (self.level * 15), 45)
        if self.spawn_timer >= spawn_rate:
            self.spawn_timer = 0
            types = [["basic"], ["basic", "fast"], ["basic", "fast", "tank"]][self.level-1]
            enemy = Enemy(WIDTH + random.randint(50, 200), random.choice(types))
            self.all_sprites.add(enemy); self.enemies.add(enemy)
            self.enemies_spawned += 1

    def spawn_boss(self):
        if self.level == 3 and not self.boss_spawned and \
           self.enemies_spawned >= [15,25,20][self.level-1] and len(self.enemies) == 0:
            boss = Boss(WIDTH - 150)
            self.all_sprites.add(boss); self.bosses.add(boss)
            self.boss_spawned = True

    def spawn_collectibles(self):
        types = ["health", "points"] + (["life"] if self.level > 1 else [])
        num_spawn = self.level * 2 + 1
        for i in range(num_spawn):
            x_pos = WIDTH + random.randint(200,1000) + i * (WIDTH / num_spawn)
            coll = Collectible(x_pos, random.choice(types))
            self.all_sprites.add(coll); self.collectibles.add(coll)

    def check_level_complete(self):
        if self.level_complete: return # Already completed, do nothing

        max_enemies_for_level = [15, 25, 20][self.level - 1]
        if self.level < self.max_level:
            if self.enemies_spawned >= max_enemies_for_level and len(self.enemies) == 0:
                self.level_complete = True
        else: # Max level
            if self.boss_spawned and len(self.bosses) == 0:
                self.level_complete = True

    def advance_level(self):
        if self.level < self.max_level:
            self.level += 1
            self.start_level() # This will show transition screen
        else:
            self.show_victory_screen() # This will loop until R or Q

    def show_level_transition_screen(self, message):
        screen.fill(BLACK)
        text = font_large.render(message, True, WHITE)
        screen.blit(text, (WIDTH//2 - text.get_width()//2, HEIGHT//2 - text.get_height()//2))
        pygame.display.flip()
        pygame.time.wait(2000)

    def handle_collisions(self):
        for proj in self.projectiles:
            hits_e = pygame.sprite.spritecollide(proj, self.enemies, False)
            for e in hits_e:
                if e.take_damage(proj.damage): self.player.add_score(e.points)
                proj.kill()
            hits_b = pygame.sprite.spritecollide(proj, self.bosses, False)
            for b in hits_b:
                if b.take_damage(proj.damage): self.player.add_score(b.points)
                proj.kill()

        collected = pygame.sprite.spritecollide(self.player, self.collectibles, True)
        for item in collected:
            if item.collectible_type == "health": self.player.heal(item.value)
            elif item.collectible_type == "life": self.player.add_life()
            elif item.collectible_type == "points": self.player.add_score(item.value)
            self.player.add_score(item.points)

        if not self.player.invulnerable:
            if pygame.sprite.spritecollide(self.player, self.enemies, False, pygame.sprite.collide_mask) or \
               pygame.sprite.spritecollide(self.player, self.bosses, False, pygame.sprite.collide_mask):
                # Determine damage based on what was hit (simplified here)
                # For simplicity, assume any enemy/boss collision does some base damage
                # A more robust way would be to check which enemy specifically.
                collided_with = pygame.sprite.spritecollide(self.player, self.enemies, False)
                if not collided_with:
                    collided_with = pygame.sprite.spritecollide(self.player, self.bosses, False)

                if collided_with:
                    self.player.take_damage(collided_with[0].damage)


            hit_by_ep = pygame.sprite.spritecollide(self.player, self.enemy_projectiles, True, pygame.sprite.collide_mask)
            for ep in hit_by_ep:
                self.player.take_damage(ep.damage)

    def update(self):
        if self.player.lives <= 0 and not self.game_over_active: # Check for game over condition
            return # Stop updates if game over is about to be handled by main loop

        self.all_sprites.update()

        if not self.level_complete:
            self.spawn_enemies()
            self.spawn_boss()

        for boss in self.bosses:
            new_proj = boss.update() # Boss update might return projectile
            if new_proj:
                self.all_sprites.add(new_proj); self.enemy_projectiles.add(new_proj)

        self.handle_collisions()
        self.check_level_complete()

        if self.level_complete:
            # Check if we are on the final level and boss is defeated
            if self.level == self.max_level and self.boss_spawned and len(self.bosses) == 0:
                if not self.game_over_active: # Ensure victory screen isn't called multiple times
                    self.show_victory_screen()
            elif self.level < self.max_level :
                 self.advance_level() # This will set level_complete to False for the new level


    def draw_ui(self, screen_surface):
        hp_w, hp_h = 200, 20
        hp_r = max(0, self.player.health / self.player.max_health)
        pygame.draw.rect(screen_surface, RED, (10,10,hp_w,hp_h))
        pygame.draw.rect(screen_surface, GREEN, (10,10,hp_w*hp_r,hp_h))
        pygame.draw.rect(screen_surface, BLACK, (10,10,hp_w,hp_h), 2)

        if len(self.bosses) > 0:
            boss = list(self.bosses)[0]
            b_hp_r = max(0, boss.health / boss.max_health)
            b_bar_y = 40
            pygame.draw.rect(screen_surface, DARK_RED, (10,b_bar_y,hp_w,hp_h))
            pygame.draw.rect(screen_surface, RED, (10,b_bar_y,hp_w*b_hp_r,hp_h))
            pygame.draw.rect(screen_surface, BLACK, (10,b_bar_y,hp_w,hp_h), 2)
            b_txt = font_small.render("BOSS", True, BLACK)
            screen_surface.blit(b_txt, (220, b_bar_y+2))

        s_txt = font_medium.render(f"Score: {self.player.score}", True, BLACK)
        screen_surface.blit(s_txt, (WIDTH - 200, 10))
        l_txt = font_medium.render(f"Lives: {self.player.lives}", True, BLACK)
        screen_surface.blit(l_txt, (WIDTH - 200, 40))
        lvl_txt = font_medium.render(f"Level: {self.level}", True, BLACK)
        screen_surface.blit(lvl_txt, (WIDTH - 200, 70))

        ctrl_y = HEIGHT - 90
        ctrls = ["Arrows/WASD: Move", "Space/Up/W: Jump", "F: Shoot"]
        for i, c in enumerate(ctrls):
            c_txt = font_small.render(c, True, BLACK)
            screen_surface.blit(c_txt, (10, ctrl_y + i * 20))

    def _wait_for_restart_or_quit(self):
        waiting = True
        while waiting:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit(); exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r:
                        self.reset_game() # This will call start_level()
                        self.game_over_active = False
                        waiting = False
                    elif event.key == pygame.K_q:
                        pygame.quit(); exit()
            clock.tick(FPS)

    def show_victory_screen(self):
        self.game_over_active = True # Use this to control game flow
        screen.fill(DARK_GREEN)
        vic_txt = font_large.render("CONGRATULATIONS! YOU WON!", True, YELLOW)
        screen.blit(vic_txt, (WIDTH//2 - vic_txt.get_width()//2, HEIGHT//2 - 100))
        scr_txt = font_medium.render(f"Final Score: {self.player.score}", True, WHITE)
        screen.blit(scr_txt, (WIDTH//2 - scr_txt.get_width()//2, HEIGHT//2 - 40))
        rst_txt = font_medium.render("Press R to Restart or Q to Quit", True, WHITE)
        screen.blit(rst_txt, (WIDTH//2 - rst_txt.get_width()//2, HEIGHT//2 + 20))
        pygame.display.flip()
        self._wait_for_restart_or_quit()

def game_over_screen_display(game_instance):
    game_instance.game_over_active = True # Signal that game over is active
    screen.fill(BLACK)
    go_txt = font_large.render("GAME OVER", True, RED)
    screen.blit(go_txt, (WIDTH//2 - go_txt.get_width()//2, HEIGHT//2 - 120))
    scr_txt = font_medium.render(f"Final Score: {game_instance.player.score}", True, WHITE)
    screen.blit(scr_txt, (WIDTH//2 - scr_txt.get_width()//2, HEIGHT//2 - 60))
    lvl_txt = font_medium.render(f"Reached Level: {game_instance.level}", True, WHITE)
    screen.blit(lvl_txt, (WIDTH//2 - lvl_txt.get_width()//2, HEIGHT//2 - 20))
    rst_txt = font_medium.render("Press R to Restart or Q to Quit", True, WHITE)
    screen.blit(rst_txt, (WIDTH//2 - rst_txt.get_width()//2, HEIGHT//2 + 40))
    pygame.display.flip()
    game_instance._wait_for_restart_or_quit()


def main():
    game = Game()
    running = True

    while running:
        clock.tick(FPS)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    if game.player.lives > 0 and not game.game_over_active:
                        proj = game.player.shoot()
                        game.all_sprites.add(proj); game.projectiles.add(proj)
                elif event.key == pygame.K_ESCAPE:
                    running = False

        if game.player.lives <= 0 and not game.game_over_active:
            game_over_screen_display(game)
            # If _wait_for_restart_or_quit exited due to 'R', game is reset.
            # If it exited due to 'Q', program is terminated.
            # No need to set running = False here as _wait_for_restart_or_quit handles exit.
            if game.player.lives <=0: # If quit was chosen, this ensures loop terminates
                running = False
                continue


        if not game.game_over_active : # Only update and draw if game is not in a "waiting" state
            game.update()

            screen.fill(SKY_BLUE)
            pygame.draw.rect(screen, DARK_GREEN, (0, GROUND_Y, WIDTH, HEIGHT - GROUND_Y))
            pygame.draw.line(screen, GREEN, (0, GROUND_Y), (WIDTH, GROUND_Y), 3)

            for entity in game.all_sprites:
                if entity == game.player and game.player.invulnerable:
                    if game.player.invulnerable_timer % 12 < 6: # Blink effect
                        continue
                screen.blit(entity.image, entity.rect)

            if game.player.lives > 0: # Only draw UI if player is "active"
                game.draw_ui(screen)

        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()