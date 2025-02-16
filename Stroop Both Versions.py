import tkinter as tk
import random
import time

# List of colors and custom shades
COLORS = {
    'red': 'red',
    'blue': 'blue',
    'green': 'green',
    'yellow': 'yellow',
    'violet': '#4B0082',  # Darker shade of violet
    'orange': 'orange',
    'pink': 'pink',
    'brown': '#8B4513'  # Tree brown
}
SCORE = 0
TOTAL = 0
start_time = None
mode = None  # Mode selection: 1 for Classic Stroop, 2 for Reverse Stroop

def start_game():
    global start_time, SCORE, TOTAL
    start_button.pack_forget()  # Hide start button after clicking
    replay_button.pack_forget()  # Hide replay button if it was displayed
    start_time = time.time()
    SCORE = 0
    TOTAL = 0
    next_word()

def next_word():
    global correct_word, displayed_color, correct_color
    
    if TOTAL >= 10:  # Limit test to 10 rounds
        end_game()
        return
    
    if mode == 1:
        # Classic Stroop: User clicks the color of the word
        displayed_word = random.choice(list(COLORS.keys()))
        correct_color = random.choice(list(COLORS.keys()))
        while displayed_word == correct_color:
            correct_color = random.choice(list(COLORS.keys()))
        word_display.config(text=displayed_word.capitalize(), fg=COLORS[correct_color])
    else:
        # Reverse Stroop: User clicks the meaning of the word
        correct_word = random.choice(list(COLORS.keys()))
        displayed_color = random.choice(list(COLORS.keys()))
        while correct_word == displayed_color:
            displayed_color = random.choice(list(COLORS.keys()))
        word_display.config(text=correct_word.capitalize(), fg=COLORS[displayed_color])
    
    update_buttons()

def check_answer(selected_color):
    global SCORE, TOTAL
    if (mode == 1 and selected_color == correct_color) or (mode == 2 and selected_color == correct_word):
        SCORE += 1
    TOTAL += 1
    next_word()

def end_game():
    elapsed_time = time.time() - start_time
    result_label.config(text=f"Score: {SCORE}/{TOTAL}\nTime: {elapsed_time:.2f} sec")
    word_display.config(text="Game Over", fg='black')
    replay_button.pack(pady=10)  # Show replay button after game ends

def show_word_guide():
    for widget in guide_frame.winfo_children():
        widget.destroy()
    row, col = 0, 0
    for word, hex_value in COLORS.items():
        word_label = tk.Label(guide_frame, text=word.capitalize(), fg=hex_value, font=("Arial", 20))
        word_label.grid(row=row, column=col, padx=5, pady=5)
        col += 1
        if col > 3:  # Move to the next row after 4 columns
            col = 0
            row += 1

def update_buttons():
    for widget in button_frame.winfo_children():
        widget.destroy()
    row, col = 0, 0
    for color, hex_value in COLORS.items():
        button = tk.Button(button_frame, bg=hex_value, width=15, height=3, command=lambda c=color: check_answer(c))
        button.grid(row=row, column=col, padx=10, pady=10)
        col += 1
        if col > 3:
            col = 0
            row += 1

def select_mode():
    mode_selection_frame.pack()
    word_display.config(text="")
    result_label.config(text="")
    replay_button.pack_forget()

def start_mode(selected_mode):
    global mode
    mode = selected_mode
    mode_selection_frame.pack_forget()
    show_word_guide()
    start_button.pack(pady=10)  # Show start button after mode selection

def replay_game():
    select_mode()  # Return to mode selection screen

# GUI Setup
root = tk.Tk()
root.title("Stroop Test Selector")
root.geometry("800x800")

instructions = tk.Label(root, text="Select the Stroop Test Mode:\n1. Classic Stroop (Click the color of the word)\n2. Reverse Stroop (Click the color that matches the word meaning)", font=("Arial", 18))
instructions.pack(pady=10)

mode_selection_frame = tk.Frame(root)
mode_selection_frame.pack()

mode1_button = tk.Button(mode_selection_frame, text="Classic Stroop", font=("Arial", 18), command=lambda: start_mode(1))
mode1_button.pack(pady=10)
mode2_button = tk.Button(mode_selection_frame, text="Reverse Stroop", font=("Arial", 18), command=lambda: start_mode(2))
mode2_button.pack(pady=10)

guide_frame = tk.Frame(root)
guide_frame.pack(pady=5)

word_display = tk.Label(root, text="", font=("Arial", 40))
word_display.pack(pady=20)

button_frame = tk.Frame(root)
button_frame.pack(pady=20)

start_button = tk.Button(root, text="Start Test", font=("Arial", 22), command=start_game)
replay_button = tk.Button(root, text="Replay Game", font=("Arial", 22), command=replay_game)

result_label = tk.Label(root, text="", font=("Arial", 20))
result_label.pack()

select_mode()
root.mainloop()
