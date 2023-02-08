'''
2022 Fall CS5001
Sliding Puzzle Game
Chuhan Ren
'''

import turtle
import os
import time
import puzzle


SPLASH = "./assets/Resources/splash_screen.gif"
QUIT = "./assets/Resources/quitbutton.gif"
LOAD = "./assets/Resources/loadbutton.gif"
RESET = "./assets/Resources/resetbutton.gif"
FILE_ERROR = "./assets/Resources/file_error.gif"
CREDITS = "./assets/Resources/credits.gif"
QUIT_MSG = "./assets/Resources/quitmsg.gif"
RESET_BUTTON = [50, -250]
LOAD_BUTTON = [150, -250]
QUIT_BUTTON = [250, -250]

myturtle = turtle.Turtle()
screen = turtle.Screen()
screen.setup(width=700, height=700)
screen.title("CS5001 Sliding Puzzle Game")


# set up screen and add splash screen
def show_splash():
    '''
        add splash screen at the beginning
    '''
    splash = turtle.Turtle()
    screen.addshape(SPLASH)
    splash.shape(SPLASH)
    time.sleep(3)
    screen.clear()


def draw_squares(myTurtle, xcor, ycor, width, height):
    '''
        function to draw square
    '''
    myTurtle.penup()
    myTurtle.goto(xcor, ycor)
    myTurtle.pendown()
    myTurtle.setheading(0)
    myTurtle.forward(width)
    myTurtle.setheading(90)
    myTurtle.forward(height)
    myTurtle.setheading(180)
    myTurtle.forward(width)
    myTurtle.setheading(270)
    myTurtle.forward(height)


def display_button(myTurtle, xcor, ycor, gif_name):
    '''
    display button
    :param myTurtle: turtle object
    :param xcor: x
    :param ycor: y
    :param gif_name: button name
    '''
    myTurtle.hideturtle()
    myTurtle.penup()
    myTurtle.goto(xcor, ycor)
    screen.addshape(gif_name)
    myTurtle.shape(gif_name)
    myTurtle.showturtle()


def draw_boards():
    '''
     draw boards
    '''
    _pen = turtle.Turtle()
    _pen.hideturtle()
    _pen.speed(10)
    _pen.pensize(6)
    draw_squares(_pen, -300, -300, 600, 100)
    draw_squares(_pen, -300, -150, 430, 450)
    _pen.pencolor("blue")
    draw_squares(_pen, 150, -150, 150, 450)


def create_buttons():
    '''
    add buttons
    '''
    reset_button = turtle.Turtle()
    load_button = turtle.Turtle()
    quit_button = turtle.Turtle()
    display_button(reset_button, RESET_BUTTON[0], RESET_BUTTON[1], RESET)
    display_button(load_button, LOAD_BUTTON[0], LOAD_BUTTON[1], LOAD)
    display_button(quit_button, QUIT_BUTTON[0], QUIT_BUTTON[1], QUIT)


def load():
    '''
    return puzzle file name
    '''
    folder_dir = "."
    puzzle_files = []
    for file in os.listdir(folder_dir):
        if file.endswith(".puz"):
            puzzle_files.append(file)
    puzzle_list = "\n".join(puzzle_files)
    choice = screen.textinput("Load Puzzle", f"Enter the name of the puzzle you wish to load. \n"
                                             f"Choices are:\n{puzzle_list}")
    return choice


def update_moves(moves):
    '''
        rewrite moves after each swap
    '''
    global myturtle
    myturtle.clear()
    myturtle.goto(-280, -260)
    # move_board().hideturtle()
    myturtle.write(f"Player Moves: {moves}", align="left", font=("Courier", 24, "normal"))


def update_leaderboard():
    '''
        update leaderboard after one user win one game, show the first
    '''
    leader_board = turtle.Turtle()
    leader_board.hideturtle()
    leader_board.penup()
    leader_board.pencolor("blue")
    leader_board.goto(160, 260)
    leader_board.write("Leaders:", align="left", font=("Courier", 18, "normal"))
    leaders = turtle.Turtle()
    leaders.clear()
    leaders.pencolor("blue")
    leaders.penup()
    leaders.goto(160, 220)
    screen.tracer(0)
    with open("leader_ranking.txt", mode="r") as data:
        for line in data:
            leaders.hideturtle()
            leaders.setheading(270)
            leaders.forward(30)
            leaders.write(f"{line}\n", align="left", font=("Courier", 18, "normal"))
    screen.update()


def quit_game():
    '''
    quit the game, show credits and close window
    '''
    quit_turtle = turtle.Turtle()
    # myturtle.reset()
    screen.addshape(QUIT_MSG)
    screen.addshape(CREDITS)
    screen.tracer(0)
    quit_turtle.shape(QUIT_MSG)
    screen.update()
    time.sleep(1)
    quit_turtle.reset()
    screen.tracer(0)
    quit_turtle.shape(CREDITS)
    quit_turtle.showturtle()
    screen.update()
    time.sleep(1)
    exit()


def click_buttons(x, y):
    '''
    function for three buttons and the puzzle game board, to reset puzzle, to load different puzzle or to quit the
    window, if click on the puzzle board, start the game
    '''
    global current_puzzle

    # to reset the current puzzle
    if RESET_BUTTON[0] - 40 < x < RESET_BUTTON[0] + 40 and RESET_BUTTON[1] - 40 < y < RESET_BUTTON[1] + 40:
        myturtle.clear()
        current_puzzle.clear_squares()
        current_puzzle.moves = 0
        current_puzzle.puz_reset()

    # load new puzzle
    if LOAD_BUTTON[0] - 40 < x < LOAD_BUTTON[0] + 40 and LOAD_BUTTON[1] - 40 < y < LOAD_BUTTON[1] + 40:
        screen.tracer(0)
        choice = load()
        if os.path.exists(choice): # if file exists, create the game board
            screen.tracer(0)
            myturtle.clear()
            current_puzzle.clear_squares()
            current_puzzle.clear_image()
            current_puzzle.clear_logo()
            current_puzzle = puzzle.Tiles(choice, max_moves, name)
            current_puzzle.create_tiles()
            current_puzzle.show_logo()
            screen.update()
        if not os.path.exists(choice):  # if file doesn't exist, show error message
            error = turtle.Turtle()
            screen.tracer(0)
            screen.addshape(FILE_ERROR)
            error.shape(FILE_ERROR)
            error.showturtle()
            screen.update()
            time.sleep(2)
            error.reset()

    if QUIT_BUTTON[0] - 40 < x < QUIT_BUTTON[0] + 40 and QUIT_BUTTON[1] - 26.5 < y < QUIT_BUTTON[1] + 26.5:
        quit_game()

    # if we click on other areas, in the game board, the game starts
    else:
        current_puzzle.if_win(x, y)
        update_moves(current_puzzle.moves)


show_splash()
name = screen.textinput("CS5001 Puzzle Slide", "Your name:")
max_moves = screen.numinput("CS5001 Puzzle Slide - Moves",
                            "Enter the number of moves (chances) you want (5-200):",
                            minval=5, maxval=200)
current_puzzle = puzzle.Tiles("mario.puz", max_moves, name) # set default puzzle to mario


def main():
    draw_boards()
    create_buttons()
    current_puzzle.create_tiles()
    current_puzzle.show_logo()
    update_leaderboard()
    screen.onclick(click_buttons)
    screen.mainloop()


if __name__ == '__main__':
    main()
