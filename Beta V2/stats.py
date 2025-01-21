import tkinter as tk
from tkinter import messagebox, filedialog
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
        'title': 'Dictionary App',
        'word_count': 'Word count: ',
        'error': 'Error',
        'file_not_found': 'File not found: ',
    },
    'Russian': {
        'title': 'Приложение для словаря',
        'word_count': 'Количество слов: ',
        'error': 'Ошибка',
        'file_not_found': 'Файл не найден: ',
    },
}

# Функция для загрузки содержимого файла
def load_file():
    # Получаем путь к файлу logs.txt в той же директории, что и скрипт
    filepath = os.path.join(os.path.dirname(__file__), "logs.txt")

    try:
        # Открываем файл и читаем его содержимое
        with open(filepath, 'r', encoding='utf-8') as file:
            content = file.readlines()

        # Выводим количество строк в файле (слова с переводами)
        word_count = len(content)
        word_count_label.config(text=f"{translations[language]['word_count']} {word_count}")

        # Отображаем содержимое файла в текстовом виджете
        text_area.delete(1.0, tk.END)
        text_area.insert(tk.END, "".join(content))

    except FileNotFoundError:
        messagebox.showerror(translations[language]['error'], f"{translations[language]['file_not_found']} logs.txt")
        word_count_label.config(text="0")
        text_area.delete(1.0, tk.END)

# Загружаем настройки из файла
language, color1, color2 = load_settings()

# Создаем главное окно
root = tk.Tk()
root.title(translations[language]['title'])
root.geometry("600x400")  # Размер окна
root.configure(bg=color1)

# Стиль кнопок
button_style = {
    "bg": color2,
    "fg": "white",
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

# Заголовок
header_label = tk.Label(root, text=translations[language]['title'], font=("Arial", 16, "bold"), fg='black', bg=color1)
header_label.pack(pady=20)

# Метка для количества слов
word_count_label = tk.Label(root, text=f"{translations[language]['word_count']} 0", font=("Arial", 12), bg=color1)
word_count_label.pack(pady=10)

# Кнопка загрузки файла
load_button = tk.Button(root, text="Load Dictionary", **button_style, command=load_file)
load_button.pack(pady=10)

# Создаем фрейм для текстовой области и скроллбар
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

# Текстовое поле с прокруткой
text_area = tk.Text(frame, wrap=tk.WORD, height=10, width=50)
text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Скроллбар, который привязан к текстовой области
scrollbar = tk.Scrollbar(frame, command=text_area.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

# Связка скроллбара с текстовой областью
text_area.config(yscrollcommand=scrollbar.set)

# Запускаем функцию загрузки файла при старте
load_file()

# Запускаем главный цикл приложения
root.mainloop()
