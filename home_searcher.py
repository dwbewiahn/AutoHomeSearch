import requests
import json
import winsound
import schedule
import time
from pushover_notifier import PushoverNotifier
from datetime import datetime, timedelta

# define the search filters
search_filters = {
    "category_id": "4777",
    "city_id": "15738887",
    "filter_enum_tipologia[0]": "t1",
    "filter_enum_tipologia[1]": "t0",
    "filter_enum_tipologia[2]": "t2",
    "filter_enum_tipologia[3]": "t2",
    "filter_float_price:from": "200",
    "filter_float_price:to": "800",
    "filter_refiners": "spell_checker",
    "limit": "40",
    "offset": "0",
    "region_id": "15",
    "sl": "1864fc050fex69f04b73",
    "strategy": "extended_distance"
}

# define the search frequency (every 5 minutes)
search_frequency = 3  # minutes
# initialize the winsound library
winsound.PlaySound(None, winsound.SND_PURGE)
# initialize the schedule library
schedule.clear()
# counter for the search ***it's been incremented inside job()***
search_count = 1

# initialize the class for push notifications
notifier = PushoverNotifier('C:\\Projects\\PythonProjects\\AutoHomeSearch\\config\\pushover_config.json')


def is_new_apartment(apartment):
    last_refresh_time = datetime.fromisoformat(apartment['last_refresh_time'][:-6])  # remove timezone offset
    created_time = datetime.fromisoformat(apartment['created_time'][:-6])  # remove timezone offset
    now = datetime.now()
    delta = now - last_refresh_time
    days = delta.days
    hours, remainder = divmod(delta.seconds, 3600)
    minutes, _ = divmod(remainder, 60)
    delta_created = now - created_time
    days_created = delta_created.days
    if now - last_refresh_time < timedelta(minutes=search_frequency):
        print(f"Search: {datetime.now().strftime('%H:%M:%S')} | Advertised : {last_refresh_time.strftime('%H:%M:%S - %d/%m/%Y')}  | {days:03d} days {hours:02d} hours {minutes:02d} minutes | Created on: {created_time.strftime('%d/%m/%Y')} | {(days_created):03d} days | {apartment['url']} ")
        notifier.send_notification(f"Apartment found!{last_refresh_time.strftime('%H:%M')}|{apartment['url']}")
        return True
    else:
        return False


def search_apartments():
    url = "https://www.olx.pt/api/v1/offers/"
    response = None
    while response is None:
        try:
            response = requests.get(url, params=search_filters)
        except requests.exceptions.ConnectionError:
            print("Connection error. Retrying in 10 seconds...")
            time.sleep(10)
            continue   
    data = json.loads(response.text)
    apartments = data['data']
    for apartment in apartments:
         if is_new_apartment(apartment):
            duration = 400  # milliseconds
            frequency = 2500  # Hz
            for i in range(3):
                time.sleep(0.9) 
                winsound.Beep(frequency, duration)
                time.sleep(0.1) 
                winsound.Beep(frequency, duration)
                

def job():
    global search_count
    print(f"## Search {search_count} : {datetime.now().strftime('%H:%M')} # Next search in {search_frequency} minutes ##")
    try:
        search_apartments()
    except requests.exceptions.ConnectionError:
        print("Connection error. Skipping search {search_count}")
        pass
    search_count+=1

print('################ Starting Search ################')
job()
schedule.every(search_frequency).minutes.do(job)


while True:
    schedule.run_pending()
    time.sleep(1)
