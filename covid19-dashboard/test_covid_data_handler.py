from globals import config_data
from covid_data_handler import parse_csv_data
from covid_data_handler import process_covid_csv_data
from covid_data_handler import covid_API_request
from covid_data_handler import schedule_covid_updates
from covid_data_handler import hhmm_seconds_conversion
from covid_data_handler import process_covid_json_data
from covid_data_handler import update_covid_data
from covid_data_handler import dashboard_process

def test_parse_csv_data():
    data = parse_csv_data('covid19-dashboard/nation_2021-10-28.csv')
    assert len(data) == 639

def test_process_covid_csv_data():
    last7days_cases , current_hospital_cases , total_deaths = \
        process_covid_csv_data ( parse_csv_data (
            'covid19-dashboard/nation_2021-10-28.csv' ) )
    assert last7days_cases == 240_299
    assert current_hospital_cases == 7_019
    assert total_deaths == 141_544

def test_covid_API_request():
    data = covid_API_request()
    assert isinstance(data, dict)

def test_schedule_covid_updates():
    schedule_covid_updates(update_interval=10, update_name='update test')

def test_hhmm_seconds_conversion():
    assert hhmm_seconds_conversion("03:04") == 11040

def test_process_covid_json_data():
    location, local_7day_infections = process_covid_json_data(covid_API_request())
    assert location == config_data["local_location"]
    assert isinstance(local_7day_infections, int)

def test_update_covid_data():
    update_covid_data('test')
