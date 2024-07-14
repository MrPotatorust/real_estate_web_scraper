from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

import time


driver = webdriver.Chrome()
wait = WebDriverWait(driver, 10)


driver.get("https://www.nehnutelnosti.sk/")

iframe = wait.until(EC.presence_of_element_located((By.ID, "sp_message_iframe_1109525")))
driver.switch_to.frame(iframe)

print("AAAAAAAAAAAA")

button = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Pokračovať s nevyhnutnými cookies →']")))
print("SSSSSSSSSSSSSSS")

button.click()

driver.switch_to.default_content()


time.sleep(500)