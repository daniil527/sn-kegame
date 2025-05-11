import random
import pygame
import sys

# Константы экрана и сетки
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE
BOARD_BACKGROUND_COLOR = (40, 40, 40)

# Направления движения змейки
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Настройка FPS
FPS = 20

# Инициализация Pygame и глобальных объектов
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()
font = pygame.font.SysFont('Arial', 25)


def handle_keys(snake):
    """Обрабатывает нажатия клавиш и ставит следующую дирекцию движения."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = UP
            elif event.key == pygame.K_DOWN:
                snake.next_direction = DOWN
            elif event.key == pygame.K_LEFT:
                snake.next_direction = LEFT
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = RIGHT


def draw_text(surface, text, position):
    """Выводит текст белым цветом в заданной позиции."""
    rendered = font.render(text, True, (255, 255, 255))
    surface.blit(rendered, position)


class GameObject:
    """Базовый класс для игровых объектов."""
    def __init__(self,
                 position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                 body_color=None):
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Шаблон отрисовки; должен быть переопределён в наследниках."""
        pass


class Apple(GameObject):
    """Яблоко: наследует GameObject и размещается случайно на сетке."""
    def __init__(self):
        position = self._randomize_position()
        super().__init__(position, body_color=(255, 0, 0))

    def _randomize_position(self):
        """Возвращает случайную позицию на сетке."""
        x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        return x, y

    def randomize_position(self):
        """Перемещает яблоко в новую случайную позицию."""
        self.position = self._randomize_position()

    def draw(self, surface):
        """Рисует яблоко в качестве квадрата на экране."""
        rect = pygame.Rect(self.position[0], self.position[1], GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, self.body_color, rect)


class Snake(GameObject):
    """Змейка: наследует GameObject, управляет телом и движением."""
    def __init__(self):
        super().__init__(position=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                         body_color=(0, 255, 0))
        self.positions = [self.position]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения, предотвращая разворот на 180°."""
        if self.next_direction:
            opposite = (-self.direction[0], -self.direction[1])
            if self.next_direction != opposite:
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Сдвигает змейку на одну клетку по текущему направлению."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = ((head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
                    (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT)
        self.last = self.positions[-1]
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        """Сбрасывает змейку к начальным параметрам игры."""
        self.positions = [(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def draw(self, surface):
        """Отрисовывает змейку и стирает хвостовой сегмент."""
        if self.last:
            rect = pygame.Rect(self.last[0], self.last[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, rect)
        for pos in self.positions:
            rect = pygame.Rect(pos[0], pos[1], GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, self.body_color, rect)

    def check_collision(self):
        """Проверяет столкновение головы со своим телом."""
        return self.get_head_position() in self.positions[1:]


def main():
    """Главная функция: цикл игры и управление объектами."""
    snake = Snake()
    apple = Apple()
    score = 0
    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        if snake.get_head_position() == apple.position:
            snake.length += 1
            score += 1
            apple.randomize_position()
        if snake.check_collision():
            snake.reset()
        screen.fill(BOARD_BACKGROUND_COLOR)
        apple.draw(screen)
        snake.draw(screen)
        draw_text(screen, f'Score: {score}', (10, 10))
        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()
