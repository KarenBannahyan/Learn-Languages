import customtkinter as ctk
import os
from tkinter import filedialog, messagebox, Listbox
from PIL import Image, ImageTk

class WordCardApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.language, self.color1, self.color2 = self.load_settings()

        self.translations = {
            'English': {
                'title': 'Word Card Manager',
                'word': 'Word:',
                'image': 'Attach Image:',
                'add_card': 'Add Card',
                'delete_card': 'Delete Selected Card',
                'input_error': 'Please fill in the word and attach an image!',
                'duplicate_entry': 'This word already exists!',
                'success': "Card for '{word}' added successfully!",
                'delete_confirm': 'Are you sure you want to delete the selected card?',
                'image_not_found': 'Image file not found for this card!'
            },
            'Russian': {
                'title': 'Менеджер карточек слов',
                'word': 'Слово:',
                'image': 'Прикрепить изображение:',
                'add_card': 'Добавить карточку',
                'delete_card': 'Удалить выбранную карточку',
                'input_error': 'Пожалуйста, заполните слово и прикрепите изображение!',
                'duplicate_entry': 'Это слово уже существует!',
                'success': "Карточка для '{word}' успешно добавлена!",
                'delete_confirm': 'Вы уверены, что хотите удалить выбранную карточку?',
                'image_not_found': 'Файл изображения для этой карточки не найден!'
            },
        }

        self.title(self.translations[self.language]['title'])
        self.geometry("600x500")
        self.configure(fg_color=self.color1)
        self.resizable(False, False)

        self.eval('tk::PlaceWindow %s center' % self.winfo_toplevel())

        self.photos_dir = "photos"
        os.makedirs(self.photos_dir, exist_ok=True)

        self.label_word = ctk.CTkLabel(self, text=self.translations[self.language]['word'], font=ctk.CTkFont(size=14, weight="bold"))
        self.label_word.pack(pady=10)

        self.entry_word = ctk.CTkEntry(self, font=ctk.CTkFont(size=12), width=300)
        self.entry_word.pack(pady=5)

        self.label_image = ctk.CTkLabel(self, text=self.translations[self.language]['image'], font=ctk.CTkFont(size=14, weight="bold"))
        self.label_image.pack(pady=10)

        self.button_attach = ctk.CTkButton(self, text="Browse", command=self.attach_image, fg_color=self.color2)
        self.button_attach.pack(pady=5)

        self.selected_image_path = None

        self.add_button = ctk.CTkButton(self, text=self.translations[self.language]['add_card'], command=self.add_card, fg_color=self.color2)
        self.add_button.pack(pady=20)

        self.card_listbox = Listbox(self, height=10, width=50, font=("Arial", 12))
        self.card_listbox.pack(pady=10)
        self.card_listbox.bind('<<ListboxSelect>>', self.open_card_image)

        self.delete_button = ctk.CTkButton(self, text=self.translations[self.language]['delete_card'], command=self.delete_card, fg_color="#e74c3c")
        self.delete_button.pack(pady=10)

        self.load_cards()

    def load_settings(self):
        """Загружает настройки из файла config.txt"""
        language = 'English'
        color1 = '#2c3e50'
        color2 = '#34495e'

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

    def attach_image(self):
        """Открывает диалог выбора изображения"""
        self.selected_image_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")])

    def add_card(self):
        """Добавляет карточку с изображением"""
        word = self.entry_word.get().strip()

        if not word or not self.selected_image_path:
            messagebox.showwarning(self.translations[self.language]['title'], self.translations[self.language]['input_error'])
            return

        try:
            with open("photo_logs.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
                for line in lines:
                    if word == line.split(' - ')[0]:
                        messagebox.showwarning(self.translations[self.language]['title'], self.translations[self.language]['duplicate_entry'])
                        return
        except FileNotFoundError:
            pass

        image_filename = os.path.join(self.photos_dir, f"{word}.png")
        image = Image.open(self.selected_image_path)
        image.save(image_filename)

        with open("photo_logs.txt", "a", encoding="utf-8") as file:
            file.write(f"{word} - {image_filename}\n")

        self.card_listbox.insert("end", word)

        self.entry_word.delete(0, "end")
        self.selected_image_path = None

        messagebox.showinfo(self.translations[self.language]['title'], self.translations[self.language]['success'].format(word=word))

    def delete_card(self):
        """Удаляет выбранную карточку"""
        selected_index = self.card_listbox.curselection()
        if not selected_index:
            return

        word = self.card_listbox.get(selected_index)

        if messagebox.askyesno(self.translations[self.language]['title'], self.translations[self.language]['delete_confirm']):
            with open("photo_logs.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()

            with open("photo_logs.txt", "w", encoding="utf-8") as file:
                for line in lines:
                    if not line.startswith(word):
                        file.write(line)

            image_path = os.path.join(self.photos_dir, f"{word}.png")
            if os.path.exists(image_path):
                os.remove(image_path)

            self.card_listbox.delete(selected_index)

    def load_cards(self):
        """Загружает карточки из файла"""
        try:
            with open("photo_logs.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
                for line in lines:
                    word, _ = line.strip().split(' - ')
                    self.card_listbox.insert("end", word)
        except FileNotFoundError:
            pass

    def open_card_image(self, event):
        """Открывает изображение выбранной карточки"""
        selected_index = self.card_listbox.curselection()
        if not selected_index:
            return

        word = self.card_listbox.get(selected_index)

        try:
            with open("photo_logs.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
                for line in lines:
                    if line.startswith(word):
                        _, image_path = line.strip().split(' - ')
                        if os.path.exists(image_path):
                            image = Image.open(image_path)
                            image.show()
                        else:
                            messagebox.showerror(self.translations[self.language]['title'], self.translations[self.language]['image_not_found'])
                        return
        except FileNotFoundError:
            messagebox.showerror(self.translations[self.language]['title'], self.translations[self.language]['image_not_found'])

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = WordCardApp()
    app.mainloop()
