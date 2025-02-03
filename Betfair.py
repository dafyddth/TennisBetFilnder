import betfairlightweight
import json
import functions
from betfairlightweight import filters
from functions import minutes_until
from datetime import datetime
import logging

max_lay_odds = 1.21
mins_till_start = 10

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Load credentials
with open('NewCredentials.json') as config_file:
    config = json.load(config_file)

un = config['username']
pw = config['password']
key = config['api_key']
cert = config['cert_path']

def get_betfair_data():
    viable_bets = [
        ['Market_ID', 'Event', 'OpenDate', 'PlayerName', 'LayOdds', 'RunnerID']
    ]
    # Create a trading instance
    trading = betfairlightweight.APIClient(un, pw, key, certs=cert, locale='en_GB')
    tennis_filter = betfairlightweight.filters.market_filter(event_type_ids=['2'])

    try:
        # Login
        trading.login()

        events = trading.betting.list_events(tennis_filter)
        for e in events:
            market_filter = filters.market_filter(event_ids=[e.event.id], market_type_codes=['MATCH_ODDS'])

            # List market catalogues
            market_catalogues = trading.betting.list_market_catalogue(
                filter=market_filter,
                max_results='1',  # Limit to 1 result for simplicity
                market_projection=['RUNNER_METADATA']
            )

            for market in market_catalogues:
                # List market books to get the latest odds
                market_books = trading.betting.list_market_book(
                    market_ids=[market.market_id],
                    price_projection=filters.price_projection(price_data=['EX_BEST_OFFERS'])
                )
                for market_book in market_books:
                    check_and_append_bet(e, market, market_book, viable_bets)

    except Exception as e:
        logging.error(f"An error occurred: {e}")
    finally:
        trading.logout()

    #for bet in viable_bets:
        #print(bet)
    return viable_bets
def check_and_append_bet(event, market, market_book, viableBets):
    for runner_index in range(len(market_book.runners)):
        if len(market_book.runners[runner_index].ex.available_to_lay) > 0 and market_book.runners[runner_index].ex.available_to_lay[0].price < max_lay_odds and mins_till_start > minutes_until(
                event.event.open_date) > 0:
            logging.info(f""" {market_book.market_id} {event.event.name}  {market.runners[runner_index].runner_name} {market_book.runners[runner_index].ex.available_to_lay[0].price}
            {market.total_matched} {event.event.open_date} {market_book.inplay} minutesuntil: {minutes_until(event.event.open_date)} """)

            current_market_book = [
                market_book.market_id,
                event.event.name,
                event.event.open_date.strftime('%Y-%m-%d %H:%M:%S'),
                market.runners[runner_index].runner_name,
                market_book.runners[runner_index].ex.available_to_lay[0].price,
                market_book.runners[runner_index].selection_id

            ]
            viableBets.append(current_market_book)



