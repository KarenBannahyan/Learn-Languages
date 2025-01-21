import customtkinter as ctk
import os
from tkinter import messagebox, Listbox

class TopicManagerApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.language, self.color1, self.color2 = self.load_settings()

        self.translations = {
            'English': {
                'title': 'Topic Manager',
                'topic': 'Topic:',
                'word': 'Word:',
                'add_topic': 'Add Topic',
                'select_topic': 'Select Topic',
                'add_word': 'Add Word',
                'delete_word': 'Delete Selected Word',
                'input_error': 'Please fill in the required fields!',
                'topic_exists': 'This topic already exists!',
                'word_exists': 'This word already exists in the topic!',
                'topic_created': "Topic '{topic}' created successfully!",
                'word_added': "Word '{word}' added successfully to topic '{topic}'!",
                'delete_confirm': 'Are you sure you want to delete the selected word?'
            },
            'Russian': {
                'title': 'Менеджер тем',
                'topic': 'Тема:',
                'word': 'Слово:',
                'add_topic': 'Добавить тему',
                'select_topic': 'Выбрать тему',
                'add_word': 'Добавить слово',
                'delete_word': 'Удалить выбранное слово',
                'input_error': 'Пожалуйста, заполните необходимые поля!',
                'topic_exists': 'Такая тема уже существует!',
                'word_exists': 'Это слово уже существует в теме!',
                'topic_created': "Тема '{topic}' успешно создана!",
                'word_added': "Слово '{word}' успешно добавлено в тему '{topic}'!",
                'delete_confirm': 'Вы уверены, что хотите удалить выбранное слово?'
            },
        }

        self.title(self.translations[self.language]['title'])
        self.geometry("600x601")
        self.configure(fg_color=self.color1)
        self.resizable(False, False)

        self.eval('tk::PlaceWindow %s center' % self.winfo_toplevel())

        self.topics_dir = "topics"
        os.makedirs(self.topics_dir, exist_ok=True)

        self.label_topic = ctk.CTkLabel(self, text=self.translations[self.language]['topic'], font=ctk.CTkFont(size=14, weight="bold"))
        self.label_topic.pack(pady=10)

        self.entry_topic = ctk.CTkEntry(self, font=ctk.CTkFont(size=12), width=300)
        self.entry_topic.pack(pady=5)

        self.add_topic_button = ctk.CTkButton(self, text=self.translations[self.language]['add_topic'], command=self.add_topic, fg_color=self.color2)
        self.add_topic_button.pack(pady=10)

        self.topic_listbox = Listbox(self, height=5, width=50, font=("Arial", 12))
        self.topic_listbox.pack(pady=10)
        self.topic_listbox.bind('<<ListboxSelect>>', self.load_words)

        self.label_word = ctk.CTkLabel(self, text=self.translations[self.language]['word'], font=ctk.CTkFont(size=14, weight="bold"))
        self.label_word.pack(pady=10)

        self.entry_word = ctk.CTkEntry(self, font=ctk.CTkFont(size=12), width=300)
        self.entry_word.pack(pady=5)

        self.add_word_button = ctk.CTkButton(self, text=self.translations[self.language]['add_word'], command=self.add_word, fg_color=self.color2)
        self.add_word_button.pack(pady=10)

        self.word_listbox = Listbox(self, height=10, width=50, font=("Arial", 12))
        self.word_listbox.pack(pady=10)

        self.delete_word_button = ctk.CTkButton(self, text=self.translations[self.language]['delete_word'], command=self.delete_word, fg_color="#e74c3c")
        self.delete_word_button.pack(pady=10)

        self.load_topics()

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

    def add_topic(self):
        """Добавляет новую тему"""
        topic = self.entry_topic.get().strip()

        if not topic:
            messagebox.showwarning(self.translations[self.language]['title'], self.translations[self.language]['input_error'])
            return

        topic_path = os.path.join(self.topics_dir, f"{topic}.txt")

        if os.path.exists(topic_path):
            messagebox.showwarning(self.translations[self.language]['title'], self.translations[self.language]['topic_exists'])
            return

        with open(topic_path, "w", encoding="utf-8") as file:
            pass

        self.topic_listbox.insert("end", topic)
        self.entry_topic.delete(0, "end")
        messagebox.showinfo(self.translations[self.language]['title'], self.translations[self.language]['topic_created'].format(topic=topic))

    def load_topics(self):
        """Загружает список тем"""
        self.topic_listbox.delete(0, "end")
        for filename in os.listdir(self.topics_dir):
            if filename.endswith(".txt"):
                self.topic_listbox.insert("end", filename[:-4])

    def load_words(self, event):
        """Загружает слова для выбранной темы"""
        selected_index = self.topic_listbox.curselection()
        if not selected_index:
            return

        topic = self.topic_listbox.get(selected_index)
        topic_path = os.path.join(self.topics_dir, f"{topic}.txt")

        self.word_listbox.delete(0, "end")

        try:
            with open(topic_path, "r", encoding="utf-8") as file:
                for line in file:
                    self.word_listbox.insert("end", line.strip())
        except FileNotFoundError:
            pass

    def add_word(self):
        """Добавляет слово в текущую тему"""
        selected_index = self.topic_listbox.curselection()
        if not selected_index:
            return

        word = self.entry_word.get().strip()
        topic = self.topic_listbox.get(selected_index)
        topic_path = os.path.join(self.topics_dir, f"{topic}.txt")

        if not word:
            messagebox.showwarning(self.translations[self.language]['title'], self.translations[self.language]['input_error'])
            return

        try:
            with open(topic_path, "r", encoding="utf-8") as file:
                if word in [line.strip() for line in file]:
                    messagebox.showwarning(self.translations[self.language]['title'], self.translations[self.language]['word_exists'])
                    return
        except FileNotFoundError:
            pass

        with open(topic_path, "a", encoding="utf-8") as file:
            file.write(word + "\n")

        self.word_listbox.insert("end", word)
        self.entry_word.delete(0, "end")
        messagebox.showinfo(self.translations[self.language]['title'], self.translations[self.language]['word_added'].format(word=word, topic=topic))

    def delete_word(self):
        """Удаляет выбранное слово из текущей темы"""
        selected_topic_index = self.topic_listbox.curselection()
        selected_word_index = self.word_listbox.curselection()

        if not selected_topic_index or not selected_word_index:
            return

        word = self.word_listbox.get(selected_word_index)
        topic = self.topic_listbox.get(selected_topic_index)
        topic_path = os.path.join(self.topics_dir, f"{topic}.txt")

        if messagebox.askyesno(self.translations[self.language]['title'], self.translations[self.language]['delete_confirm']):
            try:
                with open(topic_path, "r", encoding="utf-8") as file:
                    words = file.readlines()

                with open(topic_path, "w", encoding="utf-8") as file:
                    for line in words:
                        if line.strip() != word:
                            file.write(line)

                self.word_listbox.delete(selected_word_index)
            except FileNotFoundError:
                pass

if __name__ == "__main__":
    app = TopicManagerApp()
    app.mainloop()
