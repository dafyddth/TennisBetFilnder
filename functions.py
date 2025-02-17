import json
from datetime import datetime
import sqlite3
from notifiers import get_notifier


def minutes_until(target_time):
    # Convert the target time string to a datetime object

    # Get the current time
    current_time = datetime.now()

    # Calculate the difference between the target time and the current time
    time_difference = target_time - current_time

    # Convert the time difference to minutes
    minutes_to_go = time_difference.total_seconds() / 60

    return minutes_to_go


def check_if_new_bet(market_id):
    sql = "SELECT COUNT(*) FROM BetRecord WHERE MarketID = ?;"
    conn = sqlite3.connect("C:/Users/dafyd/PycharmProjects/TennisHistoric/Tennis.db")
    cursor = conn.cursor()

    try:
        cursor.execute(sql, (market_id,))
        result = cursor.fetchone()[0]

        if result == 0:
            return True
        else:
            return False
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        conn.close()


def record_bet(market_id,player_id, lay_odds, back_odds, lay_stake, back_stake, total_matched, total_available, size):
    sql = ("INSERT INTO BetRecord (MarketID, NotificationDate, PlayerID, LayOdds, BackOdds, LayStake,BackStake, TotalMatched, TotalAvailable, Size)"
           " VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?);")
    conn = sqlite3.connect("C:/Users/dafyd/PycharmProjects/TennisHistoric/Tennis.db")
    cursor = conn.cursor()

    try:
        cursor.execute(sql, (market_id, datetime.now(),player_id, lay_odds, back_odds, lay_stake, back_stake, total_matched, total_available, size))
        conn.commit()  # Commit the transaction
        return True
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        return False
    finally:
        conn.close()


def send_bet_notification(my_message):
    # Load credentials
    with open('NewCredentials.json') as config_file:
        tg_config = json.load(config_file)
        bot_name = tg_config['telegram_bot_name']
        bot_username = tg_config['telegram_bot_username']
        t_token = tg_config['telegram_token']
        t_chat_id = tg_config['telegram_chat_id']

    telegram = get_notifier('telegram')
    telegram.notify(token=t_token, chat_id=t_chat_id, message=my_message)


def ideal_back_stake(lay_odds, back_odds, lay_stake):
    if back_odds is not None:
        return float(lay_stake) * float(lay_odds) / float(back_odds)
    else:
        return None  # Optional: Handle the case where back_odds is None
