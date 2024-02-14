# Galaxy Explorer version 1.1.1 Full Version
# Update: now characters have their own icons!!!
# In this game, you as an explorer in the vastness of space.
# Navigating through galaxies, fighting off pirates and monsters.
# Use your spaceship to dodge enemies and collect fuel and repair kits to stay alive.
# Control your ship with WASD keys for movement and use the mouse to aim and shoot at enemies.

import pygame
import random
import math

# Pygame initialization
pygame.init()

icon = pygame.image.load('GameMedia/icon.png')  # Load icon
pygame.display.set_icon(icon)  # Load icon

pirate_bullets = pygame.sprite.Group()
pygame.mixer.init()

# Game Window Size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Galaxy Explorer")

# Game Music
pygame.mixer.music.load('GameMedia/GalaxyExplorer.mp3')  # Background music
pygame.mixer.music.play(-1)  # Music Loop
shoot_sound = pygame.mixer.Sound('GameMedia/GalaxyExplorer_Fire.mp3')  # Player Shoot SFX
damage_sound = pygame.mixer.Sound('GameMedia/GalaxyExplorer_TakeDamage.mp3')  # Player Damage SFX

# Color setting
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
BLUE = (0, 0, 255)
PURPLE = (128, 0, 128)

# Game Clock
clock = pygame.time.Clock()

# FPS
FPS = 60

def Game_Loop():
    pygame.init()
    class Player(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            self.image = pygame.Surface((40, 40))
            original_image = pygame.image.load('GameMedia/ship.png')  # Load player icon
            self.image = pygame.transform.scale(original_image, (40, 40))  # Resize image to fit 30x30 pixels
            self.rect = self.image.get_rect(center=(screen_width / 2, screen_height / 2))
            self.hp = 70
            self.fuel = 50  # Default fuel value
            self.score = 0
            self.shoot_delay = 400  # milliseconds default:400
            self.last_shot = pygame.time.get_ticks()
            self.fuel_decrease_timer = pygame.time.get_ticks()  # Fuel decrease timer

        def update(self):
            keys = pygame.key.get_pressed()
            if keys[pygame.K_a]:
                self.rect.x -= 5
            if keys[pygame.K_d]:
                self.rect.x += 5
            if keys[pygame.K_w]:
                self.rect.y -= 5
            if keys[pygame.K_s]:
                self.rect.y += 5

            self.rect.x = max(0, min(screen_width - self.rect.width, self.rect.x))
            self.rect.y = max(0, min(screen_height - self.rect.height, self.rect.y))

            # Fuel decrease timer
            if pygame.time.get_ticks() - self.fuel_decrease_timer > 30000:  # Every 30 seconds
                self.fuel -= 10  # Fuel decrease by 10
                if self.fuel < 0:  # Fuel doesnt go to negative (Unused)
                    self.fuel = 0
                self.fuel_decrease_timer = pygame.time.get_ticks()  # Timer reset

            # Bullet direction by mouse
            now = pygame.time.get_ticks()
            if pygame.mouse.get_pressed()[0] and now - self.last_shot > self.shoot_delay:
                self.shoot()
                self.last_shot = now

        def shoot(self):
            mouse_x, mouse_y = pygame.mouse.get_pos()
            rel_x, rel_y = mouse_x - self.rect.centerx, mouse_y - self.rect.centery
            angle = math.atan2(rel_y, rel_x)
            angle_degrees = math.degrees(angle)
            bullet = Bullet(self.rect.centerx, self.rect.centery, angle_degrees)
            all_sprites.add(bullet)
            bullets.add(bullet)
            shoot_sound.play()

    class PirateBullet(pygame.sprite.Sprite):
        def __init__(self, x, y, target_x, target_y):
            super().__init__()
            self.image = pygame.Surface((5, 10))
            self.image.fill((255, 105, 180))  # Pink
            self.rect = self.image.get_rect(center=(x, y))
            self.speed = 3
            # Calculate bullet speed
            dx, dy = target_x - x, target_y - y
            dist = math.hypot(dx, dy)
            self.dx = dx / dist * self.speed
            self.dy = dy / dist * self.speed

        def update(self):
            self.rect.x += self.dx
            self.rect.y += self.dy
            # Clear bullets out of window
            if self.rect.right < 0 or self.rect.left > screen_width or self.rect.bottom < 0 or self.rect.top > screen_height:
                self.kill()


    class Bullet(pygame.sprite.Sprite):
        def __init__(self, x, y, angle):
            super().__init__()
            self.image = pygame.Surface((5, 10))
            self.image.fill(GREEN)
            self.rect = self.image.get_rect(center=(x, y))
            self.speed = 10
            # Calculate bullet speed
            self.vx = self.speed * math.cos(math.radians(angle))
            self.vy = self.speed * math.sin(math.radians(angle))

        def update(self):
            self.rect.x += self.vx
            self.rect.y += self.vy
            # Clear bullets out of window
            if self.rect.right < 0 or self.rect.left > screen_width or self.rect.bottom < 0 or self.rect.top > screen_height:
                self.kill()

    class Enemy(pygame.sprite.Sprite):
        def __init__(self, x, y, type):
            super().__init__()
            self.type = type
            if self.type == "monster":
                original_image = pygame.image.load('GameMedia/monster.png').convert_alpha()  # Load original image for monster

            elif self.type == "pirate":
                original_image = pygame.image.load('GameMedia/pirate.png').convert_alpha()  # Load original image for pirate

                self.shoot_delay = 2000  # Pirate attack delay  (ms)
                self.last_shot = pygame.time.get_ticks()
            self.image = pygame.transform.scale(original_image, (40, 40))  # Resize image to fit 30x30 pixels
            self.rect = self.image.get_rect(center=(x, y))
            self.hp = 20 if self.type == "monster" else 50

        def update(self):
            if self.type == "pirate":
                now = pygame.time.get_ticks()
                if now - self.last_shot > self.shoot_delay:
                    self.shoot()
                    self.last_shot = now

        def shoot(self):
            bullet = PirateBullet(self.rect.centerx, self.rect.centery, player.rect.centerx, player.rect.centery)
            all_sprites.add(bullet)
            pirate_bullets.add(bullet)



    class Item(pygame.sprite.Sprite):
        def __init__(self, x, y, type):
            super().__init__()
            self.type = type
            if self.type == "fuel":
                self.image = pygame.Surface((10, 10))
                self.image.fill(YELLOW)
            elif self.type == "repair":
                self.image = pygame.Surface((10, 10))
                self.image.fill(RED)
            self.rect = self.image.get_rect(center=(x, y))

    class Portal(pygame.sprite.Sprite):
        def __init__(self):
            super().__init__()
            # self.image = pygame.Surface((60, 60))
            # self.image.fill(BLUE)
            original_image = pygame.image.load('GameMedia/portal.png').convert_alpha()  # Load original image for monster
            self.image = pygame.transform.scale(original_image, (100, 100))  # Resize image to fit 30x30 pixels
            self.rect = self.image.get_rect(center=(random.randint(0, screen_width), random.randint(0, screen_height)))
            self.item_spawn_timer = random.randint(20, 60)  # Increase spawn time
            self.items_spawned = 0

        def update(self):
            self.item_spawn_timer -= 1
            if self.item_spawn_timer <= 0:
                self.spawn_item_or_enemy()
                self.item_spawn_timer = random.randint(20, 60)  # Increase timer for next item/enemy
                self.items_spawned += 1
                if self.items_spawned >= 2:  # After spawning 2 items/enemies, planet disappears
                    self.kill()

        def spawn_item_or_enemy(self):
            # Spawning offset range
            offset_range = 20  # Offset by 20 pixels

            # Calculate the final cord
            offset_x = random.randint(-offset_range, offset_range)
            offset_y = random.randint(-offset_range, offset_range)

            # Item generate rate with 10%，Enemy generate rate with 90%
            if random.randint(1, 100) <= 10:  # 10% Item
                item_or_enemy = "item"
            else:  # 90% Enemy
                item_or_enemy = "enemy"

            if item_or_enemy == "item":
                new_item = Item(self.rect.centerx + offset_x, self.rect.centery + offset_y,
                                random.choice(["fuel", "repair"]))
                all_sprites.add(new_item)
                items.add(new_item)
            else:  # Enemy Spawn
                new_enemy = Enemy(self.rect.centerx + offset_x, self.rect.centery + offset_y,
                                  random.choice(["monster", "pirate"]))
                all_sprites.add(new_enemy)
                enemies.add(new_enemy)

    # Sprites
    all_sprites = pygame.sprite.Group()
    bullets = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    items = pygame.sprite.Group()
    planets = pygame.sprite.Group()

    player = Player()
    all_sprites.add(player)

    # Game Loop
    running = True
    game_over = False  # Track if the game ends
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        if not game_over:
            # Plannet spawning rate
            if random.randint(1, 150) > 148:
                planet = Portal()
                all_sprites.add(planet)
                planets.add(planet)

            # Refresh all sprites
            all_sprites.update()
            pirate_bullets.update()

            # Player enemy hitbox detection
            enemy_hits = pygame.sprite.spritecollide(player, enemies, False)
            for enemy in enemy_hits:
                player.hp -= 5  # If hit then cause a 5 dmg on player
                enemy.kill()  # Kill the enemy after hit
                damage_sound.play()

            # Pirate bullet hitbox detection
            bullet_hits = pygame.sprite.spritecollide(player, pirate_bullets, True)
            for hit in bullet_hits:
                player.hp -= 10  # If hit then cause a 10 dmg on player
                damage_sound.play()

            # Player bullet hitbox detection
            hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
            for hit in hits:
                player.score += 20 if hit.type == "monster" else 50

            # Player & Item hitbox detection
            items_hit = pygame.sprite.spritecollide(player, items, True)
            for item in items_hit:
                if item.type == "fuel":
                    player.fuel = min(100, player.fuel + 10)
                elif item.type == "repair":
                    player.hp = min(100, player.hp + 10)

            # Game Over
            if player.hp <= 0 or player.fuel <= 0:
                game_over = True

        # Screen fill
        screen.fill(BLACK)

        if not game_over:
            # Draw all sprites and UI
            all_sprites.draw(screen)
            pirate_bullets.draw(screen)

            hp_text = pygame.font.SysFont(None, 24).render(f'HP: {player.hp}', True, WHITE)
            fuel_text = pygame.font.SysFont(None, 24).render(f'Fuel: {player.fuel}', True, WHITE)
            score_text = pygame.font.SysFont(None, 24).render(f'Score: {player.score}', True, WHITE)
            screen.blit(hp_text, (10, 10))
            screen.blit(fuel_text, (10, 30))
            screen.blit(score_text, (10, 50))
        else:
            # Game over window
            font = pygame.font.SysFont(None, 55)
            lose_text = font.render('Game Over', True, RED)
            score_text = font.render(f'Your Score: {player.score}', True, WHITE)
            screen.blit(lose_text, (screen_width/2 - lose_text.get_width()/2, screen_height/2 - lose_text.get_height()/2))
            screen.blit(score_text, (screen_width/2 - score_text.get_width()/2, screen_height/2 + 50))

        # Screen display
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

Game_Loop()