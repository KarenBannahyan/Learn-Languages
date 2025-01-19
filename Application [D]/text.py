import tkinter as tk
from tkinter import messagebox

def save_word():
    german_word = entry_german.get().strip() 
    translation = entry_translation.get().strip() 

    if not german_word or not translation:
        messagebox.showwarning("Input Error", "Please fill in both fields!")
        return

    try:
        with open("logs.txt", "r", encoding="utf-8") as file:
            lines = file.readlines()
            for line in lines:
                if german_word == line.split(' - ')[0] and translation == line.split(' - ')[1].strip():
                    messagebox.showwarning("Duplicate Entry", "This word and translation already exist!")
                    return
    except FileNotFoundError:
        pass

    with open("logs.txt", "a", encoding="utf-8") as file:
        file.write(f"{german_word} - {translation}\n")

    entry_german.delete(0, tk.END)
    entry_translation.delete(0, tk.END)
    
    messagebox.showinfo("Success", f"Word '{german_word}' with translation '{translation}' saved successfully!")

root = tk.Tk()
root.title("German Word and Translation Input")

root.geometry("400x200")

root.configure(bg="#a8d5ba")

label_german = tk.Label(root, text="German Word:", bg="#a8d5ba", font=("Arial", 12))
label_german.pack(pady=5)

entry_german = tk.Entry(root, font=("Arial", 12), width=30)
entry_german.pack(pady=5)

label_translation = tk.Label(root, text="Translation:", bg="#a8d5ba", font=("Arial", 12))
label_translation.pack(pady=5)

entry_translation = tk.Entry(root, font=("Arial", 12), width=30)
entry_translation.pack(pady=5)

button_save = tk.Button(root, text="Save Word", bg="#4caf50", fg="white", font=("Arial", 12), width=20, height=2, relief="flat", command=save_word)
button_save.pack(pady=15)

root.mainloop()
