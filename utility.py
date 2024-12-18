from datetime import datetime

def get_curr_time():
    current_time = datetime.now()
    return current_time.strftime("%H:%M:%S")