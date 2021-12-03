from covid_news_handling import news_API_request
from covid_news_handling import update_news
from covid_news_handling import schedule_news_updates
from covid_news_handling import process_news_json_data
from covid_news_handling import remove_update
from covid_news_handling import remove_news

def test_news_API_request():
    assert news_API_request()
    assert news_API_request('Covid COVID-19 coronavirus') == news_API_request()

def test_update_news():
    update_news('test')

def test_schedule_news_updates():
    schedule_news_updates(update_interval=10, update_name='update test')

def test_process_news_json_data():
    assert isinstance(process_news_json_data(), list)
    assert isinstance((process_news_json_data())[0], dict)

def test_remove_update():
    remove_update('test')
    
def test_remove_news():
    remove_update('news')
