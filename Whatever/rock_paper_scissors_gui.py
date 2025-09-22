import random
import tkinter as tk
from tkinter import ttk, messagebox

class RockPaperScissorsGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Rock Paper Scissors")
        self.root.geometry("400x500")
        self.root.resizable(False, False)
        
        # Game state
        self.player_score = 0
        self.computer_score = 0
        
        self.setup_ui()
    
    def setup_ui(self):
        # Title
        title_label = tk.Label(self.root, text="Rock Paper Scissors", 
                              font=("Arial", 20, "bold"))
        title_label.pack(pady=10)
        
        # Score display
        self.score_frame = tk.Frame(self.root)
        self.score_frame.pack(pady=10)
        
        self.score_label = tk.Label(self.score_frame, 
                                   text=f"Player: {self.player_score}  Computer: {self.computer_score}",
                                   font=("Arial", 14))
        self.score_label.pack()
        
        # Choice buttons frame
        button_frame = tk.Frame(self.root)
        button_frame.pack(pady=20)
        
        # Player choice buttons
        tk.Label(button_frame, text="Choose your move:", font=("Arial", 12)).pack()
        
        choices_frame = tk.Frame(button_frame)
        choices_frame.pack(pady=10)
        
        self.rock_btn = tk.Button(choices_frame, text="🪨\nRock", 
                                 font=("Arial", 12), width=8, height=3,
                                 command=lambda: self.play_round('rock'))
        self.rock_btn.pack(side=tk.LEFT, padx=5)
        
        self.paper_btn = tk.Button(choices_frame, text="📄\nPaper", 
                                  font=("Arial", 12), width=8, height=3,
                                  command=lambda: self.play_round('paper'))
        self.paper_btn.pack(side=tk.LEFT, padx=5)
        
        self.scissors_btn = tk.Button(choices_frame, text="✂️\nScissors", 
                                     font=("Arial", 12), width=8, height=3,
                                     command=lambda: self.play_round('scissors'))
        self.scissors_btn.pack(side=tk.LEFT, padx=5)
        
        # Results display area
        self.results_frame = tk.Frame(self.root)
        self.results_frame.pack(pady=20, fill=tk.BOTH, expand=True)
        
        # Choice display
        self.choice_display = tk.Label(self.results_frame, text="", 
                                      font=("Arial", 12))
        self.choice_display.pack(pady=5)
        
        # Winner display
        self.winner_label = tk.Label(self.results_frame, text="", 
                                    font=("Arial", 14, "bold"))
        self.winner_label.pack(pady=5)
        
        # Game history text area
        self.history_label = tk.Label(self.results_frame, text="Game History:", 
                                     font=("Arial", 10))
        self.history_label.pack(anchor=tk.W, padx=20)
        
        self.history_text = tk.Text(self.results_frame, height=8, width=45, 
                                   font=("Arial", 9))
        self.history_text.pack(pady=5, padx=20)
        
        # Scrollbar for history
        scrollbar = tk.Scrollbar(self.history_text)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.history_text.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.history_text.yview)
        
        # Control buttons
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        
        self.reset_btn = tk.Button(control_frame, text="Reset Game", 
                                  font=("Arial", 10), 
                                  command=self.reset_game)
        self.reset_btn.pack(side=tk.LEFT, padx=5)
        
        self.quit_btn = tk.Button(control_frame, text="Quit", 
                                 font=("Arial", 10), 
                                 command=self.quit_game)
        self.quit_btn.pack(side=tk.LEFT, padx=5)
    
    def get_computer_choice(self):
        return random.choice(['rock', 'paper', 'scissors'])
    
    def get_winner(self, player, computer):
        if player == computer:
            return 'tie'
        elif (player == 'rock' and computer == 'scissors') or \
             (player == 'paper' and computer == 'rock') or \
             (player == 'scissors' and computer == 'paper'):
            return 'player'
        else:
            return 'computer'
    
    def play_round(self, player_choice):
        computer_choice = self.get_computer_choice()
        winner = self.get_winner(player_choice, computer_choice)
        
        # Update display
        choice_text = f"You chose: {player_choice.title()}   Computer chose: {computer_choice.title()}"
        self.choice_display.config(text=choice_text)
        
        # Update scores and winner display
        if winner == 'player':
            self.player_score += 1
            self.winner_label.config(text="You Win This Round!", fg="green")
            result_text = "You win!"
        elif winner == 'computer':
            self.computer_score += 1
            self.winner_label.config(text="Computer Wins This Round!", fg="red")
            result_text = "Computer wins!"
        else:
            self.winner_label.config(text="It's a Tie!", fg="blue")
            result_text = "Tie!"
        
        # Update score display
        self.score_label.config(text=f"Player: {self.player_score}  Computer: {self.computer_score}")
        
        # Add to history
        history_entry = f"{player_choice.title()} vs {computer_choice.title()} - {result_text}\n"
        self.history_text.insert(tk.END, history_entry)
        self.history_text.see(tk.END)
    
    def reset_game(self):
        if messagebox.askyesno("Reset Game", "Are you sure you want to reset the game?"):
            self.player_score = 0
            self.computer_score = 0
            self.score_label.config(text=f"Player: {self.player_score}  Computer: {self.computer_score}")
            self.choice_display.config(text="")
            self.winner_label.config(text="")
            self.history_text.delete(1.0, tk.END)
    
    def quit_game(self):
        if messagebox.askyesno("Quit", "Are you sure you want to quit?"):
            self.root.quit()

def main():
    root = tk.Tk()
    game = RockPaperScissorsGUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()