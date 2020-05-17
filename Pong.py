# Import the pygame library and initialise the game engine
import pygame
from paddle import Paddle
from ball import Ball
import math

pygame.init()

# Define some colors
GRASS = (102, 205, 0)
WHITE = (255, 255, 255)
GREY = (100, 100, 100)
BLACK = (0, 0, 0)

# Open a new window
size = (700, 500)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Pong Soccer")

paddleA = Paddle(WHITE, 10, 90)
paddleA.rect.x = 20
paddleA.rect.y = 200

paddleB = Paddle(WHITE, 10, 90)
paddleB.rect.x = 670
paddleB.rect.y = 200

ball = Ball(WHITE, 10, 10)
ball.rect.x = 345
ball.rect.y = 195


game_over = False
# This will be a list that will contain all the sprites we intend to use in our game.
all_sprites_list = pygame.sprite.Group()

# Add the car to the list of objects
all_sprites_list.add(paddleA)
all_sprites_list.add(paddleB)
all_sprites_list.add(ball)

# The loop will carry on until the user exit the game (e.g. clicks the close button).
carryOn = True

# The clock will be used to control how fast the screen updates
clock = pygame.time.Clock()

# Initialise player scores
scoreA = 0
scoreB = 0

# -------- Main Program Loop -----------
while carryOn:
    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.QUIT:  # If user clicked close
            carryOn = False  # Flag that we are done so we exit this loop
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_x:  # Pressing the x Key will quit the game
                carryOn = False

    # Moving the paddles when the use uses the arrow keys (player A) or "W/S" keys (player B)
    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        paddleA.moveUp(5)
    if keys[pygame.K_s]:
        paddleA.moveDown(5)
    if keys[pygame.K_UP]:
        paddleB.moveUp(5)
    if keys[pygame.K_DOWN]:
        paddleB.moveDown(5)
    if keys[pygame.K_a]:
        paddleA.moveLEFT(5)
    if keys[pygame.K_d]:
        paddleA.moveRIGHT(5)
    if keys[pygame.K_LEFT]:
        paddleB.moveLEFT(5)
    if keys[pygame.K_RIGHT]:
        paddleB.moveRIGHT(5)

    # --- Game logic should go here
    all_sprites_list.update()

    # define game reset
    def resetBall():
        ball.rect.x = 350
        ball.rect.y = 250
        ballAngle = math.radians(0)
        ballSpeed = 10
        ballDirection = -1

    # Set walls and goals, set score and game reset:
    if ball.rect.x >= 690:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.x <= 0:
        ball.velocity[0] = -ball.velocity[0]
    if ball.rect.y > 490:
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.y < 0:
        ball.velocity[1] = -ball.velocity[1]
    if ball.rect.x >= 690 and ball.rect.y >= 150 and ball.rect.y <= 350:
        scoreA += 1
        resetBall()
    if ball.rect.x <= 0 and ball.rect.y >= 150 and ball.rect.y <= 350:
        scoreB += 1
        resetBall()
    # Detect collisions between the ball and the paddles
    if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(ball, paddleB):
        ball.bounce()
    if scoreA >= 10 or scoreB >= 10:
        game_over = True
    # --- Drawing code should go here
    # First, clear the screen to black.
    screen.fill(GRASS)
    # Draw the field
    pygame.draw.line(screen, WHITE, [350, 0], [350, 500], 5)
    pygame.draw.line(screen, WHITE, [5, 0], [5, 500], 5)
    pygame.draw.line(screen, WHITE, [695, 0], [695, 500], 5)
    pygame.draw.circle(screen, WHITE, [350, 250], 68, 5)
    pygame.draw.rect(screen, WHITE, (5, 90, 125, 310), 5)
    pygame.draw.rect(screen, WHITE, (570, 90, 125, 310), 5)
    pygame.draw.line(screen, GREY, [695, 150], [695, 350], 8)
    pygame.draw.line(screen, GREY, [5, 150], [5, 350], 8)
    # Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
    all_sprites_list.draw(screen)

    # Display scores:
    font = pygame.font.Font(None, 74)
    text = font.render(str(scoreA), 1, WHITE)
    screen.blit(text, (250, 10))
    text = font.render(str(scoreB), 1, WHITE)
    screen.blit(text, (420, 10))

    if game_over:
        # If game over is true, draw game over
        text = font.render("Game Over", True, BLACK)
        text_rect = text.get_rect()
        text_x = screen.get_width() / 2 - text_rect.width / 2
        text_y = screen.get_height() / 2 - text_rect.height / 2
        screen.blit(text, [text_x, text_y])
        pygame.time.delay(100)

    # --- Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

    # --- Limit to 60 frames per second
    clock = pygame.time.Clock()
    clock.tick(100)

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()
