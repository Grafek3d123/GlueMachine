import time
import tkinter as tk
from tkinter import font
import board
import adafruit_htu21d
from gpiozero import Button
import threading

# Инициализация датчика температуры и влажности HTU21D
i2c = board.I2C()
sensor = adafruit_htu21d.HTU21D(i2c)

# Инициализация переменных
time_left = 421  # 7 минут и 1 секунда в секундах (421 секунда)
count = 0  # Счётчик срабатываний
temp = 99  # Температура, изначально 99°C
timer_running = False  # Таймер изначально остановлен
fullscreen = False  # Начальный режим: тестирование

# Настройка GPIO кнопок
start_button = Button(17, pull_up=True)  # Кнопка запуска таймера (GPIO 17)
stop_button = Button(27, pull_up=True)   # Кнопка остановки таймера (GPIO 27)

# Функция для обновления таймера
def update_timer():
    global time_left, timer_running

    if timer_running:  # Если таймер запущен
        if time_left > 0:
            time_left -= 1
            time_label.config(text=f"{time_left // 60}:{time_left % 60:02}")
        else:
            timer_running = False  # Останавливаем таймер, если время вышло

    count_label.config(text=f"{count:02}")
    temp_label.config(text=f"{temp:.1f}°C")

    # Повторное обновление через 1 секунду
    root.after(1000, update_timer)

# Функция для обновления температуры каждые 10 секунд
def update_temperature():
    global temp
    while True:
        temp = sensor.temperature  # Чтение температуры с датчика
        time.sleep(10)

# Функция для обработки нажатия кнопки запуска
def start_button_pressed():
    global timer_running, time_left, count

    if not timer_running:  # Если таймер остановлен
        count += 1  # Увеличиваем счётчик
        time_left = 421  # Сбрасываем таймер на 7 минут и 1 секунду
        time_label.config(text=f"{time_left // 60}:{time_left % 60:02}")  # Обновляем отображение времени
        timer_running = True  # Запускаем таймер

# Функция для обработки нажатия кнопки остановки
def stop_button_pressed():
    global timer_running
    timer_running = False  # Останавливаем таймер

# Функция переключения между режимами
def toggle_mode():
    global fullscreen
    fullscreen = not fullscreen

    # Очистка окна
    for widget in root.winfo_children():
        widget.destroy()

    # Переключение между режимами
    if fullscreen:
        root.attributes('-fullscreen', True)
        display_fullscreen_mode()
    else:
        root.attributes('-fullscreen', False)
        display_testing_mode()

# Функция для размещения кнопки переключения режима
def position_toggle_button():
    toggle_button.place(x=root.winfo_width() - 60, y=10)

# Функция отображения элементов в тестовом режиме
def display_testing_mode():
    global time_label, count_label, temp_label, toggle_button

    # Метка времени
    time_label = tk.Label(root, text="7:01", font=large_font)
    time_label.pack()

    # Метка счётчика
    count_label = tk.Label(root, text="00", font=large_font)
    count_label.pack()

    # Метка температуры
    temp_label = tk.Label(root, text="99°C", font=large_font)
    temp_label.pack()

    # Кнопка "Сработать"
    start_button_gui = tk.Button(root, text="Сработать", font=large_font, command=start_button_pressed)
    start_button_gui.pack()

    # Кнопка "Остановить"
    stop_button_gui = tk.Button(root, text="Остановить", font=large_font, command=stop_button_pressed)
    stop_button_gui.pack()

    # Кнопка переключения режима
    toggle_button = tk.Button(root, text="🔄", font=small_font, command=toggle_mode, width=2, height=1)
    position_toggle_button()  # Устанавливаем положение кнопки

# Функция отображения элементов в полноэкранном режиме
def display_fullscreen_mode():
    global time_label, count_label, temp_label, toggle_button

    # Метка времени
    time_label = tk.Label(root, text="7:01", font=font.Font(family="Helvetica", size=250, weight="bold"))
    time_label.pack()

    # Метка счётчика
    count_label = tk.Label(root, text="00", font=font.Font(family="Helvetica", size=250, weight="bold"))
    count_label.pack()

    # Метка температуры
    temp_label = tk.Label(root, text="99°C", font=font.Font(family="Helvetica", size=250, weight="bold"))
    temp_label.pack()

    # Кнопка переключения режима
    toggle_button = tk.Button(root, text="🔄", font=small_font, command=toggle_mode, width=2, height=1)
    position_toggle_button()  # Устанавливаем положение кнопки

# Создание главного окна
root = tk.Tk()
root.title("Таймер")
root.geometry("800x480")  # Размер окна для тестирования

# Настройка шрифтов
large_font = font.Font(family="Helvetica", size=50, weight="bold")
small_font = font.Font(family="Helvetica", size=20, weight="bold")

# Отображение элементов в тестовом режиме по умолчанию
display_testing_mode()

# Привязываем изменение размера окна к обновлению положения кнопки
root.bind("<Configure>", lambda event: position_toggle_button())

# Запуск потока для обновления температуры
temperature_thread = threading.Thread(target=update_temperature, daemon=True)
temperature_thread.start()

# Запуск обновления таймера
update_timer()

# Привязываем кнопки к функциям
start_button.when_pressed = start_button_pressed
stop_button.when_pressed = stop_button_pressed

# Функция для закрытия приложения
def close_app(event):
    root.quit()

# Привязываем нажатие клавиши 'q' к функции закрытия
root.bind('q', close_app)

# Запуск главного цикла программы
root.mainloop()

