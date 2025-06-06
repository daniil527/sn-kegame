
## Что нужно установить

- Python 3.10+ — язык, на котором написана игра.
- pip — менеджер пакетов для Python.
- Pygame — библиотека для создания игр.

## Установка проекта
- Создайте виртуальное окружение (рекомендуется):

```sh
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```
- Установите зависимости:

```sh
pip install -r requirements.txt
```

## Запуск проекта
```sh
py the_snake.py
```

## Управление

- Стрелки на клавиатуре — управляют движением змейки.
- Закрыть окно или нажать Esc — выйти из игры.


## Структура кода

```
snake_game/
├── the_snake.py      # Основной файл с игрой
├── requirements.txt  # Список зависимостей
└── README.md         # Этот файл
```

Внутри the_snake.py:

GameObject — базовый класс для рисования квадратиков.
Apple — класс, который отвечает за яблоко (случайная позиция вне тела змейки).
Snake — класс, управляющий телом змейки и её движением.
main() — точка входа: инициализирует игру, обрабатывает ввод, обновляет состояние и отрисовывает кадры.
