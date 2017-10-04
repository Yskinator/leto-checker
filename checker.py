import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import psycopg2
import urlparse
import smtplib
 
def sendemail(from_addr, to_addr,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s' % from_addr +"\n"
    header += 'To: %s' % to_addr +"\n"
    header += 'Subject: %s' % subject +"\n"
    message = header + message
 
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr, message)
    server.quit()


def send_alert():
    problems = sendemail(from_addr = os.environ["GMAIL_USERNAME"], 
                        to_addr    = os.environ["EMAIL_RECEIVER"],
                        subject    = 'Website down', 
                        message    = 'Fix it!', 
                        login      = os.environ["GMAIL_USERNAME"], 
                        password   = os.environ["GMAIL_PASSWORD"])

def check_status():
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
    driver.get("https://staging.artemisumbrella.com")
    print("Looking for 'Artemi' to see if the page loaded correctly")
    if ("Artemi" in driver.page_source):
        print("Page loaded correctly.")
    else:
        print("Page did not load correctly.")
    print("Closing browser")
    driver.quit()

def check_prev_status():
    print("Attempting to connect to database")
    urlparse.uses_netloc.append("postgres")
    url = urlparse.urlparse(os.environ["DATABASE_URL"])
    conn = psycopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        host=url.hostname,
       port=url.port
    )
    print("Opened database successfully")
    cur = conn.cursor()
    print("Checking previous status")
    cur.execute("SELECT worked FROM previous_status WHERE id=1")
    status = str(cur.fetchone())
    print("Previous status: " + status) 
    if status == "t":
        print("Uh oh, it stopped working. Updating status")
        cur.execute("UPDATE previous_status SET worked=FALSE WHERE id = 1;")
        print("Committing changes")
        conn.commit()
        print("Sending alert email.")
        send_alert()
    print("Closing connection")
    cur.close()
    conn.close()

check_status()

