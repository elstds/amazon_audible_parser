import pandas as pd
import time

from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

options = Options()
options.headless = False
options.add_argument('window-size=1366x768')

web = 'https://www.audible.com/search'
path = '/home/elst/Documents/geckodriver'
driver = webdriver.Firefox(executable_path=path, options=options)
data = {
    'title': [],
    'author': [],
    'length': []
}

def collects_prudcts_from_page(container):
    products = WebDriverWait(container, 5).until(EC.presence_of_all_elements_located((By.XPATH, "./li")))
    for product in products:
        data['title'].append(product.find_element(By.XPATH, ".//h3[contains(@class, 'bc-heading')]").text)
        data['author'].append(product.find_element(By.XPATH, ".//li[contains(@class, 'authorLabel')]").text)
        data['length'].append(product.find_element(By.XPATH, ".//li[contains(@class, 'runtimeLabel')]").text)


def main():
    try:
        driver.get(web)

        pagination = driver.find_element(By.XPATH, "//ul[contains(@class, 'pagingElements')]")
        pages = pagination.find_elements(By.TAG_NAME, "li")
        last_page = int(pages[-2].text)
        current_page = 1

        while current_page <= last_page:
            container = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.CLASS_NAME, "adbl-impression-container ")))
            collects_prudcts_from_page(container)

            current_page += 1
            try:
                next_page = driver.find_element(By.XPATH, '//span[contains(@class, "nextButton")]')
                next_page.click()
            except:
                pass

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()
        df_books = pd.DataFrame(data)
        df_books.to_csv('books.csv', index=False)

if __name__ == '__main__':
    main()
