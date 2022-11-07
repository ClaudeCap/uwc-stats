from flask import Flask, render_template, redirect, session, url_for
app = Flask(__name__)

import sqlite3

app.config['SECRET_KEY'] = '354e1ab4c6d9c6bc661c258a618947bf'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

from uwc_back import UserFilterDavis, construct_filter_query
from uwc_back import list_school, list_uwc, list_countries
from uwc_back import summary

from img_scrap import all_uwc_img_src, all_country_img_src

import math

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def home():

    filter_query = "SELECT name, country, uwc, school, year FROM scholars"
    if 'filter_query' in session:
        filter_query = session['filter_query']
        session.pop('filter_query', None)

    # The form submit
    form = UserFilterDavis()
    if form.validate_on_submit():

        # When submit, make new query and render new templalte
        filter_query = construct_filter_query(form)        
        session['filter_query'] = filter_query
        return redirect(url_for('home'))    

    conn = sqlite3.connect('scholars.db')
    c = conn.cursor()
    scholars = c.execute(filter_query)
    conn.commit()

    return render_template('home.html', scholars=scholars, form=form)




@app.route("/uwc")
def uwc():
    # Empty Card
    empty_card = ["Unknown", "0", "?", "0", "?", "0"]

    # Data to display on phone
    phone_summary_all_uwc = summary("uwc", "school", "country", list_uwc, list_school, list_countries)

    # Data to display on desktop
    num_grid_row = math.ceil(len(phone_summary_all_uwc) / 3)
    desktop_summary_all_uwc = []
    row = 0
    ii = 0
    while row < num_grid_row:

        if len(phone_summary_all_uwc) <= (ii+1):
            row_data = [phone_summary_all_uwc[ii], empty_card, empty_card]
            desktop_summary_all_uwc.append(row_data)
            break
        elif len(phone_summary_all_uwc) <= (ii+2):
            row_data = [phone_summary_all_uwc[ii], phone_summary_all_uwc[ii+1], empty_card]
            desktop_summary_all_uwc.append(row_data)
            break

        row_data = [phone_summary_all_uwc[ii], phone_summary_all_uwc[ii+1], phone_summary_all_uwc[ii+2]]
        desktop_summary_all_uwc.append(row_data)
        row += 1
        ii = 3*row
    
    # Data to display on tablet
    num_grid_row = math.ceil(len(phone_summary_all_uwc) / 2)
    tablet_summary_all_uwc = []
    row = 0
    ii = 0
    while row < num_grid_row:

        if len(phone_summary_all_uwc) <= (ii+1):
            row_data = [phone_summary_all_uwc[ii], empty_card]
            tablet_summary_all_uwc.append(row_data)
            all_uwc_img_src.append("https://montevista.greatheartsamerica.org/wp-content/uploads/sites/2/2016/11/default-placeholder.png")
            break

        row_data = [phone_summary_all_uwc[ii], phone_summary_all_uwc[ii+1]]
        tablet_summary_all_uwc.append(row_data)
        row += 1
        ii = 2*row
    
    # Adding in empty UWC to the list for empty card
    list_uwc.append("Unknown")
    all_uwc_img_src.append("https://montevista.greatheartsamerica.org/wp-content/uploads/sites/2/2016/11/default-placeholder.png")

    return render_template('uwc.html', desktop_summary_all_uwc = desktop_summary_all_uwc, tablet_summary_all_uwc = tablet_summary_all_uwc, phone_summary_all_uwc = phone_summary_all_uwc, all_uwc_img_src = all_uwc_img_src, list_uwc = list_uwc)




@app.route("/country")
def country():
    # Empty
    empty_card = ["Unknown", "0", "?", "0"]

    # Data to display on phone
    phone_summary_all_country = summary("country", "school", "uwc", list_countries, list_school, list_uwc)

    # Data to display on desktop
    num_grid_row = math.ceil(len(phone_summary_all_country) / 3)
    desktop_summary_all_country = []
    row = 0;
    ii = 0;
    while row < num_grid_row:

        if len(phone_summary_all_country) <= (ii+1):
            row_data = [phone_summary_all_country[ii], empty_card, empty_card]
            desktop_summary_all_country.append(row_data)
            break
        elif len(phone_summary_all_country) <= (ii+2):
            row_data = [phone_summary_all_country[ii], phone_summary_all_country[ii+1], empty_card]
            desktop_summary_all_country.append(row_data)
            break
        
        row_data = [phone_summary_all_country[ii], phone_summary_all_country[ii+1], phone_summary_all_country[ii+2]]
        desktop_summary_all_country.append(row_data)
        row += 1
        ii = 3*row
    
    # Data to display on tablet
    num_grid_row = math.ceil(len(phone_summary_all_country) / 2)
    tablet_summary_all_country = []
    row = 0
    ii = 0
    while row < num_grid_row:

        if len(phone_summary_all_country) <= (ii+1):
            row_data = [phone_summary_all_country[ii], empty_card]
            tablet_summary_all_country.append(row_data)
            break
    
        row_data = [phone_summary_all_country[ii], phone_summary_all_country[ii+1]]
        tablet_summary_all_country.append(row_data)
        row += 1
        ii = 2*row

    # Adding in empty UWC to the list for empty card
    list_countries.append("Unknown")
    all_country_img_src.append("https://montevista.greatheartsamerica.org/wp-content/uploads/sites/2/2016/11/default-placeholder.png")


    return render_template("country.html", desktop_summary_all_country = desktop_summary_all_country, tablet_summary_all_country = tablet_summary_all_country, phone_summary_all_country = phone_summary_all_country, all_country_img_src = all_country_img_src, list_countries = list_countries)




@app.route("/about")
def about():
    test = "testing GitHub
    return render_template('about.html')




if __name__ == '__main__':
    app.run(debug=True)
