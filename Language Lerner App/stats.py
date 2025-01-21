import customtkinter as ctk
import os

class DictionaryApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.language, self.color1, self.color2 = self.load_settings()

        self.translations = {
            'English': {
                'title': 'Dictionary App',
                'word_count': 'Word count: ',
                'error': 'Error',
                'file_not_found': 'File not found: ',
                'load_dictionary': 'Load Dictionary'
            },
            'Russian': {
                'title': 'Приложение для словаря',
                'word_count': 'Количество слов: ',
                'error': 'Ошибка',
                'file_not_found': 'Файл не найден: ',
                'load_dictionary': 'Загрузить словарь'
            },
        }

        self.title(self.translations[self.language]['title'])
        self.geometry("600x400")
        self.configure(fg_color=self.color1)
        self.resizable(False, False)

        self.header_label = ctk.CTkLabel(self, text=self.translations[self.language]['title'], font=ctk.CTkFont(size=20, weight="bold"))
        self.header_label.pack(pady=20)

        self.word_count_label = ctk.CTkLabel(self, text=f"{self.translations[self.language]['word_count']} 0", font=ctk.CTkFont(size=14))
        self.word_count_label.pack(pady=10)

        self.load_button = ctk.CTkButton(self, text=self.translations[self.language]['load_dictionary'], command=self.load_file)
        self.load_button.pack(pady=10)

        self.text_frame = ctk.CTkFrame(self)
        self.text_frame.pack(padx=10, pady=10, fill="both", expand=True)

        self.text_area = ctk.CTkTextbox(self.text_frame, wrap="word", font=ctk.CTkFont(size=14))
        self.text_area.pack(side="left", fill="both", expand=True, padx=5, pady=5)

        self.scrollbar = ctk.CTkScrollbar(self.text_frame, command=self.text_area.yview)
        self.scrollbar.pack(side="right", fill="y")
        self.text_area.configure(yscrollcommand=self.scrollbar.set)

        self.load_file()

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

    def load_file(self):
        """Загружает содержимое файла logs.txt и отображает его в текстовом поле"""
        filepath = os.path.join(os.path.dirname(__file__), "logs.txt")

        try:
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.readlines()

            word_count = len(content)
            self.word_count_label.configure(text=f"{self.translations[self.language]['word_count']} {word_count}")

            self.text_area.delete("1.0", "end")
            self.text_area.insert("end", "".join(content))

        except FileNotFoundError:
            ctk.CTkMessagebox(title=self.translations[self.language]['error'], message=f"{self.translations[self.language]['file_not_found']} logs.txt")
            self.word_count_label.configure(text=f"{self.translations[self.language]['word_count']} 0")
            self.text_area.delete("1.0", "end")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = DictionaryApp()
    app.mainloop()
