from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from parsel import Selector

options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options)

url = 'https://www.google.com/maps/place/Hudson+Buffet/@41.5286056,-73.8972371,17z/data=!4m8!3m7!1s0x89dd36fc398c602f:0x929fb2bcf9639a91!8m2!3d41.5286056!4d-73.8946622!9m1!1b1!16s%2Fg%2F1tdxlwgg?entry=ttu'

driver.get(url)

page_content = driver.page_source

response = Selector(text=page_content)

results = []

for element in response.xpath('//div[@data-review-id]'):
    # Extract data from each review
    name = element.css('div.d4r55::text').get(default='').strip()
    rating = element.css('span.kvMYJc::attr(aria-label)').get(default='').replace(' stars', '').strip()
    body = element.css('span.wiI7pd::text').get(default='').strip()

    name_exists = False
    for review in results:
        if review['name'] == name:
            name_exists = True
            break
        
    # if not checks if the variable is False. If it is false, execute 
    if not name_exists:
        results.append({'name': name, 'rating': rating, 'body': body})

driver.close()

for review in results:
    print(
        "{",
        "\n\t" + "name:", review['name'],
        "\n\t" + "rating:", review['rating'],
        "\n\t" + "body:", review['body'],
        "\n},"
    )

