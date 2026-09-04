import os
import sys
import tkinter as tk
from tkinter import messagebox

root = tk.Tk()
root.title("Крестики-нолики")
root.resizable(False, False)  # Запрещаем растягивать окно, чтобы сетка не плыла

# ===== НАСТРОЙКА ЦВЕТОВОЙ ПАЛИТРЫ =====
DARK_BG = "#1e1e2e"
PANEL_BG = "#252538"
BTN_BG = "#2d2d44"
BTN_HOVER = "#363652"     # Цвет кнопки при наведении мыши
BTN_ACTIVE = "#414161"
TEXT_COLOR = "#cdd6f4"

COLOR_X = "#89b4fa"
COLOR_O = "#f38ba8"
COLOR_WIN = "#a6e3a1"

root.configure(bg=DARK_BG)

# ===== ИКОНКА =====
def resource_path(relative):
    """Путь к ресурсу с учётом распаковки PyInstaller onefile (_MEIPASS)."""
    base = getattr(sys, "_MEIPASS", os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, relative)

png_path = resource_path("icon.png")
ico_path = resource_path("icon.ico")

_window_icon = None  # держим ссылку, чтобы не собрал garbage collector

# Windows: иконка окна и панели задач корректно ставится через ICO (iconbitmap).
# Linux/macOS: iconphoto с PNG (PhotoImage не умеет читать ICO).
if sys.platform == "win32" and os.path.exists(ico_path):
    try:
        root.iconbitmap(default=ico_path)
    except tk.TclError:
        pass

if os.path.exists(png_path):
    try:
        _window_icon = tk.PhotoImage(file=png_path)
        root.iconphoto(True, _window_icon)  # True = распространять на все окна
    except tk.TclError:
        pass

# ===== ГЛОБАЛЬНЫЕ ПЕРЕМЕННЫЕ =====
current_player = "X"
buttons = []
game_active = True

# Переменные для хранения счета
score_x = 0
score_o = 0
score_draws = 0

# ===== ИНФОРМАЦИОННАЯ ПАНЕЛЬ СЧЕТА =====
score_frame = tk.Frame(root, bg=DARK_BG)
score_frame.grid(row=0, column=0, columnspan=3, pady=(10, 5))

score_label = tk.Label(
    score_frame,
    text="Игрок X: 0  |  Ничьи: 0  |  Игрок O: 0",
    font=("Arial", 12, "bold"),
    bg=DARK_BG,
    fg=TEXT_COLOR
)
score_label.pack()

# ===== ФУНКЦИЯ ОБНОВЛЕНИЯ ТЕКСТА СЧЕТА =====
def update_score_text():
    score_label.config(text=f"Игрок X: {score_x}  |  Ничьи: {score_draws}  |  Игрок O: {score_o}")

# ===== ФУНКЦИЯ ПРОВЕРКИ ПОБЕДЫ =====
def check_winner():
    global game_active, score_x, score_o
    winning_combinations = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),
        (0, 3, 6), (1, 4, 7), (2, 5, 8),
        (0, 4, 8), (2, 4, 6)
    ]
    for combo in winning_combinations:
        a, b, c = combo
        if buttons[a]["text"] == buttons[b]["text"] == buttons[c]["text"] != "":
            for idx in combo:
                buttons[idx].config(bg=COLOR_WIN, fg=DARK_BG)
            game_active = False

            # Начисляем очки
            if current_player == "X":
                score_x += 1
            else:
                score_o += 1
            update_score_text()
            return True
    return False

# ===== ФУНКЦИЯ ОБРАБОТКИ КЛИКА =====
def on_click(index):
    global current_player, game_active, score_draws

    if game_active and buttons[index]["text"] == "":
        buttons[index]["text"] = current_player

        if current_player == "X":
            buttons[index].config(fg=COLOR_X)
        else:
            buttons[index].config(fg=COLOR_O)

        if check_winner():
            messagebox.showinfo("Победа!", f"Победил {current_player}!")
        elif all(button["text"] != "" for button in buttons):
            score_draws += 1
            update_score_text()
            messagebox.showinfo("Ничья!", "Игра окончена. Ничья!")
            game_active = False
        else:
            current_player = "O" if current_player == "X" else "X"

# ===== ФУНКЦИЯ СБРОСА ИГРЫ =====
def reset_game():
    global current_player, game_active
    current_player = "X"
    game_active = True
    for button in buttons:
        button.config(text="", bg=BTN_BG, fg=TEXT_COLOR)

# ===== ФУНКЦИИ ХОВЕРА (НАВЕДЕНИЯ МЫШКИ) =====
def on_enter(event):
    # Подсвечиваем серым только те кнопки, где еще нет символа и игра продолжается
    if game_active and event.widget["text"] == "":
        event.widget.config(bg=BTN_HOVER)

def on_leave(event):
    # Возвращаем стандартный цвет, если это не победная кнопка
    if game_active and event.widget["bg"] != COLOR_WIN:
        event.widget.config(bg=BTN_BG)

# ===== СОЗДАНИЕ ИГРОВОГО ПОЛЯ =====
for i in range(9):
    button = tk.Button(
        root,
        text="",
        font=("DejaVu Sans", 46, "bold"),
        width=3,
        height=1,
        bg=BTN_BG,
        fg=TEXT_COLOR,
        activebackground=BTN_ACTIVE,
        activeforeground=TEXT_COLOR,
        relief="flat",
        bd=2
    )
    # Привязываем функции клика и наведения мыши
    button.config(command=lambda idx=i: on_click(idx))
    button.bind("<Enter>", on_enter)
    button.bind("<Leave>", on_leave)

    # Сдвигаем сетку на row=1, так как row=0 занят счетом
    button.grid(row=(i // 3) + 1, column=i % 3, padx=4, pady=4)
    buttons.append(button)

# ===== КНОПКА СБРОСА =====
reset_button = tk.Button(
    root,
    text="Новая игра",
    font=("Arial", 12, "bold"),
    bg=PANEL_BG,
    fg=TEXT_COLOR,
    activebackground=BTN_ACTIVE,
    activeforeground=TEXT_COLOR,
    relief="flat",
    bd=0,
    height=2,
    command=reset_game
)
# Размещаем кнопку в самом низу (row=4)
reset_button.grid(row=4, column=0, columnspan=3, sticky="we", padx=4, pady=8)

root.mainloop()
