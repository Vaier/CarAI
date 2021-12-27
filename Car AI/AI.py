import pygame
import neat
from car import Car
from drawer import Drawer
import sys
sys.path.append(".")


#Размер карты
WIDTH = 1920
HEIGHT = 1080

CAR_SIZE_X = 60
CAR_SIZE_Y = 60

BORDER_COLOR = (255, 255, 255, 255)  # Цвет границы

current_generation = 0  # Счётчик поколений

radar_visibility = 1

def run_simulation(genomes, config):

    # Листы сетей и машин
    nets = []
    cars = []

    global radar_visibility

    drawer = Drawer(WIDTH, HEIGHT, cars, radar_visibility)

    game_map = drawer.game_map
    clock = pygame.time.Clock()

    # Создаём новую сеть для каждого генома
    for i, g in genomes:
        net = neat.nn.FeedForwardNetwork.create(g, config)
        nets.append(net)
        g.fitness = 0
        sprite = pygame.image.load('car.png').convert_alpha()
        sprite = pygame.transform.scale(sprite, (CAR_SIZE_X, CAR_SIZE_Y))
        cars.append(Car(sprite, CAR_SIZE_X, CAR_SIZE_Y))

    global current_generation
    current_generation += 1

    # Счётчик для ограничения по времени
    counter = 0

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(0)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    sys.exit(0)
                if event.key == pygame.K_SPACE:
                    drawer.change_radar_visibility()
                    radar_visibility = (radar_visibility + 1) % 2

        # Для каждой машины получаем действие
        for i, car in enumerate(cars):
            output = nets[i].activate(car.get_data())
            choice = output.index(max(output))
            if choice == 0:
                car.angle += 10  # Влево
            elif choice == 1:
                car.angle -= 10  # Вправо
            elif choice == 2:
                if(car.speed - 2 >= 12):
                    car.speed -= 2  # Тормоз
            else:
                car.speed += 2  # Газ

        # Проверка не разбилась ли машина
        # Вознаградить если жива, уничтожить, если нет
        still_alive = 0
        for i, car in enumerate(cars):
            if car.is_alive():
                still_alive += 1
                car.update(game_map, WIDTH, HEIGHT, BORDER_COLOR)
                genomes[i][1].fitness += car.get_reward()

        if still_alive == 0:
            break

        counter += 1
        if counter == 30 * 40:  # ~20 секунд
            break

        # Отображение карты и машин
        drawer.draw_screen(current_generation, still_alive)

        clock.tick(60)