import sched, time

data_updates = []
hidden_article_titles = []
global national_7day_infections, hospital_cases, deaths_total, local_7day_infections
s = sched.scheduler(time.time, time.sleep)