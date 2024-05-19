import pygame

def play_again(screen, SCREEN_WIDTH, SCREEN_HEIGHT, player_lives):
    font = pygame.font.Font(None, 36)
    button_width = 300
    button_height = 100
    button = pygame.Rect(SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 - button_height // 2, button_width, button_height)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False, player_lives
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(event.pos):
                    return True, player_lives

        pygame.draw.rect(screen, (0, 255, 0), button)  # Draw the button

        text = font.render('Keep Playing', True, (255, 255, 255))
        screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))

        pygame.display.flip()