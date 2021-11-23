import json, requests

def news_API_request(covid_terms : str = "Covid COVID-19 coronavirus"):
    fixed_terms = covid_terms.replace(" ", " OR ")
    base_url_with_api_key = f"https://newsapi.org/v2/everything?q=\u0027{fixed_terms}\u0027&apiKey=38f40c38c5b44f8c8b84b89135578a9c"
    response = requests.get(base_url_with_api_key)
    print(response.json())

def update_news():
    news_API_request()
