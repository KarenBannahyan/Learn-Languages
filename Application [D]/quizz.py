import tkinter as tk
from tkinter import messagebox
import random

def start_quiz():
    try:
        with open("logs.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
    except FileNotFoundError:
        messagebox.showerror("File Not Found", "The file 'logs.txt' does not exist!")
        return

    if not lines:
        messagebox.showwarning("No Words", "The file 'logs.txt' is empty!")
        return

    try:
        num_words = int(entry_num_words.get())
        if num_words <= 0 or num_words > len(lines):
            messagebox.showwarning("Invalid Number", f"Please enter a number between 1 and {len(lines)}")
            return
    except ValueError:
        messagebox.showwarning("Invalid Input", "Please enter a valid number!")
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
            messagebox.showerror("File Format Error", f"Invalid format in file line: {line.strip()}")
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
            messagebox.showinfo("Quiz Finished", f"You answered {correct_answers}/{total_answers} correctly.\nAccuracy: {accuracy:.2f}%")
            root.quit()  

    question_index = [0]

    question_label.config(text=f"Translate this word: {questions[question_index[0]]}")
    entry_answer.delete(0, tk.END)

    button_check.config(state=tk.NORMAL, command=check_answer)

root = tk.Tk()
root.title("German Translation Quiz")

root.geometry("400x300")

root.configure(bg="#a8d5ba")

label_num_words = tk.Label(root, text="Number of words to translate:", bg="#a8d5ba", font=("Arial", 12))
label_num_words.pack(pady=5)

entry_num_words = tk.Entry(root, font=("Arial", 12), width=10)
entry_num_words.pack(pady=5)

button_start = tk.Button(root, text="Start Quiz", bg="#4caf50", fg="white", font=("Arial", 12), width=20, height=2, relief="flat", command=start_quiz)
button_start.pack(pady=15)

question_label = tk.Label(root, text="Enter number of words to start", bg="#a8d5ba", font=("Arial", 14))
question_label.pack(pady=10)

entry_answer = tk.Entry(root, font=("Arial", 12), width=30)
entry_answer.pack(pady=5)

button_check = tk.Button(root, text="Check Answer", bg="#2196f3", fg="white", font=("Arial", 12), width=20, height=2, relief="flat", state=tk.DISABLED)
button_check.pack(pady=15)

root.mainloop()
