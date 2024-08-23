import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Настройки экрана
WIDTH, HEIGHT = 300, 600
GRID_SIZE = 30
COLUMNS = WIDTH // GRID_SIZE
ROWS = HEIGHT // GRID_SIZE

# Определение цветов
COLORS = {
    'I': (0, 240, 240),
    'O': (240, 240, 0),
    'T': (160, 0, 240),
    'S': (0, 240, 0),
    'Z': (240, 0, 0),
    'J': (0, 0, 240),
    'L': (240, 160, 0)
}

# Определение фигур тетромино и их вращений
TETROMINOES = {
    'I': [
        [[1, 1, 1, 1]],
        [[1], [1], [1], [1]]
    ],
    'O': [
        [[1, 1],
         [1, 1]]
    ],
    'T': [
        [[0, 1, 0],
         [1, 1, 1]],
        [[1, 0],
         [1, 1],
         [1, 0]],
        [[1, 1, 1],
         [0, 1, 0]],
        [[0, 1],
         [0, 1],
         [1, 1]]
    ],
    'S': [
        [[0, 1, 1],
         [1, 1, 0]],
        [[1, 0],
         [1, 1],
         [0, 1]]
    ],
    'Z': [
        [[1, 1, 0],
         [0, 1, 1]],
        [[0, 1],
         [1, 1],
         [1, 0]]
    ],
    'J': [
        [[1, 0, 0],
         [1, 1, 1]],
        [[1, 1],
         [1, 0],
         [1, 0]],
        [[1, 1, 1],
         [0, 0, 1]],
        [[0, 1],
         [0, 1],
         [1, 1]]
    ],
    'L': [
        [[0, 0, 1],
         [1, 1, 1]],
        [[1, 0],
         [1, 0],
         [1, 1]],
        [[1, 1, 1],
         [1, 0, 0]],
        [[1, 1],
         [0, 1],
         [0, 1]]
    ]
}

# Создание окна игры
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Тетрис")

# Класс Tetromino
class Tetromino:
    def __init__(self, shape):
        self.shape = shape
        self.color = COLORS[shape]
        self.rotation = 0
        self.x = COLUMNS // 2 - len(TETROMINOES[shape][0]) // 2
        self.y = 0

    def image(self):
        """Возвращает форму тетромино с учётом текущего поворота."""
        return TETROMINOES[self.shape][self.rotation]

    def rotate(self):
        """Поворачивает тетромино на 90 градусов."""
        self.rotation = (self.rotation + 1) % len(TETROMINOES[self.shape])

def draw_grid():
    """Отрисовка сетки игрового поля."""
    for x in range(0, WIDTH, GRID_SIZE):
        pygame.draw.line(screen, (128, 128, 128), (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, GRID_SIZE):
        pygame.draw.line(screen, (128, 128, 128), (0, y), (WIDTH, y))

def draw_tetromino(tetromino):
    """Отрисовка тетромино на игровом поле."""
    for y, row in enumerate(tetromino.image()):
        for x, cell in enumerate(row):
            if cell:
                pygame.draw.rect(
                    screen,
                    tetromino.color,
                    pygame.Rect(
                        (tetromino.x + x) * GRID_SIZE,
                        (tetromino.y + y) * GRID_SIZE,
                        GRID_SIZE,
                        GRID_SIZE
                    )
                )

def check_collision(grid, tetromino):
    """Проверка столкновений тетромино с границами и другими блоками."""
    for y, row in enumerate(tetromino.image()):
        for x, cell in enumerate(row):
            if cell:
                if (
                    x + tetromino.x < 0 or
                    x + tetromino.x >= COLUMNS or
                    y + tetromino.y >= ROWS or
                    grid[y + tetromino.y][x + tetromino.x] != (0, 0, 0)
                ):
                    return True
    return False

def lock_tetromino(grid, tetromino):
    """Закрепление тетромино на игровом поле."""
    for y, row in enumerate(tetromino.image()):
        for x, cell in enumerate(row):
            if cell:
                grid[y + tetromino.y][x + tetromino.x] = tetromino.color

def clear_rows(grid):
    """Очистка заполненных линий на игровом поле."""
    full_rows = 0
    new_grid = [row for row in grid if any(cell == (0, 0, 0) for cell in row)]
    full_rows = ROWS - len(new_grid)
    new_grid = [[(0, 0, 0)] * COLUMNS for _ in range(full_rows)] + new_grid
    return new_grid, full_rows

def draw_grid_blocks(grid):
    """Отрисовка всех заблокированных блоков на игровом поле."""
    for y, row in enumerate(grid):
        for x, cell in enumerate(row):
            if cell != (0, 0, 0):
                pygame.draw.rect(
                    screen,
                    cell,
                    pygame.Rect(
                        x * GRID_SIZE,
                        y * GRID_SIZE,
                        GRID_SIZE,
                        GRID_SIZE
                    )
                )

def new_tetromino():
    """Создает новое тетромино и проверяет, можно ли его разместить."""
    tetromino = Tetromino(random.choice(list(TETROMINOES.keys())))
    if check_collision(grid, tetromino):
        print("Game Over!")  # Сообщение для отладки
        pygame.quit()
        sys.exit()
    return tetromino

def main():
    global grid
    grid = [[(0, 0, 0) for _ in range(COLUMNS)] for _ in range(ROWS)]
    current_tetromino = new_tetromino()
    clock = pygame.time.Clock()
    fall_time = 0

    while True:
        screen.fill((0, 0, 0))
        fall_speed = 0.5
        fall_time += clock.get_rawtime()
        clock.tick()

        # Падение тетромино
        if fall_time / 1000 >= fall_speed:
            current_tetromino.y += 1
            if check_collision(grid, current_tetromino):
                current_tetromino.y -= 1
                lock_tetromino(grid, current_tetromino)
                grid, full_rows = clear_rows(grid)
                current_tetromino = new_tetromino()
            fall_time = 0

        # Обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_tetromino.x -= 1
                    if check_collision(grid, current_tetromino):
                        current_tetromino.x += 1
                elif event.key == pygame.K_RIGHT:
                    current_tetromino.x += 1
                    if check_collision(grid, current_tetromino):
                        current_tetromino.x -= 1
                elif event.key == pygame.K_DOWN:
                    current_tetromino.y += 1
                    if check_collision(grid, current_tetromino):
                        current_tetromino.y -= 1
                elif event.key == pygame.K_UP:
                    current_tetromino.rotate()
                    if check_collision(grid, current_tetromino):
                        current_tetromino.rotate()
                        current_tetromino.rotate()
                        current_tetromino.rotate()

        # Отрисовка игры
        draw_grid()
        draw_grid_blocks(grid)
        draw_tetromino(current_tetromino)
        pygame.display.flip()

if __name__ == "__main__":
    main()
