import customtkinter as ctk
import os
import random
from tkinter import messagebox

def load_settings():
    """Загружает настройки из файла config.txt"""
    language = 'English'
    color1 = '#f0f4f4'
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
            question_label.configure(text=f"Translate this word: {questions[question_index[0]]}")
            entry_answer.delete(0, ctk.END)
        else:
            accuracy = (correct_answers / total_answers) * 100
            messagebox.showinfo(translations[language]['quiz_finished'], translations[language]['quiz_results'].format(correct=correct_answers, total=total_answers, accuracy=accuracy))
            root.quit()

    question_index = [0]

    question_label.configure(text=f"Translate this word: {questions[question_index[0]]}")
    entry_answer.delete(0, ctk.END)

    button_check.configure(state=ctk.NORMAL, command=check_answer)

language, color1, color2 = load_settings()

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("green")

root = ctk.CTk()
root.title(translations[language]['title'])
root.geometry("450x350")

root.eval('tk::PlaceWindow %s center' % root.winfo_toplevel())

label_num_words = ctk.CTkLabel(root, text=translations[language]['num_words'], font=("Arial", 12, "bold"))
label_num_words.pack(pady=10)

entry_num_words = ctk.CTkEntry(root, placeholder_text="Enter number of words", width=300, font=("Arial", 12))
entry_num_words.pack(pady=10)

button_start = ctk.CTkButton(root, text=translations[language]['start_quiz'], command=start_quiz, width=200, height=40, font=("Arial", 12, "bold"))
button_start.pack(pady=15)

question_label = ctk.CTkLabel(root, text=translations[language]['enter_num_words'], font=("Arial", 12, "bold"))
question_label.pack(pady=20)

entry_answer = ctk.CTkEntry(root, placeholder_text="Enter your answer", width=300, font=("Arial", 12))
entry_answer.pack(pady=10)

button_check = ctk.CTkButton(root, text=translations[language]['check_answer'], state=ctk.DISABLED, width=200, height=40, font=("Arial", 12, "bold"))
button_check.pack(pady=15)

root.mainloop()
