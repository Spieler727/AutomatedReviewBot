from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from parsel import Selector
import time

options = webdriver.ChromeOptions()

# To make browser stay open
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

url = 'https://www.google.com/maps/place/Hudson+Buffet/@41.5286056,-73.8972371,17z/data=!4m8!3m7!1s0x89dd36fc398c602f:0x929fb2bcf9639a91!8m2!3d41.5286056!4d-73.8946622!9m1!1b1!16s%2Fg%2F1tdxlwgg?entry=ttu'

driver.get(url)
   
# Function to click "More..." to expand on a review
def expand_review():
    more_buttons = driver.find_elements(By.CSS_SELECTOR, ".w8nwRe.kyuRq")
    
    for button in more_buttons:
    # In the cases of the class corresponding to the wrong element, an exception is needed
        try:
            # more_button = driver.find_element(By.CSS_SELECTOR, ".w8nwRe.kyuRq")
            button.click()
            time.sleep(1)
            
        except:
            pass

expand_review()
WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, '//div[@data-review-id]')))
page_content = driver.page_source

response = Selector(text=page_content)

results = []

for element in response.xpath('//div[@data-review-id]'):
    # expand_review()
    
    # Extract data from each review
    name = element.css('div.d4r55::text').get(default='').strip()
    rating = element.css('span.kvMYJc::attr(aria-label)').get(default='').replace(' stars', '').strip()
    body = element.css('span.wiI7pd::text').get(default='').strip()

    name_exists = False
    for review in results:
        if review['name'] == name:
            name_exists = True
            break
        
    # "if not" checks if the variable is False. If it is false, execute 
    if not name_exists:
        results.append({'name': name, 'rating': rating, 'body': body})

driver.close()

for review in results:
    print(
        "{",
        "\n\t" + "Name:", review['name'],
        "\n\t" + "Rating:", review['rating'],
        "\n\t" + "Body:"
    )

    for line in review['body'].split('\n'):
        print("\t\t", line.strip())

    print("},")

