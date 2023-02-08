'''
class Leaders
methods to read player moves file and write a new file with the right ranking
'''


class Leaders:
    def __init__(self, user_name, final_moves):
        self.max_moves = final_moves
        self.user_name = user_name
        self.leader_list = []  # should be a nested list

    def update_moves(self):
        '''
        write name and its moves to the leaderboard file
        :return:
        '''
        with open("leaders.txt", mode="a") as self.out_data:
            self.out_data.write(f"{self.max_moves}:{self.user_name}\n")

    def rank(self):
        """
         rank the dictionary and return the first 10 players
        """
        with open("leaders.txt", mode="r") as self.data:  # make a nested list of name and move
            for line in self.data:
                a, b = line.strip().split(":")
                a_list = [a, b]
                self.leader_list.append(a_list)
        self.leader_list.sort(key=lambda x: int(x[0]))  # rank nested list
        return self.leader_list

    def rewrite_file(self):
        '''
            rewrite leaders file with the right rank
        '''
        self.update_moves()
        rank_list = self.rank()
        with open("leader_ranking.txt", mode="w") as self.rank_data:
            for each in rank_list:
                self.rank_data.write(f"{each[0]} : {each[1]}\n")
