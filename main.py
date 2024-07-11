import pygame
import random
import sys

# Initialize Pygame
pygame.init()

pygame.mixer.music.load("corsairs-studiokolomna-main-version-23542-02-33.mp3") 
pygame.mixer.music.play(-1)  

# Set up display
width, height = 800, 600
win = pygame.display.set_mode((width, height))
pygame.display.set_caption("Battle Game")

# Load background image
background = pygame.image.load("background.png")
background = pygame.transform.scale(background, (width, height))

# Colors
white = (255, 255, 255)
black = (0, 0, 0)
red = (255, 0, 0)
blue = (0, 0, 255)

# Creature properties
creature_size = 50

class AnimatedCreature(pygame.sprite.Sprite):
    def __init__(self, color, pos, idle_images, attack_images):
        super().__init__()
        self.color = color
        self.pos = pos
        self.idle_images = idle_images
        self.attack_images = attack_images
        self.current_image = 0
        self.images = self.idle_images
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect(center=self.pos)
        self.animation_speed = 0.2 # Animation speed
        self.animation_counter = 0
        self.is_attacking = False

    def update(self):
        self.animation_counter += self.animation_speed
        if self.animation_counter >= 1:
            self.animation_counter = 0
            self.current_image = (self.current_image + 1) % len(self.images)
            self.image = self.images[self.current_image]
            self.rect = self.image.get_rect(center=self.pos)
        if self.is_attacking and self.current_image == len(self.images) - 1:
            self.is_attacking = False
            self.images = self.idle_images
            self.current_image = 0

    def attack(self):
        self.is_attacking = True
        self.images = self.attack_images
        self.current_image = 0

# Define new size for the blue character
blue_creature_size = (480, 350)  

# Load and scale animation frames for the blue character
blue_creature_idle = [pygame.transform.scale(pygame.image.load(f"Elementals_fire_knight_FREE_v1.1/png/fire_knight/01_idle/idle_{i}.png"), blue_creature_size) for i in range(1, 8)]
blue_creature_attack = [pygame.transform.scale(pygame.image.load(f"Elementals_fire_knight_FREE_v1.1/png/fire_knight/07_3_atk/3_atk_{i}.png"), blue_creature_size) for i in range(1, 28)]

red_creature_size = (480, 350) 

# Load and scale animation frames for the red character
red_creature_idle = [pygame.transform.scale(pygame.image.load(f"boss_demon_slime_FREE_v1.0/individual_sprites/01_demon_idle/demon_idle_{i}.png"), red_creature_size) for i in range(1, 6)]
red_creature_attack = [pygame.transform.scale(pygame.image.load(f"boss_demon_slime_FREE_v1.0/individual_sprites/03_demon_cleave/demon_cleave_{i}.png"), red_creature_size) for i in range(1, 15)]


# Player and enemy creatures
player_creature = None
player_creature_pos = [width // 4, height // 2]
player_creature_health = 100

enemy_creature_pos = [3 * width // 4.5, height // 3]
enemy_creature_health = 100

# Create sprite groups
all_sprites = pygame.sprite.Group()
player_group = pygame.sprite.GroupSingle()
enemy_group = pygame.sprite.GroupSingle()

# Clock
clock = pygame.time.Clock()
fps = 60

# Font
font = pygame.font.Font(None, 36)

# Game state
choosing_creature = True
turn = "player"

# Define next_turn function
def next_turn(new_turn):
    global turn
    turn = new_turn

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw background
    win.blit(background, (0, 0))

    if choosing_creature:
        # Display creature choices
        red_creature_rect = pygame.draw.rect(win, red, (width // 4 - creature_size // 2, height // 1.3 - creature_size // 7, creature_size, creature_size))
        blue_creature_rect = pygame.draw.rect(win, blue, (3 * width // 4.5 - creature_size // 2, height // 2 - creature_size // 2, creature_size, creature_size))

        text = font.render("Choose your creature: Red or Blue", True, white)
        win.blit(text, (width // 2 - text.get_width() // 2, height // 4))

        # Check for creature selection
        if event.type == pygame.MOUSEBUTTONDOWN:
            if red_creature_rect.collidepoint(event.pos):
                player_creature = AnimatedCreature(red, player_creature_pos, red_creature_idle, red_creature_attack)
                enemy_creature = AnimatedCreature(blue, enemy_creature_pos, blue_creature_idle, blue_creature_attack)
                player_group.add(player_creature)
                enemy_group.add(enemy_creature)
                all_sprites.add(player_creature, enemy_creature)
                choosing_creature = False
            elif blue_creature_rect.collidepoint(event.pos):
                player_creature = AnimatedCreature(blue, player_creature_pos, blue_creature_idle, blue_creature_attack)
                enemy_creature = AnimatedCreature(red, enemy_creature_pos, red_creature_idle, red_creature_attack)
                player_group.add(player_creature)
                enemy_group.add(enemy_creature)
                all_sprites.add(player_creature, enemy_creature)
                choosing_creature = False

    else:
        # Update and draw all sprites
        all_sprites.update()
        all_sprites.draw(win)

        # Display health
        player_health_text = font.render(f"Player Health: {player_creature_health}", True, white)
        enemy_health_text = font.render(f"Enemy Health: {enemy_creature_health}", True, white)
        win.blit(player_health_text, (10, 10))
        win.blit(enemy_health_text, (width - enemy_health_text.get_width() - 10, 10))

        if turn == "player":
            text = font.render("Your turn! Click on the enemy to attack.", True, white)
            win.blit(text, (width // 2 - text.get_width() // 2, height // 6))

            if event.type == pygame.MOUSEBUTTONDOWN and enemy_creature.rect.collidepoint(event.pos):
                damage = random.randint(5, 20)
                enemy_creature_health -= damage
                player_creature.attack()
                turn = "enemy"

        else:
            text = font.render("Enemy's turn!", True, white)
            win.blit(text, (width // 2 - text.get_width() // 2, height // 4))

            pygame.display.update()
            pygame.time.wait(1000)

            damage = random.randint(5, 20)
            player_creature_health -= damage
            enemy_creature.attack()
            turn = "player"

        if player_creature_health <= 0 or enemy_creature_health <= 0:
            if player_creature_health <= 0:
                text = font.render("You lost!", True, red)

            win.blit(text, (width // 2 - text.get_width() // 2, height // 2))
            pygame.display.update()
            pygame.time.wait(3000)
            running = False

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
sys.exit()
