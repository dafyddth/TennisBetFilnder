import csv


class OddsHolder:

    def __init__(self,filepath,filename):
        self.odds_data = {}
        with open(filepath + filename, mode='r') as file:
            my_reader = csv.reader(file)
            next(my_reader) # skip header row
            for row in my_reader:
                lay = row[0]
                back = row[1]
                self.odds_data[lay] = back

    def get_back_odds(self,lay_odds):
        return self.odds_data.get(lay_odds)

