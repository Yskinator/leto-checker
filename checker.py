import time
from selenium import webdriver

print("Opening browser")
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
