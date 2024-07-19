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

#get_newer_data("byty-zilina-predaj")

def get_avg(folder_name):
    averages = pd.DataFrame()

    files = os.scandir(f"data/{folder_name}")
    dates = []

    for i in files:
        test = pd.read_csv(f"data/{folder_name}/"+i.name).mean(numeric_only=True)
        averages = pd.concat([averages, test.to_frame().T], ignore_index=True)


        if "copy" in i.name:
            dates.append(pd.to_datetime(i.name.split("_")[1][:-9]))
        else:
            dates.append(pd.to_datetime(i.name.split("_")[1][:-4]))

    averages.index = dates

    return averages

#get_avg("byty-okres-zilina-predaj")


def get_total_avg(folder_name):
    return get_avg(folder_name).mean()

#get_total_avg("byty-okres-zilina-predaj")




get_avg("byty-okres-zilina-predaj").plot()

plt.show()


