import pygame
import random
import time

pygame.init()

WIDTH, HEIGHT, BLOCK_SIZE = 600, 400, 15
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")
clock = pygame.time.Clock()

BLACK, WHITE, GREEN, RED = (0, 0, 0), (255, 255, 255), (0, 255, 0), (255, 0, 0)

font = pygame.font.SysFont("arial", 25)
title_font = pygame.font.SysFont("arial", 50)

def display_score(screen, score):
    screen.blit(font.render(f"Score: {score}", True, WHITE), [10, 10])

def spawn_food():
    return [random.randint(0, (WIDTH // BLOCK_SIZE) - 1) * BLOCK_SIZE,
            random.randint(0, (HEIGHT // BLOCK_SIZE) - 1) * BLOCK_SIZE]

def menu_screen():
    while True:
        screen.fill(BLACK)
        title = title_font.render("SNAKE", True, WHITE)
        play_text = font.render("Press ENTER to Play", True, GREEN)

        screen.blit(title, [WIDTH // 2 - title.get_width() // 2, HEIGHT // 3])
        screen.blit(play_text, [WIDTH // 2 - play_text.get_width() // 2, HEIGHT // 2])

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return True

def game_over_screen(score):
    while True:
        screen.fill(BLACK)
        game_over_text = font.render(f"Game Over! Score: {score}", True, RED)
        play_again_text = font.render("Press R to Play Again", True, GREEN)
        quit_text = font.render("Press Q to Quit", True, WHITE)

        screen.blit(game_over_text, [WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 3])
        screen.blit(play_again_text, [WIDTH // 2 - play_again_text.get_width() // 2, HEIGHT // 2])
        screen.blit(quit_text, [WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 40])

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    pygame.quit()
                    return False

# Main game loop
def main():
    while True:
        if not menu_screen():
            break

        snake = [[BLOCK_SIZE * 5, BLOCK_SIZE * 5], [BLOCK_SIZE * 4, BLOCK_SIZE * 5]]  # Snake starts with two segments
        direction, score, food = 'RIGHT', 0, spawn_food()
        move_delay = 90  # Delay in milliseconds between snake moves
        last_move_time = pygame.time.get_ticks()  # Track time of the last movement

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    return
                if event.type == pygame.KEYDOWN:
                    new_dir = pygame.key.name(event.key).upper()
                    if new_dir in {'UP', 'DOWN', 'LEFT', 'RIGHT'} and \
                       {'UP': 'DOWN', 'DOWN': 'UP', 'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}.get(direction) != new_dir:
                        direction = new_dir

            # This just helps with the framerate.
            current_time = pygame.time.get_ticks()
            if current_time - last_move_time >= move_delay:
                last_move_time = current_time

                # Controls
                head = snake[0][:]
                head[1] -= BLOCK_SIZE if direction == 'UP' else 0
                head[1] += BLOCK_SIZE if direction == 'DOWN' else 0
                head[0] -= BLOCK_SIZE if direction == 'LEFT' else 0
                head[0] += BLOCK_SIZE if direction == 'RIGHT' else 0
                snake.insert(0, head)

                # Checks if food is eaten
                if head == food:
                    score += 1
                    food = spawn_food()
                else:
                    snake.pop()

                # Collisions
                if (head[0] < 0 or head[1] < 0 or head[0] >= WIDTH or head[1] >= HEIGHT or head in snake[1:]):
                    if not game_over_screen(score):
                        return
                    else:
                        break

            screen.fill(BLACK)
            pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], BLOCK_SIZE, BLOCK_SIZE))
            [pygame.draw.rect(screen, GREEN, pygame.Rect(segment[0], segment[1], BLOCK_SIZE, BLOCK_SIZE)) for segment in snake]
            display_score(screen, score)
            pygame.display.flip()

            clock.tick(40)

if __name__ == "__main__":
    main()
