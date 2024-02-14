import pygame
import sys

# Pygame initialization
pygame.init()

icon = pygame.image.load('GameMedia/icon.png')  # Load icon
pygame.display.set_icon(icon)  # Load icon

# Set window size
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Galaxy Explorer")

# Color setting
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Rescale the image
background_image = pygame.image.load('GameMedia/Background.png')
background_image = pygame.transform.scale(background_image, (screen_width, screen_height))

# Background music
pygame.mixer.music.load('GameMedia/GalaxyExplorer.mp3')
pygame.mixer.music.play(-1)  # Music Loop


# Draw play button
def draw_button(surface, text, position, size, bg_color, text_color, font_size):
    font = pygame.font.Font(None, font_size)
    text_surf = font.render(text, True, text_color)
    x, y = position
    width, height = size
    button_rect = pygame.Rect(x, y, width, height)

    pygame.draw.rect(surface, bg_color, button_rect)
    text_rect = text_surf.get_rect(center=button_rect.center)
    surface.blit(text_surf, text_rect)

    return button_rect


# Draw game title
def game_title_screen():
    running = True
    game_over = False

    while running:
        screen.blit(background_image, (0, 0))  # Fill the background with picture

        # Draw game title
        font = pygame.font.Font(None, 72)
        title_text = font.render("Galaxy Explorer", True, WHITE)
        screen.blit(title_text, (screen_width / 2 - title_text.get_width() / 2, 100))

        # Draw play button
        play_button_rect = draw_button(screen, "Play", (screen_width / 2 - 50, screen_height / 2), (100, 50), GREEN,
                                       WHITE, 36)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if play_button_rect.collidepoint(event.pos):
                    # print("Play button clicked")  # Button clicked test
                    pygame.quit()

                    from GalaxyExplorer_CORE import Game_Loop
                    Game_Loop()

        pygame.display.flip()
        pygame.time.Clock().tick(60)


# Start title page
game_title_screen()

pygame.quit()
