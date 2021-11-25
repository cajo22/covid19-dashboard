import json, requests
from flask import templating

def news_API_request(covid_terms : str = "Covid COVID-19 coronavirus") -> dict:
    fixed_terms = covid_terms.replace(" ", " OR ")
    base_url_with_api_key = f"https://newsapi.org/v2/everything?q=\u0027{fixed_terms}\u0027&apiKey=38f40c38c5b44f8c8b84b89135578a9c"
    response = requests.get(base_url_with_api_key)
    return(response.json())

def process_news_json_data(json_data : dict) -> dict:
    return_dicts = []
    temp_article = {}

    for i in range(10):
        temp_article = ((json_data["articles"])[i])
        return_dicts.append( { "title": temp_article["title"]
         #+ " (" + (temp_article["source"])["name"] + ")"
         , "content": (temp_article["content"])[:192] + "... (" + temp_article["url"] + ")" } )

    return return_dicts

def update_news():
    news_API_request()

process_news_json_data(news_API_request())
