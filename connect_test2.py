import mysql.connector

def connect_to_db():
    return mysql.connector.connect(
        host='localhost',
        user='root',
        password='Frederick$01',
        database='elite_savings'
    )

if __name__ == '__main__':
    connection = connect_to_db()
    cursor =connection.cursor()
    cursor.execute("SELECT * FROM elite_users")
    for x in cursor:
        print (x)