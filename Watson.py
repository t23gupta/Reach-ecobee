import json
import ast
from watson_developer_cloud import NaturalLanguageUnderstandingV1
from watson_developer_cloud.natural_language_understanding_v1 import Features, CategoriesOptions, KeywordsOptions
import pymysql
from sqlalchemy import create_engine
import pandas as pd
import sys

# Authentication for Watson API
natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2018-11-16',
    iam_apikey='IUeEAqs02hnZsmgR2hcQ4pyudKdPP2RwXKqQZF959Idb',
    url='https://gateway.watsonplatform.net/natural-language-understanding/api'
)

# Connection to database
engine_string = "mysql+pymysql://"+"sql9287699"+":"+"4hz5yerXZE"+"@"+"sql9.freesqldatabase.com"+":"+"3306"+"/sql9287699?charset=utf8mb4"
try:
    engine = create_engine(engine_string)
except Exception as e:
    print("Error connecting to MySQL DB: " +str(e))
    sys.exit()

# Getting required data
sql = "SELECT * FROM employee_details WHERE ID > (SELECT MAX(Employee_ID) FROM employee_interests_normalized)"

try:
    df = pd.read_sql_query(sql, engine)
    print(df)
except Exception as e:
    print(e)

final_df = pd.DataFrame()

for index, row in df.head().iterrows():

    raw_text = row['Description']

    # Analysis using IBM Watson
    response = natural_language_understanding.analyze(
        text = raw_text,
        features=Features(keywords=KeywordsOptions(sentiment=True,emotion=True,limit=10))).get_result()

    # JSON analysis response
    analysis = json.dumps(response, indent=2)
    analysis = ast.literal_eval(analysis)
    listOfKeywordsData = analysis["keywords"]
    listKeywords = []

    # Getting a list of keywords
    for i in listOfKeywordsData:
        keyword = i['text']
        listKeywords.append(keyword)

    newdf = pd.DataFrame()
    for i in listKeywords:
        newdf = newdf.append({'Employee_Name': row['Employee_Name'], 'Interest': i, 'Employee_ID': row['ID']}, ignore_index=True)

    final_df = final_df.append(newdf)

try:
    print(final_df)
    final_df.to_sql('employee_interests_normalized', engine, if_exists = 'append', index = False)
    print("Done!")
except Exception as e:
    print(e)
