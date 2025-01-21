import tkinter as tk
from tkinter import messagebox
import os

# Функция для загрузки настроек
def load_settings():
    """Загружает настройки из файла config.txt"""
    language = 'English'
    color1 = '#f1f1f1'  # Светлый цвет фона
    color2 = '#4caf50'  # Зеленый цвет кнопок

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
        'title': 'Delete Word by Translation',
        'translation': 'Translation:',
        'delete_word': 'Delete Word',
        'input_error': 'Please fill in the translation field!',
        'file_not_found': "The file 'logs.txt' does not exist!",
        'word_not_found': "No word found with the translation '{translation}'.",
        'success': "The word with translation '{translation}' has been deleted successfully."
    },
    'Russian': {
        'title': 'Удалить слово по переводу',
        'translation': 'Перевод:',
        'delete_word': 'Удалить слово',
        'input_error': 'Пожалуйста, заполните поле перевода!',
        'file_not_found': "Файл 'logs.txt' не существует!",
        'word_not_found': "Слово с переводом '{translation}' не найдено.",
        'success': "Слово с переводом '{translation}' успешно удалено."
    },
    # Добавьте другие языки по аналогии
}

# Функция для удаления слова по переводу
def delete_word_by_translation():
    translation = entry_translation.get().strip()
    if not translation:
        messagebox.showwarning(translations[language]['title'], translations[language]['input_error'])
        return

    found = False
    lines = []

    try:
        with open("logs.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()

        with open("logs.txt", "w", encoding="utf-8") as file:
            for line in lines:
                german_word, file_translation = line.split(' - ')
                file_translation = file_translation.strip()

                if file_translation != translation:
                    file.write(line)
                else:
                    found = True

    except FileNotFoundError:
        messagebox.showwarning(translations[language]['title'], translations[language]['file_not_found'])
        return

    if found:
        messagebox.showinfo(translations[language]['title'], translations[language]['success'].format(translation=translation))
        entry_translation.delete(0, tk.END)
    else:
        messagebox.showwarning(translations[language]['title'], translations[language]['word_not_found'].format(translation=translation))

# Загружаем настройки из файла
language, color1, color2 = load_settings()

root = tk.Tk()
root.title(translations[language]['title'])

root.geometry("400x250")  # Увеличиваем размер окна
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

# Стиль для меток и полей ввода
label_style = {
    "bg": color1,
    "font": ("Arial", 12, "bold"),
    "fg": "black"
}

entry_style = {
    "font": ("Arial", 12),
    "width": 30,
    "bd": 2,
    "relief": "solid",
    "highlightthickness": 0
}

# Центрируем окно
root.eval('tk::PlaceWindow %s center' % root.winfo_toplevel())

# Метки и поля ввода
label_translation = tk.Label(root, text=translations[language]['translation'], **label_style)
label_translation.pack(pady=10)

entry_translation = tk.Entry(root, **entry_style)
entry_translation.pack(pady=10)

# Кнопка для удаления слова
button_delete = tk.Button(root, text=translations[language]['delete_word'], **button_style, command=delete_word_by_translation)
button_delete.pack(pady=15)

root.mainloop()
