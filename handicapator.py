import itertools


class Game:

    def __init__(self, data, players_per_team, threshold):
        self.data = data
        self.playersPerTeam = players_per_team
        self.threshold = threshold
        self.pairs = []

    def __get_combinations(self):
        self.comb = list(itertools.combinations(
            data['players'], players_per_team))

    def __make_pairs(self):
        for i in range(len(self.comb)):
            pair = [self.comb[i]]

            for j in range(len(self.comb)):
                if set(pair[0]).isdisjoint(self.comb[j]):
                    pair.append(self.comb[j])

            self.pairs.append(pair)

    def __get_team_handicap(self, team):
        team_handicap = 0.0
        for i in range(len(team)):
            index = self.data['players'].index(team[i])
            team_handicap += self.data['handicap'][index]
        return team_handicap

    def __append_handicap_to_list(self):
        for i in range(len(self.pairs)):
            self.pairs[i].append(self.__get_team_handicap(self.pairs[i][0]))
            self.pairs[i].append(self.__get_team_handicap(self.pairs[i][1]))

    def __remove_unbalanced_matchups(self):
        indexes_to_remove = []
        for i in range(len(self.pairs)):
            handicap_difference = abs(self.pairs[i][2] - self.pairs[i][3])
            self.pairs[i].append(handicap_difference)
            if handicap_difference > self.threshold:
                indexes_to_remove.append(i)

        for i in range(len(indexes_to_remove) - 1, -1, -1):
            self.pairs.remove(self.pairs[indexes_to_remove[i]])

    def __remove_duplicates(self):
        diffs = []
        length = len(self.pairs)
        for i in range(length - 1):
            index = i - len(diffs)
            if diffs.count(self.pairs[index][4]) > 0:
                self.pairs.pop(index)
            else:
                diffs.append(self.pairs[index][4])

    def __nice_print(self):
        self.pairs.sort(key=lambda x: x[4])
        for i in range(len(self.pairs)):
            print(self.pairs[i])
        print("There are " + str(len(self.pairs)) + " possible combinations.")

    def make_matchup(self):
        self.__get_combinations()
        self.__make_pairs()
        self.__append_handicap_to_list()
        self.__remove_unbalanced_matchups()
        self.__remove_duplicates()
        self.__nice_print()


data = {
    'players': ['JL', 'PAT', 'CL', 'ANDRE', 'PATC', 'CHR', 'GER', 'RV'],
    'handicap': [7.8, 9.1, 9.9, 9.4, 12.8, 13.6, 14.5, 10.2]
}
players_per_team = 4
threshold = 3

game = Game(data, players_per_team, threshold)
game.make_matchup()
