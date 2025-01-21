import tkinter as tk
from tkinter import messagebox
from tkinter import Toplevel
from PIL import Image, ImageTk
import subprocess
import os

# Функция для загрузки настроек
def load_settings():
    """Загружает настройки из файла config.txt"""
    language = 'English'
    color1 = '#f5f5f5'  # Цвет фона по умолчанию (светлый)
    color2 = '#4caf50'  # Цвет кнопок по умолчанию (зеленый)

    if os.path.exists("config.txt"):
        with open("config.txt", "r", encoding="utf-8") as file:
            for line in file:
                if line.startswith("language="):
                    language = line.strip().split("=")[1]
                if line.startswith("color1="):
                    color1 = line.strip().split("=")[1]
                if line.startswith("color2="):
                    color2 = line.strip().split("=")[1]

    return language, color1, color2


# Словарь переводов
translations = {
    'English': {
        'title': 'Language Learning App',
        'add_word': 'Add new word',
        'delete_word': 'Delete word',
        'fast_quiz': 'Fast quiz',
        'settings': 'Settings',
        'error': 'Error',
        'cant_add_word': 'Cant add a new word: ',
        'cant_delete_word': 'Cant delete word: ',
        'cant_open_quiz': 'Cant open quiz: ',
        'cant_open_settings': 'Cant open settings: ',
        'statistics': 'Statistics',
        'search': 'Search word in logs.txt',
        'not_found': 'not found',
        'profile': 'User Profile'
    },
    'Russian': {
        'title': 'Приложение для изучения языка',
        'add_word': 'Добавить новое слово',
        'delete_word': 'Удалить слово',
        'fast_quiz': 'Быстрый тест',
        'settings': 'Настройки',
        'error': 'Ошибка',
        'cant_add_word': 'Не удалось добавить новое слово: ',
        'cant_delete_word': 'Не удалось удалить слово: ',
        'cant_open_quiz': 'Не удалось открыть тест: ',
        'cant_open_settings': 'Не удалось открыть настройки: ',
        'statistics': 'Статистика',
        'search': 'Поиск слова в logs.txt',
        'not_found': 'не найдено',
        'profile': 'Профиль пользователя'
    },
}

# Функции для открытия других скриптов
def add_new_word():
    try:
        current_dir = os.path.dirname(os.path.realpath(__file__))  # Получаем директорию с текущим файлом
        subprocess.Popen(['python', os.path.join(current_dir, 'text.py')])
    except Exception as e:
        messagebox.showerror(translations[language]['error'], f"{translations[language]['cant_add_word']} {e}")

def delete_word():
    try:
        current_dir = os.path.dirname(os.path.realpath(__file__))  # Получаем директорию с текущим файлом
        subprocess.Popen(['python', os.path.join(current_dir, 'pop.py')])
    except Exception as e:
        messagebox.showerror(translations[language]['error'], f"{translations[language]['cant_delete_word']} {e}")

def fast_quiz():
    try:
        current_dir = os.path.dirname(os.path.realpath(__file__))  # Получаем директорию с текущим файлом
        subprocess.Popen(['python', os.path.join(current_dir, 'quizz.py')])
    except Exception as e:
        messagebox.showerror(translations[language]['error'], f"{translations[language]['cant_open_quiz']} {e}")

def settings():
    try:
        current_dir = os.path.dirname(os.path.realpath(__file__))  # Получаем директорию с текущим файлом
        subprocess.Popen(['python', os.path.join(current_dir, 'settings.py')])
    except Exception as e:
        messagebox.showerror(translations[language]['error'], f"{translations[language]['cant_open_settings']} {e}")

def stats():
    try:
        current_dir = os.path.dirname(os.path.realpath(__file__))  # Получаем директорию с текущим файлом
        subprocess.Popen(['python', os.path.join(current_dir, 'stats.py')])
    except Exception as e:
        messagebox.showerror(translations[language]['error'], f"{translations[language]['cant_open_stats']} {e}")

# Функция для анимации меню
def toggle_menu():
    if menu_frame.winfo_x() < 0:
        menu_frame.place(x=0, y=0)
        root.after(20, slide_in)
    else:
        slide_out()

def slide_in():
    if menu_frame.winfo_x() < -250:
        menu_frame.place(x=menu_frame.winfo_x() + 15, y=0)
        root.after(10, slide_in)
    else:
        menu_button.config(state=tk.NORMAL)

def slide_out():
    if menu_frame.winfo_x() > -250:
        menu_frame.place(x=menu_frame.winfo_x() - 15, y=0)
        root.after(10, slide_out)
    else:
        menu_button.config(state=tk.NORMAL)

# Функция для поиска в logs.txt
def search_word():
    search_query = search_entry.get().strip().lower()  # Получаем текст из поисковой строки
    results.delete(1.0, tk.END)  # Очищаем старые результаты
    if search_query:
        try:
            with open("logs.txt", "r", encoding="utf-8") as file:
                found = False
                for line in file:
                    if search_query in line.lower():
                        results.insert(tk.END, line)  # Добавляем найденное слово в текстовое поле
                        found = True
                if not found:
                    results.insert(tk.END, f"{translations[language]['search']} '{search_query}' {translations[language]['not_found']}\n")
        except FileNotFoundError:
            messagebox.showerror(translations[language]['error'], "logs.txt file not found.")
        except Exception as e:
            messagebox.showerror(translations[language]['error'], f"Error: {e}")

# Функция для открытия окна профиля
def open_profile():
    profile_window = Toplevel(root)
    profile_window.title(translations[language]['profile'])
    profile_window.geometry("400x300")

    label = tk.Label(profile_window, text=translations[language]['profile'], font=("Arial", 16))
    label.pack(pady=20)

    # Здесь можно добавить элементы профиля пользователя (например, имя, настройки и т.д.)
    profile_info = tk.Label(profile_window, text="User Profile Information", font=("Arial", 12))
    profile_info.pack(pady=10)

# Загружаем настройки из файла
language, color1, color2 = load_settings()

root = tk.Tk()
root.title(translations[language]['title'])
root.resizable(False, False)
root.geometry("700x500")  # Увеличиваем размер окна для лучшего отображения
root.configure(bg=color1)

# Стиль кнопок
button_style = {
    "bg": color2,  # Зеленый фон для кнопок
    "fg": "white",  # Белый текст
    "font": ("Arial", 12, "bold"),
    "relief": "raised",
    "width": 20,
    "height": 2,
    "activebackground": "#45a049",
    "activeforeground": "white",
    "bd": 2,
    "highlightthickness": 0,
    "padx": 10,
    "pady": 5
}

# Панель меню (по умолчанию скрыта, светло-голубой фон)
menu_frame = tk.Frame(root, bg="#ADD8E6", width=250, height=500)  # Светло-голубой фон
menu_frame.place(x=-250, y=0)

# Вставляем иконку меню (три линии)
menu_button = tk.Canvas(root, width=30, height=30, bg=color1, bd=0, highlightthickness=0)
menu_button.create_line(5, 5, 25, 5, width=3, fill='black')
menu_button.create_line(5, 15, 25, 15, width=3, fill='black')
menu_button.create_line(5, 25, 25, 25, width=3, fill='black')
menu_button.place(x=10, y=10)
menu_button.bind("<Button-1>", lambda event: toggle_menu())

# Поисковая строка (сдвигаем вправо)
search_label = tk.Label(root, text=translations[language]['search'], bg=color1, font=("Arial", 12))
search_label.place(x=250, y=50)  # Отступ 250 пикселей вправо, 50 пикселей от верха

search_entry = tk.Entry(root, font=("Arial", 12), width=30)
search_entry.place(x=250, y=80)  # Отступ 250 пикселей вправо, 80 пикселей от верха

search_button = tk.Button(root, text="Search", bg=color2, fg="white", font=("Arial", 12), command=search_word)
search_button.place(x=250, y=120)  # Отступ 250 пикселей вправо, 120 пикселей от верха

# Текстовое поле для отображения результатов поиска
results = tk.Text(root, width=30, height=15, wrap=tk.WORD, font=("Arial", 12))
results.place(x=250, y=160)  # Отступ 250 пикселей вправо, 160 пикселей от верха

# Кнопки в меню (с белым фоном, отступы между кнопками)
button_add = tk.Button(menu_frame, text=translations[language]['add_word'], **button_style, command=add_new_word)
button_add.pack(pady=(50, 10))  # Первая кнопка с отступом в 50 пикселей сверху

button_delete = tk.Button(menu_frame, text=translations[language]['delete_word'], **button_style, command=delete_word)
button_delete.pack(pady=10)

button_quiz = tk.Button(menu_frame, text=translations[language]['fast_quiz'], **button_style, command=fast_quiz)
button_quiz.pack(pady=10)

button_settings = tk.Button(menu_frame, text=translations[language]['settings'], **button_style, command=settings)
button_settings.pack(pady=10)

button_stats = tk.Button(menu_frame, text=translations[language]['statistics'], **button_style, command=stats)
button_stats.pack(pady=10)

# Добавляем круг с изображением пользователя в правый верхний угол
profile_image = Image.open("user.jpg")  # Замените на свой путь к изображению
profile_image = profile_image.resize((40, 40), Image.Resampling.LANCZOS)  # Уменьшаем изображение до 40x40 пикселей

# Обрезаем изображение в круг
mask = Image.new('L', profile_image.size, 0)
mask.paste(255, (0, 0, profile_image.size[0], profile_image.size[1]))
profile_image = Image.composite(profile_image, Image.new("RGBA", profile_image.size), mask)

profile_image_tk = ImageTk.PhotoImage(profile_image)

# Отображаем изображение пользователя
profile_button = tk.Button(root, image=profile_image_tk, bd=0, highlightthickness=0, command=open_profile)
profile_button.place(x=660, y=10)

root.mainloop()
