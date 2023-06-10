import requests
from bs4 import BeautifulSoup
import smtplib
from dotenv import load_dotenv
from send_message import send_message, service
import os
import pprint as p

load_dotenv()

EMAIL = os.getenv('EMAIL')
PASSWORD = os.getenv('PASSWORD')
recipients = [os.getenv('RECIPIENTS')]
# recipients = ["lewishalstead5@gmail.com"]

URL = os.getenv("URL")
page = requests.get(URL)

# Soup
soup = BeautifulSoup(page.content, "html.parser")

# Get job titles
job_titles = []
for x in soup.find_all('a', class_="card__title"):
    job_titles.append(str(x.contents))


x = str(job_titles)
x = x.replace('[\"[\'\\\\r\\\\n', '')
x = x.replace('[\'\\\\r\\\\n', '')
x = x.replace('"', '')
x = x.replace("'", '')
x = x.replace(']', '')

resultsJobList = soup.find_all("div", class_="webContentItem")
if resultsJobList:
    f = open("jobs.txt", 'r')
    if x == f.read():
        print("SAME")
        f.close()
    else:
        f = open("jobs.txt", "w")
        f.write(x)
        f.close()

        send_message(
            service=service,
             destination=recipients,
             obj="CC Job Alert",
             body=f"""
            A new job has been posted at {URL}
            {x}
            """)
else:
    print("Nae Joabs")

