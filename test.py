from uwc_back import list_countries
from uwc_back import list_uwc
from uwc_back import list_school

import sqlite3





from datetime import date
CUR_YEAR = date.today().year

import pandas as pd
import plotly.express as px


def find_start_year(key, value):
    filter_query = "SELECT year FROM scholars WHERE"
    filter_query = filter_query + " " + key + " = " + "\"" + value + "\""
    conn = sqlite3.connect('scholars.db')
    c = conn.cursor()
    
    START_YEAR = int(c.execute(filter_query).fetchall()[0][0])

    return START_YEAR





def construct_bart05_chart(key, value, t05_key, t05_list):

    conn = sqlite3.connect('scholars.db')
    c = conn.cursor()

    # Total number of scholar
    total_scholar = "SELECT COUNT(*) FROM scholars WHERE"
    total_scholar = total_scholar + " " + key + " = " + "\"" + value + "\""
    total_scholar = c.execute(total_scholar).fetchall()[0][0]


    data_t05 = [0, 0, 0, 0]
    columns_t05 = [None, None, None, None]
    for t05_value in t05_list:
        filter_query = "SELECT COUNT(*) FROM scholars WHERE"
        filter_query = filter_query + " " + key + " = " + "\"" + value + "\""
        filter_query = filter_query + " AND " + t05_key + " = " + "\"" + t05_value + "\""

        bar_data = c.execute(filter_query).fetchall()[0]

        scholars_at_t05_key = bar_data[0]

        for i in range(4):

            if scholars_at_t05_key > data_t05[i]:
                data_t05[i] = scholars_at_t05_key
                columns_t05[i] = t05_value
                break
    
    data = []
    for i in range(4):
        data.append([columns_t05[3-i], round((data_t05[3-i]/total_scholar)*100)])
    
    # Add in remainin of other for reference
    remain = 100
    for i in data:
        remain = remain - i[1]
    data.append(["Others", remain])

    columns = [t05_key, "scholar"]

    index = []
    for i in range(5):
        index.append(i)

    df = pd.DataFrame(data, index, columns)

    bar_chart_t05 = px.bar(df, x="scholar", y=t05_key, orientation="h")

    return bar_chart_t05



construct_bart05_chart("uwc", "USA", "school", list_school)