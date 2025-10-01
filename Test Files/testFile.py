import time
import pygame

# Initialize pygame
pygame.init()

# Screen dimensions
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

# Colors
BACKGROUND_COLOR = (30, 30, 30)
RECTANGLE_COLOR = (255, 0, 0)

# Rectangle setup
RECT_WIDTH = 60
RECT_HEIGHT = 60
rect = pygame.Rect(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2, RECT_WIDTH, RECT_HEIGHT)

# Rectangle movement
speed = 200  # Pixels per second (speed of movement)

# Start with both previous and current positions at the same location
prev_rect_pos = pygame.Vector2(rect.topleft)
current_rect_pos = pygame.Vector2(rect.topleft)

# Screen setup
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Character Movement with Arrow Keys")


# Main functions
def process_input(velocity):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()


    # Process movement based on arrow key input
    keys = pygame.key.get_pressed()
    velocity.x = 0
    velocity.y = 0
    if keys[pygame.K_UP]:  # Move up
        velocity.y = -1
    if keys[pygame.K_DOWN]:  # Move down
        velocity.y = 1
    if keys[pygame.K_LEFT]:  # Move left
        velocity.x = -1
    if keys[pygame.K_RIGHT]:  # Move right
        velocity.x = 1


def update(elapsed, velocity):
    global prev_rect_pos, current_rect_pos

    # Store previous position for interpolation
    prev_rect_pos = pygame.Vector2(current_rect_pos)

    # Update current position based on velocity and elapsed time
    current_rect_pos.x += velocity.x * speed * elapsed
    current_rect_pos.y += velocity.y * speed * elapsed

    # Keep rectangle within screen bounds
    current_rect_pos.x = max(0, min(SCREEN_WIDTH - RECT_WIDTH, current_rect_pos.x))
    current_rect_pos.y = max(0, min(SCREEN_HEIGHT - RECT_HEIGHT, current_rect_pos.y))

    # Update the rect (used for collision checks)
    rect.x = current_rect_pos.x
    rect.y = current_rect_pos.y


def render(interpolation):
    # Interpolate rectangle position
    interpolated_x = prev_rect_pos.x + (current_rect_pos.x - prev_rect_pos.x) * interpolation
    interpolated_y = prev_rect_pos.y + (current_rect_pos.y - prev_rect_pos.y) * interpolation

    # Clear the screen
    screen.fill(BACKGROUND_COLOR)

    # Draw the rectangle
    pygame.draw.rect(
        screen,
        RECTANGLE_COLOR,
        pygame.Rect(interpolated_x, interpolated_y, RECT_WIDTH, RECT_HEIGHT),
    )

    # Update the display
    pygame.display.flip()


# Main game loop
MS_PER_UPDATE = 0.016  # ~60 FPS

previous_time = time.time()
lag = 0
velocity = pygame.Vector2(0, 0)  # Velocity vector for key movement

while True:

    # time.sleep(0.032)
    current_time = time.time()
    elapsed_time = current_time - previous_time
    previous_time = current_time
    lag += elapsed_time

    process_input(velocity)

    while lag >= MS_PER_UPDATE:
        update(MS_PER_UPDATE, velocity)
        lag -= MS_PER_UPDATE

    render(lag / MS_PER_UPDATE)
