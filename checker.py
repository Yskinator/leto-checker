import time
import os
from selenium import webdriver

print("Opening browser")
if 'HEROKU' in os.environ:
    chrome_options = Options()
    chrome_options.binary_location = GOOGLE_CHROME_BIN
    driver=webdriver.Chrome(executable_path=CHROMEDRIVER_PATH, chrome_options=chrome_options)
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
