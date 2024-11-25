import betfairlightweight
import json

from betfairlightweight import filters

with open('credentials.json') as config_file:
    config = json.load(config_file)

un = config['username']
pw = config['password']
key = config['api_key']
cert = config['cert_path']


def get_betfair_data():
    # Create a trading instance
    trading = betfairlightweight.APIClient(un, pw, key, certs=cert, locale='en_GB')
    tennis_filter = betfairlightweight.filters.market_filter(event_type_ids=['2'])

    # Login
    trading.login()

    events = trading.betting.list_events(tennis_filter)
    for e in events:
        #print(e.event.name, e.event.open_date.date(), e.event.id)
        # Create a market filter for match odds market
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
            #print(e.event.name, e.event.open_date)
            #print(market.market_name, market.runners[0].runner_name)
            for market_book in market_books:
                print(e.event.name)
                #print(market.runners[0].runner_name)
                #print(market_book.runners[0].ex.available_to_lay[0].price)
                if len(market_book.runners[0].ex.available_to_lay) > 0 and market_book.runners[0].ex.available_to_lay[0].price < 1.23:
                    print(f"""{e.event.name}  {market.runners[0].runner_name} {market_book.runners[0].ex.available_to_lay[0].price}
                    {market.total_matched} {e.event.open_date} {market_book.inplay} """ )


get_betfair_data()
