import MySQLdb
import os

QUESTION_METADATA = '''select distinct question.title, question.question, question.page_number_start, 
question.page_number_end, question_id from question_data_1 inner join question
on question_data_1.question_id = question.id;'''

QUESTION_DATA_1 = '''select country.country_name, lesbian_gay_homosexual, bisexual, pansexual_omnisexual, asexual, 
`total_lgb+`, change_vs_2021 from question_data_1 inner join country on question_data_1.country_id = country.id;'''

INTERACTIVETABLE = '''select country.country_name, lesbian_gay_homosexual, bisexual, pansexual_omnisexual, asexual, 
`total_lgb+`, change_vs_2021 from question_data_1 inner join country on question_data_1.country_id = country.id;'''

def connect():
    # export IPSOS_DB_USER and IPSOS_DB_PASS with DB username and password respectively
    user = os.environ.get('IPSOS_DB_USER')
    password = os.environ.get('IPSOS_DB_PASS')
    conn = MySQLdb.connect(host="127.0.0.1", user=user, passwd=password, db="ipsospride2023")
    return conn


def run_query(querystring):
    conn = connect()
    cursor = conn.cursor()
    cursor.execute(querystring)
    rows = cursor.fetchall()
    return rows
