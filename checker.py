import time
import os
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

print("Opening browser")
if 'HEROKU' in os.environ:
    chrome_options = Options()
    chrome_options.binary_location = os.environ.get('GOOGLE_CHROME_BIN')
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
