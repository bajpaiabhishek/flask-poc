import mysql.connector
from mysql.connector import Error


def get_database_connection():
    try:
        connection = mysql.connector.connect(host='localhost', port='3306', database='login_db', user='root',
                                             password='public')
        return connection
    except Error as e:
        print("Error while connecting to MySQL", e)


def close_database_connection(connection):
    if connection.is_connected():
        connection.close()
