from datetime import datetime


def minutes_until(target_time):
    # Convert the target time string to a datetime object


    # Get the current time
    current_time = datetime.now()

    # Calculate the difference between the target time and the current time
    time_difference = target_time - current_time

    # Convert the time difference to minutes
    minutes_to_go = time_difference.total_seconds() / 60

    return minutes_to_go