from flask import Flask, render_template, redirect, session, url_for
app = Flask(__name__)

import sqlite3

app.config['SECRET_KEY'] = '354e1ab4c6d9c6bc661c258a618947bf'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

from uwc_back import UserFilterDavis, construct_filter_query
from uwc_back import list_school, list_uwc, list_countries

from uwc_back import summary
from uwc_back import display_summary

from img_scrap import all_uwc_img_src, all_country_img_src, all_school_img_src

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
   
    from pre_uwc_summary import uwc_output_display_summary
    output_display_summary = uwc_output_display_summary

    list_uwc.append("Empty")
    all_uwc_img_src.append("https://montevista.greatheartsamerica.org/wp-content/uploads/sites/2/2016/11/default-placeholder.png")
    
    desktop_summary_all_uwc = output_display_summary[0]
    tablet_summary_all_uwc = output_display_summary[1]
    phone_summary_all_uwc = output_display_summary[2]

    return render_template("uwc.html", desktop_summary_all_uwc = desktop_summary_all_uwc, tablet_summary_all_uwc = tablet_summary_all_uwc, phone_summary_all_uwc = phone_summary_all_uwc, all_uwc_img_src = all_uwc_img_src, list_uwc = list_uwc)


@app.route("/country")
def country():
    from pre_country_summary import country_output_display_summary
    output_display_summary = country_output_display_summary

    list_countries.append("Empty")
    all_country_img_src.append("https://montevista.greatheartsamerica.org/wp-content/uploads/sites/2/2016/11/default-placeholder.png")

    desktop_summary_all_country = output_display_summary[0]
    tablet_summary_all_country = output_display_summary[1]
    phone_summary_all_country = output_display_summary[2]

    return render_template("country.html", desktop_summary_all_country = desktop_summary_all_country, tablet_summary_all_country = tablet_summary_all_country, phone_summary_all_country = phone_summary_all_country, all_country_img_src = all_country_img_src, list_countries = list_countries)






@app.route("/undergraduate")
# On UI it is undergrad
# Backend everything is refer to as school for simplicity
@app.route("/school")
def school():
    from pre_school_summary import school_output_display_summary
    output_display_summary = school_output_display_summary

    list_school.append("Empty")
    all_school_img_src.append("https://montevista.greatheartsamerica.org/wp-content/uploads/sites/2/2016/11/default-placeholder.png")

    desktop_summary_all_school = output_display_summary[0]
    tablet_summary_all_school = output_display_summary[1]
    phone_summary_all_school = output_display_summary[2]

    return render_template("school.html", desktop_summary_all_school = desktop_summary_all_school, tablet_summary_all_school = tablet_summary_all_school, phone_summary_all_school = phone_summary_all_school, all_school_img_src = all_school_img_src, list_school = list_school)




@app.route("/about")
def about():
    return render_template('about.html')




if __name__ == '__main__':
    app.run(debug=True)
