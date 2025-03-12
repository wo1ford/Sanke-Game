from tkinter import *
from random import randint

class Game:
    def __init__(self, canvas):
        self.canvas = canvas
        self.snake_coords = [[14, 14]]  # Начальные координаты змейки
        self.apple_coords = [randint(0, 29) for i in range(2)]  # Начальные координаты яблока
        self.vector = {"Up": (0, -1), "Down": (0, 1), "Left": (-1, 0), "Right": (1, 0)}  # Направления
        self.direction = self.vector["Right"]  # Начальное направление
        self.canvas.focus_set()
        self.canvas.bind("<KeyPress>", self.set_direction)
        self.GAME()

    # Метод для нового положения "Яблока"
    def set_apple(self):
        self.apple_coords = [randint(0, 29) for i in range(2)]
        # Условие, чтобы яблоко не лежало на змейке
        if self.apple_coords in self.snake_coords:
            self.set_apple()

    # Установка нового направления змейки
    def set_direction(self, event):
        # Условие, которое проверяет нажатие кнопки
        if event.keysym in self.vector:
            self.direction = self.vector[event.keysym]

    # Отрисовка сцены
    def draw(self):
        self.canvas.delete(ALL)
        x_apple, y_apple = self.apple_coords
        self.canvas.create_rectangle(x_apple * 10, y_apple * 10, (x_apple + 1) * 10, (y_apple + 1) * 10, fill="red", width=0)
        for x, y in self.snake_coords:
            self.canvas.create_rectangle(x * 10, y * 10, (x + 1) * 10, (y + 1) * 10, fill="green", width=0)

    # Метод, который возвращает координаты на интервале [0, 29]
    @staticmethod
    def coord_check(coord):
        return 0 if coord > 29 else 29 if coord < 0 else coord

    # Проверка столкновения со стеной
    def check_wall_collision(self, x, y):
        # Если змейка выходит за границы поля
        if x < 0 or x > 29 or y < 0 or y > 29:
            return True
        return False

    # Рестарт игры
    def restart_game(self):
        self.snake_coords = [[14, 14]]  # Возвращаем змейку в начальное положение
        self.apple_coords = [randint(0, 29) for i in range(2)]  # Новое яблоко
        self.direction = self.vector["Right"]  # Сброс направления

    # Алгоритм "Оторванный Хвост\Логика игры"
    def GAME(self):
        self.draw()
        x, y = self.snake_coords[0]
        x += self.direction[0]
        y += self.direction[1]

        # Проверка столкновения со стеной
        if self.check_wall_collision(x, y):
            self.restart_game()  # Рестарт игры
        else:
            x = self.coord_check(x)
            y = self.coord_check(y)

            # Проверка на съедание яблока
            if x == self.apple_coords[0] and y == self.apple_coords[1]:
                self.set_apple()
            # Проверка на столкновение с собой
            elif [x, y] in self.snake_coords:
                self.restart_game()  # Рестарт игры
            else:
                self.snake_coords.pop()

            self.snake_coords.insert(0, [x, y])

        self.canvas.after(100, self.GAME)


# Создание окна и запуск игры
root = Tk()
canvas = Canvas(root, width=300, height=300, bg="black")
canvas.pack()
game = Game(canvas)
root.mainloop()