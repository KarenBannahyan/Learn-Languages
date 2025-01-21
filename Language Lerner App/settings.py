import customtkinter as ctk
import os

class SettingsMenu(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.language, self.color1, self.color2 = self.load_settings()

        self.translations = {
            'English': {
                'title': "Settings Menu",
                'header': "Settings",
                'language': "Language",
                'status': "Status",
                'design': "Design",
                'exit': "Exit",
                'choose_language': "Choose Language",
                'choose_design': "Choose Design Color",
                'select': "Select",
            },
            'Russian': {
                'title': "Меню настроек",
                'header': "Настройки",
                'language': "Язык",
                'status': "Статус",
                'design': "Дизайн",
                'exit': "Выход",
                'choose_language': "Выберите язык",
                'choose_design': "Выберите цвет дизайна",
                'select': "Выбрать",
            }
        }

        self.title(self.translations[self.language]['title'])
        self.geometry("400x400")
        self.configure(fg_color=self.color1)
        self.resizable(False, False)

        self.header_label = ctk.CTkLabel(self, text=self.translations[self.language]['header'], font=ctk.CTkFont(size=20, weight="bold"))
        self.header_label.pack(pady=20)

        self.btn_language = ctk.CTkButton(self, text=self.translations[self.language]['language'], command=self.open_language_popup)
        self.btn_language.pack(pady=10)

        self.btn_status = ctk.CTkButton(self, text=self.translations[self.language]['status'])
        self.btn_status.pack(pady=10)

        self.btn_design = ctk.CTkButton(self, text=self.translations[self.language]['design'], command=self.open_design_popup)
        self.btn_design.pack(pady=10)

        self.btn_exit = ctk.CTkButton(self, text=self.translations[self.language]['exit'], fg_color="red", command=self.quit)
        self.btn_exit.pack(pady=20)

    def load_settings(self):
        """Загружает язык и цвет из файла config.txt, если файл существует, иначе возвращает 'English' и два дефолтных цвета"""
        language = 'English'
        color1 = '#2c3e50'
        color2 = '#34495e'
        if os.path.exists("config.txt"):
            with open("config.txt", "r") as file:
                for line in file:
                    if line.startswith("language="):
                        language = line.strip().split("=")[1]
                    if line.startswith("color1="):
                        color1 = line.strip().split("=")[1]
                    if line.startswith("color2="):
                        color2 = line.strip().split("=")[1]

        return language, color1, color2

    def save_settings(self):
        """Сохраняет выбранный язык и цвет в файл config.txt"""
        with open("config.txt", "w") as file:
            file.write(f"language={self.language}\n")
            file.write(f"color1={self.color1}\n")
            file.write(f"color2={self.color2}\n")

    def open_language_popup(self):
        """Открывает окно выбора языка"""
        popup = ctk.CTkToplevel(self)
        popup.title(self.translations[self.language]['choose_language'])
        popup.geometry("300x200")

        label = ctk.CTkLabel(popup, text=self.translations[self.language]['choose_language'], font=ctk.CTkFont(size=16))
        label.pack(pady=20)

        listbox = ctk.CTkComboBox(popup, values=["English", "Russian"], font=ctk.CTkFont(size=14))
        listbox.pack(pady=10)

        def on_select():
            self.language = listbox.get()
            self.save_settings()
            self.update_interface()
            popup.destroy()

        btn_select = ctk.CTkButton(popup, text=self.translations[self.language]['select'], command=on_select)
        btn_select.pack(pady=10)

    def open_design_popup(self):
        """Открывает окно выбора схемы дизайна"""
        popup = ctk.CTkToplevel(self)
        popup.title(self.translations[self.language]['choose_design'])
        popup.geometry("300x250")

        label = ctk.CTkLabel(popup, text=self.translations[self.language]['choose_design'], font=ctk.CTkFont(size=16))
        label.pack(pady=20)

        designs = [
            ("Sunset", "#FF5733", "#FFC300"),
            ("Ocean", "#1E90FF", "#00CED1"),
            ("Forest", "#228B22", "#6B8E23"),
            ("Lavender", "#9370DB", "#D8BFD8"),
            ("Night Sky", "#2C3E50", "#34495E")
        ]

        listbox = ctk.CTkComboBox(popup, values=[design[0] for design in designs], font=ctk.CTkFont(size=14))
        listbox.pack(pady=10)

        def on_select():
            selected_design = listbox.get()
            for design in designs:
                if design[0] == selected_design:
                    self.color1, self.color2 = design[1], design[2]
                    self.apply_design()
            self.save_settings()
            popup.destroy()

        btn_select = ctk.CTkButton(popup, text=self.translations[self.language]['select'], command=on_select)
        btn_select.pack(pady=10)

    def apply_design(self):
        """Применяет выбранный дизайн для кнопок и фона"""
        self.configure(fg_color=self.color1)
        self.header_label.configure(fg_color=self.color1)

        self.btn_language.configure(fg_color=self.color1)
        self.btn_status.configure(fg_color=self.color1)
        self.btn_design.configure(fg_color=self.color1)
        self.btn_exit.configure(fg_color="red")

    def update_interface(self):
        """Обновляет текст интерфейса в зависимости от выбранного языка"""
        self.title(self.translations[self.language]['title'])
        self.header_label.configure(text=self.translations[self.language]['header'])
        self.btn_language.configure(text=self.translations[self.language]['language'])
        self.btn_status.configure(text=self.translations[self.language]['status'])
        self.btn_design.configure(text=self.translations[self.language]['design'])
        self.btn_exit.configure(text=self.translations[self.language]['exit'])

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    ctk.set_default_color_theme("dark-blue")
    app = SettingsMenu()
    app.mainloop()
