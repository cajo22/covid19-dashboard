from constants import *
from uk_covid19 import Cov19API
import sched, time, random
from flask import Flask, render_template, request

from covid_news_handling import news_API_request, process_news_json_data

app = Flask(__name__)

data_updates = []
hidden_article_titles = []
global national_7day_infections, hospital_cases, deaths_total, local_7day_infections
s = sched.scheduler(time.time, time.sleep)

def parse_csv_data(csv_filename : str) -> str:

    # Each line (row) of file {csv_filename} is appended to a list, not including line breaks.
    # This list is then returned.

    src_csv = open(csv_filename, "r")
    data = []
    for line in src_csv:
        data.append(line[:-1])
    src_csv.close()
    return(data)

def process_covid_csv_data(covid_csv_data : str) -> int:
    # Takes a list of strings (intended to be the output of parse_csv_data).
    # Returns three integers: new cases in last 7 days, current hospital cases, total deaths.

    # New cases in the last 7 days
    # The most recent day (row 1) is invalid, so sum daily cases for rows 2 - 8.
    cases_7days = 0
    for i in range(ROW_FIRST_COMPLETE_DAY, ROW_FIRST_COMPLETE_DAY + 7):
        cases_7days += int((covid_csv_data[i].split(","))[COL_NEW_CASES])

    # Current hospital cases
    current_hospital_cases = (covid_csv_data[ROW_MOST_RECENT_DAY].split(","))[COL_HOSPITAL_CASES]

    # Total deaths
    # Continue iterating until the value of 'cumDailyNsoDeathsByDeathDate' is not blank.
    total_deaths = ""
    i = ROW_MOST_RECENT_DAY
    while total_deaths == "":
        total_deaths = (covid_csv_data[i].split(","))[COL_TOTAL_DEATHS]
        i += 1

    return cases_7days, int(total_deaths), int(current_hospital_cases)

def covid_API_request(location : str = "Exeter", location_type : str = "ltla") -> dict:
    # Takes location & location type (defaulting to Exeter and ltla) and uses them as filters
    # when retrieving information about COVID-19 statistics.
    # The output is a dictionary with the retrieved information.

    location_info = [
        f"areaName={location}",
        f"areaType={location_type}"
    ]
    target_info = {
        "areaName": "areaName",
        "newCasesByPublishDate": "newCasesByPublishDate",
    }

    api = Cov19API(filters=location_info, structure=target_info)
    json_data = api.get_json()
    
    return json_data

def update_covid_data(update_name : str):
    national_7day_infections, hospital_cases, deaths_total = process_covid_csv_data(parse_csv_data("resource/nation_2021-10-28.csv"))
    location, local_7day_infections = process_covid_json_data(covid_API_request())

    # Remove update from data_updates
    print("Update complete.")
    remove_update(update_name)

def schedule_covid_updates(update_interval : int, update_name : str):
    # Schedule a covid data update with the specified delay.
    # The name is passed so the update can be deleted from the dashboard after it occurs.
    return s.enter(update_interval, 1, update_covid_data, (update_name,))

def process_covid_json_data(json_data : dict) -> str:
    # Intended to be used with the json data retrieved with the Cov19API
    # Extract the location of data and infections in the last 7 days and return them

    local_7day_infections = 0
    for i in range(1, 8):
        local_7day_infections += ((json_data["data"])[i])["newCasesByPublishDate"]
    location = ((json_data["data"])[1])["areaName"]
    return(location, local_7day_infections)

# Convert hhmmss values to seconds only
# Used for update timings

def hhmmss_seconds_conversion(time : str) -> int:
    hhmmss_array = time.split(":")
    return((int(hhmmss_array[0]) * 3600) + (int(hhmmss_array[1]) * 60) + (int(hhmmss_array[2])))

def remove_update(update_name : str):
    # When removing an update, binary search based on title and remove from data_updates when found
    # Also cancel its event.

    for i in range(len(data_updates)):
        if (data_updates[i])["title"] == update_name:
            s.cancel((data_updates[i])["covid_update_event"])
            del data_updates[i]

@app.route('/index')
def dashboard_process():
    # This function is the 'meat' of the dashboard and adds virtually all of the interactivity.

    s.run(blocking=False)

    # When removing news, add it to the list of titles that should not be displayed.

    news_to_remove = request.args.get("notif")
    if news_to_remove:
        #print(request.values.get("notif"))
        hidden_article_titles.append(news_to_remove)
    
    update_to_remove = request.args.get("update_item")
    if update_to_remove:
        remove_update(update_to_remove)

    # This section handles how updates are processed.
    # Updates are stored in data_updates.

    text_field = request.args.get("two")
    if text_field:
        update_time = request.args.get("update")
        if update_time:
            local_seconds = hhmmss_seconds_conversion(f"{(time.localtime())[3]}:{(time.localtime())[4]}:{(time.localtime())[5]}")
            update_seconds = hhmmss_seconds_conversion(f"{update_time}:00")
            if (local_seconds < update_seconds):
                delay = update_seconds - local_seconds
            else:
                delay = 86400 - (local_seconds - update_seconds)
        
        if request.args.get("repeat"):
            should_repeat = "True"
        else:
            should_repeat = "False"

        if request.args.get("covid-data"):
            should_update_covid = "True"
        else:
            should_update_covid = "False"

        if request.args.get("news"):
            should_update_news = "True"
        else:
            should_update_news = "False"
        
        # Each update has its own unique ID which is appended to the label.
        # This is because of a bug that arises when 2+ identically-labelled updates exist.
        # Updates are removed from data_updates by finding their title in a binary search, so...
        # Without an ID, when removing one of these updates, it's always the first update that is removed.

        next_id_no = 0
        while next_id_no == 0:
            next_id_no = random.randint(0,65535)
            if len(data_updates) > 0:
                for i in range(len(data_updates) - 1):
                    if (data_updates[i])["id"] == next_id_no:
                        next_id_no = 0

        # Schedule updates

        if should_update_covid:
            covid_update_event = schedule_covid_updates( delay, f"{text_field} (id: {next_id_no})" )
        else:
            covid_update_event = None

        #if should_update_news:
        #    schedule_news_updates( s, delay, f"{text_field} (id: {next_id_no})" )

        data_updates.append({"id": {next_id_no}, "title": f"{text_field} (id: {next_id_no})",
        "content": f"""Time: {update_time}, Repeat: {should_repeat}
        Update covid data: {should_update_covid}, Update news: {should_update_news}""",
        "covid_update_event": covid_update_event })

    return(render_template("index.html", national_7day_infections = national_7day_infections,
    hospital_cases = f"Total hospital cases: {hospital_cases}",
    deaths_total = f"Total deaths: {deaths_total}", location = location,
    local_7day_infections = local_7day_infections, title = "Daily updates",
    nation_location = "England", news_articles = news, updates = data_updates))

if __name__ == "__main__":

    # Initial data grab

    national_7day_infections, hospital_cases, deaths_total = process_covid_csv_data(parse_csv_data("resource/nation_2021-10-28.csv"))
    location, local_7day_infections = process_covid_json_data(covid_API_request())
    news = process_news_json_data(news_API_request(), hidden_article_titles)

    # Run dashboard

    app.run()
