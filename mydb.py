from psycopg2 import connect

# connection
connection = connect(
    user='postgres',
    password='root',
    host='localhost',
    port='5432',
    database='postgres'
)

try:
    with connection as conn:
        with conn.cursor() as cursor:
            sql = 'CREATE DATABASE crm;'
            cursor.execute(sql)

except Exception as e:
    print(f'Ha ocurrido Un error: {e}')
finally:
  connection.close()