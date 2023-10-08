import pygame
import random
import os
import math

# Initialize pygame
pygame.init()

# Define color constants
DEBRIS_COLOR = (255, 0, 0)  # Red for debris
ROBOT_COLOR = (0, 128, 255)  # Blue for the robot
TEXT_COLOR = (255, 255, 255)  # White for text

# Constants
WIDTH, HEIGHT = 800, 600
ROBOT_RADIUS = 20
ROBOT_SPEED = 3
DETECTION_RADIUS_SQUARED = (400 ** 2)  # Increased detection radius squared for debris (adjust as needed)
SCORE_FONT_SIZE = 36

# Create the game window
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Debris Avoidance Game")

# Load the user-defined background image (change the path)
background_image = pygame.image.load("/Users/macos/PycharmProjects/minigame/venv/background.jpeg")  # Update with your background image path
background_image = pygame.transform.scale(background_image, (WIDTH, HEIGHT))

# Initialize robot position and direction
robot_x, robot_y = WIDTH // 2, HEIGHT // 2
robot_angle = 0  # Robot's initial direction

# Initialize clock for controlling simulation speed
clock = pygame.time.Clock()

# Define the path to the sound file
sound_file_path = '/Users/macos/PycharmProjects/minigame/venv/emergency-alarm-with-reverb-29431.wav'  # Update with the correct path

# Check if the sound file exists
if not os.path.exists(sound_file_path):
    print(f"Error: Sound file '{sound_file_path}' not found.")
    pygame.quit()
    exit()

# Try to initialize the sound
try:
    collision_sound = pygame.mixer.Sound(sound_file_path)
except pygame.error as e:
    print(f"Error: Unable to load sound file '{sound_file_path}': {e}")
    pygame.quit()
    exit()

# Function to calculate the distance between two points
def distance(x1, y1, x2, y2):
    return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)

# Function to generate random debris
def generate_random_debris():
    x = random.randint(0, WIDTH - 20)
    y = random.randint(0, HEIGHT - 20)
    return x, y

# Function to draw the robot
def draw_robot(x, y, angle):
    # Draw robot as a triangle with a direction indicator
    triangle_vertices = [
        (x, y - ROBOT_RADIUS),
        (x - ROBOT_RADIUS, y + ROBOT_RADIUS),
        (x + ROBOT_RADIUS, y + ROBOT_RADIUS)
    ]
    pygame.draw.polygon(screen, ROBOT_COLOR, triangle_vertices)

    # Draw direction indicator
    dx = ROBOT_RADIUS * math.sin(angle)
    dy = ROBOT_RADIUS * math.cos(angle)
    pygame.draw.line(screen, ROBOT_COLOR, (x, y), (x + dx, y - dy), 2)

# Function to draw debris
def draw_debris(x, y):
    pygame.draw.rect(screen, DEBRIS_COLOR, (x, y, 20, 20))

# Function to check collision
def is_collision(x1, y1, x2, y2):
    return (x1 - x2) ** 2 + (y1 - y2) ** 2 < (2 * ROBOT_RADIUS) ** 2

# Function to detect debris within the increased detection radius
def detect_debris(robot_x, robot_y, debris_list):
    detected_debris = []
    for debris_x, debris_y in debris_list:
        dist = distance(robot_x, robot_y, debris_x, debris_y)
        if dist <= math.sqrt(DETECTION_RADIUS_SQUARED):
            detected_debris.append((debris_x, debris_y))
    return detected_debris

# Main loop for the game
running = True
debris_list = [generate_random_debris() for _ in range(50)]  # Increased number of debris
score = 0
score_font = pygame.font.Font(None, SCORE_FONT_SIZE)

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Draw the user-defined background image
    screen.blit(background_image, (0, 0))

    # Calculate forces from debris
    detected_debris = detect_debris(robot_x, robot_y, debris_list)

    if detected_debris:
        nearest_debris_x, nearest_debris_y = detected_debris[0]
        target_angle = math.atan2(nearest_debris_y - robot_y, nearest_debris_x - robot_x)
        angle_diff = target_angle - robot_angle
        ROTATE_SPEED = math.radians(2)  # Rotation speed in radians

        # Adjust robot's angle towards the nearest debris
        if angle_diff > 0:
            robot_angle += ROTATE_SPEED
        elif angle_diff < 0:
            robot_angle -= ROTATE_SPEED

    # Update robot position based on speed
    robot_speed_x = ROBOT_SPEED * math.sin(robot_angle)
    robot_speed_y = -ROBOT_SPEED * math.cos(robot_angle)

    # Check for collisions with debris before updating position
    collision_detected = False
    for debris_x, debris_y in detected_debris:
        if distance(robot_x + robot_speed_x, robot_y + robot_speed_y, debris_x, debris_y) < 2 * ROBOT_RADIUS:
            collision_detected = True
            break

    # If collision detected, change robot's direction randomly
    if collision_detected:
        robot_angle = random.uniform(0, 2 * math.pi)

    # Update robot position
    robot_x += robot_speed_x
    robot_y += robot_speed_y

    # Handle collision with screen boundaries
    if robot_x < ROBOT_RADIUS:
        robot_x = ROBOT_RADIUS
        robot_angle = random.uniform(0, 2 * math.pi)
    elif robot_x > WIDTH - ROBOT_RADIUS:
        robot_x = WIDTH - ROBOT_RADIUS
        robot_angle = random.uniform(0, 2 * math.pi)
    if robot_y < ROBOT_RADIUS:
        robot_y = ROBOT_RADIUS
        robot_angle = random.uniform(0, 2 * math.pi)
    elif robot_y > HEIGHT - ROBOT_RADIUS:
        robot_y = HEIGHT - ROBOT_RADIUS
        robot_angle = random.uniform(0, 2 * math.pi)

    # Clear the screen
    screen.fill((0, 0, 0))

    # Draw debris
    for debris_x, debris_y in debris_list:
        draw_debris(debris_x, debris_y)

    # Draw robot
    draw_robot(robot_x, robot_y, robot_angle)

    if collision_detected:
        print("Collision imminent! Playing sound.")
        collision_sound.play()
        if score > 0:
            score -= 1
    else:
        score += 1

    score_text = score_font.render(f"Score: {score}", True, TEXT_COLOR)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
