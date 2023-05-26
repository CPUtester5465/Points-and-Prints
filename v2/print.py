import pygame
import pandas as pd
import numpy as np


def read_data(filename):
    try:
        with open(filename, 'r') as file:
            # Используем параметр header=None, чтобы Pandas не считал первую строкуоловком
            return pd.read_csv(file, header=None)
    except FileNotFoundError:
        print(f'File {filename} not found')
        return None

def draw_polygon(screen, points, polygon_color):
    from pygame import gfxdraw
    for point in points:
        gfxdraw.pixel(screen, int(point[0]), int(point[1]), polygon_color)

def print_points(points):
    points = np.array(points)
    np.set_printoptions(suppress=True)
    np.savetxt('points_converted.csv', points, delimiter=',', fmt='%.2f')

def calculate_centroid(points):
    x = [point[0] for point in points]
    y = [point[1] for point in points]
    centroid_x = sum(x) / len(points)
    centroid_y = sum(y) / len(points)
    return (centroid_x, centroid_y)

def main():
    # Инициализируем pygame
    pygame.init()

    # Устанавливаем размеры окна
    size = (900, 900)
    screen = pygame.display.set_mode(size)

    # Устанавливаем заголовок окна
    pygame.display.set_caption("My Game")

    # Устанавливаем белый цвет фона
    background_color = (255, 255, 255)

    # Считываем данные из файла CSV
    data = read_data('file.csv')
    if data is None:
        return

    # Создаем список точек
    points = []
    for index, row in data.iterrows():
        # Исправляем ошибку: используем правильные индексы столбцов
        points.append((row[0], row[1]))

    # Рассчитываем центр масс многоугольника
    centroid = calculate_centroid(points)
    print(f'Центр масс многоугольника: {centroid}')

    # Запускаем игровой цикл
    done = False
    polygon_color = (0, 0, 255)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True

        # Заливаем фон белым цветом
        screen.fill(background_color)

        # Рисуем фигуру по точкам
        print_points(points)
        draw_polygon(screen, points, polygon_color)

        # Рисуем центр масс многоугольника
        pygame.draw.circle(screen, (255, 0, 0), (int(centroid[0]), int(centroid[1])), 5)

        # Отображаем изменения на экране
        pygame.display.flip()

    # Выходим из pygame
    pygame.quit()

if __name__ == '__main__':
    main()