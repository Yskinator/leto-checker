import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import psycopg2
import urlparse
import smtplib
 
def sendemail(from_addr, to_addr_list,
              subject, message,
              login, password,
              smtpserver='smtp.gmail.com:587'):
    header  = 'From: %s' % from_addr
    header += 'To: %s' % ','.join(to_addr_list)
    header += 'Subject: %s' % subject
    message = header + message
 
    server = smtplib.SMTP(smtpserver)
    server.starttls()
    server.login(login,password)
    problems = server.sendmail(from_addr, to_addr_list, message)
    server.quit()


problems = sendemail(from_addr    = os.environ["GMAIL_USERNAME"], 
                    to_addr_list = os.environ["EMAIL_RECEIVER"],
                    subject      = 'Mail from python', 
                    message      = 'A thing has happened. Do another thing.', 
                    login        = os.environ["GMAIL_USERNAME"], 
                    password     = os.environ["GMAIL_PASSWORD"])
print(problems)


#print("Attempting to connect to database")
#urlparse.uses_netloc.append("postgres")
#url = urlparse.urlparse(os.environ["DATABASE_URL"])
#print(url)
#conn = psycopg2.connect(
#    database=url.path[1:],
#    user=url.username,
#    password=url.password,
#    host=url.hostname,
#    port=url.port
#)
#print("Opened database successfully")
#cur = conn.cursor()
#print("Checking previous status")
#cur.execute("SELECT worked FROM previous_status WHERE id=1")
#print("Previous status: " + str(cur.fetchone())) 
#print("Closing connection")
#cur.close()
#conn.close()


#print("Opening browser")
#if 'HEROKU' in os.environ:
#    chrome_options = Options()
#    chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
#    chrome_options.add_argument('--disable-gpu')
#    chrome_options.add_argument('--no-sandbox')
#    driver=webdriver.Chrome(executable_path=os.environ.get('CHROMEDRIVER_PATH'), #chrome_options=chrome_options)
#else:
#    driver = webdriver.Chrome()
#print("Opening Artemis' Umbrella")
#driver.get("https://info.artemisumbrella.com")
#print("Looking for 'Artemi' to see if the page loaded correctly")
#if ("Artemi" in driver.page_source):
#    print("Page contains 'Artemi'")
#else:
#    print("Page doesn't contain 'Artemi'")
#print("Closing browser")
#driver.quit()
