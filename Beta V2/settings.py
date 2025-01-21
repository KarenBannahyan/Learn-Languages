import tkinter as tk
import os

class SettingsMenu(tk.Tk):
    def __init__(self):
        super().__init__()

        # Считываем выбранный язык и цвет из файла
        self.language, self.color1, self.color2 = self.load_settings()

        # Словарь переводов
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

        # Настройки окна
        self.title(self.translations[self.language]['title'])
        self.geometry("400x350")
        self.configure(bg=self.color1)
        self.resizable(False, False)

        # Заголовок меню
        header_frame = tk.Frame(self, bg=self.color1)
        header_frame.pack(fill='x', pady=20)

        self.header_label = tk.Label(header_frame, text=self.translations[self.language]['header'], font=("Arial", 18, "bold"), bg=self.color1, fg='white')
        self.header_label.pack()

        # Разделитель
        separator = tk.Frame(self, height=2, bg='white')
        separator.pack(fill='x', padx=20, pady=10)

        # Кнопки в меню настроек
        btn_frame = tk.Frame(self, bg=self.color1)
        btn_frame.pack(pady=20)

        # Общий стиль для кнопок
        button_style = {
            'font': ("Arial", 12, "bold"),
            'bg': self.color1,
            'fg': 'white',
            'relief': "raised",
            'width': 20,
            'height': 2,
            'activebackground': '#45a049',
            'activeforeground': 'white',
            'bd': 2,
            'highlightthickness': 0,
            'padx': 10,
            'pady': 5
        }

        # Кнопка Language - Setting 1
        self.btn_language = tk.Button(btn_frame, text=self.translations[self.language]['language'], **button_style, command=self.open_language_popup)
        self.btn_language.grid(row=0, column=0, padx=10, pady=5)

        # Кнопка Status - Setting 2
        self.btn_status = tk.Button(btn_frame, text=self.translations[self.language]['status'], **button_style)
        self.btn_status.grid(row=1, column=0, padx=10, pady=5)

        # Кнопка Design - Setting 3
        self.btn_design = tk.Button(btn_frame, text=self.translations[self.language]['design'], **button_style, command=self.open_design_popup)
        self.btn_design.grid(row=2, column=0, padx=10, pady=5)

        # Разделитель внизу
        separator_bottom = tk.Frame(self, height=2, bg='white')
        separator_bottom.pack(fill='x', padx=20, pady=10)

        # Кнопка выхода
        self.btn_exit = tk.Button(self, text=self.translations[self.language]['exit'], font=("Arial", 12, "bold"), bg='#f44336', fg='white',
                                  relief="raised", width=20, height=2, activebackground='#e53935', activeforeground='white', bd=2, command=self.quit)
        self.btn_exit.pack(pady=10)

    def load_settings(self):
        """Загружает язык и цвет из файла config.txt, если файл существует, иначе возвращает 'English' и два дефолтных цвета"""
        language = 'English'
        color1 = '#4caf50'  # по умолчанию зеленый
        color2 = '#81c784'  # по умолчанию светло-зеленый
        if os.path.exists("config.txt"):
            with open("config.txt", "r") as file:
                for line in file:
                    if line.startswith("language="):
                        language = line.strip().split("=")[1]
                    if line.startswith("color1="):
                        color1 = line.strip().split("=")[1]
                    if line.startswith("color2="):
                        color2 = line.strip().split("=")[1]

        return language, color1, color2  # возвращаем 3 значения

    def save_settings(self):
        """Сохраняет выбранный язык и цвет в файл config.txt"""
        with open("config.txt", "w") as file:
            file.write(f"language={self.language}\n")
            file.write(f"color1={self.color1}\n")
            file.write(f"color2={self.color2}\n")

    def open_language_popup(self):
        """Открывает окно выбора языка"""
        popup = tk.Toplevel(self)
        popup.title(self.translations[self.language]['choose_language'])
        popup.geometry("300x200")
        popup.configure(bg=self.color1)

        # Центрируем окно на экране
        window_width = 300
        window_height = 200
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        popup.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        label = tk.Label(popup, text=self.translations[self.language]['choose_language'], font=("Arial", 16, "bold"), bg=self.color1, fg='white')
        label.pack(pady=20)

        # Создаем список выбора языка
        listbox = tk.Listbox(popup, font=("Arial", 14), height=3, width=20, bd=2, relief="raised")
        listbox.insert(tk.END, "English")
        listbox.insert(tk.END, "Russian")
        listbox.pack(pady=10)

        # Кнопка выбора
        def on_select():
            selected_language = listbox.get(tk.ACTIVE)
            print(f"Selected language: {selected_language}")
            self.language = selected_language  # Обновляем переменную языка
            self.save_settings()  # Сохраняем выбранный язык и цвет в файл
            self.update_interface()  # Обновляем интерфейс с новым языком
            popup.destroy()  # Закрыть окно после выбора

        btn_select = tk.Button(popup, text=self.translations[self.language]['select'], font=("Arial", 12, "bold"), bg='#45a049', fg='white', relief="raised", command=on_select)
        btn_select.pack(pady=10)

    def open_design_popup(self):
        """Открывает окно выбора схемы дизайна"""
        popup = tk.Toplevel(self)
        popup.title(self.translations[self.language]['choose_design'])
        popup.geometry("300x200")
        popup.configure(bg=self.color1)

        # Центрируем окно на экране
        window_width = 300
        window_height = 200
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        position_top = int(screen_height / 2 - window_height / 2)
        position_right = int(screen_width / 2 - window_width / 2)
        popup.geometry(f'{window_width}x{window_height}+{position_right}+{position_top}')

        label = tk.Label(popup, text=self.translations[self.language]['choose_design'], font=("Arial", 16, "bold"), bg=self.color1, fg='white')
        label.pack(pady=20)

        # Создаем список вариантов дизайна
        designs = [
            ("Red and Orange", "#f44336", "#ff9800"),
            ("Blue and Light Blue", "#2196f3", "#03a9f4"),
            ("Purple and Pink", "#9c27b0", "#e91e63")
        ]

        listbox = tk.Listbox(popup, font=("Arial", 14), height=3, width=20, bd=2, relief="raised")
        for design in designs:
            listbox.insert(tk.END, design[0])
        listbox.pack(pady=10)

        # Кнопка выбора
        def on_select():
            selected_design = listbox.get(tk.ACTIVE)
            print(f"Selected design: {selected_design}")
            for design in designs:
                if design[0] == selected_design:
                    self.color1, self.color2 = design[1], design[2]
                    self.apply_design()  # Применяем выбранный дизайн
            self.save_settings()  # Сохраняем настройки
            popup.destroy()  # Закрыть окно после выбора

        btn_select = tk.Button(popup, text=self.translations[self.language]['select'], font=("Arial", 12, "bold"), bg='#45a049', fg='white', relief="raised", command=on_select)
        btn_select.pack(pady=10)

    def apply_design(self):
        """Применяет выбранный дизайн для кнопок и фона"""
        self.configure(bg=self.color1)
        self.header_label.config(bg=self.color1, fg='white')

        # Обновляем цвет кнопок
        self.btn_language.config(bg=self.color1)
        self.btn_status.config(bg=self.color1)
        self.btn_design.config(bg=self.color1)
        self.btn_exit.config(bg='#f44336')  # Кнопка выхода сохраняет свой цвет

        # Обновляем текст элементов
        self.title(self.translations[self.language]['title'])
        self.btn_language.config(text=self.translations[self.language]['language'])
        self.btn_status.config(text=self.translations[self.language]['status'])
        self.btn_design.config(text=self.translations[self.language]['design'])
        self.btn_exit.config(text=self.translations[self.language]['exit'])

    def update_interface(self):
        """Обновляет текст интерфейса в зависимости от выбранного языка и цвета"""
        self.header_label.config(text=self.translations[self.language]['header'])
        self.title(self.translations[self.language]['title'])
        self.btn_language.config(text=self.translations[self.language]['language'])
        self.btn_status.config(text=self.translations[self.language]['status'])
        self.btn_design.config(text=self.translations[self.language]['design'])
        self.btn_exit.config(text=self.translations[self.language]['exit'])


if __name__ == "__main__":
    app = SettingsMenu()
    app.mainloop()
