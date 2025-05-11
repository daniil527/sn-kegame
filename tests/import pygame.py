import pygame
import random

CELL_SIZE = 20
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_WIDTH = SCREEN_WIDTH // CELL_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // CELL_SIZE

class GameObject:
    """Базовый класс для всех игровых объектов."""
    
    def __init__(self, position=None, body_color=(255, 255, 255)):
        """Инициализация базовых атрибутов."""
        self.position = position if position else (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.body_color = body_color

    def draw(self, surface):
        """Метод отрисовки объекта. Переопределяется в подклассах."""
        pass
class Apple(GameObject):
    """Класс для объекта яблока."""
    
    def __init__(self):
        """Создаёт яблоко в случайной позиции."""
        super().__init__(body_color=(255, 0, 0))
        self.randomize_position()

    def randomize_position(self):
        """Устанавливает случайную позицию яблока в пределах игрового поля."""
        x = random.randint(0, GRID_WIDTH - 1) * CELL_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * CELL_SIZE
        self.position = (x, y)

    def draw(self, surface):
        """Отрисовывает яблоко на игровом поле."""
        rect = pygame.Rect(self.position, (CELL_SIZE, CELL_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
class Snake(GameObject):
    """Класс, описывающий змейку."""
    
    def __init__(self):
        """Инициализация змейки."""
        super().__init__(body_color=(0, 255, 0))
        self.length = 1
        self.positions = [self.position]
        self.direction = (CELL_SIZE, 0)  # движение вправо
        self.next_direction = None

    def update_direction(self):
        """Обновляет направление движения, если задано новое."""
        if self.next_direction:
            # Запрет движения в противоположном направлении
            if (self.next_direction[0] * -1, self.next_direction[1] * -1) != self.direction:
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Передвигает змейку в текущем направлении."""
        head_x, head_y = self.positions[0]
        delta_x, delta_y = self.direction
        new_head = ((head_x + delta_x) % SCREEN_WIDTH, (head_y + delta_y) % SCREEN_HEIGHT)
        if new_head in self.positions:
            self.reset()
        else:
            self.positions.insert(0, new_head)
            if len(self.positions) > self.length:
                tail = self.positions.pop()
                pygame.draw.rect(pygame.display.get_surface(), (0, 0, 0), pygame.Rect(tail, (CELL_SIZE, CELL_SIZE)))

    def draw(self, surface):
        """Отрисовывает змейку на экране."""
        for segment in self.positions:
            rect = pygame.Rect(segment, (CELL_SIZE, CELL_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)

    def get_head_position(self):
        """Возвращает координаты головы змейки."""
        return self.positions[0]

    def reset(self):
        """Сбрасывает змейку в начальное состояние."""
        self.length = 1
        self.position = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        self.positions = [self.position]
        self.direction = (CELL_SIZE, 0)
        self.next_direction = None
def handle_keys(snake):
    """Обрабатывает нажатия клавиш для управления направлением."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                snake.next_direction = (0, -CELL_SIZE)
            elif event.key == pygame.K_DOWN:
                snake.next_direction = (0, CELL_SIZE)
            elif event.key == pygame.K_LEFT:
                snake.next_direction = (-CELL_SIZE, 0)
            elif event.key == pygame.K_RIGHT:
                snake.next_direction = (CELL_SIZE, 0)
    return True

def main():
    """Основной игровой цикл."""
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption("Изгиб Питона 🐍")
    clock = pygame.time.Clock()

    snake = Snake()
    apple = Apple()

    running = True
    while running:
        clock.tick(20)
        running = handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Проверка столкновения с яблоком
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()

        screen.fill((0, 0, 0))
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()

    pygame.quit()
