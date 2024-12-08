from OddsLookup import OddsHolder
import Betfair
import functions
import time


my_odds_holder = OddsHolder(r"C:\Users\dafyd\PycharmProjects\TennisBetfinder\\", r"OddsLookup.csv")
max_iterations = 144
iterations = 0
while iterations < max_iterations:
    #Get the list of bets
    bet_list = Betfair.get_betfair_data()

    # Iterate through each bet in the list
    for bet in bet_list:
        print(bet[0])
        market_id = bet[0]

        # Check if the bet is new
        if functions.check_if_new_bet(market_id):
            print(f"Send Notification {market_id}")
            event_name = bet[1]
            match_start_time = bet[2]
            player = bet[3]
            lay_odds = bet[4]
            back_odds = my_odds_holder.get_back_odds(str(bet[4]))
            text_message = (f"Tennis Bet: \n"
                            f"Match: {event_name}\n"
                            f"Start time: {match_start_time}\n"
                            f"Player: {player.upper()}\n"
                            f"Lay odds: {lay_odds}\n"
                            f"Back odds: {back_odds}")

            print(text_message)
            functions.send_bet_notification(text_message)

            functions.record_bet(bet[0])

        else:
            print(f"Don't send Notification {bet[0]}")
    time.sleep(300)
    iterations +=1
# Print the second bet in the list

