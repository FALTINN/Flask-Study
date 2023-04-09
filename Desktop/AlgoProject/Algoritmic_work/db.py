from mysql.connector import connect
import json


def query(con, request):
    cursor = con.cursor()
    cursor.execute(request)
    return cursor.fetchall()


def insert(con, request):
    cursor = con.cursor()
    cursor.execute(request)
    con.commit()


def debug(con, text, place="base", type="INFO"):
    insert(
        con, f'INSERT INTO `logs` (`place`, `text`, `type`) VALUES ("{place}", "{text}", "{type}");')
    

file_name = "config_algoritmic.json"
with open(file_name, 'r') as config:
    my_data = json.load(config)
    

con = connect(
        host = my_data['server'],
        user = my_data['user'],
        password = my_data['password'],
        database = my_data['database']
)