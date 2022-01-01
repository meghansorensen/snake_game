import curses
from random import randint

WINDOW_WIDTH = 60
WINDOW_HEIGHT = 20

# setup window for game
curses.initscr()
win = curses.newwin(WINDOW_HEIGHT, WINDOW_WIDTH, 0, 0)  # row, column
win.keypad(1)
curses.noecho()
curses.curs_set(0)
win.border(0)
win.nodelay(1)

# Snake and Food
# Snake is a Tuple
snake = [(4, 10), (4, 9), (4, 8)]
food = (10, 20)

# Set up food in the window
win.addch(food[0], food[1], '$')
# Game Logic
score = 0
ESC = 27
# Start by moving the snake to the right
key = curses.KEY_RIGHT
key_list = [curses.KEY_LEFT, curses.KEY_RIGHT,
            curses.KEY_UP, curses.KEY_DOWN, ESC]

while key != ESC:
    win.addstr(0, 2, 'Score ' + str(score) + ' ')
    # Increase the speed of the snake as it gets larger
    win.timeout(150 - (len(snake)) // 5 + len(snake) // 10 % 120)

    prev_key = key
    event = win.getch()
    key = event if event != -1 else prev_key

    if key not in key_list:
        key = prev_key

    # Calculate the next coordinates of the snake
    y = snake[0][0]
    x = snake[0][1]
    if key == curses.KEY_DOWN:
        y += 1
    elif key == curses.KEY_UP:
        y -= 1
    elif key == curses.KEY_LEFT:
        x -= 1
    elif key == curses.KEY_RIGHT:
        x += 1
    snake.insert(0, (y, x))

    # Check if we hit the border
    if y == 0:
        break
    if y == 19:
        break
    if x == 0:
        break
    if x == 59:
        break

    # Check if the Snake runs over itself
    if snake[0] in snake[1:]:
        break

    # Check if the Snake hits the food
    if snake[0] == food:
        # Add it to the snale
        score += 1
        food = ()
        # Get a new food location
        while food == ():
            food = (randint(1, WINDOW_HEIGHT - 2),
                    randint(1, WINDOW_WIDTH - 2))
            # Make sure the new food doesn't show up in the snake spots
            if food in snake:
                food = ()
        win.addch(food[0], food[1], '$')
    else:
        # move snake
        last = snake.pop()
        win.addch(last[0], last[1], ' ')

    # Put food in the window
    win.addch(snake[0][0], snake[0][1], '*')

curses.endwin()
print(f"Final Score = {score}")
