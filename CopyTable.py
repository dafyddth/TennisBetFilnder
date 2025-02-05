import sqlite3

with sqlite3.connect("TennisMarkets.db") as source_conn:
    with sqlite3.connect("C:/Users/dafyd/PycharmProjects/TennisHistoric/Tennis.db") as destination_conn:
        # Your code to move data between databases
        source_cursor = source_conn.cursor()
        dest_cursor = destination_conn.cursor()

        select_sql = "SELECT MarketID, NotificationDate, PlayerID FROM Markets;"
        source_cursor.execute(select_sql)
        rows = source_cursor.fetchall()

        for row in rows:
            r_market_id = row[0]
            r_notification_date = row[1]
            r_player_id = row[2]

            insert_sql = ("INSERT INTO BetRecord (MarketID, NotificationDate, PlayerID) "
                          "VALUES (?, ?, ?)")

            dest_cursor.execute(insert_sql, (r_market_id, r_notification_date, r_player_id))

        destination_conn.commit()
