import pygame

# Initialize pygame modules
pygame.init()

# Set up display window
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pygame Typing Input")

# Set up clock for FPS management
clock = pygame.time.Clock()

# Initialize styling options
FONT_SIZE = 32
font = pygame.font.Font(None, FONT_SIZE)

COLOR_BACKGROUND = pygame.Color("gray15")
COLOR_INACTIVE = pygame.Color("lightskyblue3")
COLOR_ACTIVE = pygame.Color("dodgerblue2")
COLOR_TEXT = pygame.Color("white")

# Box placement variables
input_rect = pygame.Rect(200, 250, 400, 50)
box_color = COLOR_INACTIVE

# Text management variables
user_text = ""
is_active = False

# Main game loop flag
running = True

while running:
    # Process game mechanics and inputs
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Toggle selection if user clicks on or off the text box
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_rect.collidepoint(event.pos):
                is_active = True
                box_color = COLOR_ACTIVE
            else:
                is_active = False
                box_color = COLOR_INACTIVE

        # Handle keyboard input when box is active
        if event.type == pygame.KEYDOWN and is_active:
            if event.key == pygame.K_BACKSPACE:
                # Remove the last character
                user_text = user_text[:-1]
            elif event.key == pygame.K_RETURN:
                # Submit or print input, then clear box
                print(f"User Submitted: {user_text}")
                user_text = ""
            else:
                # Append typed character
                user_text += event.unicode

    # Clear screen with background color
    screen.fill(COLOR_BACKGROUND)

    # Render typed text to a surface
    text_surface = font.render(user_text, True, COLOR_TEXT)
    
    # Dynamically expand box width if text exceeds initial size
    input_rect.width = max(400, text_surface.get_width() + 20)

    # Draw text box container and text surface onto screen
    screen.blit(text_surface, (input_rect.x + 10, input_rect.y + 13))
    pygame.draw.rect(screen, box_color, input_rect, 2)

    # Update frame display and regulate speed
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
