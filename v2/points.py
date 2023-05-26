import cv2
import numpy as np

# Загружаем изображение
img = cv2.imread('image.png')

# Преобразуем изображение в черно-белый формат
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Применяем бинаризацию для выделения точек
_, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)

# Ием контуры точек
contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

# Создаем массив для хранения координат точек
points = []

# Извлекаем координаты точек из контуров
for contour in contours:
    for point in contour:
        x, y = point[0]
        # Форматируем координаты в целое число mod 1000
        x_mod = x % 1000
        y_mod = y % 1000
        points.append([x_mod, y_mod])

# Преобразуем массив точек в массив NumPy
points = np.array(points)

# Настраиваем формат вывода
np.set_printoptions(suppress=True)

# Сохраняем координаты точек в файл
np.savetxt('points.csv', points, delimiter=',', fmt='%.2f')