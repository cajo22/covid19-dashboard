from globals import s, data_updates, hidden_article_titles, config_data
import json, requests, sched, time
from flask import templating

def news_API_request(covid_terms : str = config_data["news_search_terms"]) -> dict:
    fixed_terms = covid_terms.replace(" ", " OR ")

    api_key = config_data["news_api_key"]

    base_url_with_api_key = f"https://newsapi.org/v2/everything?q=\u0027{fixed_terms}\u0027&apiKey={api_key}&sortBy=publishedAt&language=en"
    response = requests.get(base_url_with_api_key)
    return(response.json())

def process_news_json_data(json_data : dict = news_API_request()) -> dict:
    return_dicts = []
    temp_article = {}
    news_index = 0
    current_news_count = 0

    # A list of max_news_articles articles will always be displayed (unless the API call can't find that many.)
    # When removing articles, add them to the list of 'hidden titles'.
    # Continue adding titles until a list of max_news_articles articles is formed, skipping over those with a 'hidden title'.

    while current_news_count < config_data["max_news_articles"]:
        temp_article = ((json_data["articles"])[news_index])
        if temp_article["title"] not in hidden_article_titles:
            return_dicts.append( { "title": temp_article["title"]
         #+ " (" + (temp_article["source"])["name"] + ")"
         , "content": (temp_article["content"])[:192] + "... (" + temp_article["url"] + ")" } )
            current_news_count += 1
        news_index += 1

    return return_dicts

def remove_news(news_title : str, news : dict):
    # When removing news, binary search based on title.
    # Delete it from news and add it to list of hidden titles

    # TO-DO: FIX BUG WHERE LAST ARTICLE NOT REMOVED

    for i in range(len(news) - 1):
        print((news[i])["title"])
        if ((news[i])["title"]) == news_title:
            hidden_article_titles.append(news_title)
            del news[i]

def remove_update(update_name : str):
    # When removing an update, binary search based on title.
    # Cancel its events (if they exist) and delete it from data_updates.

    for i in range(len(data_updates)):
        if (data_updates[i])["title"] == update_name:
            if (data_updates[i])["covid_update_event"] in s.queue:
                s.cancel((data_updates[i])["covid_update_event"])
            if (data_updates[i])["news_update_event"] in s.queue:
                s.cancel((data_updates[i])["news_update_event"])
            del data_updates[i]

def update_news(update_name : str):
    news = process_news_json_data()

    # Remove update from data_updates
    remove_update(update_name)

def schedule_news_updates(update_interval : int, update_name : str):
    # Schedule a news update with the specified delay.
    # The name is passed so the update can be deleted from the dashboard after it occurs.
    return s.enter(update_interval, 1, update_news, (update_name,))
