# real_estate_web_scraper
Scrapes a webpage called "nehnutelnosti.sk" it's one of the biggest real estate listings websites in my country.

What it does/will do:
1. You will enter the city and if you are looking to buy or rent.
2. It will scrape that info and put it into csv file.
3. Visualize the data.


### How to run it:
1. Download this repo
2. Pip install the required libraries (selenium, pandas, numpy, matplotlib)
3. Head over to data_manipulation.py
4. There you can see loads of comments explaining the details of how it works.
5. After each function you can see a commented example of how to run that function
6. When you decide which one you want to use just uncomment it and add the desired arguments
7. In the next section I will explain the most important functions

### How to get new data - get_newer_data():
1. Head over to line 38
2. There you can see an example of the function
3. It works in this format: get_newer_data("byty-zilina-predaj") -
- the first dash "byty" where you can write "byty" which means apartments or you can write "domy" which means houses
- the second dash "zilina" is for the location of the search (the location is limited to slovakia)
- and the third "predaj" where you can write "predaj" which means buy or "prenajom" which means rent
Although you can leave it empty because the function only checks for "byty" and "predaj".

### How to format/extract the data - extract_data():
1. Head over to line 86
2. There you can see an example of the function
3. It works in this format extract_data("byty-okres-zilina-predaj", "")
4. The first argument is for the name of the folder "byty-okres-zilina-predaj" in which the csv files are saved
5. The second argument is for the function_type
- "" averages each of the files and returns a pandas dataframe with the averages
- "max" finds the maximum values from each of the collumns in every file and returns a pandas dataframe with the maximum values
- "min" finds the minimum values from each of the collumns in every file and returns a pandas dataframe with the smallest values

### Other functions:
1. get_total_avg()
2. get_total_max()
3. get_total_min()
They work in the same format as extract_data()but only return a row of data:
#### Example: get_total_max("byty-okres-zilina-predaj", "max") the biggest numbers from the max values -> extract_data("byty-okres-zilina-predaj", "max")
#### Example: get_total_max("byty-okres-zilina-predaj", "avg") the biggest numbers from the average values -> extract_data("byty-okres-zilina-predaj", "max")
#### Example: get_total_min("byty-okres-zilina-predaj", "avg") the smallest numbers from the average values -> values extract_data("byty-okres-zilina-predaj", "max")
