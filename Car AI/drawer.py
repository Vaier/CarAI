import pygame
import neat

from car import Car

class Drawer:
    def __init__(self, WIDTH, HEIGHT, cars, radar_visibility):
        # Инициализация
        pygame.init()
        self.cars = cars
        self.current_width = WIDTH, 
        self.current_height = HEIGHT
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
        self.generation_font = pygame.font.SysFont("Arial", 30)
        self.alive_font = pygame.font.SysFont("Arial", 20)
        self.game_map = pygame.image.load('map.png').convert()
        self.radar_visibility = radar_visibility

    def draw_car(self, car):
        self.screen.blit(car.rotated_sprite, car.position) # Отрисовка спрайтов
        self.draw_radar(car) #Отрисовка радаров (Необязательно)

    def draw_radar(self, car):
        if (self.radar_visibility == 0):
            return
        for radar in car.radars:
            position = radar[0]
            pygame.draw.line(self.screen, (0, 255, 0), car.center, position, 1)
            pygame.draw.circle(self.screen, (0, 255, 0), position, 5)

    def draw_screen(self, current_generation, still_alive):
        self.screen.blit(self.game_map, (0, 0))
        for car in self.cars:
            if car.is_alive():
                self.draw_car(car)
        
        # Текст на экране
        text = self.generation_font.render("Generation: " + str(current_generation), True, (0,0,0))
        text_rect = text.get_rect()
        text_rect.center = (900, 450)
        self.screen.blit(text, text_rect)

        text = self.alive_font.render("Still Alive: " + str(still_alive), True, (0, 0, 0))
        text_rect = text.get_rect()
        text_rect.center = (900, 490)
        self.screen.blit(text, text_rect)

        pygame.display.flip()

    def change_radar_visibility(self):
        self.radar_visibility = (self.radar_visibility + 1) % 2

