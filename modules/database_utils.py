import psycopg2
import psycopg2.extras
import pandas as pd
import numpy as na
import json
import datetime
import os

def db_connect(database = 'postgres', autocommit = True):
    with open(os.path.expanduser("~/myproject/myproject/database.json"), "r") as f:
        s = json.load(f)[database]
    database_type = s.pop('type')
    if database_type == 'postgres':
        con = psycopg2.connect(**s)
        if autocommit:
            con.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
        con.set_client_encoding('utf8')
        con.cursor().execute(f"""SET TIME ZONE 'EST'""")
    return con, con.cursor()