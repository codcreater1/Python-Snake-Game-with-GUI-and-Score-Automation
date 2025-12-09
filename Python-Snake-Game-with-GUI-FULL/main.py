
import tkinter as tk
import random
import csv
from datetime import datetime

GAME_WIDTH = 700
GAME_HEIGHT = 700
SPEED = 100
SPACE_SIZE = 50
BODY_PARTS = 3
SNAKE_COLOR = "#00FF00"
FOOD_COLOR = "#FF0000"
BACKGROUND_COLOR = "#000000"

score = 0
direction = 'down'

def game_over():
    global score
    # Save score into scores.csv
    with open("scores.csv", "a", newline="") as file:
        writer = csv.writer(file)
        writer.writerow([score, datetime.now().strftime("%Y-%m-%d %H:%M:%S")])

    canvas.delete("all")
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/2,
                       font=('consolas',70), text="GAME OVER", fill="red", tag="gameover")
    canvas.create_text(canvas.winfo_width()/2, canvas.winfo_height()/1.5,
                       font=('consolas',40), text=f"Score: {score}", fill="white")

def next_turn():
    global score, direction

    x, y = snake_coords[-1]

    if direction == "up":
        y -= SPACE_SIZE
    elif direction == "down":
        y += SPACE_SIZE
    elif direction == "left":
        x -= SPACE_SIZE
    elif direction == "right":
        x += SPACE_SIZE

    snake_coords.append([x, y])
    square = canvas.create_rectangle(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=SNAKE_COLOR)
    snake_squares.append(square)

    if x == food_coords[0] and y == food_coords[1]:
        score += 1
        label.config(text=f"Score: {score}")
        canvas.delete(food_square)
        create_food()
    else:
        del snake_coords[0]
        canvas.delete(snake_squares[0])
        del snake_squares[0]

    if check_collisions():
        game_over()
    else:
        window.after(SPEED, next_turn)

def change_direction(new_direction):
    global direction

    if new_direction == 'left' and direction != 'right':
        direction = new_direction
    elif new_direction == 'right' and direction != 'left':
        direction = new_direction
    elif new_direction == 'up' and direction != 'down':
        direction = new_direction
    elif new_direction == 'down' and direction != 'up':
        direction = new_direction

def create_food():
    global food_coords, food_square

    x = random.randint(0, (GAME_WIDTH // SPACE_SIZE) - 1) * SPACE_SIZE
    y = random.randint(0, (GAME_HEIGHT // SPACE_SIZE) - 1) * SPACE_SIZE

    food_coords = [x, y]
    food_square = canvas.create_oval(x, y, x + SPACE_SIZE, y + SPACE_SIZE, fill=FOOD_COLOR)

def check_collisions():
    x, y = snake_coords[-1]

    if x < 0 or x >= GAME_WIDTH or y < 0 or y >= GAME_HEIGHT:
        return True

    if [x, y] in snake_coords[:-1]:
        return True

    return False

window = tk.Tk()
window.title("Snake Game")

label = tk.Label(window, text="Score: 0", font=("consolas", 40))
label.pack()

canvas = tk.Canvas(window, bg=BACKGROUND_COLOR, height=GAME_HEIGHT, width=GAME_WIDTH)
canvas.pack()

window.update()

snake_coords = [[0,0] for _ in range(BODY_PARTS)]
snake_squares = [canvas.create_rectangle(0, 0, SPACE_SIZE, SPACE_SIZE, fill=SNAKE_COLOR) for _ in range(BODY_PARTS)]

create_food()

window.bind('<Left>', lambda event: change_direction('left'))
window.bind('<Right>', lambda event: change_direction('right'))
window.bind('<Up>', lambda event: change_direction('up'))
window.bind('<Down>', lambda event: change_direction('down'))

next_turn()

window.mainloop()
