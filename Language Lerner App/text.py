import customtkinter as ctk
import os

class WordInputApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.language, self.color1, self.color2 = self.load_settings()

        self.translations = {
            'English': {
                'title': 'Translation Input',
                'german_word': 'Word:',
                'translation': 'Translation:',
                'save_word': 'Save Word',
                'input_error': 'Please fill in both fields!',
                'duplicate_entry': 'This word and translation already exist!',
                'success': "Word '{word}' with translation '{translation}' saved successfully!"
            },
            'Russian': {
                'title': 'Ввод слова и перевода',
                'german_word': 'Слово:',
                'translation': 'Перевод:',
                'save_word': 'Сохранить слово',
                'input_error': 'Пожалуйста, заполните оба поля!',
                'duplicate_entry': 'Это слово и перевод уже существуют!',
                'success': "Слово '{word}' с переводом '{translation}' успешно сохранено!"
            },
        }

        self.title(self.translations[self.language]['title'])
        self.geometry("450x300")
        self.configure(fg_color=self.color1)
        self.resizable(False, False)

        self.eval('tk::PlaceWindow %s center' % self.winfo_toplevel())

        self.label_german = ctk.CTkLabel(self, text=self.translations[self.language]['german_word'], font=ctk.CTkFont(size=14, weight="bold"))
        self.label_german.pack(pady=10)

        self.entry_german = ctk.CTkEntry(self, font=ctk.CTkFont(size=12), width=300)
        self.entry_german.pack(pady=5)

        self.label_translation = ctk.CTkLabel(self, text=self.translations[self.language]['translation'], font=ctk.CTkFont(size=14, weight="bold"))
        self.label_translation.pack(pady=10)

        self.entry_translation = ctk.CTkEntry(self, font=ctk.CTkFont(size=12), width=300)
        self.entry_translation.pack(pady=5)

        self.save_button = ctk.CTkButton(self, text=self.translations[self.language]['save_word'], command=self.save_word, fg_color=self.color2)
        self.save_button.pack(pady=20)

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

    def save_word(self):
        """Сохраняет слово и его перевод в файл"""
        german_word = self.entry_german.get().strip()
        translation = self.entry_translation.get().strip()

        if not german_word or not translation:
            ctk.CTkMessagebox(title=self.translations[self.language]['title'], message=self.translations[self.language]['input_error'])
            return

        try:
            with open("logs.txt", "r", encoding="utf-8") as file:
                lines = file.readlines()
                for line in lines:
                    if german_word == line.split(' - ')[0] and translation == line.split(' - ')[1].strip():
                        ctk.CTkMessagebox(title=self.translations[self.language]['title'], message=self.translations[self.language]['duplicate_entry'])
                        return
        except FileNotFoundError:
            pass

        with open("logs.txt", "a", encoding="utf-8") as file:
            file.write(f"{german_word} - {translation}\n")

        self.entry_german.delete(0, "end")
        self.entry_translation.delete(0, "end")

        ctk.CTkMessagebox(title=self.translations[self.language]['title'], message=self.translations[self.language]['success'].format(word=german_word, translation=translation))

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = WordInputApp()
    app.mainloop()
