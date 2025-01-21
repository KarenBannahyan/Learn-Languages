import customtkinter as ctk
import os
from tkinter import messagebox

def load_settings():
    """Загружает настройки из файла config.txt"""
    language = 'English'
    color1 = '#f1f1f1'
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
}

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
        entry_translation.delete(0, ctk.END)
    else:
        messagebox.showwarning(translations[language]['title'], translations[language]['word_not_found'].format(translation=translation))

language, color1, color2 = load_settings()

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title(translations[language]['title'])
root.geometry("400x250")

root.eval('tk::PlaceWindow %s center' % root.winfo_toplevel())

label_translation = ctk.CTkLabel(root, text=translations[language]['translation'], font=("Arial", 12, "bold"))
label_translation.pack(pady=10)

entry_translation = ctk.CTkEntry(root, placeholder_text="Enter translation", width=300, font=("Arial", 12))
entry_translation.pack(pady=10)

button_delete = ctk.CTkButton(root, text=translations[language]['delete_word'], command=delete_word_by_translation,
                              width=200, height=40, font=("Arial", 12, "bold"))
button_delete.pack(pady=15)

root.mainloop()
