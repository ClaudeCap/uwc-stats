import sqlite3, csv

from uwc_back import fuzzywuzzy_check_w_list, fuzzywuzzy_check_w_string, outlier_check
from uwc_back import list_countries, list_previous_countries, list_countries_alt
from uwc_back import list_uwc
from uwc_back import list_school, list_school_alt


conn = sqlite3.connect('scholars.db')
list_invalid_scholars = []

c = conn.cursor()


c.execute("""
DROP TABLE scholars
""")

c.execute("""CREATE TABLE scholars (
            id integer primary key autoincrement,
            name text,
            country text,
            uwc text,
            school text,
            year text
)""")






#davis_scholar_database.csv
# ï»¿Name
with open('davis_scholar_database.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for line in csv_reader:
        name = line['ï»¿Name']
        country = line['Country']
        uwc = line['UWC School']
        school = line['School']
        year = line['Year']

        # Cleaning Country
        if country in list_countries:
            country = country
        else:
    
            if "Korea" in country:
                if "Democratic" in country:
                    country = "Korea, Democratic People's Republic of"
                else:
                    country = "Korea, Republic of"
            elif "Congo" in country:
                if "Democratic" in country:
                    country = "Congo, Democratic Republic of the"
                else:
                    country = "Congo"
            else:
        
                # Previous name
                for change in list_previous_countries:
                    if change[0] == country:
                        country = change[1]
                
                for alt in list_countries_alt:
                    # Alternative name
                    if alt[0] == country:
                        country = alt[1]
                    # Is the alternative name but mispelled
                    if fuzzywuzzy_check_w_string(country, alt[0], 90) != None:
                        country = alt[1]
                        
                # Enter UWC as Country
                if outlier_check(country, list_uwc) != None:
                    print("Enter UWC as Country")
                    print(str(name) + "||" + str(country) + "||" + str(uwc) + "||" + str(school) + "||" + str(year))
                    list_invalid_scholars.append([str(name), str(country), str(uwc), str(school), str(year)])
                    continue
                # Enter School as Country
                # Hard Code check
                # The code think Columbia country is the same as Columbia University
                if fuzzywuzzy_check_w_list(country, list_school, 90) != "Columbia University":
                    if outlier_check(country, list_school) != None:
                        print("Enter School as Country")
                        print(str(name) + "||" + str(country) + "||" + str(uwc) + "||" + str(school) + "||" + str(year))
                        list_invalid_scholars.append([str(name), str(country), str(uwc), str(school), str(year)])
                        continue
                
        
                country = fuzzywuzzy_check_w_list(country, list_countries, 90)

        # Cleaning UWC
        if uwc in list_uwc:
            uwc = uwc
        else:
            uwc = fuzzywuzzy_check_w_list(uwc, list_uwc, 90)
        
        # Cleaning School
        if fuzzywuzzy_check_w_list(school, list_school, 90) == None:
            school_outlier = True

            # Check for alt school name
            for alt in list_school_alt:
                if fuzzywuzzy_check_w_string(school, alt[0], 90) != None:
                    school = alt[1]
                    school_outlier = False
            
            # Hard code similar name
            if fuzzywuzzy_check_w_string(school, "College of the Atlantic", 90) != None:
                school = fuzzywuzzy_check_w_list(school, list_school, 90)
                school_outlier = False
            
            if school_outlier == True:
                print("Invalid School name")
                print(str(name) + "||" + str(country) + "||" + str(uwc) + "||" + str(school) + "||" + str(year))
                list_invalid_scholars.append([str(name), str(country), str(uwc), str(school), str(year)])
                continue

        previous = school
        school = fuzzywuzzy_check_w_list(school, list_school, 90)

        c.execute("INSERT INTO scholars (name, country, uwc, school, year) VALUES(?, ?, ?, ?, ?)", (name, country, uwc, school, year))


conn.commit()
conn.close()


###################################
##########INVALID SCHOLARS#########
###################################

conn = sqlite3.connect('invalidscholars.db')

c = conn.cursor()


c.execute("""
DROP TABLE invalidscholars
""")

c.execute("""CREATE TABLE invalidscholars (
            id integer primary key autoincrement,
            name text,
            country text,
            uwc text,
            school text,
            year text
)""")

for scholar in list_invalid_scholars:
    print(str(scholar) + " " + str(len(scholar)))
    name = scholar[0]
    country = scholar[1]
    uwc = scholar[2]
    school = scholar[3]
    year = scholar[4]

    c.execute("INSERT INTO invalidscholars (name, country, uwc, school, year) VALUES(?, ?, ?, ?, ?)", (name, country, uwc, school, year))

conn.commit()
conn.close()



