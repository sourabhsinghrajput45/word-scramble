import random
import json
import os
import tkinter as tk
from tkinter import messagebox, ttk

# --- Word Lists by Difficulty ---
EASY = ["cat", "dog", "ball", "tree", "book", "car", "sun"]
MEDIUM = ["python", "syntax", "debug", "project", "function"]
HARD = ["algorithm", "developer", "variable", "programming", "scramble"]

HIGHSCORE_FILE = "highscore.json"


# --- High Score Management ---
def load_highscore():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as f:
            return json.load(f).get("highscore", 0)
    return 0


def save_highscore(score):
    with open(HIGHSCORE_FILE, "w") as f:
        json.dump({"highscore": score}, f)


# --- Main Game Class ---
class WordScrambleApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🧩 Word Scramble Game")
        self.root.geometry("480x420")
        self.root.resizable(False, False)
        self.root.config(bg="#222831")

        self.score = 0
        self.highscore = load_highscore()
        self.round = 1
        self.total_rounds = 5
        self.current_word = ""
        self.used_words = []
        self.words = EASY  # default until chosen

        # ---------- SCREENS ----------
        self.create_start_screen()

    # ---------- START SCREEN ----------
    def create_start_screen(self):
        self.clear_screen()

        title = tk.Label(
            self.root,
            text="🧩 Word Scramble",
            font=("Arial Rounded MT Bold", 26, "bold"),
            fg="#00ADB5",
            bg="#222831",
        )
        title.pack(pady=30)

        diff_frame = tk.Frame(self.root, bg="#222831")
        diff_frame.pack(pady=10)

        tk.Label(
            diff_frame, text="Select Difficulty:", font=("Arial", 12),
            fg="#EEEEEE", bg="#222831"
        ).pack(side=tk.LEFT, padx=5)

        self.difficulty_var = tk.StringVar(value="Easy")
        dropdown = ttk.Combobox(
            diff_frame,
            textvariable=self.difficulty_var,
            values=["Easy", "Medium", "Hard"],
            font=("Arial", 12),
            state="readonly",
            width=10
        )
        dropdown.pack(side=tk.LEFT, padx=5)

        start_btn = tk.Button(
            self.root,
            text="Start Game",
            command=self.start_game,
            font=("Arial", 14, "bold"),
            bg="#00ADB5",
            fg="#222831",
            width=15,
        )
        start_btn.pack(pady=20)

        hs_label = tk.Label(
            self.root,
            text=f"🏆 High Score: {self.highscore}",
            font=("Arial", 12, "bold"),
            fg="#FFD369",
            bg="#222831",
        )
        hs_label.pack(pady=10)

    # ---------- GAME SCREEN ----------
    def start_game(self):
        level = self.difficulty_var.get()
        self.words = {"Easy": EASY, "Medium": MEDIUM, "Hard": HARD}[level]
        self.difficulty = level
        self.score = 0
        self.round = 1
        self.used_words = []
        self.create_game_screen()
        self.new_word()

    def create_game_screen(self):
        self.clear_screen()

        self.title_label = tk.Label(
            self.root, text=f"Word Scramble ({self.difficulty})",
            font=("Arial Rounded MT Bold", 20), fg="#00ADB5", bg="#222831"
        )
        self.title_label.pack(pady=20)

        self.round_label = tk.Label(
            self.root, text=f"Round {self.round}/{self.total_rounds}",
            font=("Arial", 12), fg="#EEEEEE", bg="#222831"
        )
        self.round_label.pack()

        self.word_label = tk.Label(
            self.root, text="", font=("Consolas", 24, "bold"),
            fg="#FFD369", bg="#222831"
        )
        self.word_label.pack(pady=15)

        self.entry = tk.Entry(self.root, font=("Arial", 16), justify="center", width=20)
        self.entry.pack(pady=10)

        btn_frame = tk.Frame(self.root, bg="#222831")
        btn_frame.pack(pady=10)

        self.submit_button = tk.Button(
            btn_frame, text="Submit", command=self.check_answer,
            font=("Arial", 12, "bold"), bg="#00ADB5", fg="#222831", width=10
        )
        self.submit_button.grid(row=0, column=0, padx=10)

        self.next_button = tk.Button(
            btn_frame, text="Next Word", command=self.next_round,
            font=("Arial", 12, "bold"), bg="#393E46", fg="#EEEEEE",
            width=10, state="disabled"
        )
        self.next_button.grid(row=0, column=1, padx=10)

        self.score_label = tk.Label(
            self.root,
            text=f"Score: {self.score} | High Score: {self.highscore}",
            font=("Arial", 12, "bold"), fg="#EEEEEE", bg="#222831"
        )
        self.score_label.pack(pady=10)

        # Keyboard shortcuts
        self.root.bind("<Return>", lambda event: self.check_answer())
        self.root.bind("<space>", lambda event: self.next_round())

    # ---------- GAME LOGIC ----------
    def new_word(self):
        available_words = [w for w in self.words if w not in self.used_words]
        if not available_words:
            self.used_words = []
            available_words = self.words[:]

        self.current_word = random.choice(available_words)
        self.used_words.append(self.current_word)

        scrambled = list(self.current_word)
        random.shuffle(scrambled)
        self.word_label.config(text="".join(scrambled))
        self.entry.config(state="normal")
        self.entry.delete(0, tk.END)
        self.entry.focus()

    def check_answer(self):
        guess = self.entry.get().strip().lower()
        self.entry.config(state="disabled")

        if guess == self.current_word:
            messagebox.showinfo("✅ Correct!", f"Nice! The word was '{self.current_word}'.")
            self.score += 1
        else:
            messagebox.showerror("❌ Incorrect!", f"Oops! The correct word was '{self.current_word}'.")

        self.score_label.config(
            text=f"Score: {self.score} | High Score: {self.highscore}"
        )
        self.submit_button.config(state="disabled")
        self.next_button.config(state="normal")

    def next_round(self):
        self.round += 1
        if self.round > self.total_rounds:
            self.end_game()
        else:
            self.round_label.config(text=f"Round {self.round}/{self.total_rounds}")
            self.submit_button.config(state="normal")
            self.next_button.config(state="disabled")
            self.new_word()

    def end_game(self):
        messagebox.showinfo("🏁 Game Over", f"Your final score: {self.score}/{self.total_rounds}")

        if self.score > self.highscore:
            save_highscore(self.score)
            messagebox.showinfo("🎉 New High Score!", f"You set a new record: {self.score}!")
            self.highscore = self.score

        if messagebox.askyesno("Play Again?", "Do you want to play again?"):
            self.create_start_screen()
        else:
            self.root.destroy()

    # ---------- Helper ----------
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()


# --- Entry Point ---
def main():
    root = tk.Tk()
    app = WordScrambleApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
