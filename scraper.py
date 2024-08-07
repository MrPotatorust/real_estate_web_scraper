from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC

import pandas as pd
import numpy as np


import datetime
import os





def convert_to_num(num):
    return num.replace(",", ".").replace(" ", "")


def get_data(buy_or_rent, type_of_property, location):

    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)


    data = {"price": [], "price_per_sq_m": [], "sq_meter": [], "location": [], "type_of_property": []}
    no_price_per_meter = False


    driver.get("https://www.nehnutelnosti.sk/")

    #CHANGING TO IFRAME

    #changing to the cookies iframe
    iframe = wait.until(EC.presence_of_element_located((By.ID, "sp_message_iframe_1109525")))

    driver.switch_to.frame(iframe)

    #rejecting most of the cookies
    wait.until(EC.element_to_be_clickable((By.XPATH, "//button[@title='Pokračovať s nevyhnutnými cookies →']"))).click()


    #CHANGING BACK TO MAIN PAGE

    driver.switch_to.default_content()

    #opening the dropdown menu
    driver.find_element(By.XPATH, "//input[@placeholder='Celá ponuka']").click()

    #selects if you want to buy or rent
    driver.find_element(By.XPATH, f"(//div[contains(@class, 'css-13womkq')])[{buy_or_rent}]").click()

    #searches for the desired location
    driver.find_element(By.XPATH, "//input[@placeholder='Kde hľadáte?']").send_keys(location)

    #selecting the first instance of the location
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "div.css-1krtfkx"))).click()

    #selects which type of property you want to search for
    wait.until(EC.element_to_be_clickable((By.XPATH, '//button[.//p[text()="Hľadať"]]'))).click()

    #clicks the search button
    wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "button.css-1nte1ih"))).click()



    #NEW PAGE

    #waits for the page to load
    wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.advertisement-item--content__price")))


    #gets the number of pages
    try:
        num_pages = range(2, int(driver.find_element(By.XPATH, "(//li[contains(@class, 'component-pagination__item')])[5]").text))
    except:
        num_pages = range(1)


    #getting the url so i can switch to next page
    url = driver.current_url


    for page in num_pages:
        #getting the data
        prices = driver.find_elements(By.CSS_SELECTOR, "div.advertisement-item--content__price")
        main_info = driver.find_elements(By.CSS_SELECTOR, "div.advertisement-item--content__info")



        #gets and appends the price
        for price in prices:
            text = price.text
            index = text.find("\n")


            #checks if the property has a set price per meter squared
            if text[index:-9] == "" or text[index:-2] == "":
                no_price_per_meter = True

            #checks if the property has a set price
            if index == -1 or no_price_per_meter == True:
                data["price"].append(np.nan)
                data["price_per_sq_m"].append(np.nan)
                no_price_per_meter = False

            else:
                data["price"].append(float(convert_to_num(text[:index-2])))



                #checks if its a house or a apartment
                if buy_or_rent == 1:
                    data["price_per_sq_m"].append(float(convert_to_num(text[index+2:-4])))

                else:
                    data["price_per_sq_m"].append(float(convert_to_num(text[index:-5])))

        #scrapes and append rest of the data
        count = 0
        for info in main_info:

            count += 1

            if count == 1:
                adress = info.text
                data["location"].append(adress)


            if count == 2:
                sq_meter_index = info.text.find("•")
                property_type = info.text[:sq_meter_index-1]
                count = 0

                if sq_meter_index == -1:
                    sq_meters = np.nan

                else:
                    sq_meters = float(convert_to_num(info.text[sq_meter_index+2:-3]))
                    

                data["sq_meter"].append(sq_meters)
                data["type_of_property"].append(property_type)


        #goes to next page
        driver.get(url+f"?p[page]={page}")
        wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "div.advertisement-item--content__price")))
        


    driver.quit()



    # creates a csv if it doesnt exist and puts it in the data folder
    cur_date = datetime.datetime.now()
    file_name = url[29:-1].replace('/', '-')
    directory = 'data/'+file_name+"/"


    os.makedirs(directory, exist_ok=True)




    #creates the dataframe and puts it in the csv
    df = pd.DataFrame(data)
    df.to_csv((directory+file_name+"_"+str(cur_date.date())+".csv"), index=False)