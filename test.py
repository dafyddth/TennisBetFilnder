import OddsLookup
from OddsLookup import OddsHolder

my_odds_holder = OddsHolder(r"C:\Users\dafyd\PycharmProjects\TennisBetfinder\\", r"OddsLookup.csv")
print(my_odds_holder.get_back_odds('1.17'))
