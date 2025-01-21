import tkinter as tk
from tkinter import messagebox
import os

# Функция для загрузки настроек
def load_settings():
    """Загружает настройки из файла config.txt, если файл существует"""
    language = 'English'
    color1 = '#f0f0f0'  # Светлый серый цвет фона
    color2 = '#607d8b'  # Цвет кнопок (светло-серый с голубым оттенком)

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

# Словарь переводов для разных языков
translations = {
    'English': {
        'title': 'German Word and Translation Input',
        'german_word': 'German Word:',
        'translation': 'Translation:',
        'save_word': 'Save Word',
        'input_error': 'Please fill in both fields!',
        'duplicate_entry': 'This word and translation already exist!',
        'success': "Word '{word}' with translation '{translation}' saved successfully!"
    },
    'Russian': {
        'title': 'Ввод немецкого слова и перевода',
        'german_word': 'Немецкое слово:',
        'translation': 'Перевод:',
        'save_word': 'Сохранить слово',
        'input_error': 'Пожалуйста, заполните оба поля!',
        'duplicate_entry': 'Это слово и перевод уже существуют!',
        'success': "Слово '{word}' с переводом '{translation}' успешно сохранено!"
    },
    # Добавьте другие языки по аналогии
}

# Функция для сохранения слова
def save_word():
    german_word = entry_german.get().strip()
    translation = entry_translation.get().strip()

    if not german_word or not translation:
        messagebox.showwarning(translations[language]['title'], translations[language]['input_error'])
        return

    try:
        with open("logs.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                if german_word == line.split(' - ')[0] and translation == line.split(' - ')[1].strip():
                    messagebox.showwarning(translations[language]['title'], translations[language]['duplicate_entry'])
                    return
    except FileNotFoundError:
        pass

    with open("logs.txt", "a", encoding="utf-8") as file:
        file.write(f"{german_word} - {translation}\n")

    entry_german.delete(0, tk.END)
    entry_translation.delete(0, tk.END)

    messagebox.showinfo(translations[language]['title'], translations[language]['success'].format(word=german_word, translation=translation))

# Загрузка настроек
language, color1, color2 = load_settings()

root = tk.Tk()
root.title(translations[language]['title'])

root.geometry("450x300")  # Увеличиваем размер окна
root.configure(bg=color1)

# Центрируем окно
root.eval('tk::PlaceWindow %s center' % root.winfo_toplevel())

# Стиль кнопок и элементов
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

# Стиль меток с улучшением дизайна
label_style = {
    "bg": color1,
    "font": ("Arial", 14, "bold"),  # Сделаем шрифт жирным и немного крупнее
    "fg": "#333333",  # Темно-серый цвет для текста
    "padx": 10,  # Добавляем немного отступов
    "pady": 5  # Параметры отступов для меток
}

# Стиль полей ввода
entry_style = {
    "font": ("Arial", 12),
    "width": 30,
    "bd": 2,
    "relief": "solid",
    "highlightthickness": 0
}

# Метки и поля ввода
label_german = tk.Label(root, text=translations[language]['german_word'], **label_style)
label_german.pack(pady=10)

entry_german = tk.Entry(root, **entry_style)
entry_german.pack(pady=5)

label_translation = tk.Label(root, text=translations[language]['translation'], **label_style)
label_translation.pack(pady=10)

entry_translation = tk.Entry(root, **entry_style)
entry_translation.pack(pady=5)

# Кнопка сохранения
button_save = tk.Button(root, text=translations[language]['save_word'], **button_style, command=save_word)
button_save.pack(pady=20)

root.mainloop()
