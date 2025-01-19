import tkinter as tk
from tkinter import messagebox
import subprocess
def add_new_word():
    try:
        subprocess.Popen(['python', 'text.py'])
    except Exception as e:
        messagebox.showerror("Error", f"Cant add a new word: {e}")

def delete_word():
    try:
        subprocess.Popen(['python', 'pop.py']) 
    except Exception as e:
        messagebox.showerror("Error", f"Cant delete word: {e}")

def fast_quiz():
    try:
        subprocess.Popen(['python', 'quizz.py'])
    except Exception as e:
        messagebox.showerror("Error", f"Cant open quizz: {e}")

root = tk.Tk()
root.title("German Language Learning App")
root.resizable(False, False)

root.geometry("300x250")

root.configure(bg="#a8d5ba")

button_style = {
    "bg": "#4caf50",
    "fg": "white",
    "font": ("Arial", 12, "bold"),
    "relief": "flat",
    "width": 20,
    "height": 2,
    "activebackground": "#45a049",
    "activeforeground": "white",
    "bd": 0
}

button_add = tk.Button(root, text="Add new word", **button_style, command=add_new_word)
button_add.pack(pady=15)

button_delete = tk.Button(root, text="Delete word", **button_style, command=delete_word)
button_delete.pack(pady=15)

button_quiz = tk.Button(root, text="Fast quiz", **button_style, command=fast_quiz)
button_quiz.pack(pady=15)

root.mainloop()
