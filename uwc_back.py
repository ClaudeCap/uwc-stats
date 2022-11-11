from flask import flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from fuzzywuzzy import fuzz

from iso3166 import countries

import math
import sqlite3




class UserFilterDavis(FlaskForm):
    name = StringField('Name')
    country = StringField('Country')
    uwc = StringField('UWC')
    school = StringField('Undergraduate')
    year = StringField('Year')
    submit = SubmitField('Filter Data')

def construct_filter_query(form):

    filter_query = 'SELECT name, country, uwc, school, year FROM scholars'

    if form.name.data != "" or form.country.data != "" or form.uwc.data != "" or form.school.data != "" or form.year.data != "":
        filter_query = filter_query + " WHERE"

    # Flash header
    if form.name.data != "":
        filter_query = filter_query + " name = " + "\"" + form.name.data + "\""
        flash(f'Filtering out the database for {form.name.data}', 'success')
    if form.country.data != "":
        if form.name.data != "":
            filter_query = filter_query + " AND"
        filter_query = filter_query + " country = " + "\"" + form.country.data + "\""
        flash(f'Filtering out the database for {form.country.data}', 'success')
    if form.uwc.data != "":
        if form.name.data != "" or form.country.data != "":
            filter_query = filter_query + " AND"
        filter_query = filter_query + " uwc = " + "\"" + form.uwc.data + "\""
        flash(f'Filtering out the database for {form.uwc.data}', 'success')
    if form.school.data != "":
        if form.name.data != "" or form.country.data != "" or form.uwc.data != "":
            filter_query = filter_query + " AND"
        filter_query = filter_query + " school = " + "\"" + form.school.data + "\""
        flash(f'Filtering out the database for {form.school.data}', 'success')
    if form.year.data != "":
        if form.name.data != "" or form.country.data != "" or form.uwc.data != "" or form.school.data != "":
            filter_query = filter_query + " AND"
        filter_query = filter_query + " year = " + "\"" + form.year.data + "\""
        flash(f'Filtering out the database for {form.year.data}', 'success')
    
    return filter_query

def construct_count_query(form):
    count_query = "SELECT COUNT(*) FROM scholars"

    if form.country.data != "" or form.uwc.data != "" or form.school.data != "":
        count_query = count_query + " WHERE"
   
    if form.country.data != "":
        count_query = count_query + " country = " + "\"" + form.country.data + "\""
    if form.uwc.data != "":
        if form.country.data != "":
            count_query = count_query + " AND"
        count_query = count_query + " uwc = " + "\"" + form.uwc.data + "\""
    if form.school.data != "":
        if form.country.data != "" or form.uwc.data != "":
            count_query = count_query + " AND"
        count_query = count_query + " school = " + "\"" + form.school.data + "\""

    return count_query



def correction_filter(country, uwc, school):
    all_correction = []
    if country != None:
        cut_off = 100
        while cut_off > 0:
            if fuzzywuzzy_check_w_list(country, list_countries, cut_off) != None:
                result = ["country", fuzzywuzzy_check_w_list(country, list_countries, cut_off)]
                all_correction.append(result)
                break

            cut_off = cut_off - 10
        

    if uwc != None:
        cut_off = 100
        while cut_off > 0:
            if fuzzywuzzy_check_w_list(uwc, list_uwc, cut_off) != None:
                result = ["uwc", fuzzywuzzy_check_w_list(uwc, list_uwc, cut_off)]
                all_correction.append(result)
                break

            cut_off = cut_off - 10
        

    if school != None:
        cut_off = 100
        while cut_off > 0:
            if fuzzywuzzy_check_w_list(school, list_school, cut_off) != None:
                result = ["school", fuzzywuzzy_check_w_list(school, list_school, cut_off)]
                all_correction.append(result)
                break

            cut_off = cut_off - 10
        

    return all_correction



# https://www.datacamp.com/tutorial/fuzzy-string-python
def fuzzywuzzy_check_w_list(str2Match, list_x, cut_off):
    for strOption in list_x:

                Ratios = fuzz.ratio(str2Match, strOption)
                Partial_ratio = fuzz.partial_ratio(str2Match, strOption)
                Token_Sort_Ratio = fuzz.token_sort_ratio(str2Match, strOption)
                Token_Set_Ratio = fuzz.token_set_ratio(str2Match, strOption)

                if Ratios > cut_off or Partial_ratio > cut_off or Token_Sort_Ratio > cut_off or Token_Set_Ratio > cut_off:
                    return strOption




def fuzzywuzzy_check_w_string(str2Match, strOption, cut_off):
    Ratios = fuzz.ratio(str2Match, strOption)
    Partial_ratio = fuzz.partial_ratio(str2Match, strOption)
    Token_Sort_Ratio = fuzz.token_sort_ratio(str2Match, strOption)
    Token_Set_Ratio = fuzz.token_set_ratio(str2Match, strOption)

    if Ratios > cut_off or Partial_ratio > cut_off or Token_Sort_Ratio > cut_off or Token_Set_Ratio > cut_off:
        return strOption





# Construct a list of countries from the library
list_countries = []
for country in countries:
    list_countries.append(country[0])

# Alternative country name
list_countries_alt = [
    ("USA", "United States"),
    ("Vietnam", "Viet Nam"),
    ("Chechnya", "Russian Federation"),
    ("South Korea", "Korea Republic of"),
    ("Korea", "Korea Republic of"),
    ("Laos", "The Lao People's Democratic"),
    ("Venezuela", "The Bolivarian Republic of Venezuela")
]

# Previous country name
list_previous_countries = [
    ("Swaziland", "Eswatini"),
    ("Cape Verde", "The epublic of Cabo Verde")
]

# Hard code country naame
list_countries.append("Tibet")




# List of all UWC keyword
list_uwc = [
    "UWC Atlantic",
    "Pearson",
    "South East Asia",
    "Waterford Kamhlaba Southern Africa",
    "USA",
    "Adriatic",
    "Li Po Chun",
    "Red Cross Nordic",
    "Mahindra",
    "Costa Rica",
    "Mostar",
    "Maastricht",
    "Robert Bosch",
    "Dilijan",
    "Changshu China",
    "Thailand",
    "ISAK Japan",
    "East Africa",
    "Simon Bolivar UWC of Agriculture"
]
list_uwc.sort()




# List of all School
list_school = []

# Alternative school name
list_school_alt = [
    ("Massachusetts Institute of Technology", "MIT"),
    ("St. Johnâ€™s College", "St. John's College"),
    ("Harvard College", "Harvard University"),
    ("Wesleyan College", "Wesleyan University"),
    ("St. Lawrence College", "St. Lawrence University")
]

# with open('davis_scholar_database.csv', 'r') as csv_file:
#     csv_reader = csv.DictReader(csv_file)

#     for line in csv_reader:
#         school = line['School']

#         # School already exist in the school list
#         if fuzzywuzzy_check_w_list(school, list_school, 90) != None:
#             # print(school + "---->" + fuzzywuzzy_check_w_list(school, list_school, 90))
#             school = fuzzywuzzy_check_w_list(school, list_school, 90)
#         else:

#             # Checking if school is an outlier
#             outlier_school = False

#             # Enter an invalid or non-string as School
#             if len(school) == 0 or school == None:
#                 outlier_school = True
#             # Enter UWC as School
#             elif fuzzywuzzy_check_w_list(school, list_uwc, 90) != None:
#                 outlier_school = True
#             # Enter Country as School
#             elif fuzzywuzzy_check_w_list(school, list_countries, 90) != None:
#                 outlier_school = True
#             elif fuzzywuzzy_check_w_list(school, list_countries, 90) == None:
#                 for alt in list_countries_alt:
#                     if fuzzywuzzy_check_w_string(school, alt[0], 90) != None:
#                         outlier_school = True
#                         break
#                 for previous in list_previous_countries:
#                     if fuzzywuzzy_check_w_string(school, previous[0], 90) != None:
#                         outlier_school = True
#                         break

#             # Check for Alt School name
#             is_alt = False
#             for alt in list_school_alt:
#                 if fuzzywuzzy_check_w_string(school, alt[0], 90) != None:
#                     is_alt = True
#                     break
            
#             # If it is not an outlier and not an alt name
#             # Then it does not exist and need to add to the list
#             if outlier_school == False and is_alt == False:
#                 list_school.append(school)
    
#     print(list_school)



#####################################################
# Run uwc_back.py in above line to print out the list
#####################################################
list_school = ['Princeton University', 'College of the Atlantic', 'Wellesley College', 'Colby College', 'Middlebury College', 'San Francisco Art Institute', 'Connecticut College', 'Carleton College', 'University of Virginia', 'Hood College', 'Hamilton College', 'Johns Hopkins University', 'Methodist University', 'Earlham College', 'Swarthmore College', 'Macalester', 'Westminster College', 'Harvard University', 'Cornell University', 'Lake Forest College', 'Vassar College', 'Skidmore College', 'Dickinson College', 'Brown University', 'Bates College', 'School of the Art Institute of Chicago', 'Wesleyan University', 'Smith College', 'Dartmouth College', 'Yale University', 'St. Lawrence University', 'Whitman College', 'Williams College', 'Colorado College', 'Oberlin College', 'Mount Holyoke College', 'Lafayette College', 'University of Richmond', 'Franklin and Marshall College', 'Bryn Mawr College', 'Lewis and Clark College', 'Washington and Lee University', 'Colgate University', 'Amherst College', 'Tufts University', 'Brandeis University', 'University of Florida', 'Wheaton College', 'Luther College', 'Grinnell College', 'The Boston Conservatory', 'Barnard College', 'Bucknell University', 'Bowdoin College', 'Lehigh University', 'Union College', 'Columbia University', 'Kenyon College', 'Denison University', 'Trinity College', 'Haverford College', 'Claremont McKenna College', 'University of Pennsylvania', 'Northwestern University', 'Notre Dame of Maryland', 'The College of Idaho', 'University of Chicago', 'Gettysburg College', 'Duke University', 'Agnes Scott College', 'University of North Carolina at Chapel Hill', 'College of the Holy Cross', 'Wartburg College', 'Simmons College', 'Clark University', 'Ringling College of Art and Design', 'Stanford University', 'University of Oklahoma', 'Reed College', 'Scripps College', 'Kalamazoo College', 'University of Notre Dame', 'University of Michigan', 'Georgetown University', 'St. Olaf College', 'Occidental College', 'Pomona College', 'Randolph-Macon College', 'New York University', 'MIT', 'Bennington College', 'Savannah College of Art and Design', 'Davidson College', 'University of Rochester', 'University of California Berkeley', 'Pitzer College', 'Emory University', 'Case Western Reserve University', 'Worcester Polytechnic Institute', 'Babson College', 'George Washington University']
list_school.sort()


def summary(type_key, type_value_1, type_value_2, list_key, list_value_1, list_value_2):

    conn = sqlite3.connect('scholars.db')
    c = conn.cursor()

    summary_all = []

    for key in list_key:
        # Number of scholars from that UWC
        total_scholars = c.execute(f"""SELECT COUNT(*) FROM scholars WHERE {type_key} = \"{key}\"""").fetchall()[0][0]

        # Data format
        # key_to_value_1 = {
        #     "Tufts university": 10,
        #     "MIT": 5,
        #     ...
        #     "Harvard University": 15
        # }


        # Create a dict with school as key and nummber of student as value
        key_to_value_1 = {}
        for value_1 in list_value_1:
            count = c.execute(f"""SELECT COUNT(*) FROM scholars WHERE {type_key} = ? AND {type_value_1} = ?""", (key, value_1)).fetchall()[0][0]
            key_to_value_1.update({f"{value_1}": count})

        # Most popular School
        # key_to_value_1
        k = list(key_to_value_1.keys())
        v = list(key_to_value_1.values())
        popular_value_1 = k[v.index(max(v))]
        if total_scholars == 0:
            value_1_out_of_key = 0
        else:
            value_1_out_of_key = round((max(v)/total_scholars) * 100)


        # Data format
        # key_to_value_2 = {
        #     "Cambodia": 10,
        #     "USA": 5,
        #     ...
        #     "Thailand": 15
        # }

        # Create a dict with school as key and number of student as value
        key_to_value_2 = {}
        for value_2 in list_value_2:
            count = c.execute(f"SELECT COUNT(*) FROM scholars WHERE {type_key} = ? AND {type_value_2} = ?", (key, value_2)).fetchall()[0][0]
            key_to_value_2.update({f"{value_2}": count})

        # Most popular Country
        # uwc_to_country
        k = list(key_to_value_2.keys())
        v = list(key_to_value_2.values())
        popular_value_2 = k[v.index(max(v))]
        if total_scholars == 0:
            value_2_out_of_key = 0
        else:
            value_2_out_of_key = round((max(v)/total_scholars) * 100)


        summary_key = [key, total_scholars, popular_value_1, value_1_out_of_key, popular_value_2, value_2_out_of_key]
        summary_all.append(summary_key)

        # print(" ")
        # print(f"{uwc} has a total of {total_scholars} Davis Scholars")
        # print(f"Most popular school is {popular_school}")
        # print(f"with average of {school_acceptance_among_uwc}% acceptance among the school")
        # print(f"Most popular country is {popular_country}")
        # print(f"with average of {country_acceptance_among_uwc}% acceptance among the school")


    conn.commit()

    return summary_all



def display_summary(all_key_img_src, type_key, type_value_1, type_value_2, list_key, list_value_1, list_value_2):

    # Empty Card
    empty_card = ["Empty", "0", "?", "0", "?", "0"]

    # Data to display on phone
    phone_summary_all_type_key = summary(type_key, type_value_1, type_value_2, list_key, list_value_1, list_value_2)

    # Data to display on desktop
    num_grid_row = math.ceil(len(phone_summary_all_type_key) / 3)
    desktop_summary_all_type_key = []
    row = 0
    ii = 0
    while row < num_grid_row:

        if len(phone_summary_all_type_key) <= (ii+1):
            row_data = [phone_summary_all_type_key[ii], empty_card, empty_card]
            desktop_summary_all_type_key.append(row_data)
            break
        elif len(phone_summary_all_type_key) <= (ii+2):
            row_data = [phone_summary_all_type_key[ii], phone_summary_all_type_key[ii+1], empty_card]
            desktop_summary_all_type_key.append(row_data)
            break

        row_data = [phone_summary_all_type_key[ii], phone_summary_all_type_key[ii+1], phone_summary_all_type_key[ii+2]]
        desktop_summary_all_type_key.append(row_data)
        row += 1
        ii = 3*row

    # Data to display on tablet
    num_grid_row = math.ceil(len(phone_summary_all_type_key) / 2)
    tablet_summary_all_type_key = []
    row = 0
    ii = 0
    while row < num_grid_row:

        if len(phone_summary_all_type_key) <= (ii+1):
            row_data = [phone_summary_all_type_key[ii], empty_card]
            tablet_summary_all_type_key.append(row_data)
            break

        row_data = [phone_summary_all_type_key[ii], phone_summary_all_type_key[ii+1]]
        tablet_summary_all_type_key.append(row_data)
        row += 1
        ii = 2*row

    ############################################################################
    # Add Empty to the list where the fuction display summary is being call
    # # Adding in empty UWC to the list for empty card
    # list_key.append("Empty")
    # all_key_img_src.append("https://montevista.greatheartsamerica.org/wp-content/uploads/sites/2/2016/11/default-placeholder.png")
    ############################################################################

    output_display_summary = [desktop_summary_all_type_key, tablet_summary_all_type_key, phone_summary_all_type_key]

    return output_display_summary