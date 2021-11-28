import json, requests
from flask import templating

def news_API_request(covid_terms : str = "Covid COVID-19 coronavirus") -> dict:
    fixed_terms = covid_terms.replace(" ", " OR ")
    base_url_with_api_key = f"https://newsapi.org/v2/everything?q=\u0027{fixed_terms}\u0027&apiKey=38f40c38c5b44f8c8b84b89135578a9c"
    response = requests.get(base_url_with_api_key)
    return(response.json())

def process_news_json_data(json_data : dict, hidden_article_titles : str) -> dict:
    return_dicts = []
    temp_article = {}
    news_index = 0
    current_news_count = 0

    # A list of 10 articles will always be displayed (unless the API call can't find that many.)
    # When removing articles, add them to the list of 'hidden titles'.
    # Continue adding titles until a list of 10 articles is formed, skipping over those with a 'hidden title'.

    while current_news_count < 10:
        temp_article = ((json_data["articles"])[news_index])
        if temp_article["title"] not in hidden_article_titles:
            return_dicts.append( { "title": temp_article["title"]
         #+ " (" + (temp_article["source"])["name"] + ")"
         , "content": (temp_article["content"])[:192] + "... (" + temp_article["url"] + ")" } )
            current_news_count += 1
        news_index += 1

    return return_dicts

def update_news(news : dict, hidden_article_titles : str):
    news = process_news_json_data(news_API_request(), hidden_article_titles)
