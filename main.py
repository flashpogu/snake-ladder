import tkinter as tk
from PIL import Image, ImageTk
import random

# Board setup with snakes and ladders
snakes = {16: 6, 46: 26, 49: 11, 62: 19, 74: 53, 89: 68, 92: 88, 95: 75, 99: 80}
ladders = {2: 38, 7: 14, 8: 31, 15: 26, 21: 42, 28: 84, 36: 44, 51: 67, 78: 98}

class SnakeLadderGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Snake and Ladder Game")
        
        self.board_size = 10
        self.cell_size = 50
        self.players = {"Player 1": 0, "Player 2": 0}
        self.current_player = "Player 1"
        
        self.canvas = tk.Canvas(root, width=500, height=500)
        self.canvas.pack()
        
        # Load and place the board image
        self.board_img = Image.open("./src/ULAR.gif")
        self.board_img = self.board_img.resize((500, 500))
        self.board_photo = ImageTk.PhotoImage(self.board_img)
        self.canvas.create_image(250, 250, image=self.board_photo)
        
        
        self.dice_label = tk.Label(root, text="Roll the Dice", font=("Arial", 14))
        self.dice_label.pack()
        
        self.roll_button = tk.Button(root, text="Roll Dice", command=self.roll_dice)
        self.roll_button.pack()
        
        self.status_label = tk.Label(root, text="Player 1's turn", font=("Arial", 12))
        self.status_label.pack()
        
        self.player_positions = {"Player 1": self.canvas.create_oval(5, 5, 20, 20, fill="red"),
                                "Player 2": self.canvas.create_oval(25, 5, 40, 20, fill="blue")}
    
    def roll_dice(self):
        roll = random.randint(1, 6)
        self.dice_label.config(text=f"Dice Roll: {roll}")
        self.animate_move(roll)
    
    def animate_move(self, steps):
        player = self.current_player
        start_position = self.players[player]
        end_position = start_position + steps
        
        if end_position > 100:
            return
        
        end_position = snakes.get(end_position, end_position)  # Snake check
        end_position = ladders.get(end_position, end_position)  # Ladder check
        
        def step_animation(pos):
            self.players[player] = pos
            self.update_player_position(player)
            if pos < end_position:
                self.root.after(300, lambda: step_animation(pos + 1))
            else:
                self.check_win_condition(player)
        
        step_animation(start_position + 1)
    
    def check_win_condition(self, player):
        if self.players[player] == 100:
            self.status_label.config(text=f"{player} Wins!")
            self.roll_button.config(state=tk.DISABLED)
        else:
            self.current_player = "Player 1" if self.current_player == "Player 2" else "Player 2"
            self.status_label.config(text=f"{self.current_player}'s turn")
    
    def update_player_position(self, player):
        position = self.players[player]
        row, col = divmod(position - 1, self.board_size)
        x = (col * self.cell_size) + 10 if row % 2 == 0 else ((9 - col) * self.cell_size) + 10
        y = (9 - row) * self.cell_size + 10
        self.canvas.coords(self.player_positions[player], x, y, x + 15, y + 15)

if __name__ == "__main__":
    root = tk.Tk()
    game = SnakeLadderGame(root)
    root.mainloop()
