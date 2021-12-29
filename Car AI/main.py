from AI import run_simulation
import neat

if __name__ == "__main__":
    
    # Подгрузка config файла для neat
    config_path = "./config.ini"
    config = neat.config.Config(neat.DefaultGenome,
                                neat.DefaultReproduction,
                                neat.DefaultSpeciesSet,
                                neat.DefaultStagnation,
                                config_path)

    # Начальное создание объектов
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    population.add_reporter(stats)
    
    # Запуск симуляции в максимум 1000 поколений
    population.run(run_simulation, 1000)
