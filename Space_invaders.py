import pygame
import random
import math
from pygame import mixer
import io

# Initialize pygame
pygame.init()

# Create screen
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption('Space Invasion')
icon = pygame.image.load('ovni-volando.png')
pygame.display.set_icon(icon)
background = pygame.image.load('fondo.jpg')

# Add music
mixer.music.load('Musica.mp3')
mixer.music.play(-1)


# Function to load fonts in memory
def font_bytes(font):
    with open(font, 'rb') as f:
        ttf_bytes = f.read()
    return io.BytesIO(ttf_bytes)


# Player
player_img = pygame.image.load('nave-espacial.png')
player_x = 368
player_y = 500
player_x_change = 0

# Bullet
bullet_img = pygame.image.load('bala.png')
bullet_x = 0
bullet_y = 500
bullet_y_change = 1
bullet_visible = False

# Score
score = 0
font_bytes_io = font_bytes("FreeSansBold.ttf")  # Load font in memory
score_font = pygame.font.Font(font_bytes_io, 28)  # Font for score
final_font = pygame.font.Font(font_bytes_io, 64)  # Font for "Game Over"
text_x = 10
text_y = 10

# Variable to indicate if the game is over
game_over = False


def show_score(x, y):
    """ Display the score on the screen """
    text = score_font.render(f'Score: {score}', True, (255, 255, 255))
    screen.blit(text, (x, y))


def final_text():
    """ Display Game Over message and final score """
    my_final_font = final_font.render('Game Over', True, (255, 0, 0))
    screen.blit(my_final_font, (200, 280))

    score_message = score_font.render(f'Final Score: {score}', True, (255, 255, 255))
    screen.blit(score_message, (300, 370))


# Function to detect collisions
def is_collision(x1, x2, y1, y2):
    distance = math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
    return distance < 27


# Enemy class
class Enemy:
    def __init__(self):
        self.img = pygame.image.load('astronave.png')
        self.x = random.randint(40, 696)
        self.y = random.randint(50, 200)
        self.x_change = 0.3
        self.y_change = 50

    def enemy_movement(self):
        self.x += self.x_change
        if self.x <= 40:
            self.x = 40
            self.y += self.y_change
            self.x_change = 0.3
        elif self.x >= 696:
            self.x = 696
            self.y += self.y_change
            self.x_change = -0.3

    def draw_enemy(self, screen):
        screen.blit(self.img, (self.x, self.y))

    def respawn(self):
        self.x = random.randint(40, 696)
        self.y = random.randint(50, 200)


# Function to draw the player
def player(x, y):
    screen.blit(player_img, (x, y))


# Function to shoot bullet
def fire_bullet(x, y):
    global bullet_visible
    bullet_visible = True
    screen.blit(bullet_img, (x, y))


# Create multiple enemies using the Enemy class
enemies_count = 10
enemies = [Enemy() for _ in range(enemies_count)]

# Main game loop
running = True
while running:
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if not game_over:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    player_x_change = -0.3
                if event.key == pygame.K_RIGHT:
                    player_x_change = 0.3
                if event.key == pygame.K_SPACE:
                    if not bullet_visible:
                        bullet_sound = mixer.Sound('Laser.mp3')
                        bullet_sound.play()
                        bullet_x = player_x
                        fire_bullet(bullet_x, bullet_y)

            if event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                    player_x_change = 0

    if not game_over:
        # Player movement and boundaries
        player_x += player_x_change
        if player_x <= 40:
            player_x = 40
        elif player_x >= 696:
            player_x = 696

        # Update and draw each enemy
        for enemy in enemies:
            enemy.enemy_movement()

            # Check for collision between enemy and player
            if is_collision(player_x, enemy.x, player_y, enemy.y):
                enemies = []  # Empty the list of enemies
                game_over = True
                break

            # Check for collision between enemy and bullet
            if bullet_visible and is_collision(bullet_x, enemy.x, bullet_y, enemy.y):
                explosion_sound = mixer.Sound('Explosion.mp3')
                explosion_sound.play()
                bullet_visible = False
                bullet_y = 500
                score += 1
                enemy.respawn()

            enemy.draw_enemy(screen)

        # Bullet movement
        if bullet_y <= -64:
            bullet_y = 500
            bullet_visible = False
        if bullet_visible:
            fire_bullet(bullet_x, bullet_y)
            bullet_y -= bullet_y_change

        # Draw the player
        player(player_x, player_y)

        # Show current score
        show_score(text_x, text_y)
    else:
        final_text()

    pygame.display.update()
