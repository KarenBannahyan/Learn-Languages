import tkinter as tk
from tkinter import messagebox

def delete_word_by_translation():
    translation = entry_translation.get().strip()  
    if not translation:
        messagebox.showwarning("Input Error", "Please fill in the translation field!")
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
        messagebox.showwarning("File Not Found", "The file 'logs.txt' does not exist!")
        return
    
    if found:
        messagebox.showinfo("Success", f"The word with translation '{translation}' has been deleted successfully.")
        entry_translation.delete(0, tk.END)  
    else:
        messagebox.showwarning("Word Not Found", f"No word found with the translation '{translation}'.")

root = tk.Tk()
root.title("Delete Word by Translation")

root.geometry("400x200")

root.configure(bg="#a8d5ba")

label_translation = tk.Label(root, text="Translation:", bg="#a8d5ba", font=("Arial", 12))
label_translation.pack(pady=5)

entry_translation = tk.Entry(root, font=("Arial", 12), width=30)
entry_translation.pack(pady=5)

button_delete = tk.Button(root, text="Delete Word", bg="#f44336", fg="white", font=("Arial", 12), width=20, height=2, relief="flat", command=delete_word_by_translation)
button_delete.pack(pady=15)

root.mainloop()
