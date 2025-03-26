import pygame
import random
import time

# Inicializa o Pygame
pygame.init()

# Configurações da tela
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Console de Videogame")
clock = pygame.time.Clock()
FPS = 60

# Definições de cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

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
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((20, 20))
        pygame.draw.ellipse(self.image, WHITE, [0, 0, 20, 20])
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT//2))
        self.speed_x = random.choice([4, -4])
        self.speed_y = random.choice([4, -4])

    def update(self):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1

    def reset(self):
        self.rect.center = (WIDTH//2, HEIGHT//2)
        self.speed_x = random.choice([4, -4])
        self.speed_y = random.choice([4, -4])

def pong_game():
    pygame.joystick.init()
    joystick_count = pygame.joystick.get_count()

    all_sprites = pygame.sprite.Group()
    if joystick_count >= 1:
        j0 = pygame.joystick.Joystick(0)
        j0.init()
        left_paddle = Paddle(30, HEIGHT//2, 20, 100, joystick=j0)
    else:
        left_paddle = Paddle(30, HEIGHT//2, 20, 100, controls={"up": pygame.K_w, "down": pygame.K_s})

    if joystick_count >= 2:
        j1 = pygame.joystick.Joystick(1)
        j1.init()
        right_paddle = Paddle(WIDTH-30, HEIGHT//2, 20, 100, joystick=j1)
    else:
        right_paddle = Paddle(WIDTH-30, HEIGHT//2, 20, 100, controls={"up": pygame.K_UP, "down": pygame.K_DOWN})

    all_sprites.add(left_paddle, right_paddle)
    ball = Ball()
    all_sprites.add(ball)

    score_left = 0
    score_right = 0
    font = pygame.font.SysFont(None, 36)
    running = True
    while running:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        all_sprites.update()

        if ball.rect.colliderect(left_paddle.rect) and ball.speed_x < 0:
            ball.speed_x *= -1
        if ball.rect.colliderect(right_paddle.rect) and ball.speed_x > 0:
            ball.speed_x *= -1

        if ball.rect.left <= 0:
            score_right += 1
            ball.reset()
        if ball.rect.right >= WIDTH:
            score_left += 1
            ball.reset()

        screen.fill(BLACK)
        all_sprites.draw(screen)
        score_text = font.render(f"{score_left}   {score_right}", True, WHITE)
        screen.blit(score_text, (WIDTH//2 - score_text.get_width()//2, 20))
        pygame.display.flip()
    time.sleep(1)

# ============================== JOGO DA COBRINHA ==============================

def snake_game():
    snake_size = 20
    snake_speed = 10
    snake_pos = [[100, 50], [90, 50], [80, 50]]
    direction = "RIGHT"
    change_to = direction
    score = 0
    food_pos = [random.randrange(1, WIDTH//snake_size)*snake_size,
                random.randrange(1, HEIGHT//snake_size)*snake_size]
    food_spawn = True
    font = pygame.font.SysFont("arial", 35)
    joystick = None
    if pygame.joystick.get_count() >= 1:
        joystick = pygame.joystick.Joystick(0)
        joystick.init()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and direction != "DOWN":
                    change_to = "UP"
                elif event.key == pygame.K_DOWN and direction != "UP":
                    change_to = "DOWN"
                elif event.key == pygame.K_LEFT and direction != "RIGHT":
                    change_to = "LEFT"
                elif event.key == pygame.K_RIGHT and direction != "LEFT":
                    change_to = "RIGHT"
            if event.type == pygame.JOYAXISMOTION and joystick:
                if event.axis == 1:
                    if event.value < -0.5 and direction != "DOWN":
                        change_to = "UP"
                    elif event.value > 0.5 and direction != "UP":
                        change_to = "DOWN"
                if event.axis == 0:
                    if event.value < -0.5 and direction != "RIGHT":
                        change_to = "LEFT"
                    elif event.value > 0.5 and direction != "LEFT":
                        change_to = "RIGHT"
        direction = change_to
        if direction == "UP":
            new_head = [snake_pos[0][0], snake_pos[0][1] - snake_size]
        elif direction == "DOWN":
            new_head = [snake_pos[0][0], snake_pos[0][1] + snake_size]
        elif direction == "LEFT":
            new_head = [snake_pos[0][0] - snake_size, snake_pos[0][1]]
        elif direction == "RIGHT":
            new_head = [snake_pos[0][0] + snake_size, snake_pos[0][1]]
        snake_pos.insert(0, new_head)
        if snake_pos[0] == food_pos:
            score += 1
            food_spawn = False
        else:
            snake_pos.pop()
        if not food_spawn:
            food_pos = [random.randrange(1, WIDTH//snake_size)*snake_size,
                        random.randrange(1, HEIGHT//snake_size)*snake_size]
            food_spawn = True
        screen.fill(BLACK)
        for pos in snake_pos:
            pygame.draw.rect(screen, GREEN, pygame.Rect(pos[0], pos[1], snake_size, snake_size))
        pygame.draw.rect(screen, WHITE, pygame.Rect(food_pos[0], food_pos[1], snake_size, snake_size))
        if snake_pos[0][0] < 0 or snake_pos[0][0] > WIDTH - snake_size or snake_pos[0][1] < 0 or snake_pos[0][1] > HEIGHT - snake_size:
            running = False
        for block in snake_pos[1:]:
            if snake_pos[0] == block:
                running = False
        score_text = font.render("Score: " + str(score), True, WHITE)
        screen.blit(score_text, (10, 10))
        pygame.display.flip()
        clock.tick(snake_speed)
    time.sleep(1)

# ============================== MENU ==============================

def menu():
    options = ["Pong", "Snake", "Exit"]
    selected = 0
    font = pygame.font.SysFont(None, 48)
    menu_joystick = None
    if pygame.joystick.get_count() >= 1:
        menu_joystick = pygame.joystick.Joystick(0)
        menu_joystick.init()
    running = True
    while running:
        screen.fill(BLACK)
        title = font.render("Menu: Use joystick para navegar", True, WHITE)
        screen.blit(title, (WIDTH//4, HEIGHT//4))
        for i, option in enumerate(options):
            color = WHITE if i == selected else (100, 100, 100)
            text = font.render(option, True, color)
            screen.blit(text, (WIDTH//4, HEIGHT//2 + i * 50))
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Navegação com joystick: eixo vertical
            if event.type == pygame.JOYAXISMOTION and menu_joystick:
                if event.axis == 1:
                    if event.value < -0.5:
                        selected = (selected - 1) % len(options)
                        time.sleep(0.2)
                    elif event.value > 0.5:
                        selected = (selected + 1) % len(options)
                        time.sleep(0.2)
            if event.type == pygame.JOYBUTTONDOWN and menu_joystick:
                if event.button == 0:  # Botão X do DualSense
                    if options[selected] == "Pong":
                        pong_game()
                    elif options[selected] == "Snake":
                        snake_game()
                    elif options[selected] == "Exit":
                        running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    if options[selected] == "Pong":
                        pong_game()
                    elif options[selected] == "Snake":
                        snake_game()
                    elif options[selected] == "Exit":
                        running = False
        clock.tick(FPS)
    pygame.quit()

if __name__ == "__main__":
    menu()

