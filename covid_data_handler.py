from constants import *
from uk_covid19 import Cov19API
import sched, time
from flask import Flask, render_template

app = Flask(__name__)

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
        "date": "date",
        "areaName": "areaName",
        "newCasesByPublishDate": "newCasesByPublishDate",
    }

    api = Cov19API(filters=location_info, structure=target_info)
    json_data = api.get_json()
    
    return json_data

def schedule_covid_updates(update_interval : int, update_name : str):
    s = sched.scheduler(time.time, time.sleep)
    s.enter(update_interval, 1, update_name)
    s.run(blocking=False)

def process_covid_json_data(json_data : dict) -> str:
    # Intended to be used with the json data retrieved with the Cov19API
    # Extract the location of data and infections in the last 7 days and return them

    local_7day_infections = 0
    for i in range(1, 8):
        local_7day_infections += ((json_data["data"])[i])["newCasesByPublishDate"]
    location = ((json_data["data"])[1])["areaName"]
    return(location, local_7day_infections)

@app.route('/index')
def dashboard_process():
    national_7day_infections, hospital_cases, deaths_total = process_covid_csv_data(parse_csv_data("resource/nation_2021-10-28.csv"))
    location, local_7day_infections = process_covid_json_data(covid_API_request())
    return(render_template("index.html", national_7day_infections = national_7day_infections,
    hospital_cases = f"Total hospital cases: {hospital_cases}",
    deaths_total = f"Total deaths: {deaths_total}", location = location,
    local_7day_infections = local_7day_infections, title = "Daily updates"))

if __name__ == "__main__":
    app.run()
