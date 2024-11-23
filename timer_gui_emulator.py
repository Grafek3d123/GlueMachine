import time
import tkinter as tk
from tkinter import font
import threading
import random

# Глобальные переменные
time_left = 421  # 7 минут и 1 секунда
count = 0  # Счётчик срабатываний
temp = 24.0  # Начальная температура
timer_running = False  # Таймер изначально остановлен
fullscreen = False  # Полноэкранный режим по умолчанию

# Функции для логики приложения
def update_timer():
    """Обновление таймера и интерфейса."""
    global time_left, timer_running
    if timer_running:
        if time_left > 0:
            time_left -= 1
            time_label.config(text=f"{time_left // 60}:{time_left % 60:02}")
        else:
            timer_running = False  # Таймер остановлен
    count_label.config(text=f"{count:02}")
    temp_label.config(text=f"{temp:.1f}°C")
    root.after(1000, update_timer)

def update_temperature():
    """Обновление температуры каждые 10 секунд."""
    global temp
    while True:
        temp += random.uniform(-0.5, 0.5)
        temp = max(15, min(temp, 30))  # Ограничиваем диапазон
        time.sleep(10)

def start_timer():
    """Обработка запуска таймера."""
    global timer_running, time_left, count
    if not timer_running:
        count += 1
        time_left = 421  # Сброс таймера
        time_label.config(text=f"{time_left // 60}:{time_left % 60:02}")
        timer_running = True

def stop_timer():
    """Обработка остановки таймера."""
    global timer_running
    timer_running = False

def toggle_mode():
    """Переключение между полноэкранным и тестовым режимами."""
    global fullscreen
    fullscreen = not fullscreen
    clear_widgets()
    if fullscreen:
        root.attributes('-fullscreen', True)
        display_fullscreen_mode()
    else:
        root.attributes('-fullscreen', False)
        root.geometry("320x320")
        display_testing_mode()

def clear_widgets():
    """Удаление всех виджетов, кроме кнопки переключения режима."""
    for widget in root.winfo_children():
        if widget != toggle_button:
            widget.destroy()

# Функции отображения режимов
def display_testing_mode():
    """Отображение тестового режима."""
    global time_label, count_label, temp_label
    time_label = tk.Label(root, text="7:01", font=large_font)
    time_label.pack()
    count_label = tk.Label(root, text="00", font=large_font)
    count_label.pack()
    temp_label = tk.Label(root, text="24°C", font=large_font)
    temp_label.pack()
    tk.Button(root, text="Сработать", font=large_font, command=start_timer).pack()
    tk.Button(root, text="Остановить", font=large_font, command=stop_timer).pack()

def display_fullscreen_mode():
    """Отображение полноэкранного режима."""
    global time_label, count_label, temp_label
    time_label = tk.Label(root, text="7:01", font=extra_large_font)
    time_label.pack()
    count_label = tk.Label(root, text="00", font=extra_large_font)
    count_label.pack()
    temp_label = tk.Label(root, text="24°C", font=extra_large_font)
    temp_label.pack()

def position_toggle_button(event=None):
    """Обновление положения кнопки переключения режима в правом верхнем углу."""
    toggle_button.place(x=root.winfo_width() - 60, y=10)

# Создание главного окна
root = tk.Tk()
root.title("Таймер")

# Шрифты
extra_large_font = font.Font(family="Helvetica", size=250, weight="bold")
large_font = font.Font(family="Helvetica", size=50, weight="bold")
small_font = font.Font(family="Helvetica", size=20, weight="bold")

# Кнопка переключения режима
toggle_button = tk.Button(root, text="↔️", font=small_font, command=toggle_mode, width=2, height=1)
toggle_button.place(x=260, y=10)

# Привязка изменения размера окна к обновлению положения кнопки
root.bind("<Configure>", position_toggle_button)

# Выбор начального режима
if fullscreen:
    display_fullscreen_mode()
else:
    display_testing_mode()

# Поток для обновления температуры
temperature_thread = threading.Thread(target=update_temperature, daemon=True)
temperature_thread.start()

# Запуск таймера
update_timer()

# Закрытие приложения по нажатию 'q'
def close_app(event):
    root.quit()

root.bind('q', close_app)

# Запуск основного цикла
root.mainloop()
