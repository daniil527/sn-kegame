import random
import sys

import pygame
from typing import Collection, Tuple, Optional

# Константы экрана и сетки
SCREEN_WIDTH: int = 640
SCREEN_HEIGHT: int = 480
GRID_SIZE: int = 20
GRID_WIDTH: int = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT: int = SCREEN_HEIGHT // GRID_SIZE
BOARD_BACKGROUND_COLOR: Tuple[int, int, int] = (40, 40, 40)

# Направления движения змейки
UP: Tuple[int, int] = (0, -1)
DOWN: Tuple[int, int] = (0, 1)
LEFT: Tuple[int, int] = (-1, 0)
RIGHT: Tuple[int, int] = (1, 0)

# Настройка FPS
FPS: int = 20

# Инициализация Pygame и глобальных объектов
pygame.init()
screen = pygame.display.set_mode(
    (SCREEN_WIDTH, SCREEN_HEIGHT),
)
pygame.display.set_caption('Snake Game')
clock = pygame.time.Clock()
font = pygame.font.SysFont(
    'Arial',
    25,
)


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


def draw_text(surface, text: str, position: Tuple[int, int]):
    """Выводит текст белым цветом в заданной позиции."""
    rendered = font.render(
        text,
        True,
        (255, 255, 255),
    )
    surface.blit(
        rendered,
        position,
    )


class GameObject:
    """Базовый класс для игровых объектов."""

    def __init__(
        self,
        position: Tuple[int, int] = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
        body_color: Optional[Tuple[int, int, int]] = None,
    ):
        self.position: Tuple[int, int] = position
        self.body_color: Optional[Tuple[int, int, int]] = body_color

    def draw_cell(
        self,
        surface,
        position: Tuple[int, int],
        color: Optional[Tuple[int, int, int]],
    ):
        if color is None:
            return
        rect = pygame.Rect(position[0], position[1], GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, color, rect)

    def draw(self, surface):
        """Шаблон отрисовки; должен быть переопределён в наследниках."""
        raise NotImplementedError


class Apple(GameObject):
    """Яблоко: наследует GameObject и размещается случайно на сетке."""

    def __init__(
        self,
        occupied: Collection[Tuple[int, int]] = ()
    ):
        position = self._randomize_position(occupied)
        super().__init__(
            position=position,
            body_color=(255, 0, 0),
        )

    def _randomize_position(self, occupied: Collection[Tuple[int, int]]):
        """Возвращает случайную позицию на сетке."""
        while True:
            x = random.randint(
                0,
                GRID_WIDTH - 1,
            ) * GRID_SIZE
            y = random.randint(
                0,
                GRID_HEIGHT - 1,
            ) * GRID_SIZE
            if (x, y) not in occupied:
                return x, y

    def randomize_position(self, occupied: Collection[Tuple[int, int]]):
        """Перемещает яблоко в новую случайную позицию."""
        self.position = self._randomize_position(occupied)

    def draw(self, surface: pygame.Surface):
        """Отрисовываем яблоко"""
        self.draw_cell(surface, self.position, self.body_color)


class Snake(GameObject):
    """Змейка: наследует GameObject, управляет телом и движением."""

    def __init__(self):
        super().__init__(
            position=(
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
            ),
            body_color=(0, 255, 0),
        )
        self.reset()

    def get_head_position(self):
        """Возвращает текущую позицию головы змейки."""
        return self.positions[0]

    def update_direction(self):
        """Обновляет направление движения, предотвращая разворот на 180°."""
        if self.next_direction:
            opposite = (
                -self.direction[0],
                -self.direction[1],
            )
            if self.next_direction != opposite:
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Сдвигает змейку на одну клетку по текущему направлению."""
        head_x, head_y = self.get_head_position()
        dx, dy = self.direction
        new_head = (
            (head_x + dx * GRID_SIZE) % SCREEN_WIDTH,
            (head_y + dy * GRID_SIZE) % SCREEN_HEIGHT,
        )
        self.last = self.positions[-1]
        self.positions.insert(
            0,
            new_head,
        )
        if len(self.positions) > self.length:
            self.positions.pop()

    def reset(self):
        """Сбрасывает змейку к начальным параметрам игры."""
        self.positions = [
            (
                SCREEN_WIDTH // 2,
                SCREEN_HEIGHT // 2,
            ),
        ]
        self.length = 1
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def draw(self, surface):
        """Рисуем змейку стираем хвост и добавляя тело"""
        if self.last:
            self.draw_cell(surface, self.last, BOARD_BACKGROUND_COLOR)
        for n in self.positions:
            self.draw_cell(surface, n, self.body_color)


def main():
    """Главная функция: цикл игры и управление объектами."""
    snake = Snake()
    apple = Apple(occupied=set(snake.positions))
    score = 0

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            score += 1
            apple.randomize_position(occupied=set(snake.positions))

        head = snake.get_head_position()
        if head in snake.positions[1:]:
            snake.reset()
            score = 0
        screen.fill(
            BOARD_BACKGROUND_COLOR,
        )
        apple.draw(screen)
        snake.draw(screen)
        draw_text(
            screen,
            f'Score: {score}',
            (10, 10),
        )
        pygame.display.update()
        clock.tick(FPS)


if __name__ == '__main__':
    main()

