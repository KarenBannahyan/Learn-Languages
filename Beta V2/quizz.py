import tkinter as tk
from tkinter import messagebox
import random
import os

# Функция для загрузки настроек
def load_settings():
    """Загружает настройки из файла config.txt"""
    language = 'English'
    color1 = '#f0f4f4'  # Светлый фон
    color2 = '#4caf50'  # Зеленый цвет для кнопок

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
        'title': 'German Translation Quiz',
        'num_words': 'Number of words to translate:',
        'start_quiz': 'Start Quiz',
        'enter_num_words': 'Enter number of words to start',
        'check_answer': 'Check Answer',
        'input_error': 'Please enter a valid number!',
        'file_not_found': "The file 'logs.txt' does not exist!",
        'no_words': "The file 'logs.txt' is empty!",
        'invalid_number': "Please enter a number between 1 and {max}",
        'quiz_finished': "Quiz Finished",
        'quiz_results': "You answered {correct}/{total} correctly.\nAccuracy: {accuracy:.2f}%",
        'wrong_format': "Invalid format in file line: {line}",
    },
    'Russian': {
        'title': 'Тест на перевод с немецкого',
        'num_words': 'Количество слов для перевода:',
        'start_quiz': 'Начать тест',
        'enter_num_words': 'Введите количество слов для начала',
        'check_answer': 'Проверить ответ',
        'input_error': 'Пожалуйста, введите правильное число!',
        'file_not_found': "Файл 'logs.txt' не существует!",
        'no_words': "Файл 'logs.txt' пуст!",
        'invalid_number': "Пожалуйста, введите число от 1 до {max}",
        'quiz_finished': "Тест завершен",
        'quiz_results': "Вы правильно ответили на {correct}/{total} вопросов.\nТочность: {accuracy:.2f}%",
        'wrong_format': "Неверный формат в строке файла: {line}",
    },
}

# Функция для начала викторины
def start_quiz():
    try:
        with open("logs.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        messagebox.showerror(translations[language]['title'], translations[language]['file_not_found'])
        return

    if not lines:
        messagebox.showwarning(translations[language]['title'], translations[language]['no_words'])
        return

    try:
        num_words = int(entry_num_words.get())
        if num_words <= 0 or num_words > len(lines):
            messagebox.showwarning(translations[language]['title'], translations[language]['invalid_number'].format(max=len(lines)))
            return
    except ValueError:
        messagebox.showwarning(translations[language]['title'], translations[language]['input_error'])
        return

    random_words = random.sample(lines, num_words)

    correct_answers = 0
    total_answers = num_words

    questions = []
    answers = []

    for line in random_words:
        try:
            german_word, translation = line.strip().split(' - ')
        except ValueError:
            messagebox.showerror(translations[language]['title'], translations[language]['wrong_format'].format(line=line.strip()))
            return
        questions.append(german_word)
        answers.append(translation)

    def check_answer():
        nonlocal correct_answers

        user_answer = entry_answer.get().strip()
        current_question_index = question_index[0]

        if user_answer.lower() == answers[current_question_index].lower():
            correct_answers += 1

        question_index[0] += 1

        if question_index[0] < total_answers:
            question_label.config(text=f"Translate this word: {questions[question_index[0]]}")
            entry_answer.delete(0, tk.END)
        else:
            accuracy = (correct_answers / total_answers) * 100
            messagebox.showinfo(translations[language]['quiz_finished'], translations[language]['quiz_results'].format(correct=correct_answers, total=total_answers, accuracy=accuracy))
            root.quit()

    question_index = [0]

    question_label.config(text=f"Translate this word: {questions[question_index[0]]}")
    entry_answer.delete(0, tk.END)

    button_check.config(state=tk.NORMAL, command=check_answer)

# Загружаем настройки из файла
language, color1, color2 = load_settings()

root = tk.Tk()
root.title(translations[language]['title'])

root.geometry("450x350")  # Увеличиваем размер окна
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
    "font": ("Arial", 12, "bold"),  # Жирный шрифт
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
label_num_words = tk.Label(root, text=translations[language]['num_words'], **label_style)
label_num_words.pack(pady=10)

entry_num_words = tk.Entry(root, **entry_style)
entry_num_words.pack(pady=10)

button_start = tk.Button(root, text=translations[language]['start_quiz'], **button_style, command=start_quiz)
button_start.pack(pady=15)

question_label = tk.Label(root, text=translations[language]['enter_num_words'], **label_style)
question_label.pack(pady=20)

entry_answer = tk.Entry(root, **entry_style)
entry_answer.pack(pady=10)

button_check = tk.Button(root, text=translations[language]['check_answer'], **button_style, state=tk.DISABLED)
button_check.pack(pady=15)

root.mainloop()
