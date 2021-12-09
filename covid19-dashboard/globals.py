import sched, time, json

data_updates = []
hidden_article_titles = []
global national_7day_infections, hospital_cases, deaths_total, local_7day_infections
s = sched.scheduler(time.time, time.sleep)

config_file = open("config.json", "r")
config_data = json.load(config_file)