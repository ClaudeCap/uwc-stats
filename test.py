
from uwc_back import fuzzywuzzy_check_w_list, fuzzywuzzy_check_w_string
from uwc_back import list_countries, list_previous_countries, list_countries_alt
from uwc_back import list_uwc
from uwc_back import list_school, list_school_alt

import csv

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

with open('davis_scholar_database.csv', 'r') as csv_file:
    csv_reader = csv.DictReader(csv_file)

    for line in csv_reader:
        school = line['School']

        # School already exist in the school list
        if fuzzywuzzy_check_w_list(school, list_school, 90) != None:
            # print(school + "---->" + fuzzywuzzy_check_w_list(school, list_school, 90))
            school = fuzzywuzzy_check_w_list(school, list_school, 90)
        else:

            # Checking if school is an outlier
            outlier_school = False

            # Enter an invalid or non-string as School
            if len(school) == 0 or school == None:
                outlier_school = True
            # Enter UWC as School
            elif fuzzywuzzy_check_w_list(school, list_uwc, 90) != None:
                outlier_school = True
            # Enter Country as School
            elif fuzzywuzzy_check_w_list(school, list_countries, 90) != None:
                outlier_school = True
            elif fuzzywuzzy_check_w_list(school, list_countries, 90) == None:
                for alt in list_countries_alt:
                    if fuzzywuzzy_check_w_string(school, alt[0], 90) != None:
                        outlier_school = True
                        break
                for previous in list_previous_countries:
                    if fuzzywuzzy_check_w_string(school, previous[0], 90) != None:
                        outlier_school = True
                        break

            # Check for Alt School name
            is_alt = False
            for alt in list_school_alt:
                if fuzzywuzzy_check_w_string(school, alt[0], 90) != None:
                    is_alt = True
                    break
            
            # If it is not an outlier and not an alt name
            # Then it does not exist and need to add to the list
            if outlier_school == False and is_alt == False:
                list_school.append(school)
    
    print(list_school)
