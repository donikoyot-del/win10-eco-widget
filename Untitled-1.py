import tkinter as tk
import subprocess

# GUID схем живлення Windows
MODE_ECONOMY = "a1841308-3541-4fab-bc81-f71556f20b4a"
MODE_BALANCED = "381b4222-f694-41f0-9685-ff5bb260df2e"

class CompactTransparentWidget:
    def __init__(self, root):
        self.root = root
        self.root.title("Eco Power Widget")
        
        # Розміри віджета (приблизно 3х3 см) та язичка
        self.width = 115
        self.height = 115
        self.tab_width = 25  # Ширина видимого язичка
        
        # Стан режиму (False - баланс, True - економ)
        self.is_economy = False
        
        # Отримання розмірів екрана
        self.screen_width = self.root.winfo_screenwidth()
        self.screen_height = self.root.winfo_screenheight()
        
        # Координати: по центру екрана справа
        self.target_y = (self.screen_height // 2) - (self.height // 2)
        self.hidden_x = self.screen_width - self.tab_width
        self.visible_x = self.screen_width - self.width
        self.current_x = self.hidden_x
        
        # Налаштування вікна без рамок поверх усіх вікон
        self.root.geometry(f"{self.width}x{self.height}+{self.current_x}+{self.target_y}")
        self.root.overrideredirect(True)
        self.root.attributes("-topmost", True)
        
        # Рівень прозорості всього вікна (0.3 - дуже прозорий, 0.95 - майже непрозорий у фокусі)
        self.root.attributes("-alpha", 0.4)
        self.root.configure(bg="#1e1e1e")

        # --- Інтерфейс ---
        
        # Прозорий язичок зліва (стирчить із краю екрана)
        self.tab_label = tk.Label(root, text="   ⚡\n\n   🔋", fg="#00ff66", bg="#1e1e1e", font=("Arial", 9, "bold"), width=3)
        self.tab_label.pack(side=tk.LEFT, fill=tk.Y)

        # Фрейм для контенту (кнопка-іконка батареї)
        self.content_frame = tk.Frame(root, bg="#1e1e1e")
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=5)

        # Велика інтерактивна кнопка-батарейка
        self.btn_battery = tk.Button(
            self.content_frame, 
            text="🔋", 
            command=self.toggle_power_mode, 
            bg="#2d2d2d", 
            fg="white", 
            relief="flat", 
            font=("Segoe UI", 36), # Велика емодзі-іконка
            activebackground="#3e3e3e",
            activeforeground="white",
            cursor="hand2"
        )
        self.btn_battery.pack(fill=tk.BOTH, expand=True, pady=10, padx=5)

        # Зв'язуємо події миші для автоматичного виїзду та прозорості
        self.root.bind("<Enter>", self.on_hover)
        self.root.bind("<Leave>", self.on_leave)

    def animate_slide(self, target_x):
        """Анімація ковзання віджета"""
        step = 8  # Швидкість руху
        if self.current_x < target_x:
            self.current_x += step
            if self.current_x > target_x: self.current_x = target_x
        elif self.current_x > target_x:
            self.current_x -= step
            if self.current_x < target_x: self.current_x = target_x

        self.root.geometry(f"{self.width}x{self.height}+{self.current_x}+{self.target_y}")

        if self.current_x != target_x:
            self.root.after(10, lambda: self.animate_slide(target_x))

    def on_hover(self, event):
        """Коли мишка заходить на віджет — він виїжджає та стає чітким"""
        self.root.attributes("-alpha", 0.95)  # Робимо видимим
        self.animate_slide(self.visible_x)

    def on_leave(self, event):
        """Коли мишка йде — ховається назад і стає напівпрозорим"""
        # Перевірка, щоб мишка випадково не вважалася такою, що вийшла за межі при кліку
        x, y = self.root.winfo_pointerxy()
        if not (self.visible_x <= x <= self.screen_width and self.target_y <= y <= self.target_y + self.height):
            self.root.attributes("-alpha", 0.4)  # Знову ховаємо в прозорість
            self.animate_slide(self.hidden_x)

    def toggle_power_mode(self):
        """Перемикання режимів живлення в один клік по батарейці"""
        if not self.is_economy:
            # Вмикаємо Економ
            subprocess.run(f"powercfg /setactive {MODE_ECONOMY}", shell=True)
            self.btn_battery.config(fg="#107c41")  # Батарейка стає Зеленою
            self.is_economy = True
        else:
            # Повертаємо Баланс
            subprocess.run(f"powercfg /setactive {MODE_BALANCED}", shell=True)
            self.btn_battery.config(fg="white")    # Батарейка стає Білою
            self.is_economy = False

if __name__ == "__main__":
    root = tk.Tk()
    app = CompactTransparentWidget(root)
    root.mainloop()
