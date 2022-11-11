
from uwc_back import fuzzywuzzy_check_w_list, fuzzywuzzy_check_w_string
from uwc_back import list_countries, list_previous_countries, list_countries_alt
from uwc_back import list_uwc
from uwc_back import list_school, list_school_alt


country = "Cambod"

cut_off = 100
while cut_off > 0:
    if fuzzywuzzy_check_w_list(ountry, list_countries, cut_off) != None:
        print(cut_off)
        print(fuzzywuzzy_check_w_list(country, list_countries, cut_off))
        break
    cut_off = cut_off - 10