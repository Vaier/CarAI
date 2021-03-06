# ИИ для управления игровой машиной
Версия 1.0

Авторы:

 - Епик Александр
 - Грекалов Владимир 
 - Юн Вадим 

## Описание
Данная программа обучает машину ездить по любой нарисованной дороге с помощью алгоритма NEAT и обучения с подкреплением (reinforcement learning)

Необходимые модули: requirements.txt

Установка модулей: pip install -r requirements.txt

Запуск проекта: main.py

## Содержимое файлов

**main.py:**
Main, запуск программы
		
**car.py:**
Класс машины, все свойства и методы связанные с ней. Update для обновления данных в программе и вспомогательные методы
	
**AI.py:**
Запуск симуляции, работа с модулем NEAT, создание и изменение геномов, а также получение из них действий для машины
	
**drawer.py:**
Инициализация, отрисовка карты, машин и радаров. В качестве графического модуля был использован pygame
    
**car.png:**
Спрайт машины (Сжимается до 60х60)
    
**map.png:**
Карта, на которой программа учится (Может быть изменена в любом графическом редакторе)
    
**config.ini:**
Файл с настройками для модуля NEAT
		
## Графический интерфейс

Поколение: Номер текущего поколения

Кол-во машин: Количество неразбившихся машин

## Горячие клавиши

Space (Пробел): Включение/Выключение отображения радаров

Escape: Остановка симуляции

## Примечание
* Карта может быть изменена в любом графическом редакторе. Дорога может быть любым цветом, кроме белого. Препятствия всегда белым. Циклы могут усложнить процесс обучения. Перед запуском проверьте, что стартовая позиция в car.py находится на дороге
* В папке Maps with starting coordinates находятся примеры карт с названиями в виде стартовой позиции
* В консоли выводится общая информация по каждому поколению
* Полезные ссылки:
    + https://en.wikipedia.org/wiki/Neuroevolution_of_augmenting_topologies - Описание алгоритма NEAT
    + https://en.wikipedia.org/wiki/Reinforcement_learning - Описание обучения с подкреплением
    + https://neat-python.readthedocs.io/en/latest/index.html - Информация по модулю neat-python
    + https://neat-python.readthedocs.io/en/latest/config_file.html - Информация по параметрам в файле config.ini
    + https://www.youtube.com/watch?v=qc8_nKfcKiE - Демонстрация работы
