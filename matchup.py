import tkinter as tk
from tkinter import messagebox
import random

class TournamentApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Tournament Matchmaker")

        self.bye_var = tk.IntVar()
        self.players = []

        self.setup_ui()

    def setup_ui(self):
        tk.Label(self.root, text="Tournament Matchmaker", font=("Arial", 16, "bold")).pack(pady=10)

        # BYE checkbox
        self.bye_check = tk.Checkbutton(self.root, text="Was there a player already on BYE?", variable=self.bye_var, command=self.toggle_bye)
        self.bye_check.pack()

        # BYE name input
        self.bye_name_label = tk.Label(self.root, text="BYE Player Name:")
        self.bye_name_entry = tk.Entry(self.root, width=30)

        # Number of players
        tk.Label(self.root, text="Number of Players (excluding BYE if any):").pack(pady=(10,0))
        self.num_entry = tk.Entry(self.root, width=10)
        self.num_entry.pack()

        # Button to set player fields
        tk.Button(self.root, text="Set Player Fields", command=self.create_player_entries).pack(pady=10)

        self.players_frame = tk.Frame(self.root)
        self.players_frame.pack()

        # Match button
        self.match_button = tk.Button(self.root, text="Generate Matches", command=self.generate_matches)
        self.match_button.pack(pady=10)

        # Output
        self.output_text = tk.Text(self.root, height=15, width=50, state='disabled')
        self.output_text.pack(pady=10)

    def toggle_bye(self):
        if self.bye_var.get():
            self.bye_name_label.pack()
            self.bye_name_entry.pack()
        else:
            self.bye_name_label.pack_forget()
            self.bye_name_entry.pack_forget()

    def create_player_entries(self):
        # Clear previous player fields
        for widget in self.players_frame.winfo_children():
            widget.destroy()
        self.players = []

        try:
            count = int(self.num_entry.get())
            if count < 1:
                raise ValueError
        except ValueError:
            messagebox.showerror("Invalid Input", "Please enter a valid number of players.")
            return

        for i in range(count):
            label = tk.Label(self.players_frame, text=f"Player {i + 1} Name:")
            label.grid(row=i, column=0, sticky="e", padx=5, pady=2)
            entry = tk.Entry(self.players_frame, width=30)
            entry.grid(row=i, column=1, padx=5, pady=2)
            self.players.append(entry)

    def generate_matches(self):
        player_names = [entry.get().strip() for entry in self.players if entry.get().strip()]
        if len(player_names) != len(self.players):
            messagebox.showerror("Missing Names", "Please fill in all player names.")
            return

        if self.bye_var.get():
            bye_name = self.bye_name_entry.get().strip()
            if not bye_name:
                messagebox.showerror("Missing BYE Name", "Please enter the BYE player name.")
                return
            if bye_name in player_names:
                messagebox.showerror("Duplicate Name", "BYE player name must be different from others.")
                return
            random.shuffle(player_names)
            first_opponent = player_names.pop()
            matches = [(bye_name, first_opponent)]
        else:
            matches = []

        # Handle odd number of players
        if len(player_names) % 2 != 0:
            bye_player = random.choice(player_names)
            player_names.remove(bye_player)
            matches.append((bye_player, None))

        # Create pairs
        random.shuffle(player_names)
        while player_names:
            p1 = player_names.pop()
            p2 = player_names.pop()
            matches.append((p1, p2))

        # Display
        self.output_text.config(state='normal')
        self.output_text.delete("1.0", tk.END)
        self.output_text.insert(tk.END, "Matchups:\n")
        for p1, p2 in matches:
            if p2:
                self.output_text.insert(tk.END, f"{p1} vs {p2}\n")
            else:
                self.output_text.insert(tk.END, f"{p1} is on BYE\n")
        self.output_text.config(state='disabled')


if __name__ == "__main__":
    root = tk.Tk()
    app = TournamentApp(root)
    root.mainloop()
