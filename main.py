"""
Hero's Destiny - A 2D Action Game
A polished arcade-style battle game where the player survives waves of enemies.
"""

import pygame
import random
import math

# Initialize pygame
pygame.init()

# Try to initialize mixer (may fail in headless environments like Replit)
try:
    pygame.mixer.init()
except:
    print("Audio not available - running in headless mode")

# ==================== CONSTANTS ====================
# Screen settings
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (220, 50, 50)
GREEN = (50, 220, 50)
BLUE = (50, 150, 220)
YELLOW = (255, 220, 50)
ORANGE = (255, 150, 50)
PURPLE = (180, 50, 220)
DARK_RED = (150, 30, 30)
DARK_GREEN = (30, 150, 30)
DARK_BLUE = (30, 90, 150)
GRAY = (100, 100, 100)
LIGHT_GRAY = (200, 200, 200)

# Game physics
GRAVITY = 0.8
GROUND_LEVEL = 500
PLAYER_SPEED = 6
JUMP_STRENGTH = 15
MAX_FALL_SPEED = 20

# Combat settings
PLAYER_MAX_HEALTH = 100
PLAYER_ATTACK_RANGE = 80
PLAYER_ATTACK_DURATION = 15
PROJECTILE_SPEED = 10
PROJECTILE_DAMAGE = 25
MELEE_DAMAGE = 50

# Enemy settings
ENEMY_BASE_SPEED = 2
ENEMY_BASE_HEALTH = 50
SPAWN_INTERVAL = 120  # frames
MIN_SPAWN_INTERVAL = 30

# Difficulty scaling
DIFFICULTY_INCREASE_RATE = 0.02
SPEED_INCREASE_PER_SCORE = 0.05

# ==================== PARTICLE CLASS ====================
class Particle:
    """Visual effect particles for attacks and hits"""
    def __init__(self, x, y, color, velocity_x=0, velocity_y=0, lifetime=30):
        self.x = x
        self.y = y
        self.color = color
        self.velocity_x = velocity_x + random.uniform(-2, 2)
        self.velocity_y = velocity_y + random.uniform(-3, -1)
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.size = random.randint(3, 7)
    
    def update(self):
        """Update particle position and lifetime"""
        self.x += self.velocity_x
        self.y += self.velocity_y
        self.velocity_y += 0.3  # Gravity effect
        self.lifetime -= 1
        return self.lifetime > 0
    
    def draw(self, screen):
        """Draw particle with fade effect"""
        alpha_factor = self.lifetime / self.max_lifetime
        size = max(1, int(self.size * alpha_factor))
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), size)


# ==================== PROJECTILE CLASS ====================
class Projectile:
    """Energy blast projectile fired by player"""
    def __init__(self, x, y, direction):
        self.x = x
        self.y = y
        self.direction = direction  # -1 for left, 1 for right
        self.width = 12
        self.height = 8
        self.speed = PROJECTILE_SPEED
        self.damage = PROJECTILE_DAMAGE
        self.active = True
        self.trail_particles = []
    
    def update(self, particles):
        """Update projectile position"""
        self.x += self.speed * self.direction
        
        # Add trail particles
        if random.random() < 0.5:
            particle = Particle(self.x, self.y, YELLOW, velocity_x=-self.direction * 2, lifetime=15)
            particles.append(particle)
        
        # Deactivate if off screen
        if self.x < -20 or self.x > SCREEN_WIDTH + 20:
            self.active = False
    
    def draw(self, screen):
        """Draw the energy blast"""
        # Draw outer glow
        pygame.draw.ellipse(screen, YELLOW, 
                          (self.x - self.width//2 - 2, self.y - self.height//2 - 2, 
                           self.width + 4, self.height + 4))
        # Draw core
        pygame.draw.ellipse(screen, WHITE, 
                          (self.x - self.width//2, self.y - self.height//2, 
                           self.width, self.height))
    
    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x - self.width//2, self.y - self.height//2, 
                          self.width, self.height)


# ==================== PLAYER CLASS ====================
class Player:
    """The hero character controlled by the player"""
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.width = 40
        self.height = 60
        self.velocity_x = 0
        self.velocity_y = 0
        self.on_ground = False
        self.facing_right = True
        
        # Combat stats
        self.health = PLAYER_MAX_HEALTH
        self.max_health = PLAYER_MAX_HEALTH
        self.attacking = False
        self.attack_timer = 0
        self.attack_cooldown = 0
        self.last_attack_type = None  # 'melee' or 'ranged'
        
        # Animation
        self.animation_frame = 0
        self.hit_flash = 0
    
    def handle_input(self, keys):
        """Handle player keyboard input"""
        # Horizontal movement
        self.velocity_x = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.velocity_x = -PLAYER_SPEED
            self.facing_right = False
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.velocity_x = PLAYER_SPEED
            self.facing_right = True
        
        # Jumping
        if (keys[pygame.K_UP] or keys[pygame.K_w]) and self.on_ground:
            self.velocity_y = -JUMP_STRENGTH
            self.on_ground = False
    
    def attack(self, attack_type='melee'):
        """Initiate an attack"""
        if self.attack_cooldown <= 0:
            self.attacking = True
            self.attack_timer = PLAYER_ATTACK_DURATION
            self.attack_cooldown = 30
            self.last_attack_type = attack_type
            return True
        return False
    
    def update(self, particles):
        """Update player physics and state"""
        # Apply gravity
        self.velocity_y += GRAVITY
        if self.velocity_y > MAX_FALL_SPEED:
            self.velocity_y = MAX_FALL_SPEED
        
        # Update position
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # Ground collision
        if self.y + self.height >= GROUND_LEVEL:
            self.y = GROUND_LEVEL - self.height
            self.velocity_y = 0
            self.on_ground = True
        else:
            self.on_ground = False
        
        # Screen boundaries
        if self.x < 0:
            self.x = 0
        if self.x + self.width > SCREEN_WIDTH:
            self.x = SCREEN_WIDTH - self.width
        
        # Update attack timers
        if self.attack_timer > 0:
            self.attack_timer -= 1
            if self.attack_timer == 0:
                self.attacking = False
        
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
        
        # Update hit flash
        if self.hit_flash > 0:
            self.hit_flash -= 1
        
        # Animation
        self.animation_frame = (self.animation_frame + 1) % 60
    
    def take_damage(self, damage, particles):
        """Player takes damage"""
        self.health -= damage
        self.hit_flash = 10
        
        # Create damage particles
        for _ in range(15):
            particle = Particle(self.x + self.width//2, self.y + self.height//2, 
                              RED, velocity_y=-5)
            particles.append(particle)
        
        if self.health < 0:
            self.health = 0
    
    def draw(self, screen):
        """Draw the player character"""
        # Flash red when hit
        color = RED if self.hit_flash > 0 and self.hit_flash % 4 < 2 else BLUE
        
        # Draw player body
        body_rect = pygame.Rect(self.x, self.y + 15, self.width, self.height - 15)
        pygame.draw.rect(screen, color, body_rect)
        pygame.draw.rect(screen, DARK_BLUE, body_rect, 2)
        
        # Draw head
        head_x = self.x + self.width // 2
        head_y = self.y + 10
        pygame.draw.circle(screen, color, (head_x, head_y), 12)
        pygame.draw.circle(screen, DARK_BLUE, (head_x, head_y), 12, 2)
        
        # Draw attack indicator
        if self.attacking:
            attack_color = YELLOW if self.last_attack_type == 'ranged' else ORANGE
            offset = 25 if self.facing_right else -25
            attack_x = self.x + self.width // 2 + offset
            attack_y = self.y + self.height // 2
            
            if self.last_attack_type == 'melee':
                # Draw sword slash arc
                points = []
                for angle in range(-30, 60, 10):
                    rad = math.radians(angle if self.facing_right else 180 - angle)
                    px = attack_x + math.cos(rad) * 30
                    py = attack_y + math.sin(rad) * 30
                    points.append((px, py))
                if len(points) > 1:
                    pygame.draw.lines(screen, attack_color, False, points, 4)
    
    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)
    
    def get_attack_rect(self):
        """Get attack hitbox for melee attacks"""
        if self.attacking and self.last_attack_type == 'melee':
            offset = PLAYER_ATTACK_RANGE if self.facing_right else -PLAYER_ATTACK_RANGE
            return pygame.Rect(self.x + self.width // 2 + offset - 30, 
                             self.y, 60, self.height)
        return None


# ==================== ENEMY CLASS ====================
class Enemy:
    """Enemy that moves toward the player"""
    def __init__(self, x, y, enemy_type='normal', difficulty_multiplier=1.0):
        self.x = x
        self.y = y
        self.width = 35
        self.height = 50
        self.type = enemy_type
        self.velocity_y = 0
        self.on_ground = False
        
        # Type-specific stats
        if enemy_type == 'fast':
            self.speed = (ENEMY_BASE_SPEED + 2) * difficulty_multiplier
            self.health = 30
            self.max_health = 30
            self.color = ORANGE
            self.damage = 15
            self.width = 30
            self.height = 45
        elif enemy_type == 'tank':
            self.speed = (ENEMY_BASE_SPEED - 1) * difficulty_multiplier
            self.health = 100
            self.max_health = 100
            self.color = PURPLE
            self.damage = 30
            self.width = 45
            self.height = 55
        else:  # normal
            self.speed = ENEMY_BASE_SPEED * difficulty_multiplier
            self.health = ENEMY_BASE_HEALTH
            self.max_health = ENEMY_BASE_HEALTH
            self.color = RED
            self.damage = 20
        
        self.active = True
        self.hit_flash = 0
        self.attack_cooldown = 0
    
    def update(self, player_x, player_y):
        """Update enemy AI and movement"""
        # Move toward player
        if self.x < player_x:
            self.x += self.speed
        elif self.x > player_x:
            self.x -= self.speed
        
        # Apply gravity
        self.velocity_y += GRAVITY
        if self.velocity_y > MAX_FALL_SPEED:
            self.velocity_y = MAX_FALL_SPEED
        
        self.y += self.velocity_y
        
        # Ground collision
        if self.y + self.height >= GROUND_LEVEL:
            self.y = GROUND_LEVEL - self.height
            self.velocity_y = 0
            self.on_ground = True
        
        # Update timers
        if self.hit_flash > 0:
            self.hit_flash -= 1
        if self.attack_cooldown > 0:
            self.attack_cooldown -= 1
    
    def take_damage(self, damage, particles):
        """Enemy takes damage"""
        self.health -= damage
        self.hit_flash = 8
        
        # Create hit particles
        for _ in range(8):
            particle = Particle(self.x + self.width//2, self.y + self.height//2, 
                              self.color, velocity_y=-3)
            particles.append(particle)
        
        if self.health <= 0:
            self.active = False
            # Create death particles
            for _ in range(20):
                particle = Particle(self.x + self.width//2, self.y + self.height//2, 
                                  self.color, 
                                  velocity_x=random.uniform(-4, 4),
                                  velocity_y=random.uniform(-6, -2))
                particles.append(particle)
    
    def can_attack_player(self, player_rect):
        """Check if enemy can attack player"""
        if self.attack_cooldown <= 0:
            enemy_rect = self.get_rect()
            if enemy_rect.colliderect(player_rect):
                self.attack_cooldown = 60
                return True
        return False
    
    def draw(self, screen):
        """Draw the enemy"""
        # Flash white when hit
        if self.hit_flash > 0 and self.hit_flash % 4 < 2:
            color = WHITE
        else:
            color = self.color
        
        # Draw enemy body
        body_rect = pygame.Rect(self.x, self.y + 10, self.width, self.height - 10)
        pygame.draw.rect(screen, color, body_rect)
        pygame.draw.rect(screen, BLACK, body_rect, 2)
        
        # Draw head
        head_x = self.x + self.width // 2
        head_y = self.y + 8
        pygame.draw.circle(screen, color, (head_x, head_y), 10)
        pygame.draw.circle(screen, BLACK, (head_x, head_y), 10, 2)
        
        # Draw health bar
        bar_width = self.width
        bar_height = 4
        health_percentage = self.health / self.max_health
        pygame.draw.rect(screen, DARK_RED, (self.x, self.y - 8, bar_width, bar_height))
        pygame.draw.rect(screen, GREEN, (self.x, self.y - 8, bar_width * health_percentage, bar_height))
    
    def get_rect(self):
        """Get collision rectangle"""
        return pygame.Rect(self.x, self.y, self.width, self.height)


# ==================== GAME CLASS ====================
class Game:
    """Main game manager"""
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Hero's Destiny")
        self.clock = pygame.time.Clock()
        self.running = True
        
        # Game state
        self.state = 'menu'  # 'menu', 'playing', 'gameover'
        
        # Game objects
        self.player = None
        self.enemies = []
        self.projectiles = []
        self.particles = []
        
        # Game stats
        self.score = 0
        self.wave = 1
        self.spawn_timer = 0
        self.difficulty_multiplier = 1.0
        
        # Wave system
        self.wave_state = 'spawning'  # 'spawning', 'fighting', 'cleared'
        self.enemies_per_wave = 5
        self.enemies_spawned_this_wave = 0
        self.wave_clear_timer = 0
        
        # Font
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        # Background gradient colors
        self.bg_color_top = (20, 10, 40)
        self.bg_color_bottom = (60, 40, 80)
    
    def reset_game(self):
        """Reset game to initial state"""
        self.player = Player(SCREEN_WIDTH // 2 - 20, GROUND_LEVEL - 60)
        self.enemies = []
        self.projectiles = []
        self.particles = []
        self.score = 0
        self.wave = 1
        self.spawn_timer = 0
        self.difficulty_multiplier = 1.0
        self.wave_state = 'spawning'
        self.enemies_per_wave = 5
        self.enemies_spawned_this_wave = 0
        self.wave_clear_timer = 0
    
    def start_new_wave(self):
        """Start a new wave of enemies"""
        self.wave += 1
        self.difficulty_multiplier = 1.0 + ((self.wave - 1) * 0.15)
        self.enemies_per_wave = 5 + ((self.wave - 1) * 2)
        self.enemies_spawned_this_wave = 0
        self.wave_state = 'spawning'
        self.wave_clear_timer = 0
    
    def spawn_enemy(self):
        """Spawn a new enemy"""
        # Choose spawn side randomly
        if random.random() < 0.5:
            x = -40
        else:
            x = SCREEN_WIDTH + 40
        
        y = GROUND_LEVEL - 50
        
        # Determine enemy type based on wave number
        rand_val = random.random()
        if self.wave >= 5 and rand_val < 0.3:
            enemy_type = 'tank'
        elif self.wave >= 3 and rand_val < 0.5:
            enemy_type = 'fast'
        else:
            enemy_type = 'normal'
        
        enemy = Enemy(x, y, enemy_type, self.difficulty_multiplier)
        self.enemies.append(enemy)
        self.enemies_spawned_this_wave += 1
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                if self.state == 'menu':
                    if event.key == pygame.K_SPACE:
                        self.reset_game()
                        self.state = 'playing'
                
                elif self.state == 'playing':
                    if event.key == pygame.K_SPACE:
                        # Alternate between melee and ranged attacks
                        if self.player.attack('melee'):
                            # Also create projectile for ranged feel
                            direction = 1 if self.player.facing_right else -1
                            proj = Projectile(self.player.x + self.player.width // 2,
                                            self.player.y + self.player.height // 2,
                                            direction)
                            self.projectiles.append(proj)
                
                elif self.state == 'gameover':
                    if event.key == pygame.K_r:
                        self.reset_game()
                        self.state = 'playing'
    
    def update(self):
        """Update game logic"""
        if self.state != 'playing':
            return
        
        # Get keys for continuous input
        keys = pygame.key.get_pressed()
        
        # Update player
        self.player.handle_input(keys)
        self.player.update(self.particles)
        
        # Update projectiles
        for projectile in self.projectiles[:]:
            projectile.update(self.particles)
            if not projectile.active:
                self.projectiles.remove(projectile)
        
        # Update enemies
        for enemy in self.enemies[:]:
            enemy.update(self.player.x, self.player.y)
            
            # Enemy attacks player
            if enemy.can_attack_player(self.player.get_rect()):
                self.player.take_damage(enemy.damage, self.particles)
            
            # Check melee attack collision
            attack_rect = self.player.get_attack_rect()
            if attack_rect and attack_rect.colliderect(enemy.get_rect()):
                enemy.take_damage(MELEE_DAMAGE, self.particles)
                if not enemy.active:
                    self.score += 10
                    self.enemies.remove(enemy)
            
            # Check projectile collision
            for projectile in self.projectiles[:]:
                if projectile.active and projectile.get_rect().colliderect(enemy.get_rect()):
                    enemy.take_damage(projectile.damage, self.particles)
                    projectile.active = False
                    if not enemy.active:
                        self.score += 10
                        self.enemies.remove(enemy)
            
            # Remove inactive enemies
            if not enemy.active and enemy in self.enemies:
                self.enemies.remove(enemy)
        
        # Update particles
        self.particles = [p for p in self.particles if p.update()]
        
        # Wave-based enemy spawning system
        if self.wave_state == 'spawning':
            # Spawn enemies for this wave
            self.spawn_timer += 1
            spawn_interval = max(MIN_SPAWN_INTERVAL, 60 - (self.wave * 5))
            if self.spawn_timer >= spawn_interval and self.enemies_spawned_this_wave < self.enemies_per_wave:
                self.spawn_enemy()
                self.spawn_timer = 0
            
            # Check if done spawning this wave
            if self.enemies_spawned_this_wave >= self.enemies_per_wave:
                self.wave_state = 'fighting'
        
        elif self.wave_state == 'fighting':
            # Check if all enemies are defeated
            if len(self.enemies) == 0:
                self.wave_state = 'cleared'
                self.wave_clear_timer = 90  # 1.5 seconds at 60 FPS
        
        elif self.wave_state == 'cleared':
            # Show wave cleared message briefly, then start next wave
            self.wave_clear_timer -= 1
            if self.wave_clear_timer <= 0:
                self.start_new_wave()
        
        # Check game over
        if self.player.health <= 0:
            self.state = 'gameover'
    
    def draw_gradient_background(self):
        """Draw a gradient background"""
        for y in range(SCREEN_HEIGHT):
            ratio = y / SCREEN_HEIGHT
            r = int(self.bg_color_top[0] * (1 - ratio) + self.bg_color_bottom[0] * ratio)
            g = int(self.bg_color_top[1] * (1 - ratio) + self.bg_color_bottom[1] * ratio)
            b = int(self.bg_color_top[2] * (1 - ratio) + self.bg_color_bottom[2] * ratio)
            pygame.draw.line(self.screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
    
    def draw_ui(self):
        """Draw UI elements (health, score)"""
        # Health bar
        bar_x = 20
        bar_y = 20
        bar_width = 200
        bar_height = 25
        
        # Background
        pygame.draw.rect(self.screen, DARK_RED, (bar_x, bar_y, bar_width, bar_height))
        # Current health
        health_width = int(bar_width * (self.player.health / self.player.max_health))
        pygame.draw.rect(self.screen, GREEN, (bar_x, bar_y, health_width, bar_height))
        # Border
        pygame.draw.rect(self.screen, WHITE, (bar_x, bar_y, bar_width, bar_height), 2)
        
        # Health text
        health_text = self.font_small.render(f"HP: {int(self.player.health)}/{self.player.max_health}", 
                                             True, WHITE)
        self.screen.blit(health_text, (bar_x + 5, bar_y + 2))
        
        # Score
        score_text = self.font_medium.render(f"Score: {self.score}", True, YELLOW)
        score_rect = score_text.get_rect()
        score_rect.topright = (SCREEN_WIDTH - 20, 20)
        self.screen.blit(score_text, score_rect)
        
        # Wave indicator
        wave_text = self.font_medium.render(f"Wave {self.wave}", True, PURPLE)
        wave_rect = wave_text.get_rect()
        wave_rect.topright = (SCREEN_WIDTH - 20, 70)
        self.screen.blit(wave_text, wave_rect)
        
        # Enemies remaining in wave
        if self.wave_state == 'spawning':
            enemies_text = self.font_small.render(f"Spawning: {self.enemies_spawned_this_wave}/{self.enemies_per_wave}", 
                                                 True, ORANGE)
        elif self.wave_state == 'fighting':
            enemies_text = self.font_small.render(f"Enemies: {len(self.enemies)}", 
                                                 True, ORANGE)
        else:
            enemies_text = self.font_small.render("Wave Cleared!", True, GREEN)
        
        enemies_rect = enemies_text.get_rect()
        enemies_rect.topright = (SCREEN_WIDTH - 20, 120)
        self.screen.blit(enemies_text, enemies_rect)
    
    def draw_ground(self):
        """Draw the ground"""
        pygame.draw.rect(self.screen, DARK_GREEN, (0, GROUND_LEVEL, SCREEN_WIDTH, SCREEN_HEIGHT - GROUND_LEVEL))
        pygame.draw.line(self.screen, GREEN, (0, GROUND_LEVEL), (SCREEN_WIDTH, GROUND_LEVEL), 3)
    
    def draw(self):
        """Draw everything"""
        if self.state == 'menu':
            self.draw_gradient_background()
            
            # Title
            title = self.font_large.render("HERO'S DESTINY", True, YELLOW)
            title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 150))
            
            # Shadow
            shadow = self.font_large.render("HERO'S DESTINY", True, DARK_BLUE)
            shadow_rect = shadow.get_rect(center=(SCREEN_WIDTH // 2 + 3, 153))
            self.screen.blit(shadow, shadow_rect)
            self.screen.blit(title, title_rect)
            
            # Instructions
            instructions = [
                "Survive waves of enemies!",
                "",
                "Controls:",
                "Move: Arrow Keys or A/D",
                "Jump: Up Arrow or W",
                "Attack: SPACE",
                "",
                "Press SPACE to Begin"
            ]
            
            y_offset = 280
            for line in instructions:
                text = self.font_small.render(line, True, WHITE if line != "Press SPACE to Begin" else GREEN)
                text_rect = text.get_rect(center=(SCREEN_WIDTH // 2, y_offset))
                self.screen.blit(text, text_rect)
                y_offset += 35
        
        elif self.state == 'playing':
            self.draw_gradient_background()
            self.draw_ground()
            
            # Draw particles
            for particle in self.particles:
                particle.draw(self.screen)
            
            # Draw game objects
            self.player.draw(self.screen)
            for enemy in self.enemies:
                enemy.draw(self.screen)
            for projectile in self.projectiles:
                projectile.draw(self.screen)
            
            # Draw UI
            self.draw_ui()
            
            # Draw wave announcement when spawning starts
            if self.wave_state == 'spawning' and self.spawn_timer < 120:
                wave_announce = self.font_large.render(f"WAVE {self.wave}", True, YELLOW)
                announce_rect = wave_announce.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
                
                # Shadow effect
                shadow = self.font_large.render(f"WAVE {self.wave}", True, BLACK)
                shadow_rect = shadow.get_rect(center=(SCREEN_WIDTH // 2 + 3, SCREEN_HEIGHT // 2 + 3))
                
                self.screen.blit(shadow, shadow_rect)
                self.screen.blit(wave_announce, announce_rect)
        
        elif self.state == 'gameover':
            self.draw_gradient_background()
            
            # Game Over title
            game_over = self.font_large.render("GAME OVER", True, RED)
            go_rect = game_over.get_rect(center=(SCREEN_WIDTH // 2, 200))
            self.screen.blit(game_over, go_rect)
            
            # Final score
            score_text = self.font_medium.render(f"Final Score: {self.score}", True, YELLOW)
            score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, 300))
            self.screen.blit(score_text, score_rect)
            
            # Restart prompt
            restart_text = self.font_small.render("Press R to Restart", True, GREEN)
            restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, 400))
            self.screen.blit(restart_text, restart_rect)
        
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
        
        pygame.quit()


# ==================== MAIN ====================
if __name__ == "__main__":
    game = Game()
    game.run()
