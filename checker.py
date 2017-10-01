import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import psycopg2
import urlparse

print("Attempting to connect to database")
urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])
print(url)
conn = psycopg2.connect(
    database=url.path[1:],
    user=url.username,
    password=url.password,
    host=url.hostname,
    port=url.port
)
print("Opened database successfully")
cur = conn.cursor()
print("Executing query")
cur.execute("SELECT worked FROM previous_status WHERE id=1")
rows = cur.fetchall()
print("Result:" + rows)



print("Opening browser")
if 'HEROKU' in os.environ:
    chrome_options = Options()
    chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
    chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument('--no-sandbox')
    driver=webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), chrome_options=chrome_options)
else:
    driver = webdriver.Chrome()
print("Opening Artemis' Umbrella")
driver.get("https://info.artemisumbrella.com")
print("Looking for 'Artemi' to see if the page loaded correctly")
if ("Artemi" in driver.page_source):
    print("Page contains 'Artemi'")
else:
    print("Page doesn't contain 'Artemi'")
print("Closing browser")
driver.quit()
