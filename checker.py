import time
import datetime
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import StaleElementReferenceException
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

#For waiting page to load
def wait_for(condition_function, element):
    start_time = time.time()
    while time.time() < start_time + 3:
        if condition_function(element):
            return True
        else:
            time.sleep(0.1)
    raise Exception(
        'Timeout waiting for {}'.format(condition_function.__name__)
    )

def has_gone_stale(element):
    try:
        # Reference to an old element throws an exception when the page changes
        element.find_elements_by_id('literally_anything') 
        return False
    except StaleElementReferenceException:
        return True


def check_status():
    print("Incrementing test counter")
    count = increment_test_counter()
    print("Current count:" + str(count))
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
    print("Looking for 'meeting_phone_number' to see if the page loaded correctly")
    if ("meeting_phone_number" in driver.page_source):
        print("Page loaded correctly.")
    else:
        print("Page did not load correctly.")
        check_prev_status()
        print("Closing browser")
        driver.quit()
        return

    nick = "Automated test " + str("{:%Y-%m-%d %H:%M:%S}".format(datetime.datetime.now()))
    print("Typing nickname: " + nick)
    element = driver.find_element_by_id("meeting_nickname")
    element.send_keys(nick)

    print("Typing phone number")
    element = driver.find_element_by_id("meeting_phone_number")
    element.send_keys("9991231234")
    
    print("Typing duration")
    element = driver.find_element_by_id("duration-input")
    element.send_keys("1")

    print("Pressing the start button")
    element = driver.find_element_by_id("startbutton")
    element.click()

    wait_for(has_gone_stale, element)
    time.sleep(2) #Wait a little longer just in case - this seems to cause trouble occasionally

    print("Checking that the second page changed correctly by looking for the + 10 minutes button")
    if ("+10" in driver.page_source):
        print("Page loaded correctly.")
    else:
        print("Page did not load correctly.")
        check_prev_status()
        print("Closing browser")
        driver.quit()
        return

    if int(count) < int(os.environ["FULL_TEST_INTERVAL"]):
        print("Pressing the I'm OK button to avoid sending an alert")
        element = driver.find_element_by_class_name("submitbutton")
        element.click()
    else:
        print("Resetting the test counter")
        reset_test_counter()
        print("Waiting for alert to be sent")
        time.sleep(100)
        driver.execute_script("window.stop()")
	print("Clicking the I'm OK button")
        element = driver.find_element_by_class_name("submitbutton")
        element.click()

        print("Navigating to textmagic")
        driver.get("https://my.textmagic.com/online/messages/sent")

        print("Typing in username")
        element = driver.find_element_by_id("_username")
        element.send_keys(os.environ["TEXTMAGIC_USERNAME"])

        print("Typing in password")
        element = driver.find_element_by_id("_password")
        element.send_keys(os.environ["TEXTMAGIC_PASSWORD"])

        print("Clicking log in button")
        element = driver.find_element_by_id("logInBtn")
        element.click()

        wait_for(has_gone_stale, element)
        time.sleep(2) #Wait a little longer just in case - this seems to cause trouble occasionally

        print("Looking for our alert")

        if (nick.upper() in driver.page_source):
            print("Alert has been received.")
        else:
            print("Alert has not been received.")
            check_prev_status()
            print("Closing browser")
            driver.quit()
            return

    
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
    if status == "(True,)":
        print("Uh oh, it stopped working. Updating status")
        cur.execute("UPDATE previous_status SET worked=FALSE WHERE id = 1;")
        print("Committing changes")
        conn.commit()
        print("Sending alert email.")
        send_alert()
    print("Closing database connection")
    cur.close()
    conn.close()

def increment_test_counter():
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
    print("Fetching previous count")
    cur.execute("SELECT since_last_full_test FROM previous_status WHERE id=1;")
    count = int(cur.fetchone()[0])
    print("Count: " + str(count))
    print("Increasing counter by one")
    count = count + 1
    cur.execute("UPDATE previous_status SET since_last_full_test = "+str(count)+" WHERE id=1;")
    print("Committing changes")
    conn.commit()
    print("Closing database connection")
    cur.close()
    conn.close()
    return count

def reset_test_counter():
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
    print("Setting counter to 0")
    cur.execute("UPDATE previous_status SET since_last_full_test = 0 WHERE id=1;")
    print("Committing changes")
    conn.commit()
    print("Closing database connection")
    cur.close()
    conn.close()

check_status()

