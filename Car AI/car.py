import math
import pygame


class Car:
    def __init__(self, sprite, size_x, size_y):
        self.sprite = sprite
        self.size_x = size_x
        self.size_y = size_y

        self.rotated_sprite = self.sprite

        self.position = [800, 770]  # Начальная позиция
        self.angle = 0
        self.speed = 0

        self.speed_set = False  # Флаг для фиксированной скорости

        self.center = [self.position[0] + self.size_x / 2,
                       self.position[1] + self.size_y / 2]  # Центр машины

        self.radars = []  # Лист радаров
        self.drawing_radars = []  # Лист для отрисовки радаров

        self.alive = True  # Переменная жива ли машина

        self.distance = 0  # Дистанция, которую проехала машина
        self.time = 0  # Прошедшее время

    def check_collision(self, game_map, border_color):
        self.alive = True
        for point in self.corners:
            # Если один из углов касается границы - машина разбивается
            if game_map.get_at((int(point[0]), int(point[1]))) == border_color:
                self.alive = False
                break

    def check_radar(self, degree, game_map, border_color, radar_length=300):
        length = 0
        x = int(
            self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
        y = int(
            self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        # Радар "смотрит" вперёд, пока не упирается в границу или не достигает в длину 300
        while not game_map.get_at((x, y)) == border_color and length < radar_length:
            length = length + 1
            x = int(
                self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * length)
            y = int(
                self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * length)

        # Считаем дистанции до границы и добавляем в лист
        dist = int(
            math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
        self.radars.append([(x, y), dist])

    def update(self, game_map, map_width, map_height, border_color):
        # Устанавливаем начальную скорость в 20
        # Только если есть возможность ускорятся и тормозить
        if not self.speed_set:
            self.speed = 20
            self.speed_set = True

        # Поворачиваем спрайт и изменяем x координату
        self.rotated_sprite = self.rotate_center(self.sprite, self.angle)
        self.position[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        # Чтобы не выйти за границу, если трасса нарисована прямо к краю
        self.position[0] = max(self.position[0], 1)
        self.position[0] = min(self.position[0], map_width - 1)

        # Изменяем y координату
        self.position[1] += math.sin(math.radians(360 -
                                     self.angle)) * self.speed
        self.position[1] = max(self.position[1], 1)
        self.position[1] = min(self.position[1], map_height - 2)

        # Увеличиваем пройденную дистанцию и время
        self.distance += self.speed
        self.time += 1

        # Вычисляем новый центр машины
        self.center = [int(self.position[0]) + self.size_x / 2,
                       int(self.position[1]) + self.size_y / 2]

        # Координаты углов машины
        length = 0.5 * self.size_x
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) *
                    length, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * length]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) *
                     length, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * length]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) *
                       length, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * length]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) *
                        length, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * length]
        self.corners = [left_top, right_top, left_bottom, right_bottom]

        # Проверяем столкновение с границей и очищаем радары
        self.check_collision(game_map, border_color)
        self.radars.clear()
        # -90 -45 0 45 90 - углы радаров
        for d in range(-90, 120, 45):
            self.check_radar(d, game_map, border_color)

    def get_data(self):
        # Вычисление дистанции до границ
        radars = self.radars
        return_values = [0, 0, 0, 0, 0]
        for i, radar in enumerate(radars):
            return_values[i] = int(radar[1] / 30)

        return return_values

    def is_alive(self):
        return self.alive

    def get_reward(self):
        return self.distance / (self.size_x / 2)

    def rotate_center(self, image, angle):
        rectangle = image.get_rect()
        rotated_image = pygame.transform.rotate(image, angle)
        rotated_rectangle = rectangle.copy()
        rotated_rectangle.center = rotated_image.get_rect().center
        rotated_image = rotated_image.subsurface(rotated_rectangle).copy()
        return rotated_image