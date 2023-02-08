'''
Tiles class
methods for behaviors
'''
import time
from turtle import Turtle, Screen
from image_dic import ImageDic
from leaderboard import Leaders
import math

IMAGE_LOCATIONS = [[(-231, 231), (-131, 231), (-31, 231), (69, 231)], [(-231, 131), (-131, 131), (-31, 131), (69, 131)],
                   [(-231, 31), (-131, 31), (-31, 31), (69, 31)], [(-231, -69), (-131, -69), (-31, -69), (69, -69)]]

SQUARE_LOCATIONS = [[(-280, 182), (-180, 182), (-80, 182), (20, 182)], [(-280, 82), (-180, 82), (-80, 82), (20, 82)],
                    [(-280, -18), (-180, -18), (-80, -18), (20, -18)],
                    [(-280, -118), (-180, -118), (-80, -118), (20, -118)]]

CREDITS = "./assets/Resources/credits.gif"
WINNER = "./assets/Resources/winner.gif"
LOSE = "./assets/Resources/Lose.gif"

my_screen = Screen()

class Tiles(Turtle):
    def __init__(self, file_name, max_step, user_name):
        '''

        :param file_name: puz file name
        :param max_step: max steps for solving the puzzle
        :param user_name: user name
        '''
        super(Tiles).__init__()
        self.user_name = user_name
        self.file_name = file_name  # puz file name
        self.screen = Screen()
        self.puzzle = ImageDic(self.file_name)  # image object
        self.size = self.puzzle.size # image size
        self.name = self.puzzle.puzzle_name  # clean puzzle name
        self.amount = self.puzzle.tiles_amount  # puzzle amount
        self.all_tiles = self.puzzle.all_tiles  # tile list in the correct order
        self.max_step = max_step
        self.image_positions = self.tile_position_list()  # positions for turtles to go to
        self.square_positions = self.square_position_list()  # positions to start drawing
        self.random_tiles = []  # tiles after shuffle
        self.tile_objects_lst = []  # list of turtle objects with images after first created
        self.square_object_lst = []  # list of turtle objects draw squares
        self.logo = []  # list for the logo object
        self.current_positions = []  # positions for turtles once swap
        self.moves = 0

    def tile_position_list(self):
        '''
        create positions list for tiles, based on amount
        :return: list
        '''
        tile_position = []
        sqrt = int(math.sqrt(self.amount))
        for index in range(sqrt):
            tile_position.extend(IMAGE_LOCATIONS[index][0:sqrt])
        return tile_position

    def square_position_list(self):
        '''
        create position list to start drawing squares
        :return: list
        '''
        square_position = []
        sqrt = int(math.sqrt(self.amount))
        for index in range(sqrt):
            square_position.extend(SQUARE_LOCATIONS[index][0:sqrt])
        return square_position

    def create_tiles(self):
        '''
        based on tile amount, draw single square and place tile
        '''
        self.random_tiles = self.puzzle.shuffle_tiles()
        for index in range(len(self.random_tiles)):
            self.draw_squares(self.square_positions[index])
            self.add_tiles(self.random_tiles[index], self.image_positions[index])

    def draw_squares(self, location):
        '''
        behavior of drawing single square
        :param location: location of single square
        '''
        square = Turtle()
        square.speed("fastest")
        square.hideturtle()
        square.penup()
        square.pensize(2)
        square.goto(location)
        square.pendown()
        square.setheading(0)
        square.forward(self.size)
        square.setheading(90)
        square.forward(self.size)
        square.setheading(180)
        square.forward(self.size)
        square.setheading(270)
        square.forward(self.size)
        self.square_object_lst.append(square)

    def add_tiles(self, image, location):
        '''
        :param image: file path of single tile
        :param location: location of single tile
        '''
        tile = Turtle()
        tile.hideturtle()
        self.screen.addshape(image)
        tile.shape(image)
        tile.penup()
        tile.goto(location)
        tile.showturtle()
        tile.pendown()
        self.tile_objects_lst.append(tile)

    def show_logo(self):
        '''
        display thumbnail image
        '''
        screen = Screen()
        screen.tracer(0)
        logo = Turtle()
        logo.hideturtle()
        logo.penup()
        screen.addshape(self.puzzle.get_logo())
        logo.shape(self.puzzle.get_logo())
        logo.goto(280, 280)
        logo.showturtle()
        logo.pendown()
        screen.update()
        self.logo.append(logo)

    def get_blank(self):
        '''
        get blank tile's object by blank's file name
        :return: turtle object of blank image
        '''
        global pos
        for i, j in enumerate(self.random_tiles):
            if j == f"./assets/Images/{self.name}/blank.gif":
                return self.tile_objects_lst[i]

    def identify_tile(self, x, y):
        '''
        given position, find the corresponding turtle object of the tile from list
        '''
        global pos
        for each in self.tile_objects_lst:
            a, b = each.xcor(), each.ycor()
            if a - 49 <= x <= a + 49 and b - 49 <= y <= b + 49:
                return each

    def adjacent(self, x, y):
        '''
        verify if the tile is adjacent to blank tile, return true if they are adjacent
        '''
        global pos
        blank = self.get_blank()
        if 51 <= blank.distance(self.identify_tile(x, y)) <= 100:
            return True

    def swap(self, x, y):
        '''
        if adjacent, tile goto blank's position, blank goto tile's position
        '''
        global pos
        blank = self.get_blank()
        the_tile = self.identify_tile(x, y)
        if self.adjacent(x, y):
            tile_position = (the_tile.xcor(), the_tile.ycor())
            blank.hideturtle()
            the_tile.penup()
            self.screen.tracer(0)
            the_tile.goto(blank.xcor(), blank.ycor())
            self.screen.update()
            blank.penup()
            self.screen.tracer(0)
            blank.goto(tile_position)
            blank.showturtle()
            self.screen.update()
        return True

    def add_moves(self, x, y):
        '''
        if swap, add one move
        '''
        if self.swap(x, y):
            self.moves += 1
        return self.moves

    def update_positions(self, x, y):
        '''
        once we did swap, update the new positions for each turtle object
        :return: current positions for turtles once swap
        '''
        global pos
        if self.swap(x, y):
            self.current_positions.clear()
            for each in self.tile_objects_lst:
                self.current_positions.append((each.xcor(), each.ycor()))
        return self.current_positions

    def final_position(self):
        '''
        find the positions for turtle objects in the list we created at first, give the positions if they were
        in right order, it's the final positions we want for turtle objects if puzzle is solved
        '''
        index_list = []
        final_positions = []
        for each in self.random_tiles:
            index = self.all_tiles.index(each)
            index_list.append(index)
        for i, j in enumerate(index_list):
            final_positions.append(self.image_positions[j])
        return final_positions

    def if_win(self, x, y):
        '''
        justify win or lose by comparing position list from two previous functions, show gif message when you win/lose
        :return: final moves
        '''
        global pos
        winner = Turtle()
        screen = Screen()
        screen.tracer(0)
        winner.hideturtle()
        moves = self.add_moves(x, y)
        a = self.update_positions(x, y)  # turtles current positions
        b = self.final_position()  # final positions if solved

        if 1 <= moves <= self.max_step and a == b:
            screen.tracer(0)
            leaders = Leaders(self.user_name, moves)
            leaders.rewrite_file()
            screen.addshape(WINNER)
            winner.shape(WINNER)
            winner.showturtle()
            screen.update()
            time.sleep(2)
            winner.reset()
            screen.addshape(CREDITS)
            winner.shape(CREDITS)
            screen.update()
            return moves
        if moves >= self.max_step and a != b:
            screen.tracer(0)
            screen.addshape(LOSE)
            winner.shape(LOSE)
            winner.showturtle()
            screen.update()
            time.sleep(2)
            winner.reset()
            screen.addshape(CREDITS)
            winner.shape(CREDITS)
            screen.update()

    def clear_squares(self):
        '''
        clear square drawing
        '''
        self.screen.tracer(0)
        for each in self.square_object_lst:
            each.reset()
            each.hideturtle()
        self.screen.update()

    def clear_image(self):
        '''
        clear tiles
        '''
        self.screen.tracer(0)
        for each in self.tile_objects_lst:
            each.reset()
            each.hideturtle()
        self.screen.update()

    def clear_logo(self):
        '''
        clear thumbnail
        '''
        self.screen.tracer(0)
        for each in self.logo:
            each.reset()
            each.hideturtle()
        self.logo.clear()
        self.screen.update()

    def puz_reset(self):
        '''
        reset puzzle
        '''
        self.screen.tracer(0)
        for each in self.tile_objects_lst:
            each.reset()
            each.hideturtle()
        self.screen.update()
        self.random_tiles = self.all_tiles  # assign it back to the list with right order
        self.tile_objects_lst.clear()  # clear turtle object list
        self.square_object_lst.clear()
        self.screen.tracer(0)
        for index in range(len(self.random_tiles)):   # create tiles in correct order
            self.add_tiles(self.random_tiles[index], self.image_positions[index])
        self.screen.update()

