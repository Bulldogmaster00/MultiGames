import pygame
import random
import time

# Inicializa o Pygame
pygame.init()

# Configuração da tela em fullscreen
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("MultiGames")
clock = pygame.time.Clock()
FPS = 60

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# ============================== JOGO PONG ==============================

class Paddle(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, joystick=None, controls=None):
        super().__init__()
        self.image = pygame.Surface((w, h))
        self.image.fill(WHITE)
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 6
        self.joystick = joystick
        self.controls = controls

    def update(self):
        dy = 0
        if self.joystick:
            dy = self.joystick.get_axis(1) * self.speed
        elif self.controls:
            keys = pygame.key.get_pressed()
            if keys[self.controls["up"]]:
                dy = -self.speed
            elif keys[self.controls["down"]]:
                dy = self.speed
        self.rect.y += dy
        self.rect.clamp_ip(screen.get_rect())

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20), pygame.SRCALPHA)
        pygame.draw.ellipse(self.image, WHITE, [0, 0, 20, 20])
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.speed_x = random.choice([8, -8])  # Bola mais rápida
        self.speed_y = random.choice([8, -8])  # Bola mais rápida

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

    def reset(self):
        self.rect.center = (WIDTH // 2, HEIGHT // 2)
        self.speed_x = random.choice([8, -8])  # Bola mais rápida
        self.speed_y = random.choice([8, -8])  # Bola mais rápida

def pong_game():
    pygame.joystick.init()
    joystick_count = pygame.joystick.get_count()
    all_sprites = pygame.sprite.Group()

    if joystick_count >= 1:
        j0 = pygame.joystick.Joystick(0)
        j0.init()
        left_paddle = Paddle(30, HEIGHT // 2, 20, 100, joystick=j0)
    else:
        left_paddle = Paddle(30, HEIGHT // 2, 20, 100, controls={"up": pygame.K_w, "down": pygame.K_s})

    if joystick_count >= 2:
        j1 = pygame.joystick.Joystick(1)
        j1.init()
        right_paddle = Paddle(WIDTH - 30, HEIGHT // 2, 20, 100, joystick=j1)
    else:
        right_paddle = Paddle(WIDTH - 30, HEIGHT // 2, 20, 100, controls={"up": pygame.K_UP, "down": pygame.K_DOWN})

    all_sprites.add(left_paddle, right_paddle)
    ball = Ball()
    all_sprites.add(ball)

    left_score = 0
    right_score = 0
    font = pygame.font.Font(None, 36)

    running = True
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESC para voltar ao menu
                    return  # Retorna para o menu principal

        all_sprites.update()
        if ball.rect.colliderect(left_paddle.rect) and ball.speed_x < 0:
            ball.speed_x *= -1
        if ball.rect.colliderect(right_paddle.rect) and ball.speed_x > 0:
            ball.speed_x *= -1

        if ball.rect.left <= 0:
            right_score += 1
            ball.reset()

        if ball.rect.right >= WIDTH:
            left_score += 1
            ball.reset()

        screen.fill(BLACK)
        all_sprites.draw(screen)

        score_text = font.render(f"{left_score} - {right_score}", True, WHITE)
        screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, 20))

        pygame.display.flip()

# ============================== JOGO SNAKE ==============================

class Snake:
    def __init__(self, x, y, color, controls):
        self.body = [[x, y], [x - 20, y], [x - 40, y]]
        self.color = color
        self.direction = 'RIGHT'
        self.controls = controls
        self.alive = True

    def move(self):
        head = self.body[0][:]
        if self.direction == 'UP':
            head[1] -= 20
        elif self.direction == 'DOWN':
            head[1] += 20
        elif self.direction == 'LEFT':
            head[0] -= 20
        elif self.direction == 'RIGHT':
            head[0] += 20
        self.body.insert(0, head)  # Adiciona a nova cabeça
        self.body.pop()  # Remove a última parte da cauda

    def grow(self):
        # Adiciona um segmento à cauda
        tail = self.body[-1][:]
        self.body.append(tail)

    def change_direction(self, new_direction):
        if (self.direction == 'UP' and new_direction != 'DOWN') or \
           (self.direction == 'DOWN' and new_direction != 'UP') or \
           (self.direction == 'LEFT' and new_direction != 'RIGHT') or \
           (self.direction == 'RIGHT' and new_direction != 'LEFT'):
            self.direction = new_direction

    def check_collision(self):
        # Checa colisão com o próprio corpo
        if self.body[0] in self.body[1:]:
            self.alive = False
        # Checa colisão com as paredes
        if self.body[0][0] < 0 or self.body[0][0] >= WIDTH or \
           self.body[0][1] < 0 or self.body[0][1] >= HEIGHT:
            self.alive = False

    def draw(self, screen):
        for segment in self.body:
            pygame.draw.rect(screen, self.color, pygame.Rect(segment[0], segment[1], 20, 20))

def snake_game():
    snake = Snake(WIDTH // 4, HEIGHT // 2, GREEN, {"up": pygame.K_w, "down": pygame.K_s, "left": pygame.K_a, "right": pygame.K_d})
    food = [random.randint(0, (WIDTH // 20) - 1) * 20, random.randint(0, (HEIGHT // 20) - 1) * 20]
    score = 0
    snake_speed = 10

    running = True
    while running:
        screen.fill(BLACK)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:  # ESC para voltar ao menu
                    return  # Retorna para o menu principal
                if event.key == snake.controls["up"]:
                    snake.change_direction('UP')
                elif event.key == snake.controls["down"]:
                    snake.change_direction('DOWN')
                elif event.key == snake.controls["left"]:
                    snake.change_direction('LEFT')
                elif event.key == snake.controls["right"]:
                    snake.change_direction('RIGHT')

        # Movimenta a cobra
        snake.move()
        snake.check_collision()

        if not snake.alive:
            running = False

        # Colisão com a comida
        if snake.body[0] == food:
            snake.grow()
            score += 1
            food = [random.randint(0, (WIDTH // 20) - 1) * 20, random.randint(0, (HEIGHT // 20) - 1) * 20]

        # Desenha a cobrinha e a comida
        snake.draw(screen)
        pygame.draw.rect(screen, RED, pygame.Rect(food[0], food[1], 20, 20))

        # Exibe o score
        font = pygame.font.Font(None, 36)
        score_text = font.render(f"Score: {score}", True, WHITE)
        screen.blit(score_text, (10, 10))

        pygame.display.flip()
        clock.tick(snake_speed)

    # Exibe a tela de game over
    font = pygame.font.Font(None, 72)
    game_over_text = font.render("Game Over", True, WHITE)
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    pygame.display.flip()
    pygame.time.wait(2000)  # Espera 2 segundos antes de fechar
    pygame.quit()

# ============================== MENU ==============================

def menu():
    options = ["Pong", "Snake IO", "Exit"]
    selected_option = 0
    while True:
        screen.fill(BLACK)
        font = pygame.font.Font(None, 36)
        for i, option in enumerate(options):
            color = GREEN if i == selected_option else WHITE
            text = font.render(option, True, color)
            screen.blit(text, (WIDTH // 2 - text.get_width() // 2, HEIGHT // 2 + i * 50))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and selected_option > 0:
                    selected_option -= 1
                elif event.key == pygame.K_DOWN and selected_option < len(options) - 1:
                    selected_option += 1
                elif event.key == pygame.K_RETURN:
                    if selected_option == 0:
                        pong_game()
                    elif selected_option == 1:
                        snake_game()
                    elif selected_option == 2:
                        pygame.quit()
                        quit()

menu()  # Chama o menu inicial
