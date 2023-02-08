'''
ImageDic class
methods to extract puzzle's information
'''
import random
import copy
import turtle

my_turtle = turtle.Turtle()
my_screen = turtle.Screen()


class ImageDic:
    def __init__(self, file_name):
        self.file_name = file_name
        self.puz_dic = {}
        self.get_dict()
        self.all_tiles = []
        self.all_tiles_dic = {}
        self.size = int(self.get_tile_size())
        self.puzzle_name = self.get_puzzle_name()
        self.tiles_amount = int(self.get_tile_amount())
        self.get_tiles_list()
        self.get_tiles_dic()

    def get_dict(self):
        '''
        get puz information and create dictionary
        :return: dictionary
        '''
        with open(self.file_name, mode='r', encoding='utf-8') as file:
            for line in file:
                (key, value) = line.strip().split(": ")
                self.puz_dic[key] = value
        return self.puz_dic

    def get_tiles_list(self):
        '''
        create a list of image file paths
        :return: list
        '''
        for key in self.puz_dic:
            if key.isdigit():
                self.all_tiles.append(f"./assets/{self.puz_dic[key]}")
        return self.all_tiles

    def get_tiles_dic(self):
        '''
        :return: dictionary, key is the number of each image, value is file path
        '''
        for key in self.puz_dic:
            if key.isdigit():
                self.all_tiles_dic[key] = f"./assets/{self.puz_dic[key]}"
        return self.all_tiles_dic

    def shuffle_tiles(self):
        '''
        function to shuffle images and make a random list
        :return: random list
        '''
        random_tiles = copy.deepcopy(self.all_tiles)
        random.shuffle(random_tiles)
        return random_tiles

    def get_puzzle_name(self):
        '''
        :return: puzzle's name
        '''
        return self.puz_dic['name']

    def get_tile_amount(self):
        '''

        :return: puzzle's tile amount
        '''
        return self.puz_dic['number']

    def get_tile_size(self):
        '''

        :return: puzzle's size
        '''
        return self.puz_dic['size']

    def get_logo(self):
        '''

        :return: thumbnail's path
        '''
        return f"./assets/{self.puz_dic['thumbnail']}"
