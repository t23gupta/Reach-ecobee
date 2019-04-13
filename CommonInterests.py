import json
import ast
import pymysql
from sqlalchemy import create_engine
import pandas as pd
import sys
import itertools


# Connection to database
engine_string = "mysql+pymysql://"+"sql9287699"+":"+"4hz5yerXZE"+"@"+"sql9.freesqldatabase.com"+":"+"3306"+"/sql9287699?charset=utf8mb4"
try:
    engine = create_engine(engine_string)
except Exception as e:
    print("Error connecting to MySQL DB: " +str(e))
    sys.exit()


# get a list of all unique names in the normalized table
sql = "SELECT DISTINCT Employee_Name FROM employee_interests_normalized"
try:
    df = pd.read_sql_query(sql, engine)
    listNames = df.Employee_Name.unique()
except Exception as e:
    print(e)

newdf = pd.DataFrame()
#p = [4, 8, 15, 16, 23, 42]
c = itertools.combinations(listNames, 2)
for i in c:
    #print(list(i))

    # query to return
    sql = "select Interest from employee_interests_normalized where (Interest in (select Interest from employee_interests_normalized where (Employee_Name = '" + i[0] + "' OR Employee_Name = '" + i[1] + "') group by Interest having count(*) > 1) AND (Employee_Name = '" + i[0] + "'))"
    df = pd.read_sql_query(sql, engine)

    listInterests = df.Interest.unique()
    if len(listInterests) == 0:
        listInterests = "Sorry, you don't have any common interests"

    newdf = newdf.append({'EmployeeA': str(i[0]), 'EmployeeB': str(i[1]), 'Interests': str(listInterests).replace('[', '').replace(']', '')}, ignore_index=True)

newdf.to_sql('employee_common_interests', engine, if_exists = 'replace', index = False)
