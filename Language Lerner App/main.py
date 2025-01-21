import customtkinter as ctk
from tkinter import messagebox
from PIL import Image
import subprocess
import os

def load_settings():
    language = 'English'
    color1 = '#FFFFFF'
    color2 = '#4caf50'  

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

translations = {
    'English': {
        'title': 'Language Learning App',
        'add_word': 'Add new word',
        'delete_word': 'Delete word',
        'fast_quiz': 'Fast quiz',
        'settings': 'Settings',
        'error': 'Error',
        'cant_add_word': "Can't add a new word: ",
        'cant_delete_word': "Can't delete word: ",
        'cant_open_quiz': "Can't open quiz: ",
        'cant_open_settings': "Can't open settings: ",
        'cant_open_card': "Cant_open_card",
        'statistics': 'Statistics',
        'search': 'Search word in vocabulary',
        'not_found': 'not found',
        'profile': 'User Profile',
        'card': 'Cards',
        'topic': 'Themes'
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
        'cant_open_card': 'Не удалось открыть карту',
        'statistics': 'Статистика',
        'search': 'Поиск слова в словаре',
        'not_found': 'не найдено',
        'profile': 'Профиль пользователя',
        'card': 'Карты',
        'topic': 'Темы'
    },
}

def open_script(script_name, error_key):
    try:
        subprocess.Popen(['python', os.path.join(os.getcwd(), script_name)])
    except Exception as e:
        messagebox.showerror(translations[language]['error'], f"{translations[language][error_key]} {e}")

language, color1, color2 = load_settings()

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

root = ctk.CTk()
root.title(translations[language]['title'])
root.geometry("800x600")

root.configure(bg=color1)

menu_frame = ctk.CTkFrame(root, width=200, corner_radius=0)
menu_frame.pack(side="left", fill="y")

menu_buttons = [
    (translations[language]['add_word'], lambda: open_script('text.py', 'cant_add_word')),
    (translations[language]['delete_word'], lambda: open_script('pop.py', 'cant_delete_word')),
    (translations[language]['fast_quiz'], lambda: open_script('quizz.py', 'cant_open_quiz')),
    (translations[language]['settings'], lambda: open_script('settings.py', 'cant_open_settings')),
    (translations[language]['statistics'], lambda: open_script('stats.py', 'cant_open_stats')),
    (translations[language]['card'], lambda: open_script('card.py', 'cant_open_card')),
    (translations[language]['topic'], lambda: open_script('themes.py', 'cant_open_topic')),
]

for text, command in menu_buttons:
    button = ctk.CTkButton(menu_frame, text=text, command=command, fg_color=color2)
    button.pack(pady=10, padx=10, fill="x")

search_frame = ctk.CTkFrame(root)
search_frame.pack(pady=20)

search_label = ctk.CTkLabel(search_frame, text=translations[language]['search'], font=("Arial", 14))
search_label.grid(row=0, column=0, padx=10)

search_entry = ctk.CTkEntry(search_frame, width=300)
search_entry.grid(row=0, column=1, padx=10)

def search_word():
    query = search_entry.get().strip().lower()
    if not query:
        return

    try:
        with open("logs.txt", "r", encoding="utf-8") as file:
            results_textbox.delete("0.0", "end")
            found = False
            for line in file:
                if query in line.lower():
                    results_textbox.insert("end", line)
                    found = True
            if not found:
                results_textbox.insert("end", f"{translations[language]['search']} '{query}' {translations[language]['not_found']}\n")
    except FileNotFoundError:
        messagebox.showerror(translations[language]['error'], "logs.txt file not found.")

search_button = ctk.CTkButton(search_frame, text="Search", command=search_word, fg_color=color2)
search_button.grid(row=0, column=2, padx=10)

results_frame = ctk.CTkFrame(root)
results_frame.pack(pady=10, fill="both", expand=True)

results_textbox = ctk.CTkTextbox(results_frame, height=200, font=("Arial", 12))
results_textbox.pack(fill="both", expand=True, padx=10, pady=10)

root.mainloop()
