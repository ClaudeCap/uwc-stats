from flask import flash, session
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from fuzzywuzzy import fuzz

from iso3166 import countries

import math
import sqlite3

import pandas as pd
import json
import plotly
import plotly.express as px

from uwc_back import list_uwc, list_countries, list_school




from flask import Markup





filter_query = """
    SELECT name, country, uwc, school, year FROM scholars WHERE uwc = "Hey"
"""


conn_scholars = sqlite3.connect('scholars.db')
c_scholars = conn_scholars.cursor()
scholars = c_scholars.execute(filter_query).fetchall()

print(scholars)