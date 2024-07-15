from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

import time


driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)

#by changing the number you can choose if you want to rent or buy
rent_or_buy = 1
type_of_property = 1



driver.get("https://www.nehnutelnosti.sk/")


#changing to the cookies iframe
iframe = wait.until(EC.presence_of_element_located((By.ID, "sp_message_iframe_1109525")))

driver.switch_to.frame(iframe)

#rejecting most of the cookies
wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Pokračovať s nevyhnutnými cookies →']"))).click()


driver.switch_to.default_content()


#opening the dropdown menu
driver.find_element(By.XPATH, "//input[@placeholder='Celá ponuka']").click()


#selects if you want to buy or rent
driver.find_element(By.XPATH, f"(//div[contains(@class, 'css-1ch07sa')])[{rent_or_buy}]").click()


#searches for the desired location
driver.find_element(By.XPATH, "//input[@placeholder='Kde hľadáte?']").send_keys("Bratislava")


#selecting the first instance of the location
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.css-apb471"))).click()


#selects which type of property you want to search for
driver.find_element(By.XPATH, f"(//div[contains(@class, 'css-f7ujmq')])[{type_of_property}]").click()

#clicks the search button
wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.css-1nte1ih"))).click()


#waits for the page to load
wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.advertisement-item--content__price")))

prices = driver.find_elements(By.CSS_SELECTOR, "div.advertisement-item--content__price")

num_pages = driver.find_element(By.XPATH, "(//li[contains(@class, 'component-pagination__item')])[5]")


#getting the url so i can switch to next page
url = driver.current_url


for i in range(2, int(num_pages.text)):
    driver.get((url+f"?p[page]={i}"))
    time.sleep(2)

time.sleep(500)