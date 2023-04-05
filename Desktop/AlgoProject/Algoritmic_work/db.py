from mysql.connector import connect


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
    

con = connect(
    #твои данные
)