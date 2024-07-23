import matplotlib.pyplot as plt

import os

import pandas as pd
import numpy as np


from scraper import get_data

#by changing the number you can choose if you want to rent or buy
buy_or_rent = 0 # 1 = buy, 2 = rent
type_of_property = 0 # 1 = apartments, 2 = houses
location = ""

df = pd.DataFrame()


#IF YOU ALREADY HAVE DATA FOR THIS DAY IT WILL OWERWRITE IT
def get_newer_data(folder_name):
    info = folder_name.split("-")
    if info[0] == "byty":
        type_of_property = 1
    else:
        type_of_property = 2

    if info[-1] == "predaj":
        buy_or_rent = 1
    else:
        buy_or_rent = 2
    if len(info) == 4:
        location = info[2]
    else:
        location = info[1]

    get_data(buy_or_rent, type_of_property, location)

get_newer_data("byty-zilina-predaj")



#extracts and does a desired function on the csv file if you dont specify it it will return all of them
def extract_data(folder_name, function_type):
    averages = pd.DataFrame()

    files = os.scandir(f"data/{folder_name}")
    dates = []

    for i in files:
        csv_file = pd.read_csv(f"data/{folder_name}/"+i.name)

        if function_type == "avg":
            calc = csv_file.mean(numeric_only=True)
        elif function_type == "max":
            calc = csv_file.max(numeric_only=True)
        elif function_type == "min":
            calc = csv_file.min(numeric_only=True)
        else:
            calc_min = csv_file.min(numeric_only=True)
            calc_min.index = ["min_price","min_price_per_sq_m","min_sq_meter"]

            calc_max = csv_file.max(numeric_only=True)
            calc_max.index = ["max_price","max_price_per_sq_m","max_sq_meter"]

            calc_mean = csv_file.mean(numeric_only=True)
            calc_mean.index = ["avg_price","avg_price_per_sq_m","avg_sq_meter"]


            calc = pd.concat([calc_min, calc_max, calc_mean])
        
            
        averages = pd.concat([averages, calc.to_frame().T], ignore_index=True)


        #checks if copy is the name of the file 
        if "copy" in i.name:
            dates.append(pd.to_datetime(i.name.split("_")[1][:-9]))
        else:
            dates.append(pd.to_datetime(i.name.split("_")[1][:-4]))


    averages.index = dates

    return averages

#extract_data("byty-okres-zilina-predaj", "")



#if you want for example max of all averages use exapmple: get_total_max("byty-okres-zilina-predaj", "avg")
def get_total_avg(folder_name, function_type):
    return extract_data(folder_name, function_type).mean()

def get_total_max(folder_name, function_type):
    return extract_data(folder_name, function_type).max()

def get_total_min(folder_name, function_type):
    return extract_data(folder_name, function_type).min()


#get_total_max("byty-okres-zilina-predaj", "avg")




extract_data("byty-okres-zilina-predaj", "").plot()

plt.show()