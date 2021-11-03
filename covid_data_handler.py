from constants import *

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
