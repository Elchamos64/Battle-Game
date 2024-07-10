import pygame
import random
import sys

# Initialize Pygame
pygame.init()

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
green = (0, 255, 0)
yellow = (255, 255, 0)

# Creature properties
creature_size = 50

class AnimatedCreature(pygame.sprite.Sprite):
    def __init__(self, color, pos, images):
        super().__init__()
        self.color = color
        self.pos = pos
        self.images = images
        self.current_image = 0
        self.image = self.images[self.current_image]
        self.rect = self.image.get_rect(center=self.pos)
        self.animation_speed = 0.1  # Animation speed
        self.animation_counter = 0

    def update(self):
        self.animation_counter += self.animation_speed
        if self.animation_counter >= 1:
            self.animation_counter = 0
            self.current_image = (self.current_image + 1) % len(self.images)
            self.image = self.images[self.current_image]
            self.rect = self.image.get_rect(center=self.pos)

# Load animation frames
red_creature_images = [pygame.image.load(f"demon_cleave_{i}.png") for i in range(1, 15)]
blue_creature_images = [pygame.image.load(f"demon_cleave_{i}.png") for i in range(1, 15)]

# Player and enemy creatures
player_creature = None
player_creature_pos = [width // 4, height // 2]
player_creature_health = 100

enemy_creature_pos = [3 * width // 4, height // 2]
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
        red_creature_rect = pygame.draw.rect(win, red, (width // 4 - creature_size // 2, height // 2 - creature_size // 2, creature_size, creature_size))
        blue_creature_rect = pygame.draw.rect(win, blue, (3 * width // 4 - creature_size // 2, height // 2 - creature_size // 2, creature_size, creature_size))

        text = font.render("Choose your creature: Red or Blue", True, white)
        win.blit(text, (width // 2 - text.get_width() // 2, height // 4))

        # Check for creature selection
        if event.type == pygame.MOUSEBUTTONDOWN:
            if red_creature_rect.collidepoint(event.pos):
                player_creature = AnimatedCreature(red, player_creature_pos, red_creature_images)
                enemy_creature = AnimatedCreature(blue, enemy_creature_pos, blue_creature_images)
                player_group.add(player_creature)
                enemy_group.add(enemy_creature)
                all_sprites.add(player_creature, enemy_creature)
                choosing_creature = False
            elif blue_creature_rect.collidepoint(event.pos):
                player_creature = AnimatedCreature(blue, player_creature_pos, blue_creature_images)
                enemy_creature = AnimatedCreature(red, enemy_creature_pos, red_creature_images)
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
            win.blit(text, (width // 2 - text.get_width() // 2, height // 4))

            if event.type == pygame.MOUSEBUTTONDOWN and enemy_creature.rect.collidepoint(event.pos):
                damage = random.randint(5, 20)
                enemy_creature_health -= damage
                turn = "enemy"

        else:
            text = font.render("Enemy's turn!", True, white)
            win.blit(text, (width // 2 - text.get_width() // 2, height // 4))

            pygame.display.update()
            pygame.time.wait(1000)

            damage = random.randint(5, 20)
            player_creature_health -= damage
            turn = "player"

        if player_creature_health <= 0 or enemy_creature_health <= 0:
            if player_creature_health <= 0:
                text = font.render("You lost!", True, red)
            else:
                text = font.render("You won!", True, green)

            win.blit(text, (width // 2 - text.get_width() // 2, height // 2))
            pygame.display.update()
            pygame.time.wait(3000)
            running = False

    pygame.display.update()
    clock.tick(fps)

pygame.quit()
sys.exit()
