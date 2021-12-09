# covid19-dashboard

This is a dashboard for COVID-19 statistics. It displays national statistics (for England) and local statistics for an area of the user's choice. In addition, news articles related to COVID-19 are displayed. The user can schedule updates to the data and articles at a time of their choosing.

## Prerequisites
- Python 3.9.9 64-bit
- [Public Health England's uk-covid-19 module](https://publichealthengland.github.io/coronavirus-dashboard-api-python-sdk/)
- [News API (you will need an API key, which you can get for free by signing up)](https://newsapi.org/)
- [Flask](https://flask.palletsprojects.com/)

## Installation
```python setup.py install```

## Getting started
Run covid_data_handler - the dashboard will be hosted on http://127.0.0.1:5000/index

You can schedule updates by entering an update name and time in the prompt.
Updates can be repeated every 24 hours, and updates to COVID data and news articles can be scheduled.

Updates can be removed and thus cancelled by clicking the cross on the top-right.
You can do the same to remove news articles, but the same article cannot reappear once removed.

In config.json, you can customise certain aspects of the program
- news_api_key: the API key used for the News API
- max_news_articles: the maximum number of news articles that may appear at once
- update_id_upper_bound: each update has an ID associated, this is the number of possible IDs
- news_search_terms: the keywords used with the News API
- local_location: the location you would like local covid data for
- local_location_type: the type of local location data
- national_data_csv_path: the path to the csv file used for national COVID data
- image_path: the path to the image file used on the dashboard

## Testing
The best way to test is by using [pytest](https://pytest.org/). There are test functions included; you can use them with `pytest`.

## Details
### Authors
- cajo22: the software backend
- Matt Collison: the index.html used as a frontend

### License
This software is covered by the MIT License. For more information, see LICENSE.md

### GitHub link
This software is hosted on [GitHub](https://github.com/cajo22/covid19-dashboard)
