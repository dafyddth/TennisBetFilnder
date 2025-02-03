from datetime import datetime
from OddsLookup import OddsHolder
import Betfair
import functions
import time




my_odds_holder = OddsHolder(r"C:\Users\dafyd\PycharmProjects\TennisBetfinder\\", r"OddsLookupTrends.csv")
max_iterations = 3000
iterations = 0
required_liability = 0.5


while iterations < max_iterations:
    #Get the list of bets
    bet_list = Betfair.get_betfair_data()

    # Iterate through each bet in the list
    for bet in bet_list:
        #print(bet[0])
        market_id = bet[0]

        # Check if the bet is new, returns TRUE if it is
        if functions.check_if_new_bet(market_id):
            print(f"Send Notification {market_id}")
            event_name = bet[1]
            match_start_time = bet[2]
            player = bet[3]
            lay_odds = bet[4]
            lay_stake = round(required_liability / (lay_odds - 1), 2)
            back_odds = my_odds_holder.get_back_odds(str(bet[4]))
            back_stake = round(functions.ideal_back_stake(lay_odds, back_odds, lay_stake), 2)


            # Format the values as currency
            formatted_lay_stake = f"£{lay_stake:.2f}"
            formatted_back_stake = f"£{back_stake:.2f}"
            formatted_liability = f"£{required_liability:.2f}"

            text_message = (f"Tennis Bet: \n"
                            f"Match: {event_name}\n"
                            f"Start time: {match_start_time}\n"
                            f"Player: {player.upper()}\n"
                            f"Lay odds: {lay_odds}\n"
                            f"Liability: {formatted_liability}\n"
                            f"Lay stake: {formatted_lay_stake}\n"
                            f"Back odds: {back_odds}\n"
                            f"Back stake: {formatted_back_stake}")

            # print(text_message)
            functions.send_bet_notification(text_message)

            functions.record_bet(bet[0],bet[5])

        else:
            x=1+1
             #print(f"Don't send Notification {bet[0]}")
    time.sleep(300)
    iterations +=1
    print(iterations, "  ", datetime.now())
# Print the second bet in the list

