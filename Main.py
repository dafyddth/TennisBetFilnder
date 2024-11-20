import csv

data = {}
with open(r"C:\Users\dafyd\PycharmProjects\TennisBetfinder\OddsLookup.csv", mode='r') as file:
    reader = csv.reader(file)
    next(reader)  # Skip the header row
    for row in reader:
        lay_odds = row[0]
        back_odds = row[1]
        offset = row[2]
        data[lay_odds] = (back_odds, offset)

# Corrected print statement
print(data.get('1.16', ("","")))
