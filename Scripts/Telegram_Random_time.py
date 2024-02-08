import datetime
import random
import time

def wait_random_minute():
    # Get current time
    current_time = datetime.datetime.now()
    print("Current Time:", current_time)

    # Calculate time after 10 minutes
    future_time = current_time + datetime.timedelta(minutes=5)

    # Generate a random wait time within the remaining time until the target time
    time_difference = future_time - current_time
    max_wait_time = time_difference.total_seconds()
    random_wait_time = random.uniform(0, max_wait_time)

    # Print the time to wait
    print("Time to Wait:", datetime.timedelta(seconds=random_wait_time))

    # Wait until the chosen minute
    time.sleep(random_wait_time)

    # Print the final time when the chosen minute arrives
    final_time = datetime.datetime.now()
    print("Final Time:", final_time)

# Call the function
wait_random_minute()
